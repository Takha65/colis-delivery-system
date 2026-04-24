"""Mapper entre l'entite domaine Colis et le modele SQLAlchemy ColisModel."""

from src.domain.entities import Colis, HistoriqueStatut, TypeColis
from src.domain.states import etat_depuis_nom
from src.domain.value_objects import Adresse, Coordonnees, Dimensions, Poids, TrackingNumber
from src.infrastructure.persistence.colis_model import ColisModel
from src.infrastructure.persistence.historique_model import HistoriqueStatutModel


def to_model(colis: Colis) -> ColisModel:
    return ColisModel(
        id=colis.id,
        tracking_number=colis.tracking_number.valeur,
        poids_kg=colis.poids.valeur_kg,
        longueur_cm=colis.dimensions.longueur_cm,
        largeur_cm=colis.dimensions.largeur_cm,
        hauteur_cm=colis.dimensions.hauteur_cm,
        rue_origine=colis.adresse_origine.rue,
        ville_origine=colis.adresse_origine.ville,
        code_postal_origine=colis.adresse_origine.code_postal,
        pays_origine=colis.adresse_origine.pays,
        lat_origine=(
            colis.adresse_origine.coordonnees.latitude
            if colis.adresse_origine.coordonnees
            else None
        ),
        lon_origine=(
            colis.adresse_origine.coordonnees.longitude
            if colis.adresse_origine.coordonnees
            else None
        ),
        rue_destination=colis.adresse_destination.rue,
        ville_destination=colis.adresse_destination.ville,
        code_postal_destination=colis.adresse_destination.code_postal,
        pays_destination=colis.adresse_destination.pays,
        lat_destination=(
            colis.adresse_destination.coordonnees.latitude
            if colis.adresse_destination.coordonnees
            else None
        ),
        lon_destination=(
            colis.adresse_destination.coordonnees.longitude
            if colis.adresse_destination.coordonnees
            else None
        ),
        type_colis=colis.type_colis.value,
        statut=colis.etat.nom,
        date_creation=colis.date_creation,
    )


def historique_to_model(h: HistoriqueStatut) -> HistoriqueStatutModel:
    return HistoriqueStatutModel(
        id=h.id,
        colis_id=h.colis_id,
        statut_precedent=h.statut_precedent,
        statut_nouveau=h.statut_nouveau,
        date_transition=h.date_transition,
        commentaire=h.commentaire,
    )


def historique_to_entity(m: HistoriqueStatutModel) -> HistoriqueStatut:
    return HistoriqueStatut(
        id=m.id,
        colis_id=m.colis_id,
        statut_precedent=m.statut_precedent,
        statut_nouveau=m.statut_nouveau,
        date_transition=m.date_transition,
        commentaire=m.commentaire,
    )


def _adresse_depuis_model(
    rue: str,
    ville: str,
    code_postal: str,
    pays: str,
    lat: float | None,
    lon: float | None,
) -> Adresse:
    coordonnees = None
    if lat is not None and lon is not None:
        coordonnees = Coordonnees(latitude=lat, longitude=lon)
    return Adresse(
        rue=rue,
        ville=ville,
        code_postal=code_postal,
        pays=pays,
        coordonnees=coordonnees,
    )


def to_entity(
    model: ColisModel,
    historique_models: list[HistoriqueStatutModel] | None = None,
) -> Colis:
    historique = [historique_to_entity(h) for h in historique_models] if historique_models else []
    return Colis(
        id=model.id,
        tracking_number=TrackingNumber(valeur=model.tracking_number),
        poids=Poids(valeur_kg=model.poids_kg),
        dimensions=Dimensions(
            longueur_cm=model.longueur_cm,
            largeur_cm=model.largeur_cm,
            hauteur_cm=model.hauteur_cm,
        ),
        adresse_origine=_adresse_depuis_model(
            model.rue_origine,
            model.ville_origine,
            model.code_postal_origine,
            model.pays_origine,
            model.lat_origine,
            model.lon_origine,
        ),
        adresse_destination=_adresse_depuis_model(
            model.rue_destination,
            model.ville_destination,
            model.code_postal_destination,
            model.pays_destination,
            model.lat_destination,
            model.lon_destination,
        ),
        type_colis=TypeColis(model.type_colis),
        etat=etat_depuis_nom(model.statut),
        date_creation=model.date_creation,
        historique=historique,
    )
