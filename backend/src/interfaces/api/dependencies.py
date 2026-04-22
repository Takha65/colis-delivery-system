"""Dependances FastAPI : resolution des use cases et repositories."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.use_cases import (
    CreerColisUseCase,
    ListerColisUseCase,
    ObtenirColisUseCase,
    ObtenirHistoriqueUseCase,
    SupprimerColisUseCase,
    TransiterColisUseCase,
)
from src.infrastructure.persistence import SQLAlchemyColisRepository, get_db


def get_colis_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SQLAlchemyColisRepository:
    return SQLAlchemyColisRepository(db)


def get_creer_colis_use_case(
    repo: Annotated[SQLAlchemyColisRepository, Depends(get_colis_repository)],
) -> CreerColisUseCase:
    return CreerColisUseCase(repo)


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
) -> TransiterColisUseCase:
    return TransiterColisUseCase(repo)


def get_obtenir_historique_use_case(
    repo: Annotated[SQLAlchemyColisRepository, Depends(get_colis_repository)],
) -> ObtenirHistoriqueUseCase:
    return ObtenirHistoriqueUseCase(repo)
