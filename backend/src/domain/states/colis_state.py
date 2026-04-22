"""Pattern State : chaque etat d'un colis est une classe dediee."""
from abc import ABC, abstractmethod

from src.domain.exceptions import InvalidTransitionError


class ColisState(ABC):
    """Etat abstrait d'un colis.

    Chaque sous-classe represente un etat concret et definit :
    - son nom (nom)
    - les transitions qu'elle autorise
    - si l'etat est final
    - si le colis peut encore etre modifie dans cet etat
    """

    @property
    @abstractmethod
    def nom(self) -> str:
        """Nom unique de l'etat (CREE, EN_TRANSIT, LIVRE, CONFIRME)."""

    @abstractmethod
    def transitions_autorisees(self) -> set[str]:
        """Retourne les noms des etats vers lesquels on peut transiter."""

    def peut_transiter_vers(self, autre: "ColisState") -> bool:
        """Verifie si la transition vers un autre etat est autorisee."""
        return autre.nom in self.transitions_autorisees()

    def transiter_vers(self, autre: "ColisState") -> "ColisState":
        """Effectue la transition et retourne le nouvel etat.

        Raises:
            InvalidTransitionError: si la transition n'est pas autorisee.
        """
        if not self.peut_transiter_vers(autre):
            raise InvalidTransitionError(
                statut_actuel=self.nom, statut_cible=autre.nom
            )
        return autre

    def est_final(self) -> bool:
        """Un etat est final s'il n'autorise aucune transition."""
        return len(self.transitions_autorisees()) == 0

    def est_modifiable(self) -> bool:
        """Par defaut, un colis n'est modifiable que dans l'etat initial."""
        return False

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ColisState) and self.nom == other.nom

    def __hash__(self) -> int:
        return hash(self.nom)

    def __str__(self) -> str:
        return self.nom


class ColisCree(ColisState):
    """Colis cree, en attente de prise en charge."""

    @property
    def nom(self) -> str:
        return "CREE"

    def transitions_autorisees(self) -> set[str]:
        return {"EN_TRANSIT"}

    def est_modifiable(self) -> bool:
        return True


class ColisEnTransit(ColisState):
    """Colis en cours de livraison."""

    @property
    def nom(self) -> str:
        return "EN_TRANSIT"

    def transitions_autorisees(self) -> set[str]:
        return {"LIVRE"}


class ColisLivre(ColisState):
    """Colis livre, en attente de confirmation."""

    @property
    def nom(self) -> str:
        return "LIVRE"

    def transitions_autorisees(self) -> set[str]:
        return {"CONFIRME"}


class ColisConfirme(ColisState):
    """Colis livre et confirme par le destinataire (etat final)."""

    @property
    def nom(self) -> str:
        return "CONFIRME"

    def transitions_autorisees(self) -> set[str]:
        return set()  # Etat final


# Registre pour retrouver un etat par son nom (utile au mapper SQL)
_ETATS: dict[str, ColisState] = {
    "CREE": ColisCree(),
    "EN_TRANSIT": ColisEnTransit(),
    "LIVRE": ColisLivre(),
    "CONFIRME": ColisConfirme(),
}


def etat_depuis_nom(nom: str) -> ColisState:
    """Retourne l'instance d'etat correspondant au nom."""
    if nom not in _ETATS:
        raise ValueError(f"Etat inconnu: {nom}")
    return _ETATS[nom]
