"""Configuration centralisee de l'application."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Parametres applicatifs charges depuis variables d'environnement."""

    # Application
    app_name: str = "Colis Delivery System"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "postgresql://colis:colis@localhost:5432/colis_db"

    # Nominatim API
    nominatim_base_url: str = "https://nominatim.openstreetmap.org"
    nominatim_user_agent: str = "ColisDeliverySystem/0.1 (etudiant@usherbrooke.ca)"
    nominatim_timeout_seconds: int = 10

    # API
    api_prefix: str = "/api"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
