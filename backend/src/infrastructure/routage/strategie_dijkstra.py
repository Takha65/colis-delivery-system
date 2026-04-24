"""Strategie Dijkstra : exploration optimale par permutations."""

from itertools import permutations
from uuid import UUID

from src.application.ports import IStrategieRoutage
from src.domain.entities import EtapeRoute, Graphe, Route
from src.domain.value_objects import CriteresRoutage
from src.infrastructure.routage.dijkstra_utils import plus_court_chemin


class StrategieDijkstra(IStrategieRoutage):
    """Strategie optimale : essaie toutes les permutations.

    Complexite : O(n! * V log V) ou n = nombre de colis, V = noeuds du graphe.
    Adapte pour de petites tournees (< 8 colis).
    """

    @property
    def nom(self) -> str:
        return "DIJKSTRA"

    def calculer(
        self,
        graphe: Graphe,
        noeud_depart: str,
        noeuds_a_visiter: list[str],
        criteres: CriteresRoutage,
        livreur_id: UUID,
    ) -> Route:
        if not noeuds_a_visiter:
            return self._route_vide(livreur_id, noeud_depart, graphe)

        meilleure_permutation = None
        meilleur_cout = float("inf")
        meilleures_infos: list[tuple] = []

        # Tester toutes les permutations possibles
        for perm in permutations(noeuds_a_visiter):
            cout_total = 0.0
            infos_etapes: list[tuple] = []  # (noeud, distance, temps, charge)
            courant = noeud_depart

            # Calculer le cout total de cette permutation
            for noeud_suivant in perm:
                _, cout, dist, tps, charge = plus_court_chemin(
                    graphe, courant, noeud_suivant, criteres
                )
                cout_total += cout
                infos_etapes.append((noeud_suivant, dist, tps, charge))
                courant = noeud_suivant

            if cout_total < meilleur_cout:
                meilleur_cout = cout_total
                meilleure_permutation = perm
                meilleures_infos = infos_etapes

        return self._construire_route(
            livreur_id=livreur_id,
            noeud_depart=noeud_depart,
            permutation=list(meilleure_permutation or []),
            infos_etapes=meilleures_infos,
            graphe=graphe,
        )

    def _construire_route(
        self,
        livreur_id: UUID,
        noeud_depart: str,
        permutation: list[str],
        infos_etapes: list[tuple],
        graphe: Graphe,
    ) -> Route:
        """Construit l'objet Route a partir des resultats de l'algorithme."""
        etapes = [
            EtapeRoute(
                noeud_id=noeud_depart,
                nom_lieu=graphe.noeud(noeud_depart).nom,
                ordre=0,
            )
        ]
        distance_totale = 0.0
        temps_total = 0.0
        charges: list[float] = []

        for i, (noeud_id, dist, tps, charge) in enumerate(infos_etapes, start=1):
            etapes.append(
                EtapeRoute(
                    noeud_id=noeud_id,
                    nom_lieu=graphe.noeud(noeud_id).nom,
                    ordre=i,
                    distance_depuis_precedent_km=dist,
                    temps_depuis_precedent_min=tps,
                )
            )
            distance_totale += dist
            temps_total += tps
            charges.append(charge)

        charge_moyenne = sum(charges) / len(charges) if charges else 0.0

        return Route(
            livreur_id=livreur_id,
            etapes=etapes,
            strategie_utilisee=self.nom,
            distance_totale_km=distance_totale,
            temps_total_minutes=temps_total,
            charge_moyenne=charge_moyenne,
        )

    def _route_vide(self, livreur_id: UUID, noeud_depart: str, graphe: Graphe) -> Route:
        return Route(
            livreur_id=livreur_id,
            etapes=[
                EtapeRoute(
                    noeud_id=noeud_depart,
                    nom_lieu=graphe.noeud(noeud_depart).nom,
                    ordre=0,
                )
            ],
            strategie_utilisee=self.nom,
            distance_totale_km=0.0,
            temps_total_minutes=0.0,
            charge_moyenne=0.0,
        )
