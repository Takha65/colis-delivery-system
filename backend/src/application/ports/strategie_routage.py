"""Port : interface des strategies de calcul de route."""
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities import Graphe, Route
from src.domain.value_objects import CriteresRoutage


class IStrategieRoutage(ABC):
    """Interface d'une strategie de calcul de route.

    Toutes les strategies (Dijkstra, Plus proche voisin, Greedy) respectent
    ce contrat. Elles sont interchangeables via cette interface (LSP).
    """

    @property
    @abstractmethod
    def nom(self) -> str:
        """Identifiant de la strategie (DIJKSTRA, PLUS_PROCHE_VOISIN, GREEDY)."""

    @abstractmethod
    def calculer(
        self,
        graphe: Graphe,
        noeud_depart: str,
        noeuds_a_visiter: list[str],
        criteres: CriteresRoutage,
        livreur_id: UUID,
    ) -> Route:
        """Calcule la route optimale.

        Args:
            graphe: le reseau routier
            noeud_depart: id du noeud de depart
            noeuds_a_visiter: ids des noeuds a visiter (dans n'importe quel ordre)
            criteres: ponderation des 3 criteres
            livreur_id: pour referencer le livreur dans la Route resultat

        Returns:
            Une Route optimisee selon la strategie.
        """
