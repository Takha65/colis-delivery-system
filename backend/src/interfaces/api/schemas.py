"""Schemas Pydantic pour l'API REST (validation entree/sortie)."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CreerColisRequest(BaseModel):
    """Donnees JSON recues pour creer un colis."""

    poids_kg: float = Field(..., gt=0, le=1000, description="Poids en kg")
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


class AdresseResponse(BaseModel):
    """Adresse retournee dans les reponses API."""

    rue: str
    ville: str
    code_postal: str
    pays: str


class ColisResponse(BaseModel):
    """Colis retourne dans les reponses API."""

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
