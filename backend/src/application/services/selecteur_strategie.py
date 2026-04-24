"""Service : selection intelligente d'une strategie de routage."""
from typing import Optional

from src.application.ports import IStrategieRoutage


class SelecteurStrategieRoutage:
    """Choisit la strategie adaptee au contexte.

    Regles :
    - 1-5 colis  -> Dijkstra (optimal, faisable)
    - 6-15 colis -> Greedy (bon compromis)
    - > 15 colis -> PlusProcheVoisin (rapide)

    Peut etre override par un nom explicite fourni par l'utilisateur.
    """

    def __init__(self, strategies: dict[str, IStrategieRoutage]) -> None:
        """
        Args:
            strategies: dict {nom -> instance} des strategies disponibles.
                        Ex: {"DIJKSTRA": StrategieDijkstra(), ...}
        """
        self._strategies = strategies

    def selectionner(
        self,
        nombre_colis: int,
        strategie_demandee: Optional[str] = None,
    ) -> IStrategieRoutage:
        """Selectionne la strategie appropriee.

        Args:
            nombre_colis: nombre de colis a livrer
            strategie_demandee: nom explicite ou None pour selection auto

        Returns:
            Une instance de strategie.
        """
        if strategie_demandee is not None:
            if strategie_demandee not in self._strategies:
                raise ValueError(
                    f"Strategie inconnue: {strategie_demandee}. "
                    f"Disponibles: {list(self._strategies.keys())}"
                )
            return self._strategies[strategie_demandee]

        # Selection automatique
        if nombre_colis <= 5:
            return self._strategies["DIJKSTRA"]
        if nombre_colis <= 15:
            return self._strategies["GREEDY"]
        return self._strategies["PLUS_PROCHE_VOISIN"]

    def strategies_disponibles(self) -> list[str]:
        """Retourne les noms des strategies disponibles."""
        return list(self._strategies.keys())
