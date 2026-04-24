"""Tests unitaires du Value Object CriteresRoutage."""

import pytest

from src.domain.exceptions import InvalidColisError
from src.domain.value_objects import CriteresRoutage


class TestCriteresRoutage:

    def test_valeurs_par_defaut_valides(self) -> None:
        c = CriteresRoutage()
        assert c.poids_distance == 0.5
        assert c.poids_temps == 0.3
        assert c.poids_charge == 0.2

    def test_somme_invalide_leve_exception(self) -> None:
        with pytest.raises(InvalidColisError, match="somme"):
            CriteresRoutage(poids_distance=0.5, poids_temps=0.5, poids_charge=0.5)

    def test_poids_negatif_leve_exception(self) -> None:
        with pytest.raises(InvalidColisError):
            CriteresRoutage(poids_distance=-0.1, poids_temps=0.6, poids_charge=0.5)

    def test_cout_pondere_distance_seule(self) -> None:
        c = CriteresRoutage(poids_distance=1.0, poids_temps=0.0, poids_charge=0.0)
        # Seule la distance compte
        assert c.cout_pondere(distance_km=100, temps_minutes=60, charge_trafic=0.5) == 100.0

    def test_cout_pondere_temps_seul(self) -> None:
        c = CriteresRoutage(poids_distance=0.0, poids_temps=1.0, poids_charge=0.0)
        assert c.cout_pondere(distance_km=100, temps_minutes=60, charge_trafic=0.5) == 60.0

    def test_cout_pondere_mixte(self) -> None:
        c = CriteresRoutage(poids_distance=0.5, poids_temps=0.5, poids_charge=0.0)
        # 0.5*100 + 0.5*60 = 80
        assert c.cout_pondere(distance_km=100, temps_minutes=60, charge_trafic=0) == 80.0
