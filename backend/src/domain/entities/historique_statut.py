"""Entite HistoriqueStatut : trace immuable des transitions d'un colis."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True)
class HistoriqueStatut:
    """Entree immuable de l'historique d'un colis.

    Chaque transition d'etat cree une nouvelle entree. Les entrees ne
    peuvent jamais etre modifiees (frozen).
    """

    colis_id: UUID
    statut_precedent: str  # None pour la creation initiale
    statut_nouveau: str
    id: UUID = field(default_factory=uuid4)
    date_transition: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    commentaire: str = ""
