"""Mappers M2 : entites <-> schemas API."""

from src.domain.entities import Graphe, Livreur, Route
from src.interfaces.api.schemas_m2 import (
    AreteResponse,
    EtapeRouteResponse,
    GrapheResponse,
    LivreurResponse,
    NoeudResponse,
    RouteResponse,
)


def livreur_to_response(livreur: Livreur) -> LivreurResponse:
    return LivreurResponse(
        id=livreur.id,
        nom=livreur.nom,
        capacite_max_kg=livreur.capacite_max_kg,
        position_depart_id=livreur.position_depart_id,
    )


def route_to_response(route: Route) -> RouteResponse:
    return RouteResponse(
        id=route.id,
        livreur_id=route.livreur_id,
        strategie_utilisee=route.strategie_utilisee,
        etapes=[
            EtapeRouteResponse(
                noeud_id=e.noeud_id,
                nom_lieu=e.nom_lieu,
                ordre=e.ordre,
                distance_depuis_precedent_km=e.distance_depuis_precedent_km,
                temps_depuis_precedent_min=e.temps_depuis_precedent_min,
            )
            for e in route.etapes
        ],
        distance_totale_km=route.distance_totale_km,
        temps_total_minutes=route.temps_total_minutes,
        charge_moyenne=route.charge_moyenne,
        nombre_arrets=route.nombre_arrets,
    )


def graphe_to_response(graphe: Graphe) -> GrapheResponse:
    noeuds = [
        NoeudResponse(
            id=n.id,
            nom=n.nom,
            latitude=n.coordonnees.latitude,
            longitude=n.coordonnees.longitude,
        )
        for n in graphe.noeuds.values()
    ]
    # Deduplication des aretes (graphe bidirectionnel)
    aretes_vues: set[tuple[str, str]] = set()
    aretes_list = []
    for source_id, aretes in graphe.aretes_par_source.items():
        for a in aretes:
            cle = tuple(sorted([a.noeud_source, a.noeud_cible]))
            if cle in aretes_vues:
                continue
            aretes_vues.add(cle)
            aretes_list.append(
                AreteResponse(
                    source=a.noeud_source,
                    cible=a.noeud_cible,
                    distance_km=a.distance_km,
                    temps_minutes=a.temps_minutes,
                    charge_trafic=a.charge_trafic,
                )
            )
    return GrapheResponse(noeuds=noeuds, aretes=aretes_list)
