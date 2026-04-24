"""Value Object representant une adresse postale."""

from dataclasses import dataclass
from typing import Optional

from src.domain.exceptions import InvalidColisError


@dataclass(frozen=True)
class Coordonnees:
    """Coordonnees GPS (latitude, longitude)."""

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not -90 <= self.latitude <= 90:
            raise InvalidColisError(
                f"Latitude invalide: {self.latitude} (doit etre entre -90 et 90)"
            )
        if not -180 <= self.longitude <= 180:
            raise InvalidColisError(
                f"Longitude invalide: {self.longitude} (doit etre entre -180 et 180)"
            )


@dataclass(frozen=True)
class Adresse:
    """Adresse postale complete.

    Les coordonnees GPS sont optionnelles et seront renseignees par
    le service de geocodage (Nominatim) lors de la creation du colis.
    """

    rue: str
    ville: str
    code_postal: str
    pays: str = "Canada"
    coordonnees: Optional[Coordonnees] = None

    def __post_init__(self) -> None:
        if not self.rue.strip():
            raise InvalidColisError("La rue ne peut pas etre vide")
        if not self.ville.strip():
            raise InvalidColisError("La ville ne peut pas etre vide")
        if not self.code_postal.strip():
            raise InvalidColisError("Le code postal ne peut pas etre vide")

    def __str__(self) -> str:
        return f"{self.rue}, {self.ville}, {self.code_postal}, {self.pays}"

    def ligne_complete(self) -> str:
        """Format lisible pour geocodage."""
        return f"{self.rue}, {self.ville}, {self.code_postal}, {self.pays}"
