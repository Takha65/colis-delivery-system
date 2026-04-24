"""Mappers entre entites domaine et schemas API."""

from src.domain.entities import Colis, HistoriqueStatut
from src.interfaces.api.schemas import (
    AdresseResponse,
    ColisResponse,
    HistoriqueStatutResponse,
)


def colis_to_response(colis: Colis) -> ColisResponse:
    return ColisResponse(
        id=colis.id,
        tracking_number=colis.tracking_number.valeur,
        poids_kg=colis.poids.valeur_kg,
        longueur_cm=colis.dimensions.longueur_cm,
        largeur_cm=colis.dimensions.largeur_cm,
        hauteur_cm=colis.dimensions.hauteur_cm,
        adresse_origine=AdresseResponse(
            rue=colis.adresse_origine.rue,
            ville=colis.adresse_origine.ville,
            code_postal=colis.adresse_origine.code_postal,
            pays=colis.adresse_origine.pays,
        ),
        adresse_destination=AdresseResponse(
            rue=colis.adresse_destination.rue,
            ville=colis.adresse_destination.ville,
            code_postal=colis.adresse_destination.code_postal,
            pays=colis.adresse_destination.pays,
        ),
        type_colis=colis.type_colis.value,
        statut=colis.etat.nom,
        date_creation=colis.date_creation,
    )


def historique_to_response(h: HistoriqueStatut) -> HistoriqueStatutResponse:
    return HistoriqueStatutResponse(
        id=h.id,
        colis_id=h.colis_id,
        statut_precedent=h.statut_precedent,
        statut_nouveau=h.statut_nouveau,
        date_transition=h.date_transition,
        commentaire=h.commentaire,
    )
