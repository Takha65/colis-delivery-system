"""Use case : calculer une route optimisee pour un livreur."""
from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from src.application.services.selecteur_strategie import SelecteurStrategieRoutage
from src.domain.entities import Graphe, Route
from src.domain.value_objects import CriteresRoutage


@dataclass
class CalculerRouteCommand:
    """Donnees d'entree pour calculer une route."""

    livreur_id: UUID
    noeud_depart: str
    noeuds_a_visiter: list[str]
    poids_distance: float = 0.5
    poids_temps: float = 0.3
    poids_charge: float = 0.2
    strategie: Optional[str] = None  # None = selection auto


class CalculerRouteUseCase:
    """Calcule la meilleure route pour livrer une liste de colis."""

    def __init__(
        self,
        selecteur: SelecteurStrategieRoutage,
        graphe: Graphe,
    ) -> None:
        self._selecteur = selecteur
        self._graphe = graphe

    def execute(self, command: CalculerRouteCommand) -> Route:
        criteres = CriteresRoutage(
            poids_distance=command.poids_distance,
            poids_temps=command.poids_temps,
            poids_charge=command.poids_charge,
        )

        strategie = self._selecteur.selectionner(
            nombre_colis=len(command.noeuds_a_visiter),
            strategie_demandee=command.strategie,
        )

        return strategie.calculer(
            graphe=self._graphe,
            noeud_depart=command.noeud_depart,
            noeuds_a_visiter=command.noeuds_a_visiter,
            criteres=criteres,
            livreur_id=command.livreur_id,
        )
