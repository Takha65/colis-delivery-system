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
        longueur_cm=30,
        largeur_cm=20,
        hauteur_cm=10,
        rue_origine="100 rue A",
        ville_origine="Sherbrooke",
        code_postal_origine="J1K 1A1",
        rue_destination="200 rue B",
        ville_destination="Montreal",
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


class TestCreerColisAvecGeocodage:
    """Verifie l'integration du service de geocodage dans CreerColisUseCase."""

    def test_cree_colis_avec_coordonnees_si_geocoding_disponible(
        self, repository, command_valide
    ) -> None:
        from tests.fakes.fake_geocoding_service import FakeGeocodingService
        from src.domain.value_objects import Coordonnees

        geocoding = FakeGeocodingService(
            coordonnees_par_defaut=Coordonnees(latitude=45.4, longitude=-71.9)
        )
        use_case = CreerColisUseCase(repository, geocoding)

        colis = use_case.execute(command_valide)

        assert colis.adresse_origine.coordonnees is not None
        assert colis.adresse_origine.coordonnees.latitude == 45.4
        assert colis.adresse_destination.coordonnees is not None

    def test_cree_colis_sans_coordonnees_si_geocoding_echoue(
        self, repository, command_valide
    ) -> None:
        from tests.fakes.fake_geocoding_service import FakeGeocodingService

        geocoding = FakeGeocodingService(doit_echouer=True)
        use_case = CreerColisUseCase(repository, geocoding)

        colis = use_case.execute(command_valide)

        # Mode degrade : colis cree meme si geocoding echoue
        assert colis.adresse_origine.coordonnees is None

    def test_cree_colis_sans_geocoding_service(self, repository, command_valide) -> None:
        """Backward compat : sans service, colis cree normalement."""
        use_case = CreerColisUseCase(repository, geocoding=None)

        colis = use_case.execute(command_valide)

        assert colis.adresse_origine.coordonnees is None
