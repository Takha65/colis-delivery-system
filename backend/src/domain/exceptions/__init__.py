"""Exceptions metier du domaine."""

from src.domain.exceptions.colis_exceptions import (
    ColisError,
    ColisNotFoundError,
    InvalidColisError,
    InvalidTransitionError,
)
from src.domain.exceptions.routage_exceptions import (
    CapaciteDepasseeError,
    GrapheInvalideError,
    NoeudIntrouvableError,
    RoutageError,
    RouteImpossibleError,
)

__all__ = [
    "ColisError",
    "ColisNotFoundError",
    "InvalidColisError",
    "InvalidTransitionError",
    "RoutageError",
    "GrapheInvalideError",
    "NoeudIntrouvableError",
    "RouteImpossibleError",
    "CapaciteDepasseeError",
]
