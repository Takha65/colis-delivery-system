"""Port : interface du repository de colis (Pattern Repository)."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.entities import Colis
from src.domain.value_objects import TrackingNumber


class IColisRepository(ABC):
    """Interface d'acces aux colis (abstraction de la persistance).

    Les use cases dependent de cette interface, pas d'une implementation
    concrete (Principe DIP).
    """

    @abstractmethod
    def save(self, colis: Colis) -> Colis:
        """Persiste un colis (creation ou mise a jour)."""

    @abstractmethod
    def get_by_id(self, colis_id: UUID) -> Optional[Colis]:
        """Recupere un colis par son id, None si inexistant."""

    @abstractmethod
    def get_by_tracking_number(self, tracking_number: TrackingNumber) -> Optional[Colis]:
        """Recupere un colis par son numero de suivi."""

    @abstractmethod
    def find_all(self) -> list[Colis]:
        """Retourne tous les colis."""

    @abstractmethod
    def delete(self, colis_id: UUID) -> bool:
        """Supprime un colis. Retourne True si supprime, False si inexistant."""
