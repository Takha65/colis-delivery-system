"""Use case : lister tous les colis."""

from src.application.ports import IColisRepository
from src.domain.entities import Colis


class ListerColisUseCase:
    """Retourne la liste de tous les colis."""

    def __init__(self, repository: IColisRepository) -> None:
        self._repository = repository

    def execute(self) -> list[Colis]:
        return self._repository.find_all()
