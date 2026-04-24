"""Unit of Work SQLAlchemy : transactions atomiques multi-repositories."""
from sqlalchemy.orm import Session, sessionmaker

from src.application.ports import IUnitOfWork
from src.infrastructure.persistence.sqlalchemy_colis_repository import (
    SQLAlchemyColisRepository,
)
from src.infrastructure.persistence.sqlalchemy_livreur_repository import (
    SQLAlchemyLivreurRepository,
)


class SQLAlchemyUnitOfWork(IUnitOfWork):
    """Unit of Work SQLAlchemy.

    Usage :
        with SQLAlchemyUnitOfWork(session_factory) as uow:
            uow.colis.save(colis)
            uow.livreurs.save(livreur)
            uow.commit()  # tout ou rien
    """

    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory
        self._session: Session | None = None
        self.colis: SQLAlchemyColisRepository | None = None
        self.livreurs: SQLAlchemyLivreurRepository | None = None

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        self._session = self._session_factory()
        self.colis = SQLAlchemyColisRepository(self._session)
        self.livreurs = SQLAlchemyLivreurRepository(self._session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()
        if self._session is not None:
            self._session.close()
            self._session = None

    def commit(self) -> None:
        if self._session is not None:
            self._session.commit()

    def rollback(self) -> None:
        if self._session is not None:
            self._session.rollback()
