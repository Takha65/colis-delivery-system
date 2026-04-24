"""Tests unitaires de NominatimGeocodingAdapter (avec mock HTTP)."""
from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.domain.value_objects import Adresse
from src.infrastructure.external import NominatimGeocodingAdapter


@pytest.fixture
def adresse() -> Adresse:
    return Adresse(
        rue="2500 Boul Universite",
        ville="Sherbrooke",
        code_postal="J1K 2R1",
    )


@pytest.fixture
def adapter() -> NominatimGeocodingAdapter:
    """Adapter avec rate limit desactive (dernier_appel loin dans le passe)."""
    return NominatimGeocodingAdapter(
        base_url="https://fake-nominatim.test",
        user_agent="TestAgent/1.0",
        timeout_seconds=5,
    )


class TestNominatimAdapter:

    def test_geocode_reussi_retourne_coordonnees(self, adapter, adresse) -> None:
        reponse_mock = MagicMock()
        reponse_mock.raise_for_status = MagicMock()
        reponse_mock.json.return_value = [
            {"lat": "45.4000", "lon": "-71.9000", "display_name": "..."}
        ]

        with patch("httpx.get", return_value=reponse_mock):
            coord = adapter.geocoder(adresse)

        assert coord is not None
        assert coord.latitude == pytest.approx(45.4)
        assert coord.longitude == pytest.approx(-71.9)

    def test_adresse_introuvable_retourne_none(self, adapter, adresse) -> None:
        reponse_mock = MagicMock()
        reponse_mock.raise_for_status = MagicMock()
        reponse_mock.json.return_value = []  # Pas de resultat

        with patch("httpx.get", return_value=reponse_mock):
            coord = adapter.geocoder(adresse)

        assert coord is None

    def test_erreur_http_retourne_none(self, adapter, adresse) -> None:
        with patch("httpx.get", side_effect=httpx.HTTPError("Timeout")):
            coord = adapter.geocoder(adresse)

        assert coord is None

    def test_reponse_mal_formee_retourne_none(self, adapter, adresse) -> None:
        reponse_mock = MagicMock()
        reponse_mock.raise_for_status = MagicMock()
        reponse_mock.json.return_value = [{"invalid": "data"}]  # Pas de lat/lon

        with patch("httpx.get", return_value=reponse_mock):
            coord = adapter.geocoder(adresse)

        assert coord is None

    def test_envoie_bon_user_agent(self, adapter, adresse) -> None:
        reponse_mock = MagicMock()
        reponse_mock.raise_for_status = MagicMock()
        reponse_mock.json.return_value = [{"lat": "45", "lon": "-71"}]

        with patch("httpx.get", return_value=reponse_mock) as mock_get:
            adapter.geocoder(adresse)

        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["headers"]["User-Agent"] == "TestAgent/1.0"

    def test_envoie_adresse_dans_parametre_q(self, adapter, adresse) -> None:
        reponse_mock = MagicMock()
        reponse_mock.raise_for_status = MagicMock()
        reponse_mock.json.return_value = [{"lat": "45", "lon": "-71"}]

        with patch("httpx.get", return_value=reponse_mock) as mock_get:
            adapter.geocoder(adresse)

        call_kwargs = mock_get.call_args.kwargs
        assert "Sherbrooke" in call_kwargs["params"]["q"]
        assert call_kwargs["params"]["format"] == "json"
