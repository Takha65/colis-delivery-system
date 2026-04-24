"""Implementation in-memory du repository pour les tests."""

from typing import Optional
from uuid import UUID

from src.application.ports import IColisRepository
from src.domain.entities import Colis
from src.domain.value_objects import TrackingNumber


class FakeColisRepository(IColisRepository):
    """Repository in-memory : tests rapides, pas de DB requise."""

    def __init__(self) -> None:
        self._colis: dict[UUID, Colis] = {}

    def save(self, colis: Colis) -> Colis:
        self._colis[colis.id] = colis
        return colis

    def get_by_id(self, colis_id: UUID) -> Optional[Colis]:
        return self._colis.get(colis_id)

    def get_by_tracking_number(self, tracking_number: TrackingNumber) -> Optional[Colis]:
        for colis in self._colis.values():
            if colis.tracking_number == tracking_number:
                return colis
        return None

    def find_all(self) -> list[Colis]:
        return list(self._colis.values())

    def delete(self, colis_id: UUID) -> bool:
        if colis_id in self._colis:
            del self._colis[colis_id]
            return True
        return False
