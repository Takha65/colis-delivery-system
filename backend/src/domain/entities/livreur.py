"""Entite Livreur."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Livreur:
    """Un livreur qui transporte des colis."""

    nom: str
    capacite_max_kg: float
    position_depart_id: str  # ID d'un noeud du graphe
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.capacite_max_kg <= 0:
            raise ValueError("La capacite doit etre strictement positive")
        if not self.nom.strip():
            raise ValueError("Le nom du livreur ne peut pas etre vide")
