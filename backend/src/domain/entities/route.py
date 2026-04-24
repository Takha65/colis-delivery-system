"""Entite Route : resultat d'un calcul d'optimisation."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class EtapeRoute:
    """Une etape (arret) dans une route."""

    noeud_id: str
    nom_lieu: str
    ordre: int  # Position dans la sequence (0 = depart)
    distance_depuis_precedent_km: float = 0.0
    temps_depuis_precedent_min: float = 0.0
    colis_ids: list[UUID] = field(default_factory=list)  # Colis livres ici


@dataclass
class Route:
    """Resultat d'un calcul de route optimisee."""

    livreur_id: UUID
    etapes: list[EtapeRoute]
    strategie_utilisee: str  # Ex: "DIJKSTRA"
    distance_totale_km: float
    temps_total_minutes: float
    charge_moyenne: float
    id: UUID = field(default_factory=uuid4)
    date_calcul: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @property
    def nombre_arrets(self) -> int:
        return len(self.etapes)
