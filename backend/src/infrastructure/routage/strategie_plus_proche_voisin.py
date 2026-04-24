"""Strategie Plus Proche Voisin : glouton rapide."""
from uuid import UUID

from src.application.ports import IStrategieRoutage
from src.domain.entities import EtapeRoute, Graphe, Route
from src.domain.value_objects import CriteresRoutage
from src.infrastructure.routage.dijkstra_utils import plus_court_chemin


class StrategiePlusProcheVoisin(IStrategieRoutage):
    """A chaque etape, choisit le noeud non visite le plus 'proche'.

    'Proche' selon le cout pondere (pas forcement la distance pure).
    Complexite : O(n^2 * V log V).
    Rapide mais sous-optimal sur certains graphes.
    """

    @property
    def nom(self) -> str:
        return "PLUS_PROCHE_VOISIN"

    def calculer(
        self,
        graphe: Graphe,
        noeud_depart: str,
        noeuds_a_visiter: list[str],
        criteres: CriteresRoutage,
        livreur_id: UUID,
    ) -> Route:
        a_visiter = set(noeuds_a_visiter)
        courant = noeud_depart

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
        ordre = 1

        while a_visiter:
            # Trouver le plus proche parmi les noeuds restants
            meilleur = None
            meilleur_cout = float("inf")
            meilleures_infos: tuple = (0.0, 0.0, 0.0)

            for candidat in a_visiter:
                _, cout, dist, tps, charge = plus_court_chemin(
                    graphe, courant, candidat, criteres
                )
                if cout < meilleur_cout:
                    meilleur_cout = cout
                    meilleur = candidat
                    meilleures_infos = (dist, tps, charge)

            if meilleur is None:
                break

            dist, tps, charge = meilleures_infos
            etapes.append(
                EtapeRoute(
                    noeud_id=meilleur,
                    nom_lieu=graphe.noeud(meilleur).nom,
                    ordre=ordre,
                    distance_depuis_precedent_km=dist,
                    temps_depuis_precedent_min=tps,
                )
            )
            distance_totale += dist
            temps_total += tps
            charges.append(charge)

            a_visiter.remove(meilleur)
            courant = meilleur
            ordre += 1

        charge_moyenne = sum(charges) / len(charges) if charges else 0.0

        return Route(
            livreur_id=livreur_id,
            etapes=etapes,
            strategie_utilisee=self.nom,
            distance_totale_km=distance_totale,
            temps_total_minutes=temps_total,
            charge_moyenne=charge_moyenne,
        )
