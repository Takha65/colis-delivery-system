"""Use case : lister tous les livreurs."""
from src.application.ports import ILivreurRepository
from src.domain.entities import Livreur


class ListerLivreursUseCase:
    def __init__(self, repository: ILivreurRepository) -> None:
        self._repository = repository

    def execute(self) -> list[Livreur]:
        return self._repository.find_all()
