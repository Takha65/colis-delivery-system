"""Dependances FastAPI : resolution des use cases et repositories."""
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.ports import IGeocodingService, IStrategieRoutage
from src.application.services.event_bus import EventBus
from src.application.services.event_handlers import (
    log_colis_cree,
    log_colis_livre,
    log_colis_transite,
    log_route_calculee,
)
from src.application.services.selecteur_strategie import SelecteurStrategieRoutage
from src.application.use_cases import (
    CalculerRouteUseCase,
    CreerColisUseCase,
    CreerLivreurUseCase,
    ListerColisUseCase,
    ListerLivreursUseCase,
    ObtenirColisUseCase,
    ObtenirHistoriqueUseCase,
    SupprimerColisUseCase,
    TransiterColisUseCase,
)
from src.domain.entities import Graphe
from src.domain.events import (
    ColisCreeEvent,
    ColisLivreEvent,
    ColisTransiteEvent,
    RouteCalculeeEvent,
)
from src.infrastructure.external import (
    GeocodingCacheProxy,
    NominatimGeocodingAdapter,
)
from src.infrastructure.graphe import charger_graphe_depuis_json
from src.infrastructure.persistence import (
    SQLAlchemyColisRepository,
    SQLAlchemyLivreurRepository,
    get_db,
)
from src.infrastructure.routage import (
    StrategieDijkstra,
    StrategieGreedy,
    StrategiePlusProcheVoisin,
)
from src.shared.config import settings


# ===== Singletons =====

@lru_cache(maxsize=1)
def get_geocoding_service() -> IGeocodingService:
    adapter = NominatimGeocodingAdapter()
    return GeocodingCacheProxy(adapter)


@lru_cache(maxsize=1)
def get_graphe() -> Graphe:
    return charger_graphe_depuis_json(settings.graphe_json_path)


@lru_cache(maxsize=1)
def get_strategies() -> dict[str, IStrategieRoutage]:
    return {
        "DIJKSTRA": StrategieDijkstra(),
        "PLUS_PROCHE_VOISIN": StrategiePlusProcheVoisin(),
        "GREEDY": StrategieGreedy(),
    }


@lru_cache(maxsize=1)
def get_selecteur_strategie() -> SelecteurStrategieRoutage:
    return SelecteurStrategieRoutage(strategies=get_strategies())


@lru_cache(maxsize=1)
def get_event_bus() -> EventBus:
    """Event Bus singleton avec handlers deja enregistres."""
    bus = EventBus()
    bus.subscribe(ColisCreeEvent, log_colis_cree)
    bus.subscribe(ColisTransiteEvent, log_colis_transite)
    bus.subscribe(ColisLivreEvent, log_colis_livre)
    bus.subscribe(RouteCalculeeEvent, log_route_calculee)
    return bus


# ===== Repositories =====

def get_colis_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SQLAlchemyColisRepository:
    return SQLAlchemyColisRepository(db)


def get_livreur_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SQLAlchemyLivreurRepository:
    return SQLAlchemyLivreurRepository(db)


# ===== Use cases Colis =====

def get_creer_colis_use_case(
    repo: Annotated[SQLAlchemyColisRepository, Depends(get_colis_repository)],
    geocoding: Annotated[IGeocodingService, Depends(get_geocoding_service)],
    event_bus: Annotated[EventBus, Depends(get_event_bus)],
) -> CreerColisUseCase:
    return CreerColisUseCase(repo, geocoding, event_bus)


def get_obtenir_colis_use_case(
    repo: Annotated[SQLAlchemyColisRepository, Depends(get_colis_repository)],
) -> ObtenirColisUseCase:
    return ObtenirColisUseCase(repo)


def get_lister_colis_use_case(
    repo: Annotated[SQLAlchemyColisRepository, Depends(get_colis_repository)],
) -> ListerColisUseCase:
    return ListerColisUseCase(repo)


def get_supprimer_colis_use_case(
    repo: Annotated[SQLAlchemyColisRepository, Depends(get_colis_repository)],
) -> SupprimerColisUseCase:
    return SupprimerColisUseCase(repo)


def get_transiter_colis_use_case(
    repo: Annotated[SQLAlchemyColisRepository, Depends(get_colis_repository)],
    event_bus: Annotated[EventBus, Depends(get_event_bus)],
) -> TransiterColisUseCase:
    return TransiterColisUseCase(repo, event_bus)


def get_obtenir_historique_use_case(
    repo: Annotated[SQLAlchemyColisRepository, Depends(get_colis_repository)],
) -> ObtenirHistoriqueUseCase:
    return ObtenirHistoriqueUseCase(repo)


# ===== Use cases M2 =====

def get_creer_livreur_use_case(
    repo: Annotated[SQLAlchemyLivreurRepository, Depends(get_livreur_repository)],
) -> CreerLivreurUseCase:
    return CreerLivreurUseCase(repo)


def get_lister_livreurs_use_case(
    repo: Annotated[SQLAlchemyLivreurRepository, Depends(get_livreur_repository)],
) -> ListerLivreursUseCase:
    return ListerLivreursUseCase(repo)


def get_calculer_route_use_case(
    selecteur: Annotated[SelecteurStrategieRoutage, Depends(get_selecteur_strategie)],
    graphe: Annotated[Graphe, Depends(get_graphe)],
    event_bus: Annotated[EventBus, Depends(get_event_bus)],
) -> CalculerRouteUseCase:
    return CalculerRouteUseCase(selecteur, graphe, event_bus)
