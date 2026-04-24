"""Evenements du domaine (faits immuables)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID


@dataclass(frozen=True)
class DomainEvent:
    """Classe de base pour tous les evenements du domaine."""

    date: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc), kw_only=True
    )


@dataclass(frozen=True)
class ColisCreeEvent(DomainEvent):
    colis_id: UUID
    tracking_number: str
    type_colis: str


@dataclass(frozen=True)
class ColisTransiteEvent(DomainEvent):
    colis_id: UUID
    tracking_number: str
    statut_precedent: str
    statut_nouveau: str


@dataclass(frozen=True)
class ColisLivreEvent(DomainEvent):
    colis_id: UUID
    tracking_number: str


@dataclass(frozen=True)
class RouteCalculeeEvent(DomainEvent):
    route_id: UUID
    livreur_id: UUID
    strategie: str
    distance_totale_km: float
    nombre_arrets: int
