"""Tests unitaires de l'entite Colis."""
import pytest

from src.domain.entities import Colis, StatutColis, TypeColis
from src.domain.exceptions import InvalidTransitionError
from src.domain.value_objects import Adresse, Dimensions, Poids, TrackingNumber


@pytest.fixture
def colis_standard() -> Colis:
    """Fixture : un colis standard pret a l'emploi pour les tests."""
    return Colis(
        tracking_number=TrackingNumber.generer(),
        poids=Poids(valeur_kg=2.5),
        dimensions=Dimensions(longueur_cm=30, largeur_cm=20, hauteur_cm=10),
        adresse_origine=Adresse(
            rue="100 rue Origine", ville="Sherbrooke", code_postal="J1K 1A1"
        ),
        adresse_destination=Adresse(
            rue="200 rue Destination", ville="Montreal", code_postal="H3Z 2Y7"
        ),
    )


class TestColisCreation:
    """Tests de creation d'un Colis."""

    def test_colis_est_cree_en_statut_cree(self, colis_standard: Colis) -> None:
        assert colis_standard.statut == StatutColis.CREE

    def test_colis_a_un_id_unique(self) -> None:
        c1 = Colis(
            tracking_number=TrackingNumber.generer(),
            poids=Poids(valeur_kg=1),
            dimensions=Dimensions(longueur_cm=10, largeur_cm=10, hauteur_cm=10),
            adresse_origine=Adresse(rue="a", ville="b", code_postal="c"),
            adresse_destination=Adresse(rue="d", ville="e", code_postal="f"),
        )
        c2 = Colis(
            tracking_number=TrackingNumber.generer(),
            poids=Poids(valeur_kg=1),
            dimensions=Dimensions(longueur_cm=10, largeur_cm=10, hauteur_cm=10),
            adresse_origine=Adresse(rue="a", ville="b", code_postal="c"),
            adresse_destination=Adresse(rue="d", ville="e", code_postal="f"),
        )
        assert c1.id != c2.id

    def test_type_par_defaut_est_standard(self, colis_standard: Colis) -> None:
        assert colis_standard.type_colis == TypeColis.STANDARD


class TestColisTransitions:
    """Tests du cycle de vie d'un Colis."""

    def test_transition_cree_vers_en_transit_valide(
        self, colis_standard: Colis
    ) -> None:
        colis_standard.transiter_vers(StatutColis.EN_TRANSIT)
        assert colis_standard.statut == StatutColis.EN_TRANSIT

    def test_cycle_complet(self, colis_standard: Colis) -> None:
        colis_standard.transiter_vers(StatutColis.EN_TRANSIT)
        colis_standard.transiter_vers(StatutColis.LIVRE)
        colis_standard.transiter_vers(StatutColis.CONFIRME)
        assert colis_standard.statut == StatutColis.CONFIRME

    def test_transition_cree_vers_livre_invalide(
        self, colis_standard: Colis
    ) -> None:
        """On ne peut pas sauter un etat."""
        with pytest.raises(InvalidTransitionError):
            colis_standard.transiter_vers(StatutColis.LIVRE)

    def test_transition_depuis_confirme_impossible(
        self, colis_standard: Colis
    ) -> None:
        """CONFIRME est un etat final."""
        colis_standard.transiter_vers(StatutColis.EN_TRANSIT)
        colis_standard.transiter_vers(StatutColis.LIVRE)
        colis_standard.transiter_vers(StatutColis.CONFIRME)
        with pytest.raises(InvalidTransitionError):
            colis_standard.transiter_vers(StatutColis.EN_TRANSIT)

    def test_peut_transiter_vers(self, colis_standard: Colis) -> None:
        assert colis_standard.peut_transiter_vers(StatutColis.EN_TRANSIT) is True
        assert colis_standard.peut_transiter_vers(StatutColis.LIVRE) is False


class TestColisMethodesMetier:
    """Tests des methodes metier du Colis."""

    def test_est_livre_apres_livraison(self, colis_standard: Colis) -> None:
        colis_standard.transiter_vers(StatutColis.EN_TRANSIT)
        colis_standard.transiter_vers(StatutColis.LIVRE)
        assert colis_standard.est_livre() is True

    def test_pas_livre_en_transit(self, colis_standard: Colis) -> None:
        colis_standard.transiter_vers(StatutColis.EN_TRANSIT)
        assert colis_standard.est_livre() is False

    def test_modifiable_seulement_si_cree(self, colis_standard: Colis) -> None:
        assert colis_standard.est_modifiable() is True
        colis_standard.transiter_vers(StatutColis.EN_TRANSIT)
        assert colis_standard.est_modifiable() is False
