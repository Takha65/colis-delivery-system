"""Tests unitaires du pattern State (ColisState et sous-classes)."""
import pytest

from src.domain.exceptions import InvalidTransitionError
from src.domain.states import (
    ColisConfirme,
    ColisCree,
    ColisEnTransit,
    ColisLivre,
    ColisState,
    etat_depuis_nom,
)


TOUS_LES_ETATS: list[ColisState] = [
    ColisCree(),
    ColisEnTransit(),
    ColisLivre(),
    ColisConfirme(),
]


class TestColisState:
    """Tests qui s'appliquent a TOUS les etats (LSP)."""

    @pytest.mark.parametrize("etat", TOUS_LES_ETATS)
    def test_chaque_etat_a_un_nom(self, etat: ColisState) -> None:
        assert etat.nom != ""

    @pytest.mark.parametrize("etat", TOUS_LES_ETATS)
    def test_transitions_autorisees_retourne_set(self, etat: ColisState) -> None:
        assert isinstance(etat.transitions_autorisees(), set)

    @pytest.mark.parametrize("etat", TOUS_LES_ETATS)
    def test_transition_vers_meme_etat_invalide(self, etat: ColisState) -> None:
        with pytest.raises(InvalidTransitionError):
            etat.transiter_vers(etat)


class TestColisCree:

    def test_nom(self) -> None:
        assert ColisCree().nom == "CREE"

    def test_transitions_autorisees(self) -> None:
        assert ColisCree().transitions_autorisees() == {"EN_TRANSIT"}

    def test_est_modifiable(self) -> None:
        assert ColisCree().est_modifiable() is True

    def test_pas_final(self) -> None:
        assert ColisCree().est_final() is False


class TestColisEnTransit:

    def test_transitions_autorisees(self) -> None:
        assert ColisEnTransit().transitions_autorisees() == {"LIVRE"}

    def test_non_modifiable(self) -> None:
        assert ColisEnTransit().est_modifiable() is False


class TestColisLivre:

    def test_transitions_autorisees(self) -> None:
        assert ColisLivre().transitions_autorisees() == {"CONFIRME"}


class TestColisConfirme:

    def test_est_final(self) -> None:
        assert ColisConfirme().est_final() is True

    def test_aucune_transition(self) -> None:
        assert ColisConfirme().transitions_autorisees() == set()


class TestEgaliteEtats:

    def test_meme_etat_egaux(self) -> None:
        assert ColisCree() == ColisCree()

    def test_etats_differents_pas_egaux(self) -> None:
        assert ColisCree() != ColisEnTransit()

    def test_utilisable_dans_set(self) -> None:
        etats = {ColisCree(), ColisCree(), ColisEnTransit()}
        assert len(etats) == 2


class TestEtatDepuisNom:

    def test_retourne_bonne_classe(self) -> None:
        assert isinstance(etat_depuis_nom("CREE"), ColisCree)
        assert isinstance(etat_depuis_nom("EN_TRANSIT"), ColisEnTransit)
        assert isinstance(etat_depuis_nom("LIVRE"), ColisLivre)
        assert isinstance(etat_depuis_nom("CONFIRME"), ColisConfirme)

    def test_nom_inconnu_leve_exception(self) -> None:
        with pytest.raises(ValueError, match="inconnu"):
            etat_depuis_nom("UNKNOWN")
