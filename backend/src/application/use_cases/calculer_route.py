"""Use case : calculer une route optimisee pour un livreur."""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.application.services.event_bus import EventBus
from src.application.services.selecteur_strategie import SelecteurStrategieRoutage
from src.domain.entities import Graphe, Route
from src.domain.events import RouteCalculeeEvent
from src.domain.value_objects import CriteresRoutage


@dataclass
class CalculerRouteCommand:
    livreur_id: UUID
    noeud_depart: str
    noeuds_a_visiter: list[str]
    poids_distance: float = 0.5
    poids_temps: float = 0.3
    poids_charge: float = 0.2
    strategie: Optional[str] = None


class CalculerRouteUseCase:
    def __init__(
        self,
        selecteur: SelecteurStrategieRoutage,
        graphe: Graphe,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self._selecteur = selecteur
        self._graphe = graphe
        self._event_bus = event_bus

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
        route = strategie.calculer(
            graphe=self._graphe,
            noeud_depart=command.noeud_depart,
            noeuds_a_visiter=command.noeuds_a_visiter,
            criteres=criteres,
            livreur_id=command.livreur_id,
        )

        if self._event_bus is not None:
            self._event_bus.publish(
                RouteCalculeeEvent(
                    route_id=route.id,
                    livreur_id=route.livreur_id,
                    strategie=route.strategie_utilisee,
                    distance_totale_km=route.distance_totale_km,
                    nombre_arrets=route.nombre_arrets,
                )
            )

        return route
