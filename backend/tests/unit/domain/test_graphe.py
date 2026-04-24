"""Tests unitaires du graphe routier."""

import pytest

from src.domain.entities import Arete, Graphe, Noeud
from src.domain.exceptions import NoeudIntrouvableError
from src.domain.value_objects import Coordonnees


@pytest.fixture
def graphe_simple() -> Graphe:
    """Graphe a 3 noeuds : A-B-C."""
    g = Graphe()
    g.ajouter_noeud(Noeud(id="A", nom="A", coordonnees=Coordonnees(0, 0)))
    g.ajouter_noeud(Noeud(id="B", nom="B", coordonnees=Coordonnees(0, 1)))
    g.ajouter_noeud(Noeud(id="C", nom="C", coordonnees=Coordonnees(1, 1)))
    g.ajouter_arete(Arete("A", "B", 10, 15, 0.1))
    g.ajouter_arete(Arete("B", "C", 20, 30, 0.2))
    return g


class TestGraphe:

    def test_ajouter_noeud(self) -> None:
        g = Graphe()
        g.ajouter_noeud(Noeud(id="X", nom="X", coordonnees=Coordonnees(0, 0)))
        assert "X" in g.noeuds

    def test_voisins_bidirectionnels(self, graphe_simple: Graphe) -> None:
        voisins_a = graphe_simple.voisins("A")
        voisins_b = graphe_simple.voisins("B")
        assert len(voisins_a) == 1
        assert voisins_a[0].noeud_cible == "B"
        # B a 2 voisins (A et C) grace au bidirectionnel
        assert len(voisins_b) == 2

    def test_noeud_inconnu_leve_exception(self, graphe_simple: Graphe) -> None:
        with pytest.raises(NoeudIntrouvableError):
            graphe_simple.voisins("INCONNU")

    def test_arete_vers_noeud_inconnu_leve_exception(self) -> None:
        g = Graphe()
        g.ajouter_noeud(Noeud(id="A", nom="A", coordonnees=Coordonnees(0, 0)))
        with pytest.raises(NoeudIntrouvableError):
            g.ajouter_arete(Arete("A", "INCONNU", 10, 15))


class TestChargementGrapheJSON:

    def test_charger_graphe_reel(self) -> None:
        from src.infrastructure.graphe import charger_graphe_depuis_json

        graphe = charger_graphe_depuis_json("data/graphe.json")

        assert len(graphe.noeuds) == 8
        assert "SHE" in graphe.noeuds
        assert graphe.noeud("MTL").nom == "Montreal"

    def test_charger_fichier_inexistant_leve_exception(self) -> None:
        from src.domain.exceptions import GrapheInvalideError
        from src.infrastructure.graphe import charger_graphe_depuis_json

        with pytest.raises(GrapheInvalideError):
            charger_graphe_depuis_json("fichier_qui_nexiste_pas.json")
