"""Handlers concrets pour les evenements du domaine."""

import logging

from src.domain.events import (
    ColisCreeEvent,
    ColisLivreEvent,
    ColisTransiteEvent,
    RouteCalculeeEvent,
)

logger = logging.getLogger(__name__)


def log_colis_cree(event: ColisCreeEvent) -> None:
    logger.info(
        "Colis cree: %s (type=%s, id=%s)",
        event.tracking_number,
        event.type_colis,
        event.colis_id,
    )


def log_colis_transite(event: ColisTransiteEvent) -> None:
    logger.info(
        "Colis %s transite: %s -> %s",
        event.tracking_number,
        event.statut_precedent,
        event.statut_nouveau,
    )


def log_colis_livre(event: ColisLivreEvent) -> None:
    logger.info("Colis livre: %s", event.tracking_number)


def log_route_calculee(event: RouteCalculeeEvent) -> None:
    logger.info(
        "Route calculee: strategie=%s, distance=%.1fkm, arrets=%d",
        event.strategie,
        event.distance_totale_km,
        event.nombre_arrets,
    )
