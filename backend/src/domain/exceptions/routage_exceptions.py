"""Exceptions specifiques au domaine du routage."""


class RoutageError(Exception):
    """Exception de base pour les erreurs de routage."""


class GrapheInvalideError(RoutageError):
    """Leve lorsque le graphe est mal forme (noeud manquant, etc.)."""


class NoeudIntrouvableError(RoutageError):
    """Leve lorsqu'un noeud demande n'existe pas dans le graphe."""

    def __init__(self, noeud_id: str) -> None:
        super().__init__(f"Noeud '{noeud_id}' introuvable dans le graphe")
        self.noeud_id = noeud_id


class RouteImpossibleError(RoutageError):
    """Leve lorsqu'aucun chemin n'existe entre deux points."""


class CapaciteDepasseeError(RoutageError):
    """Leve lorsque la capacite du livreur est depassee."""

    def __init__(self, capacite_kg: float, poids_total_kg: float) -> None:
        super().__init__(f"Capacite depassee : {poids_total_kg} kg > {capacite_kg} kg")
        self.capacite_kg = capacite_kg
        self.poids_total_kg = poids_total_kg
