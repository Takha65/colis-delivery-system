"""Use case : faire transiter un colis vers un nouvel etat."""
from dataclasses import dataclass
from uuid import UUID

from src.application.ports import IColisRepository
from src.domain.entities import Colis
from src.domain.exceptions import ColisNotFoundError


@dataclass
class TransiterColisCommand:
    colis_id: UUID
    nouvel_etat: str
    commentaire: str = ""


class TransiterColisUseCase:
    """Fait transiter un colis d'un etat a un autre."""

    def __init__(self, repository: IColisRepository) -> None:
        self._repository = repository

    def execute(self, command: TransiterColisCommand) -> Colis:
        colis = self._repository.get_by_id(command.colis_id)
        if colis is None:
            raise ColisNotFoundError(str(command.colis_id))

        colis.transiter_vers(command.nouvel_etat, command.commentaire)
        return self._repository.save(colis)
