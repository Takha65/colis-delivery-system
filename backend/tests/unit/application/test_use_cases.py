"""Tests unitaires des use cases CRUD."""
from uuid import uuid4

import pytest

from src.application.use_cases import (
    CreerColisCommand,
    CreerColisUseCase,
    ListerColisUseCase,
    ObtenirColisUseCase,
    SupprimerColisUseCase,
)
from src.domain.entities import TypeColis
from src.domain.exceptions import ColisNotFoundError
from tests.fakes.fake_colis_repository import FakeColisRepository


@pytest.fixture
def repository() -> FakeColisRepository:
    return FakeColisRepository()


@pytest.fixture
def command_valide() -> CreerColisCommand:
    return CreerColisCommand(
        poids_kg=2.5,
        longueur_cm=30, largeur_cm=20, hauteur_cm=10,
        rue_origine="100 rue A", ville_origine="Sherbrooke",
        code_postal_origine="J1K 1A1",
        rue_destination="200 rue B", ville_destination="Montreal",
        code_postal_destination="H3Z 2Y7",
    )


class TestCreerColis:

    def test_cree_colis_avec_statut_cree(self, repository, command_valide) -> None:
        use_case = CreerColisUseCase(repository)
        colis = use_case.execute(command_valide)
        assert colis.statut == "CREE"
        assert colis.id is not None

    def test_cree_colis_est_persiste(self, repository, command_valide) -> None:
        use_case = CreerColisUseCase(repository)
        colis = use_case.execute(command_valide)
        assert repository.get_by_id(colis.id) is not None

    def test_cree_colis_fragile(self, repository, command_valide) -> None:
        command_valide.type_colis = "FRAGILE"
        colis = CreerColisUseCase(repository).execute(command_valide)
        assert colis.type_colis == TypeColis.FRAGILE


class TestObtenirColis:

    def test_retourne_colis_existant(self, repository, command_valide) -> None:
        colis = CreerColisUseCase(repository).execute(command_valide)
        resultat = ObtenirColisUseCase(repository).execute(colis.id)
        assert resultat.id == colis.id

    def test_leve_exception_si_inexistant(self, repository) -> None:
        with pytest.raises(ColisNotFoundError):
            ObtenirColisUseCase(repository).execute(uuid4())


class TestListerColis:

    def test_liste_vide(self, repository) -> None:
        assert ListerColisUseCase(repository).execute() == []

    def test_liste_tous_les_colis(self, repository, command_valide) -> None:
        CreerColisUseCase(repository).execute(command_valide)
        CreerColisUseCase(repository).execute(command_valide)
        assert len(ListerColisUseCase(repository).execute()) == 2


class TestSupprimerColis:

    def test_supprime_colis_existant(self, repository, command_valide) -> None:
        colis = CreerColisUseCase(repository).execute(command_valide)
        SupprimerColisUseCase(repository).execute(colis.id)
        assert repository.get_by_id(colis.id) is None

    def test_leve_exception_si_inexistant(self, repository) -> None:
        with pytest.raises(ColisNotFoundError):
            SupprimerColisUseCase(repository).execute(uuid4())
