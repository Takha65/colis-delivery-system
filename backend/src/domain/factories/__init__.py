"""Factories pour la creation de colis (Pattern Factory Method)."""
from src.domain.factories.colis_factory import (
    ColisFactory,
    ExpressColisFactory,
    FragileColisFactory,
    StandardColisFactory,
    get_factory,
)

__all__ = [
    "ColisFactory",
    "StandardColisFactory",
    "FragileColisFactory",
    "ExpressColisFactory",
    "get_factory",
]
