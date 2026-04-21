"""Routes REST pour les colis."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.use_cases import (
    CreerColisCommand,
    CreerColisUseCase,
    ListerColisUseCase,
    ObtenirColisUseCase,
    SupprimerColisUseCase,
)
from src.domain.exceptions import ColisNotFoundError, InvalidColisError
from src.interfaces.api.dependencies import (
    get_creer_colis_use_case,
    get_lister_colis_use_case,
    get_obtenir_colis_use_case,
    get_supprimer_colis_use_case,
)
from src.interfaces.api.mappers import colis_to_response
from src.interfaces.api.schemas import ColisResponse, CreerColisRequest


router = APIRouter(prefix="/api/colis", tags=["colis"])


@router.post(
    "",
    response_model=ColisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Creer un nouveau colis",
)
def creer_colis(
    request: CreerColisRequest,
    use_case: Annotated[CreerColisUseCase, Depends(get_creer_colis_use_case)],
) -> ColisResponse:
    """Cree un nouveau colis au statut CREE."""
    try:
        command = CreerColisCommand(**request.model_dump())
        colis = use_case.execute(command)
        return colis_to_response(colis)
    except InvalidColisError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get(
    "",
    response_model=list[ColisResponse],
    summary="Lister tous les colis",
)
def lister_colis(
    use_case: Annotated[ListerColisUseCase, Depends(get_lister_colis_use_case)],
) -> list[ColisResponse]:
    """Retourne la liste de tous les colis."""
    colis_list = use_case.execute()
    return [colis_to_response(c) for c in colis_list]


@router.get(
    "/{colis_id}",
    response_model=ColisResponse,
    summary="Obtenir un colis par son id",
)
def obtenir_colis(
    colis_id: UUID,
    use_case: Annotated[ObtenirColisUseCase, Depends(get_obtenir_colis_use_case)],
) -> ColisResponse:
    """Recupere un colis par son identifiant."""
    try:
        colis = use_case.execute(colis_id)
        return colis_to_response(colis)
    except ColisNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete(
    "/{colis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer un colis",
)
def supprimer_colis(
    colis_id: UUID,
    use_case: Annotated[SupprimerColisUseCase, Depends(get_supprimer_colis_use_case)],
) -> None:
    """Supprime un colis par son identifiant."""
    try:
        use_case.execute(colis_id)
    except ColisNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
