"""Schemas Pydantic pour les endpoints M2 (livreurs, routes, graphe)."""
from uuid import UUID

from pydantic import BaseModel, Field


# ===== Livreurs =====

class CreerLivreurRequest(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100)
    capacite_max_kg: float = Field(..., gt=0, le=5000)
    position_depart_id: str = Field(..., min_length=1, max_length=10)


class LivreurResponse(BaseModel):
    id: UUID
    nom: str
    capacite_max_kg: float
    position_depart_id: str


# ===== Routes =====

class CalculerRouteRequest(BaseModel):
    livreur_id: UUID
    noeud_depart: str = Field(..., min_length=1)
    noeuds_a_visiter: list[str] = Field(..., min_length=1, max_length=20)
    poids_distance: float = Field(default=0.5, ge=0, le=1)
    poids_temps: float = Field(default=0.3, ge=0, le=1)
    poids_charge: float = Field(default=0.2, ge=0, le=1)
    strategie: str | None = Field(
        default=None, pattern="^(DIJKSTRA|PLUS_PROCHE_VOISIN|GREEDY)$"
    )


class EtapeRouteResponse(BaseModel):
    noeud_id: str
    nom_lieu: str
    ordre: int
    distance_depuis_precedent_km: float
    temps_depuis_precedent_min: float


class RouteResponse(BaseModel):
    id: UUID
    livreur_id: UUID
    strategie_utilisee: str
    etapes: list[EtapeRouteResponse]
    distance_totale_km: float
    temps_total_minutes: float
    charge_moyenne: float
    nombre_arrets: int


# ===== Graphe =====

class NoeudResponse(BaseModel):
    id: str
    nom: str
    latitude: float
    longitude: float


class AreteResponse(BaseModel):
    source: str
    cible: str
    distance_km: float
    temps_minutes: float
    charge_trafic: float


class GrapheResponse(BaseModel):
    noeuds: list[NoeudResponse]
    aretes: list[AreteResponse]


class StrategieInfo(BaseModel):
    nom: str
    description: str
