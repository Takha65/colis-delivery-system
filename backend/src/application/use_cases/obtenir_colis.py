"""Use case : obtenir un colis par son id."""
from uuid import UUID

from src.application.ports import IColisRepository
from src.domain.entities import Colis
from src.domain.exceptions import ColisNotFoundError


class ObtenirColisUseCase:
    """Recupere un colis par son identifiant."""

    def __init__(self, repository: IColisRepository) -> None:
        self._repository = repository

    def execute(self, colis_id: UUID) -> Colis:
        colis = self._repository.get_by_id(colis_id)
        if colis is None:
            raise ColisNotFoundError(str(colis_id))
        return colis
