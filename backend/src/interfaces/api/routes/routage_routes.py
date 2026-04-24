"""Routes REST pour le routage (calcul, strategies, graphe)."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases import CalculerRouteCommand, CalculerRouteUseCase
from src.domain.entities import Graphe
from src.domain.exceptions import (
    InvalidColisError,
    NoeudIntrouvableError,
    RouteImpossibleError,
)
from src.interfaces.api.dependencies import (
    get_calculer_route_use_case,
    get_graphe,
    get_selecteur_strategie,
)
from src.interfaces.api.mappers_m2 import graphe_to_response, route_to_response
from src.interfaces.api.schemas_m2 import (
    CalculerRouteRequest,
    GrapheResponse,
    RouteResponse,
    StrategieInfo,
)

router = APIRouter(prefix="/api", tags=["routage"])


DESCRIPTIONS_STRATEGIES = {
    "DIJKSTRA": "Exploration optimale par permutations (1-5 colis)",
    "PLUS_PROCHE_VOISIN": "Glouton local rapide (> 15 colis)",
    "GREEDY": "Glouton adaptatif (compromis qualite/vitesse)",
}


@router.post("/routes/calculer", response_model=RouteResponse)
def calculer_route(
    request: CalculerRouteRequest,
    use_case: Annotated[CalculerRouteUseCase, Depends(get_calculer_route_use_case)],
) -> RouteResponse:
    try:
        command = CalculerRouteCommand(
            livreur_id=request.livreur_id,
            noeud_depart=request.noeud_depart,
            noeuds_a_visiter=request.noeuds_a_visiter,
            poids_distance=request.poids_distance,
            poids_temps=request.poids_temps,
            poids_charge=request.poids_charge,
            strategie=request.strategie,
        )
        route = use_case.execute(command)
        return route_to_response(route)
    except NoeudIntrouvableError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except RouteImpossibleError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        ) from exc
    except (InvalidColisError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/strategies", response_model=list[StrategieInfo])
def lister_strategies(
    selecteur: Annotated[
        object, Depends(get_selecteur_strategie)
    ],  # evite circular import
) -> list[StrategieInfo]:
    return [
        StrategieInfo(nom=nom, description=DESCRIPTIONS_STRATEGIES.get(nom, ""))
        for nom in selecteur.strategies_disponibles()
    ]


@router.get("/graphe", response_model=GrapheResponse)
def obtenir_graphe(
    graphe: Annotated[Graphe, Depends(get_graphe)],
) -> GrapheResponse:
    return graphe_to_response(graphe)
