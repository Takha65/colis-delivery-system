"""Use case : supprimer un colis."""
from uuid import UUID

from src.application.ports import IColisRepository
from src.domain.exceptions import ColisNotFoundError


class SupprimerColisUseCase:
    """Supprime un colis par son identifiant."""

    def __init__(self, repository: IColisRepository) -> None:
        self._repository = repository

    def execute(self, colis_id: UUID) -> None:
        supprime = self._repository.delete(colis_id)
        if not supprime:
            raise ColisNotFoundError(str(colis_id))
