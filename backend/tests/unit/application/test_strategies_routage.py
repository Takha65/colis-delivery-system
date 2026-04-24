"""Tests unitaires des strategies de routage (Strategy Pattern)."""

from uuid import uuid4

import pytest

from src.application.ports import IStrategieRoutage
from src.application.services.selecteur_strategie import SelecteurStrategieRoutage
from src.domain.entities import Arete, Graphe, Noeud
from src.domain.value_objects import Coordonnees, CriteresRoutage
from src.infrastructure.routage import (
    StrategieDijkstra,
    StrategieGreedy,
    StrategiePlusProcheVoisin,
)


@pytest.fixture
def graphe_test() -> Graphe:
    """Graphe en carre : A-B-C-D avec diagonales."""
    g = Graphe()
    for nid in ["A", "B", "C", "D"]:
        g.ajouter_noeud(Noeud(id=nid, nom=nid, coordonnees=Coordonnees(0, 0)))
    g.ajouter_arete(Arete("A", "B", 10, 10, 0.1))
    g.ajouter_arete(Arete("B", "C", 10, 10, 0.2))
    g.ajouter_arete(Arete("C", "D", 10, 10, 0.1))
    g.ajouter_arete(Arete("D", "A", 20, 20, 0.3))
    g.ajouter_arete(Arete("A", "C", 15, 15, 0.5))
    g.ajouter_arete(Arete("B", "D", 15, 15, 0.4))
    return g


@pytest.fixture
def graphe_discriminant() -> Graphe:
    """Graphe concu pour differencier les criteres.

    Deux chemins de X a Y :
    - Court mais conteste : 10 km, 0.9 charge
    - Long mais fluide : 25 km, 0.1 charge

    Selon les criteres choisis, on prend l'un ou l'autre.
    """
    g = Graphe()
    for nid in ["X", "M", "N", "Y"]:
        g.ajouter_noeud(Noeud(id=nid, nom=nid, coordonnees=Coordonnees(0, 0)))
    # Chemin court mais bouche
    g.ajouter_arete(Arete("X", "M", 5, 5, 0.9))
    g.ajouter_arete(Arete("M", "Y", 5, 5, 0.9))
    # Chemin long mais fluide
    g.ajouter_arete(Arete("X", "N", 12, 12, 0.1))
    g.ajouter_arete(Arete("N", "Y", 13, 13, 0.1))
    return g


TOUTES_LES_STRATEGIES: list[IStrategieRoutage] = [
    StrategieDijkstra(),
    StrategiePlusProcheVoisin(),
    StrategieGreedy(),
]


class TestContratStrategies:
    """Tests qui s'appliquent a TOUTES les strategies (LSP)."""

    @pytest.mark.parametrize("strategie", TOUTES_LES_STRATEGIES)
    def test_strategie_a_un_nom(self, strategie: IStrategieRoutage) -> None:
        assert strategie.nom != ""

    @pytest.mark.parametrize("strategie", TOUTES_LES_STRATEGIES)
    def test_route_vide_si_aucun_noeud_a_visiter(
        self, strategie: IStrategieRoutage, graphe_test: Graphe
    ) -> None:
        route = strategie.calculer(
            graphe=graphe_test,
            noeud_depart="A",
            noeuds_a_visiter=[],
            criteres=CriteresRoutage(),
            livreur_id=uuid4(),
        )
        assert route.nombre_arrets == 1
        assert route.distance_totale_km == 0.0

    @pytest.mark.parametrize("strategie", TOUTES_LES_STRATEGIES)
    def test_visite_tous_les_noeuds_demandes(
        self, strategie: IStrategieRoutage, graphe_test: Graphe
    ) -> None:
        route = strategie.calculer(
            graphe=graphe_test,
            noeud_depart="A",
            noeuds_a_visiter=["B", "C", "D"],
            criteres=CriteresRoutage(),
            livreur_id=uuid4(),
        )
        noeuds_visites = {e.noeud_id for e in route.etapes}
        assert {"A", "B", "C", "D"} == noeuds_visites

    @pytest.mark.parametrize("strategie", TOUTES_LES_STRATEGIES)
    def test_ordre_coherent(self, strategie: IStrategieRoutage, graphe_test: Graphe) -> None:
        route = strategie.calculer(
            graphe=graphe_test,
            noeud_depart="A",
            noeuds_a_visiter=["B", "C"],
            criteres=CriteresRoutage(),
            livreur_id=uuid4(),
        )
        ordres = [e.ordre for e in route.etapes]
        assert ordres == sorted(ordres)

    @pytest.mark.parametrize("strategie", TOUTES_LES_STRATEGIES)
    def test_metriques_positives(self, strategie: IStrategieRoutage, graphe_test: Graphe) -> None:
        route = strategie.calculer(
            graphe=graphe_test,
            noeud_depart="A",
            noeuds_a_visiter=["B", "C", "D"],
            criteres=CriteresRoutage(),
            livreur_id=uuid4(),
        )
        assert route.distance_totale_km > 0
        assert route.temps_total_minutes > 0
        assert 0 <= route.charge_moyenne <= 1


class TestStrategieDijkstra:

    def test_nom(self) -> None:
        assert StrategieDijkstra().nom == "DIJKSTRA"

    def test_dijkstra_trouve_ordre_optimal(self, graphe_test: Graphe) -> None:
        """Sur un petit graphe, Dijkstra doit trouver la distance minimale."""
        dijkstra = StrategieDijkstra()
        npv = StrategiePlusProcheVoisin()

        criteres = CriteresRoutage(poids_distance=1.0, poids_temps=0.0, poids_charge=0.0)

        route_d = dijkstra.calculer(graphe_test, "A", ["B", "C", "D"], criteres, uuid4())
        route_npv = npv.calculer(graphe_test, "A", ["B", "C", "D"], criteres, uuid4())

        assert route_d.distance_totale_km <= route_npv.distance_totale_km


class TestInfluenceDesCriteres:
    """Tests qui prouvent que les 3 criteres influencent le resultat."""

    def test_priorite_distance_vs_charge_donne_metriques_differentes(
        self, graphe_discriminant: Graphe
    ) -> None:
        """Sur un graphe avec chemin court-bouche vs long-fluide,
        changer les criteres doit changer la route choisie."""
        strategie = StrategieDijkstra()
        livreur = uuid4()

        # Priorite distance : prefere le chemin court (X->M->Y = 10 km, charge 0.9)
        criteres_distance = CriteresRoutage(poids_distance=1.0, poids_temps=0.0, poids_charge=0.0)
        # Priorite charge : prefere le chemin fluide (X->N->Y = 25 km, charge 0.1)
        criteres_charge = CriteresRoutage(poids_distance=0.0, poids_temps=0.0, poids_charge=1.0)

        route_courte = strategie.calculer(
            graphe_discriminant, "X", ["Y"], criteres_distance, livreur
        )
        route_fluide = strategie.calculer(graphe_discriminant, "X", ["Y"], criteres_charge, livreur)

        # La route courte doit etre plus courte en distance
        assert route_courte.distance_totale_km < route_fluide.distance_totale_km
        # La route fluide doit avoir une charge moyenne plus faible
        assert route_fluide.charge_moyenne < route_courte.charge_moyenne


class TestSelecteurStrategie:

    @pytest.fixture
    def selecteur(self) -> SelecteurStrategieRoutage:
        return SelecteurStrategieRoutage(
            strategies={
                "DIJKSTRA": StrategieDijkstra(),
                "GREEDY": StrategieGreedy(),
                "PLUS_PROCHE_VOISIN": StrategiePlusProcheVoisin(),
            }
        )

    def test_selection_auto_petit_nombre(self, selecteur: SelecteurStrategieRoutage) -> None:
        strat = selecteur.selectionner(nombre_colis=3)
        assert strat.nom == "DIJKSTRA"

    def test_selection_auto_nombre_moyen(self, selecteur: SelecteurStrategieRoutage) -> None:
        strat = selecteur.selectionner(nombre_colis=10)
        assert strat.nom == "GREEDY"

    def test_selection_auto_grand_nombre(self, selecteur: SelecteurStrategieRoutage) -> None:
        strat = selecteur.selectionner(nombre_colis=25)
        assert strat.nom == "PLUS_PROCHE_VOISIN"

    def test_selection_explicite_override_auto(self, selecteur: SelecteurStrategieRoutage) -> None:
        strat = selecteur.selectionner(nombre_colis=3, strategie_demandee="GREEDY")
        assert strat.nom == "GREEDY"

    def test_strategie_inconnue_leve_exception(self, selecteur: SelecteurStrategieRoutage) -> None:
        with pytest.raises(ValueError, match="inconnue"):
            selecteur.selectionner(nombre_colis=3, strategie_demandee="INVENTEE")
