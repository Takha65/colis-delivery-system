"""Port : interface du repository de livreurs."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities import Livreur


class ILivreurRepository(ABC):
    """Interface d'acces aux livreurs."""

    @abstractmethod
    def save(self, livreur: Livreur) -> Livreur:
        """Persiste un livreur."""

    @abstractmethod
    def get_by_id(self, livreur_id: UUID) -> Optional[Livreur]:
        """Recupere un livreur par son id."""

    @abstractmethod
    def find_all(self) -> list[Livreur]:
        """Retourne tous les livreurs."""
