"""Use case : creer un livreur."""

from dataclasses import dataclass

from src.application.ports import ILivreurRepository
from src.domain.entities import Livreur


@dataclass
class CreerLivreurCommand:
    nom: str
    capacite_max_kg: float
    position_depart_id: str


class CreerLivreurUseCase:
    def __init__(self, repository: ILivreurRepository) -> None:
        self._repository = repository

    def execute(self, command: CreerLivreurCommand) -> Livreur:
        livreur = Livreur(
            nom=command.nom,
            capacite_max_kg=command.capacite_max_kg,
            position_depart_id=command.position_depart_id,
        )
        return self._repository.save(livreur)
