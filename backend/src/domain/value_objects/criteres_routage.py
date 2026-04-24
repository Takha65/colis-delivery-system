"""Value Object : criteres ponderes pour le calcul de route."""

from dataclasses import dataclass

from src.domain.exceptions import InvalidColisError


@dataclass(frozen=True)
class CriteresRoutage:
    """Ponderation des 3 criteres d'optimisation de route.

    La somme doit etre egale a 1.0 (100%).
    """

    poids_distance: float = 0.5
    poids_temps: float = 0.3
    poids_charge: float = 0.2

    def __post_init__(self) -> None:
        if not all(0 <= p <= 1 for p in [self.poids_distance, self.poids_temps, self.poids_charge]):
            raise InvalidColisError("Les poids doivent etre entre 0 et 1")
        somme = self.poids_distance + self.poids_temps + self.poids_charge
        if abs(somme - 1.0) > 0.01:  # Tolerance pour les arrondis
            raise InvalidColisError(f"La somme des poids doit etre egale a 1.0 (recu: {somme})")

    def cout_pondere(self, distance_km: float, temps_minutes: float, charge_trafic: float) -> float:
        """Calcule le cout pondere d'une arete selon les criteres.

        Les valeurs sont normalisees pour etre comparables :
        - distance : km (valeur brute)
        - temps : minutes (valeur brute)
        - charge : 0-1, multiplie par 100 pour avoir un impact comparable
        """
        return (
            self.poids_distance * distance_km
            + self.poids_temps * temps_minutes
            + self.poids_charge * charge_trafic * 100
        )
