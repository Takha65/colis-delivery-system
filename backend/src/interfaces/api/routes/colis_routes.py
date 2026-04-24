"""Routes REST pour les colis."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases import (
    CreerColisCommand,
    CreerColisUseCase,
    ListerColisUseCase,
    ObtenirColisUseCase,
    ObtenirHistoriqueUseCase,
    SupprimerColisUseCase,
    TransiterColisCommand,
    TransiterColisUseCase,
)
from src.domain.exceptions import (
    ColisNotFoundError,
    InvalidColisError,
    InvalidTransitionError,
)
from src.interfaces.api.dependencies import (
    get_creer_colis_use_case,
    get_lister_colis_use_case,
    get_obtenir_colis_use_case,
    get_obtenir_historique_use_case,
    get_supprimer_colis_use_case,
    get_transiter_colis_use_case,
)
from src.interfaces.api.mappers import colis_to_response, historique_to_response
from src.interfaces.api.schemas import (
    ColisResponse,
    CreerColisRequest,
    HistoriqueStatutResponse,
    TransiterColisRequest,
)


router = APIRouter(prefix="/api/colis", tags=["colis"])


@router.post("", response_model=ColisResponse, status_code=status.HTTP_201_CREATED)
def creer_colis(
    request: CreerColisRequest,
    use_case: Annotated[CreerColisUseCase, Depends(get_creer_colis_use_case)],
) -> ColisResponse:
    try:
        command = CreerColisCommand(**request.model_dump())
        colis = use_case.execute(command)
        return colis_to_response(colis)
    except InvalidColisError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[ColisResponse])
def lister_colis(
    use_case: Annotated[ListerColisUseCase, Depends(get_lister_colis_use_case)],
) -> list[ColisResponse]:
    return [colis_to_response(c) for c in use_case.execute()]


@router.get("/{colis_id}", response_model=ColisResponse)
def obtenir_colis(
    colis_id: UUID,
    use_case: Annotated[ObtenirColisUseCase, Depends(get_obtenir_colis_use_case)],
) -> ColisResponse:
    try:
        return colis_to_response(use_case.execute(colis_id))
    except ColisNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.delete("/{colis_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_colis(
    colis_id: UUID,
    use_case: Annotated[SupprimerColisUseCase, Depends(get_supprimer_colis_use_case)],
) -> None:
    try:
        use_case.execute(colis_id)
    except ColisNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{colis_id}/transiter", response_model=ColisResponse)
def transiter_colis(
    colis_id: UUID,
    request: TransiterColisRequest,
    use_case: Annotated[TransiterColisUseCase, Depends(get_transiter_colis_use_case)],
) -> ColisResponse:
    try:
        command = TransiterColisCommand(
            colis_id=colis_id,
            nouvel_etat=request.nouvel_etat,
            commentaire=request.commentaire,
        )
        return colis_to_response(use_case.execute(command))
    except ColisNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidTransitionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/{colis_id}/historique", response_model=list[HistoriqueStatutResponse])
def obtenir_historique(
    colis_id: UUID,
    use_case: Annotated[ObtenirHistoriqueUseCase, Depends(get_obtenir_historique_use_case)],
) -> list[HistoriqueStatutResponse]:
    try:
        return [historique_to_response(h) for h in use_case.execute(colis_id)]
    except ColisNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
