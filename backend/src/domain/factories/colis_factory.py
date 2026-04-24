"""Factory Method : creation de colis selon leur type.

Chaque sous-classe de ColisFactory encapsule les regles metier
specifiques a un type de colis (Standard, Fragile, Express).
"""

from abc import ABC, abstractmethod

from src.domain.entities import Colis, TypeColis
from src.domain.exceptions import InvalidColisError
from src.domain.value_objects import (
    Adresse,
    Dimensions,
    Poids,
    TrackingNumber,
)


class ColisFactory(ABC):
    """Factory abstraite pour creer des colis.

    Chaque sous-classe :
    - valide les contraintes specifiques au type
    - cree un Colis du bon TypeColis
    """

    @abstractmethod
    def type_colis(self) -> TypeColis:
        """Retourne le type de colis produit par cette factory."""

    @abstractmethod
    def valider_contraintes(self, poids: Poids, dimensions: Dimensions) -> None:
        """Valide les contraintes specifiques au type.

        Raises:
            InvalidColisError: si les contraintes ne sont pas respectees.
        """

    def creer(
        self,
        poids: Poids,
        dimensions: Dimensions,
        adresse_origine: Adresse,
        adresse_destination: Adresse,
    ) -> Colis:
        """Template method : cree un colis en appliquant les contraintes."""
        self.valider_contraintes(poids, dimensions)
        return Colis(
            tracking_number=TrackingNumber.generer(),
            poids=poids,
            dimensions=dimensions,
            adresse_origine=adresse_origine,
            adresse_destination=adresse_destination,
            type_colis=self.type_colis(),
        )


class StandardColisFactory(ColisFactory):
    """Factory pour colis standards (aucune contrainte specifique)."""

    def type_colis(self) -> TypeColis:
        return TypeColis.STANDARD

    def valider_contraintes(self, poids: Poids, dimensions: Dimensions) -> None:
        # Les contraintes generales (poids > 0, etc.) sont deja
        # appliquees par les Value Objects eux-memes.
        pass


class FragileColisFactory(ColisFactory):
    """Factory pour colis fragiles (contraintes renforcees).

    Regles metier :
    - Poids maximum : 20 kg (au-dela, risque de casse eleve)
    - Volume maximum : 50 000 cm3 (0.05 m3)
    """

    POIDS_MAX_KG = 20.0
    VOLUME_MAX_CM3 = 50_000.0

    def type_colis(self) -> TypeColis:
        return TypeColis.FRAGILE

    def valider_contraintes(self, poids: Poids, dimensions: Dimensions) -> None:
        if poids.valeur_kg > self.POIDS_MAX_KG:
            raise InvalidColisError(
                f"Un colis fragile ne peut pas peser plus de "
                f"{self.POIDS_MAX_KG} kg (recu: {poids.valeur_kg} kg)"
            )
        if dimensions.volume_cm3 > self.VOLUME_MAX_CM3:
            raise InvalidColisError(
                f"Un colis fragile ne peut pas avoir un volume superieur "
                f"a {self.VOLUME_MAX_CM3} cm3 (recu: {dimensions.volume_cm3} cm3)"
            )


class ExpressColisFactory(ColisFactory):
    """Factory pour colis express (contraintes de rapidite).

    Regles metier :
    - Poids maximum : 10 kg (pour livraison rapide en scooter/velo)
    - Dimensions maximum : 50 cm par cote
    """

    POIDS_MAX_KG = 10.0
    DIMENSION_MAX_CM = 50.0

    def type_colis(self) -> TypeColis:
        return TypeColis.EXPRESS

    def valider_contraintes(self, poids: Poids, dimensions: Dimensions) -> None:
        if poids.valeur_kg > self.POIDS_MAX_KG:
            raise InvalidColisError(
                f"Un colis express ne peut pas peser plus de "
                f"{self.POIDS_MAX_KG} kg (recu: {poids.valeur_kg} kg)"
            )
        for nom, valeur in [
            ("longueur", dimensions.longueur_cm),
            ("largeur", dimensions.largeur_cm),
            ("hauteur", dimensions.hauteur_cm),
        ]:
            if valeur > self.DIMENSION_MAX_CM:
                raise InvalidColisError(
                    f"La {nom} d'un colis express ne peut pas depasser "
                    f"{self.DIMENSION_MAX_CM} cm (recu: {valeur} cm)"
                )


# Registre des factories par type
_FACTORIES: dict[TypeColis, ColisFactory] = {
    TypeColis.STANDARD: StandardColisFactory(),
    TypeColis.FRAGILE: FragileColisFactory(),
    TypeColis.EXPRESS: ExpressColisFactory(),
}


def get_factory(type_colis: TypeColis) -> ColisFactory:
    """Retourne la factory correspondant au type de colis."""
    if type_colis not in _FACTORIES:
        raise ValueError(f"Type de colis inconnu: {type_colis}")
    return _FACTORIES[type_colis]
