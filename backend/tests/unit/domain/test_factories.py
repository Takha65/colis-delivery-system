"""Tests unitaires des factories de colis (Pattern Factory Method)."""
import pytest

from src.domain.entities import TypeColis
from src.domain.exceptions import InvalidColisError
from src.domain.factories import (
    ColisFactory,
    ExpressColisFactory,
    FragileColisFactory,
    StandardColisFactory,
    get_factory,
)
from src.domain.value_objects import Adresse, Dimensions, Poids


@pytest.fixture
def adresse_origine() -> Adresse:
    return Adresse(rue="100 rue A", ville="Sherbrooke", code_postal="J1K 1A1")


@pytest.fixture
def adresse_destination() -> Adresse:
    return Adresse(rue="200 rue B", ville="Montreal", code_postal="H3Z 2Y7")


# ============================================================
# Tests communs a toutes les factories (LSP)
# ============================================================

TOUTES_LES_FACTORIES: list[ColisFactory] = [
    StandardColisFactory(),
    FragileColisFactory(),
    ExpressColisFactory(),
]


class TestToutesLesFactories:
    """Tests qui s'appliquent a TOUTES les factories (LSP)."""

    @pytest.mark.parametrize("factory", TOUTES_LES_FACTORIES)
    def test_cree_colis_de_bon_type(
        self, factory, adresse_origine, adresse_destination
    ) -> None:
        colis = factory.creer(
            poids=Poids(valeur_kg=1.0),
            dimensions=Dimensions(longueur_cm=10, largeur_cm=10, hauteur_cm=10),
            adresse_origine=adresse_origine,
            adresse_destination=adresse_destination,
        )
        assert colis.type_colis == factory.type_colis()

    @pytest.mark.parametrize("factory", TOUTES_LES_FACTORIES)
    def test_cree_colis_au_statut_cree(
        self, factory, adresse_origine, adresse_destination
    ) -> None:
        colis = factory.creer(
            poids=Poids(valeur_kg=1.0),
            dimensions=Dimensions(longueur_cm=10, largeur_cm=10, hauteur_cm=10),
            adresse_origine=adresse_origine,
            adresse_destination=adresse_destination,
        )
        assert colis.statut == "CREE"

    @pytest.mark.parametrize("factory", TOUTES_LES_FACTORIES)
    def test_cree_colis_avec_tracking_number(
        self, factory, adresse_origine, adresse_destination
    ) -> None:
        colis = factory.creer(
            poids=Poids(valeur_kg=1.0),
            dimensions=Dimensions(longueur_cm=10, largeur_cm=10, hauteur_cm=10),
            adresse_origine=adresse_origine,
            adresse_destination=adresse_destination,
        )
        assert colis.tracking_number.valeur.startswith("CLS-")


# ============================================================
# Tests specifiques a chaque factory
# ============================================================

class TestStandardColisFactory:

    def test_aucune_contrainte_specifique(
        self, adresse_origine, adresse_destination
    ) -> None:
        factory = StandardColisFactory()
        # Poids et dimensions "normaux" (loin des limites)
        colis = factory.creer(
            poids=Poids(valeur_kg=50.0),
            dimensions=Dimensions(longueur_cm=80, largeur_cm=60, hauteur_cm=40),
            adresse_origine=adresse_origine,
            adresse_destination=adresse_destination,
        )
        assert colis.type_colis == TypeColis.STANDARD


class TestFragileColisFactory:

    def test_poids_sous_limite_accepte(
        self, adresse_origine, adresse_destination
    ) -> None:
        factory = FragileColisFactory()
        colis = factory.creer(
            poids=Poids(valeur_kg=15.0),
            dimensions=Dimensions(longueur_cm=20, largeur_cm=20, hauteur_cm=20),
            adresse_origine=adresse_origine,
            adresse_destination=adresse_destination,
        )
        assert colis.type_colis == TypeColis.FRAGILE

    def test_poids_trop_eleve_rejete(
        self, adresse_origine, adresse_destination
    ) -> None:
        factory = FragileColisFactory()
        with pytest.raises(InvalidColisError, match="fragile"):
            factory.creer(
                poids=Poids(valeur_kg=25.0),  # > 20 kg
                dimensions=Dimensions(longueur_cm=20, largeur_cm=20, hauteur_cm=20),
                adresse_origine=adresse_origine,
                adresse_destination=adresse_destination,
            )

    def test_volume_trop_grand_rejete(
        self, adresse_origine, adresse_destination
    ) -> None:
        factory = FragileColisFactory()
        with pytest.raises(InvalidColisError, match="volume"):
            factory.creer(
                poids=Poids(valeur_kg=5.0),
                dimensions=Dimensions(longueur_cm=100, largeur_cm=100, hauteur_cm=100),
                adresse_origine=adresse_origine,
                adresse_destination=adresse_destination,
            )


class TestExpressColisFactory:

    def test_colis_leger_et_petit_accepte(
        self, adresse_origine, adresse_destination
    ) -> None:
        factory = ExpressColisFactory()
        colis = factory.creer(
            poids=Poids(valeur_kg=5.0),
            dimensions=Dimensions(longueur_cm=30, largeur_cm=20, hauteur_cm=10),
            adresse_origine=adresse_origine,
            adresse_destination=adresse_destination,
        )
        assert colis.type_colis == TypeColis.EXPRESS

    def test_poids_trop_eleve_rejete(
        self, adresse_origine, adresse_destination
    ) -> None:
        factory = ExpressColisFactory()
        with pytest.raises(InvalidColisError, match="express"):
            factory.creer(
                poids=Poids(valeur_kg=15.0),  # > 10 kg
                dimensions=Dimensions(longueur_cm=30, largeur_cm=20, hauteur_cm=10),
                adresse_origine=adresse_origine,
                adresse_destination=adresse_destination,
            )

    def test_dimension_trop_grande_rejete(
        self, adresse_origine, adresse_destination
    ) -> None:
        factory = ExpressColisFactory()
        with pytest.raises(InvalidColisError, match="longueur"):
            factory.creer(
                poids=Poids(valeur_kg=5.0),
                dimensions=Dimensions(longueur_cm=60, largeur_cm=20, hauteur_cm=10),
                adresse_origine=adresse_origine,
                adresse_destination=adresse_destination,
            )


# ============================================================
# Tests du registre
# ============================================================

class TestGetFactory:

    def test_retourne_bonne_factory(self) -> None:
        assert isinstance(get_factory(TypeColis.STANDARD), StandardColisFactory)
        assert isinstance(get_factory(TypeColis.FRAGILE), FragileColisFactory)
        assert isinstance(get_factory(TypeColis.EXPRESS), ExpressColisFactory)
