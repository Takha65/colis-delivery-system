"""Tests unitaires des Value Objects."""

import pytest

from src.domain.exceptions import InvalidColisError
from src.domain.value_objects import (
    Adresse,
    Coordonnees,
    Dimensions,
    Poids,
    TrackingNumber,
)


class TestPoids:
    """Tests du Value Object Poids."""

    def test_creation_valide(self) -> None:
        poids = Poids(valeur_kg=5.0)
        assert poids.valeur_kg == 5.0

    def test_poids_negatif_leve_exception(self) -> None:
        with pytest.raises(InvalidColisError, match="strictement positif"):
            Poids(valeur_kg=-1.0)

    def test_poids_zero_leve_exception(self) -> None:
        with pytest.raises(InvalidColisError, match="strictement positif"):
            Poids(valeur_kg=0.0)

    def test_poids_trop_lourd_leve_exception(self) -> None:
        with pytest.raises(InvalidColisError, match="1000"):
            Poids(valeur_kg=1500.0)

    def test_est_lourd(self) -> None:
        assert Poids(valeur_kg=35.0).est_lourd() is True
        assert Poids(valeur_kg=10.0).est_lourd() is False

    def test_immuable(self) -> None:
        """Un Poids ne peut pas etre modifie apres creation."""
        poids = Poids(valeur_kg=5.0)
        with pytest.raises(Exception):  # FrozenInstanceError
            poids.valeur_kg = 10.0  # type: ignore


class TestDimensions:
    """Tests du Value Object Dimensions."""

    def test_creation_valide(self) -> None:
        dim = Dimensions(longueur_cm=10, largeur_cm=20, hauteur_cm=30)
        assert dim.volume_cm3 == 6000

    def test_dimension_negative_leve_exception(self) -> None:
        with pytest.raises(InvalidColisError, match="longueur"):
            Dimensions(longueur_cm=-1, largeur_cm=20, hauteur_cm=30)

    def test_est_volumineux(self) -> None:
        grand = Dimensions(longueur_cm=100, largeur_cm=100, hauteur_cm=100)
        petit = Dimensions(longueur_cm=10, largeur_cm=10, hauteur_cm=10)
        assert grand.est_volumineux() is True
        assert petit.est_volumineux() is False


class TestAdresse:
    """Tests du Value Object Adresse."""

    def test_creation_valide(self) -> None:
        adresse = Adresse(
            rue="2500 Boul Universite",
            ville="Sherbrooke",
            code_postal="J1K 2R1",
        )
        assert adresse.pays == "Canada"
        assert adresse.coordonnees is None

    def test_avec_coordonnees(self) -> None:
        coord = Coordonnees(latitude=45.3753, longitude=-71.9247)
        adresse = Adresse(
            rue="2500 Boul Universite",
            ville="Sherbrooke",
            code_postal="J1K 2R1",
            coordonnees=coord,
        )
        assert adresse.coordonnees == coord

    def test_rue_vide_leve_exception(self) -> None:
        with pytest.raises(InvalidColisError, match="rue"):
            Adresse(rue="  ", ville="Sherbrooke", code_postal="J1K 2R1")

    def test_coordonnees_invalides_leve_exception(self) -> None:
        with pytest.raises(InvalidColisError, match="Latitude"):
            Coordonnees(latitude=100, longitude=0)
        with pytest.raises(InvalidColisError, match="Longitude"):
            Coordonnees(latitude=0, longitude=200)


class TestTrackingNumber:
    """Tests du Value Object TrackingNumber."""

    def test_creation_valide(self) -> None:
        tn = TrackingNumber(valeur="CLS-ABC12345")
        assert str(tn) == "CLS-ABC12345"

    def test_format_invalide_leve_exception(self) -> None:
        with pytest.raises(InvalidColisError, match="format attendu"):
            TrackingNumber(valeur="ABC123")
        with pytest.raises(InvalidColisError):
            TrackingNumber(valeur="CLS-abc12345")  # Minuscules

    def test_generer_produit_format_valide(self) -> None:
        tn = TrackingNumber.generer()
        assert tn.valeur.startswith("CLS-")
        assert len(tn.valeur) == 12

    def test_generer_produit_valeurs_uniques(self) -> None:
        """La generation doit produire des valeurs differentes."""
        numeros = {TrackingNumber.generer().valeur for _ in range(100)}
        assert len(numeros) == 100  # Tous uniques
