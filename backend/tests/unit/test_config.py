"""Tests unitaires de la configuration."""
from src.shared.config import Settings


def test_settings_has_defaults() -> None:
    """Les parametres ont des valeurs par defaut valides."""
    s = Settings()

    assert s.app_name == "Colis Delivery System"
    assert s.app_version == "0.1.0"
    assert s.api_prefix == "/api"
    assert s.nominatim_base_url.startswith("https://")
