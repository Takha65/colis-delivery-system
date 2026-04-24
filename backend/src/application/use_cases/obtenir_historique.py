"""Use case : obtenir l'historique des statuts d'un colis."""

from uuid import UUID

from src.application.ports import IColisRepository
from src.domain.entities import HistoriqueStatut
from src.domain.exceptions import ColisNotFoundError


class ObtenirHistoriqueUseCase:
    """Retourne l'historique des transitions d'un colis."""

    def __init__(self, repository: IColisRepository) -> None:
        self._repository = repository

    def execute(self, colis_id: UUID) -> list[HistoriqueStatut]:
        colis = self._repository.get_by_id(colis_id)
        if colis is None:
            raise ColisNotFoundError(str(colis_id))
        return colis.historique
