"""Fake repository livreurs pour tests."""

from typing import Optional
from uuid import UUID

from src.application.ports import ILivreurRepository
from src.domain.entities import Livreur


class FakeLivreurRepository(ILivreurRepository):
    def __init__(self) -> None:
        self._livreurs: dict[UUID, Livreur] = {}

    def save(self, livreur: Livreur) -> Livreur:
        self._livreurs[livreur.id] = livreur
        return livreur

    def get_by_id(self, livreur_id: UUID) -> Optional[Livreur]:
        return self._livreurs.get(livreur_id)

    def find_all(self) -> list[Livreur]:
        return list(self._livreurs.values())
