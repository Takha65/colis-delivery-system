"""Entite Colis - coeur du domaine metier."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

from src.domain.entities.historique_statut import HistoriqueStatut
from src.domain.states import ColisCree, ColisState, etat_depuis_nom
from src.domain.value_objects import Adresse, Dimensions, Poids, TrackingNumber


class TypeColis(str, Enum):
    """Types de colis (determinent les contraintes applicables)."""

    STANDARD = "STANDARD"
    FRAGILE = "FRAGILE"
    EXPRESS = "EXPRESS"


@dataclass
class Colis:
    """Entite representant un colis a livrer.

    L'etat du colis est gere par le pattern State (voir domain/states/).
    Chaque transition cree une entree dans l'historique.
    """

    tracking_number: TrackingNumber
    poids: Poids
    dimensions: Dimensions
    adresse_origine: Adresse
    adresse_destination: Adresse
    type_colis: TypeColis = TypeColis.STANDARD
    etat: ColisState = field(default_factory=ColisCree)
    id: UUID = field(default_factory=uuid4)
    date_creation: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    historique: list[HistoriqueStatut] = field(default_factory=list)

    @property
    def statut(self) -> str:
        """Nom du statut actuel (compatibilite avec l'ancienne API)."""
        return self.etat.nom

    def peut_transiter_vers(self, nom_etat_cible: str) -> bool:
        """Verifie si la transition vers un etat (par nom) est possible."""
        return nom_etat_cible in self.etat.transitions_autorisees()

    def transiter_vers(self, nom_etat_cible: str, commentaire: str = "") -> None:
        """Effectue une transition de statut et enregistre l'historique.

        Args:
            nom_etat_cible: nom de l'etat cible (ex: "EN_TRANSIT")
            commentaire: note optionnelle liee a la transition
        """
        etat_cible = etat_depuis_nom(nom_etat_cible)
        ancien_nom = self.etat.nom
        self.etat = self.etat.transiter_vers(etat_cible)
        self.historique.append(
            HistoriqueStatut(
                colis_id=self.id,
                statut_precedent=ancien_nom,
                statut_nouveau=self.etat.nom,
                commentaire=commentaire,
            )
        )

    def est_livre(self) -> bool:
        """Retourne True si le colis est livre ou confirme."""
        return self.etat.nom in {"LIVRE", "CONFIRME"}

    def est_modifiable(self) -> bool:
        """Delegue au state."""
        return self.etat.est_modifiable()
