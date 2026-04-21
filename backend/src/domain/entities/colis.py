"""Entite Colis - coeur du domaine metier."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from src.domain.exceptions import InvalidTransitionError
from src.domain.value_objects import Adresse, Dimensions, Poids, TrackingNumber


class StatutColis(str, Enum):
    """Statuts possibles d'un colis dans son cycle de vie."""

    CREE = "CREE"
    EN_TRANSIT = "EN_TRANSIT"
    LIVRE = "LIVRE"
    CONFIRME = "CONFIRME"


class TypeColis(str, Enum):
    """Types de colis, determinent les contraintes applicables."""

    STANDARD = "STANDARD"
    FRAGILE = "FRAGILE"
    EXPRESS = "EXPRESS"


# Transitions valides dans le cycle de vie
TRANSITIONS_VALIDES: dict[StatutColis, set[StatutColis]] = {
    StatutColis.CREE: {StatutColis.EN_TRANSIT},
    StatutColis.EN_TRANSIT: {StatutColis.LIVRE},
    StatutColis.LIVRE: {StatutColis.CONFIRME},
    StatutColis.CONFIRME: set(),  # Etat final
}


@dataclass
class Colis:
    """Entite representant un colis a livrer.

    Un colis passe par plusieurs statuts :
    CREE -> EN_TRANSIT -> LIVRE -> CONFIRME
    """

    tracking_number: TrackingNumber
    poids: Poids
    dimensions: Dimensions
    adresse_origine: Adresse
    adresse_destination: Adresse
    type_colis: TypeColis = TypeColis.STANDARD
    statut: StatutColis = StatutColis.CREE
    id: UUID = field(default_factory=uuid4)
    date_creation: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def peut_transiter_vers(self, nouveau_statut: StatutColis) -> bool:
        """Verifie si la transition vers un nouveau statut est valide."""
        return nouveau_statut in TRANSITIONS_VALIDES[self.statut]

    def transiter_vers(self, nouveau_statut: StatutColis) -> None:
        """Effectue une transition de statut.

        Raises:
            InvalidTransitionError: si la transition n'est pas valide.
        """
        if not self.peut_transiter_vers(nouveau_statut):
            raise InvalidTransitionError(
                statut_actuel=self.statut.value,
                statut_cible=nouveau_statut.value,
            )
        self.statut = nouveau_statut

    def est_livre(self) -> bool:
        """Retourne True si le colis est livre ou confirme."""
        return self.statut in {StatutColis.LIVRE, StatutColis.CONFIRME}

    def est_modifiable(self) -> bool:
        """Un colis n'est plus modifiable une fois en transit."""
        return self.statut == StatutColis.CREE
