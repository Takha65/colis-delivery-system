"""Strategie Greedy : glouton avec heuristique adaptative."""
from uuid import UUID

from src.application.ports import IStrategieRoutage
from src.domain.entities import EtapeRoute, Graphe, Route
from src.domain.value_objects import CriteresRoutage
from src.infrastructure.routage.dijkstra_utils import plus_court_chemin


class StrategieGreedy(IStrategieRoutage):
    """Strategie gloutonne adaptative.

    A chaque etape, combine :
    - Le cout pondere selon les criteres utilisateur
    - Une penalite sur les noeuds 'isoles' (sans voisins proches)

    Bon compromis qualite/vitesse pour des tournees moyennes.
    """

    @property
    def nom(self) -> str:
        return "GREEDY"

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
            meilleur = None
            meilleur_score = float("inf")
            meilleures_infos: tuple = (0.0, 0.0, 0.0)

            for candidat in a_visiter:
                _, cout_direct, dist, tps, charge = plus_court_chemin(
                    graphe, courant, candidat, criteres
                )

                # Score glouton : cout direct + anticipation du prochain saut
                # (penalite si le candidat isole les autres)
                autres = a_visiter - {candidat}
                penalite_isolation = 0.0
                if autres:
                    # Moyenne des couts depuis candidat vers les restants
                    couts_suivants = []
                    for autre in autres:
                        _, c_suivant, _, _, _ = plus_court_chemin(
                            graphe, candidat, autre, criteres
                        )
                        couts_suivants.append(c_suivant)
                    penalite_isolation = min(couts_suivants) * 0.3

                score = cout_direct + penalite_isolation
                if score < meilleur_score:
                    meilleur_score = score
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
