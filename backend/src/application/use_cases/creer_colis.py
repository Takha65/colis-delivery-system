"""Use case : creer un colis (avec geocodage et events)."""
from dataclasses import dataclass
from typing import Optional

from src.application.ports import IColisRepository, IGeocodingService
from src.application.services.event_bus import EventBus
from src.domain.entities import Colis, TypeColis
from src.domain.events import ColisCreeEvent
from src.domain.factories import get_factory
from src.domain.value_objects import Adresse, Dimensions, Poids


@dataclass
class CreerColisCommand:
    poids_kg: float
    longueur_cm: float
    largeur_cm: float
    hauteur_cm: float
    rue_origine: str
    ville_origine: str
    code_postal_origine: str
    rue_destination: str
    ville_destination: str
    code_postal_destination: str
    type_colis: str = "STANDARD"
    pays_origine: str = "Canada"
    pays_destination: str = "Canada"


class CreerColisUseCase:
    """Cree un nouveau colis, geocode ses adresses et publie un event."""

    def __init__(
        self,
        repository: IColisRepository,
        geocoding: Optional[IGeocodingService] = None,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self._repository = repository
        self._geocoding = geocoding
        self._event_bus = event_bus

    def execute(self, command: CreerColisCommand) -> Colis:
        poids = Poids(valeur_kg=command.poids_kg)
        dimensions = Dimensions(
            longueur_cm=command.longueur_cm,
            largeur_cm=command.largeur_cm,
            hauteur_cm=command.hauteur_cm,
        )
        adresse_origine = self._construire_adresse(
            command.rue_origine, command.ville_origine,
            command.code_postal_origine, command.pays_origine,
        )
        adresse_destination = self._construire_adresse(
            command.rue_destination, command.ville_destination,
            command.code_postal_destination, command.pays_destination,
        )

        factory = get_factory(TypeColis(command.type_colis))
        colis = factory.creer(
            poids=poids,
            dimensions=dimensions,
            adresse_origine=adresse_origine,
            adresse_destination=adresse_destination,
        )

        colis_sauve = self._repository.save(colis)

        # Publier l'evenement (Observer pattern)
        if self._event_bus is not None:
            self._event_bus.publish(
                ColisCreeEvent(
                    colis_id=colis_sauve.id,
                    tracking_number=colis_sauve.tracking_number.valeur,
                    type_colis=colis_sauve.type_colis.value,
                )
            )

        return colis_sauve

    def _construire_adresse(self, rue, ville, code_postal, pays) -> Adresse:
        adresse = Adresse(
            rue=rue, ville=ville, code_postal=code_postal, pays=pays
        )
        if self._geocoding is None:
            return adresse

        coord = self._geocoding.geocoder(adresse)
        if coord is None:
            return adresse

        return Adresse(
            rue=rue, ville=ville, code_postal=code_postal,
            pays=pays, coordonnees=coord,
        )
