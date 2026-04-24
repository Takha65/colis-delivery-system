"""Tests unitaires des use cases livreurs."""

import pytest

from src.application.use_cases import (
    CreerLivreurCommand,
    CreerLivreurUseCase,
    ListerLivreursUseCase,
)
from tests.fakes.fake_livreur_repository import FakeLivreurRepository


@pytest.fixture
def repository() -> FakeLivreurRepository:
    return FakeLivreurRepository()


class TestCreerLivreur:

    def test_cree_livreur(self, repository) -> None:
        use_case = CreerLivreurUseCase(repository)
        command = CreerLivreurCommand(nom="Jean", capacite_max_kg=50.0, position_depart_id="SHE")
        livreur = use_case.execute(command)
        assert livreur.nom == "Jean"
        assert livreur.id is not None

    def test_livreur_persiste(self, repository) -> None:
        use_case = CreerLivreurUseCase(repository)
        command = CreerLivreurCommand(nom="Marie", capacite_max_kg=30.0, position_depart_id="MTL")
        livreur = use_case.execute(command)
        assert repository.get_by_id(livreur.id) is not None


class TestListerLivreurs:

    def test_liste_vide(self, repository) -> None:
        assert ListerLivreursUseCase(repository).execute() == []

    def test_liste_tous(self, repository) -> None:
        creer = CreerLivreurUseCase(repository)
        creer.execute(CreerLivreurCommand("A", 50.0, "SHE"))
        creer.execute(CreerLivreurCommand("B", 60.0, "MTL"))
        assert len(ListerLivreursUseCase(repository).execute()) == 2
