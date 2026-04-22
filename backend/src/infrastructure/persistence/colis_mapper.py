"""Mapper entre l'entite domaine Colis et le modele SQLAlchemy ColisModel."""
from src.domain.entities import Colis, HistoriqueStatut, TypeColis
from src.domain.states import etat_depuis_nom
from src.domain.value_objects import Adresse, Dimensions, Poids, TrackingNumber
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
        rue_destination=colis.adresse_destination.rue,
        ville_destination=colis.adresse_destination.ville,
        code_postal_destination=colis.adresse_destination.code_postal,
        pays_destination=colis.adresse_destination.pays,
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


def to_entity(
    model: ColisModel,
    historique_models: list[HistoriqueStatutModel] | None = None,
) -> Colis:
    historique = (
        [historique_to_entity(h) for h in historique_models]
        if historique_models
        else []
    )
    return Colis(
        id=model.id,
        tracking_number=TrackingNumber(valeur=model.tracking_number),
        poids=Poids(valeur_kg=model.poids_kg),
        dimensions=Dimensions(
            longueur_cm=model.longueur_cm,
            largeur_cm=model.largeur_cm,
            hauteur_cm=model.hauteur_cm,
        ),
        adresse_origine=Adresse(
            rue=model.rue_origine,
            ville=model.ville_origine,
            code_postal=model.code_postal_origine,
            pays=model.pays_origine,
        ),
        adresse_destination=Adresse(
            rue=model.rue_destination,
            ville=model.ville_destination,
            code_postal=model.code_postal_destination,
            pays=model.pays_destination,
        ),
        type_colis=TypeColis(model.type_colis),
        etat=etat_depuis_nom(model.statut),
        date_creation=model.date_creation,
        historique=historique,
    )
