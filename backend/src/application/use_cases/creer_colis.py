"""Use case : creer un colis."""
from dataclasses import dataclass

from src.application.ports import IColisRepository
from src.domain.entities import Colis, TypeColis
from src.domain.factories import get_factory
from src.domain.value_objects import Adresse, Dimensions, Poids


@dataclass
class CreerColisCommand:
    """Donnees d'entree pour creer un colis."""

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
    """Cree un nouveau colis via la factory appropriee au type."""

    def __init__(self, repository: IColisRepository) -> None:
        self._repository = repository

    def execute(self, command: CreerColisCommand) -> Colis:
        # Construire les value objects (validations generales)
        poids = Poids(valeur_kg=command.poids_kg)
        dimensions = Dimensions(
            longueur_cm=command.longueur_cm,
            largeur_cm=command.largeur_cm,
            hauteur_cm=command.hauteur_cm,
        )
        adresse_origine = Adresse(
            rue=command.rue_origine,
            ville=command.ville_origine,
            code_postal=command.code_postal_origine,
            pays=command.pays_origine,
        )
        adresse_destination = Adresse(
            rue=command.rue_destination,
            ville=command.ville_destination,
            code_postal=command.code_postal_destination,
            pays=command.pays_destination,
        )

        # Deleguer a la factory du bon type (validations specifiques + creation)
        factory = get_factory(TypeColis(command.type_colis))
        colis = factory.creer(
            poids=poids,
            dimensions=dimensions,
            adresse_origine=adresse_origine,
            adresse_destination=adresse_destination,
        )

        return self._repository.save(colis)
