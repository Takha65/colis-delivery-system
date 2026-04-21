"""Value Object representant les dimensions d'un colis."""
from dataclasses import dataclass

from src.domain.exceptions import InvalidColisError


@dataclass(frozen=True)
class Dimensions:
    """Dimensions d'un colis en centimetres (longueur x largeur x hauteur)."""

    longueur_cm: float
    largeur_cm: float
    hauteur_cm: float

    def __post_init__(self) -> None:
        for nom, valeur in [
            ("longueur", self.longueur_cm),
            ("largeur", self.largeur_cm),
            ("hauteur", self.hauteur_cm),
        ]:
            if valeur <= 0:
                raise InvalidColisError(
                    f"La {nom} doit etre strictement positive, recu: {valeur}"
                )

    @property
    def volume_cm3(self) -> float:
        """Volume du colis en cm3."""
        return self.longueur_cm * self.largeur_cm * self.hauteur_cm

    def est_volumineux(self) -> bool:
        """Determine si le colis est volumineux (> 100 000 cm3 soit 0.1 m3)."""
        return self.volume_cm3 > 100_000

    def __str__(self) -> str:
        return f"{self.longueur_cm}x{self.largeur_cm}x{self.hauteur_cm} cm"
