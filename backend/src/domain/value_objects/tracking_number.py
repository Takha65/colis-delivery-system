"""Value Object representant un numero de suivi de colis."""
import re
import secrets
from dataclasses import dataclass

from src.domain.exceptions import InvalidColisError


@dataclass(frozen=True)
class TrackingNumber:
    """Numero de suivi unique au format CLS-XXXXXXXX.

    XXXXXXXX est une sequence alphanumerique majuscule.
    """

    valeur: str

    PATTERN = re.compile(r"^CLS-[A-Z0-9]{8}$")

    def __post_init__(self) -> None:
        if not self.PATTERN.match(self.valeur):
            raise InvalidColisError(
                f"Numero de suivi invalide: '{self.valeur}' "
                f"(format attendu: CLS-XXXXXXXX)"
            )

    @classmethod
    def generer(cls) -> "TrackingNumber":
        """Genere un nouveau numero de suivi aleatoire."""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        suffix = "".join(secrets.choice(alphabet) for _ in range(8))
        return cls(valeur=f"CLS-{suffix}")

    def __str__(self) -> str:
        return self.valeur
