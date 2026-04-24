"""Use case : creer plusieurs colis de facon atomique (Unit of Work)."""
from dataclasses import dataclass

from src.application.ports import IUnitOfWork
from src.application.use_cases.creer_colis import CreerColisCommand
from src.domain.entities import Colis, TypeColis
from src.domain.factories import get_factory
from src.domain.value_objects import Adresse, Dimensions, Poids


@dataclass
class CreerColisEnLotCommand:
    commandes: list[CreerColisCommand]


class CreerColisEnLotUseCase:
    """Cree plusieurs colis dans une seule transaction atomique.

    Si UN colis echoue (validation, contrainte DB), TOUS sont annules.
    """

    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    def execute(self, command: CreerColisEnLotCommand) -> list[Colis]:
        colis_crees: list[Colis] = []

        with self._uow as uow:
            for cmd in command.commandes:
                colis = self._creer_colis_domain(cmd)
                uow.colis.save(colis)
                colis_crees.append(colis)
            uow.commit()  # Commit unique pour tout le lot

        return colis_crees

    @staticmethod
    def _creer_colis_domain(cmd: CreerColisCommand) -> Colis:
        factory = get_factory(TypeColis(cmd.type_colis))
        return factory.creer(
            poids=Poids(valeur_kg=cmd.poids_kg),
            dimensions=Dimensions(
                longueur_cm=cmd.longueur_cm,
                largeur_cm=cmd.largeur_cm,
                hauteur_cm=cmd.hauteur_cm,
            ),
            adresse_origine=Adresse(
                rue=cmd.rue_origine,
                ville=cmd.ville_origine,
                code_postal=cmd.code_postal_origine,
                pays=cmd.pays_origine,
            ),
            adresse_destination=Adresse(
                rue=cmd.rue_destination,
                ville=cmd.ville_destination,
                code_postal=cmd.code_postal_destination,
                pays=cmd.pays_destination,
            ),
        )
