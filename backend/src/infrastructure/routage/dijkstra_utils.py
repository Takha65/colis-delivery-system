"""Utilitaires Dijkstra : plus court chemin pondere entre 2 noeuds."""
import heapq

from src.domain.entities import Graphe
from src.domain.exceptions import RouteImpossibleError
from src.domain.value_objects import CriteresRoutage


def plus_court_chemin(
    graphe: Graphe,
    depart: str,
    arrivee: str,
    criteres: CriteresRoutage,
) -> tuple[list[str], float, float, float, float]:
    """Calcule le plus court chemin pondere entre 2 noeuds.

    Returns:
        (chemin, cout_pondere_total, distance_km, temps_minutes, charge_moyenne)

    Raises:
        RouteImpossibleError: si aucun chemin n'existe.
    """
    if depart == arrivee:
        return ([depart], 0.0, 0.0, 0.0, 0.0)

    # Dijkstra classique avec file de priorite
    # (cout_pondere, noeud, chemin, distance_cumulee, temps_cumule, charges)
    queue: list[tuple[float, str, list[str], float, float, list[float]]] = [
        (0.0, depart, [depart], 0.0, 0.0, [])
    ]
    visites: set[str] = set()

    while queue:
        cout, noeud, chemin, distance, temps, charges = heapq.heappop(queue)

        if noeud == arrivee:
            charge_moyenne = sum(charges) / len(charges) if charges else 0.0
            return (chemin, cout, distance, temps, charge_moyenne)

        if noeud in visites:
            continue
        visites.add(noeud)

        for arete in graphe.voisins(noeud):
            if arete.noeud_cible in visites:
                continue
            cout_arete = criteres.cout_pondere(
                distance_km=arete.distance_km,
                temps_minutes=arete.temps_minutes,
                charge_trafic=arete.charge_trafic,
            )
            heapq.heappush(
                queue,
                (
                    cout + cout_arete,
                    arete.noeud_cible,
                    chemin + [arete.noeud_cible],
                    distance + arete.distance_km,
                    temps + arete.temps_minutes,
                    charges + [arete.charge_trafic],
                ),
            )

    raise RouteImpossibleError(
        f"Aucun chemin trouve entre '{depart}' et '{arrivee}'"
    )
