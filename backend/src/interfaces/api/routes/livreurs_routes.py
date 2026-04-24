"""Routes REST pour les livreurs."""
from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.application.use_cases import (
    CreerLivreurCommand,
    CreerLivreurUseCase,
    ListerLivreursUseCase,
)
from src.interfaces.api.dependencies import (
    get_creer_livreur_use_case,
    get_lister_livreurs_use_case,
)
from src.interfaces.api.mappers_m2 import livreur_to_response
from src.interfaces.api.schemas_m2 import CreerLivreurRequest, LivreurResponse


router = APIRouter(prefix="/api/livreurs", tags=["livreurs"])


@router.post("", response_model=LivreurResponse, status_code=status.HTTP_201_CREATED)
def creer_livreur(
    request: CreerLivreurRequest,
    use_case: Annotated[CreerLivreurUseCase, Depends(get_creer_livreur_use_case)],
) -> LivreurResponse:
    command = CreerLivreurCommand(**request.model_dump())
    livreur = use_case.execute(command)
    return livreur_to_response(livreur)


@router.get("", response_model=list[LivreurResponse])
def lister_livreurs(
    use_case: Annotated[ListerLivreursUseCase, Depends(get_lister_livreurs_use_case)],
) -> list[LivreurResponse]:
    return [livreur_to_response(l) for l in use_case.execute()]
