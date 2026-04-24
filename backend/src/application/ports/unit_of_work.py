"""Port : interface Unit of Work (transactions atomiques)."""
from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    """Interface Unit of Work.

    Regroupe plusieurs operations dans une seule transaction :
    - commit() : valide toutes les operations
    - rollback() : annule toutes les operations
    - context manager : rollback automatique en cas d'exception
    """

    @abstractmethod
    def __enter__(self) -> "IUnitOfWork":
        """Debut de la transaction."""

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fin de transaction : commit si pas d'exception, sinon rollback."""

    @abstractmethod
    def commit(self) -> None:
        """Valide toutes les operations."""

    @abstractmethod
    def rollback(self) -> None:
        """Annule toutes les operations."""
