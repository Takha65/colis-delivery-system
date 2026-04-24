"""Schemas Pydantic pour l'API REST (validation entree/sortie)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreerColisRequest(BaseModel):
    poids_kg: float = Field(..., gt=0, le=1000)
    longueur_cm: float = Field(..., gt=0)
    largeur_cm: float = Field(..., gt=0)
    hauteur_cm: float = Field(..., gt=0)
    rue_origine: str = Field(..., min_length=1, max_length=200)
    ville_origine: str = Field(..., min_length=1, max_length=100)
    code_postal_origine: str = Field(..., min_length=1, max_length=20)
    pays_origine: str = Field(default="Canada", max_length=50)
    rue_destination: str = Field(..., min_length=1, max_length=200)
    ville_destination: str = Field(..., min_length=1, max_length=100)
    code_postal_destination: str = Field(..., min_length=1, max_length=20)
    pays_destination: str = Field(default="Canada", max_length=50)
    type_colis: str = Field(default="STANDARD", pattern="^(STANDARD|FRAGILE|EXPRESS)$")


class TransiterColisRequest(BaseModel):
    """Corps de la requete POST /api/colis/{id}/transiter."""

    nouvel_etat: str = Field(..., pattern="^(EN_TRANSIT|LIVRE|CONFIRME)$")
    commentaire: str = Field(default="", max_length=500)


class AdresseResponse(BaseModel):
    rue: str
    ville: str
    code_postal: str
    pays: str


class ColisResponse(BaseModel):
    id: UUID
    tracking_number: str
    poids_kg: float
    longueur_cm: float
    largeur_cm: float
    hauteur_cm: float
    adresse_origine: AdresseResponse
    adresse_destination: AdresseResponse
    type_colis: str
    statut: str
    date_creation: datetime


class HistoriqueStatutResponse(BaseModel):
    id: UUID
    colis_id: UUID
    statut_precedent: str
    statut_nouveau: str
    date_transition: datetime
    commentaire: str
