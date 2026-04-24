"""Value Object representant le poids d'un colis."""

from dataclasses import dataclass

from src.domain.exceptions import InvalidColisError


@dataclass(frozen=True)
class Poids:
    """Poids d'un colis en kilogrammes.

    Value Object immuable avec validation a la creation.
    """

    valeur_kg: float

    def __post_init__(self) -> None:
        if self.valeur_kg <= 0:
            raise InvalidColisError(
                f"Le poids doit etre strictement positif, recu: {self.valeur_kg}"
            )
        if self.valeur_kg > 1000:
            raise InvalidColisError(
                f"Le poids ne peut pas depasser 1000 kg, recu: {self.valeur_kg}"
            )

    def est_lourd(self) -> bool:
        """Determine si le colis est considere comme lourd (> 30 kg)."""
        return self.valeur_kg > 30

    def __str__(self) -> str:
        return f"{self.valeur_kg} kg"
