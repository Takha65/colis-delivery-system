"""Fixtures partagees pour les tests d'integration."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.infrastructure.persistence import Base
from src.infrastructure.persistence.colis_model import ColisModel  # noqa: F401
from src.infrastructure.persistence.historique_model import HistoriqueStatutModel  # noqa: F401


@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db_session(test_engine):
    TestingSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(test_db_session, test_engine, monkeypatch):
    from src.infrastructure.persistence import database as db_module

    monkeypatch.setattr(db_module, "engine", test_engine)

    from main import app
    from src.infrastructure.persistence.database import get_db
    from src.interfaces.api.dependencies import get_geocoding_service
    from tests.fakes.fake_geocoding_service import FakeGeocodingService

    def override_get_db():
        yield test_db_session

    def override_geocoding():
        return FakeGeocodingService()  # Fake au lieu de Nominatim

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_geocoding_service] = override_geocoding

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
