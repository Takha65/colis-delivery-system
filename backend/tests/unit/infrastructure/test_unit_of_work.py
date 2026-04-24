"""Tests unitaires du SQLAlchemyUnitOfWork."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.domain.entities import Livreur
from src.infrastructure.persistence import Base, SQLAlchemyUnitOfWork
from src.infrastructure.persistence.colis_model import ColisModel  # noqa: F401
from src.infrastructure.persistence.historique_model import HistoriqueStatutModel  # noqa: F401
from src.infrastructure.persistence.livreur_model import LivreurModel  # noqa: F401


@pytest.fixture
def session_factory():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


class TestUnitOfWork:

    def test_commit_persiste_les_donnees(self, session_factory) -> None:
        with SQLAlchemyUnitOfWork(session_factory) as uow:
            livreur = Livreur(nom="Jean", capacite_max_kg=50.0, position_depart_id="SHE")
            uow.livreurs.save(livreur)
            uow.commit()
            livreur_id = livreur.id

        # Nouvelle session : verifier la persistance
        with SQLAlchemyUnitOfWork(session_factory) as uow2:
            retrieved = uow2.livreurs.get_by_id(livreur_id)
            assert retrieved is not None
            assert retrieved.nom == "Jean"

    def test_rollback_annule_les_operations(self, session_factory) -> None:
        # Capturer l'ID pour verifier plus tard
        livreur_id = None

        with SQLAlchemyUnitOfWork(session_factory) as uow:
            livreur = Livreur(nom="Marie", capacite_max_kg=30.0, position_depart_id="MTL")
            uow.livreurs.save(livreur)
            livreur_id = livreur.id
            uow.rollback()

        # Verifier que le livreur n'est PAS persiste
        with SQLAlchemyUnitOfWork(session_factory) as uow2:
            assert uow2.livreurs.get_by_id(livreur_id) is None

    def test_exception_declenche_rollback_auto(self, session_factory) -> None:
        livreur_id = None

        try:
            with SQLAlchemyUnitOfWork(session_factory) as uow:
                livreur = Livreur(nom="Paul", capacite_max_kg=40.0, position_depart_id="SHE")
                uow.livreurs.save(livreur)
                livreur_id = livreur.id
                raise RuntimeError("Erreur simulee")
        except RuntimeError:
            pass

        # Verifier que le livreur n'est pas persiste (rollback auto)
        with SQLAlchemyUnitOfWork(session_factory) as uow2:
            assert uow2.livreurs.get_by_id(livreur_id) is None

    def test_acces_aux_repositories(self, session_factory) -> None:
        with SQLAlchemyUnitOfWork(session_factory) as uow:
            assert uow.colis is not None
            assert uow.livreurs is not None
