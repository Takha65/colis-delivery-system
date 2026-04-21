"""Fixtures partagees pour les tests d'integration."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.infrastructure.persistence import Base
from src.infrastructure.persistence.colis_model import ColisModel  # noqa: F401


@pytest.fixture
def test_engine():
    """Cree un engine SQLite en memoire pour les tests."""
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
    """Session SQLAlchemy pour une DB SQLite en memoire."""
    TestingSessionLocal = sessionmaker(
        bind=test_engine, autocommit=False, autoflush=False
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(test_db_session, test_engine, monkeypatch):
    """Client HTTP de test avec DB SQLite en memoire."""
    # 1. Monkey-patch l'engine PostgreSQL pour utiliser SQLite
    from src.infrastructure.persistence import database as db_module
    monkeypatch.setattr(db_module, "engine", test_engine)

    # 2. Import de main APRES le monkey-patch
    from main import app
    from src.infrastructure.persistence.database import get_db

    # 3. Override de la session DB pour les requetes HTTP
    def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_get_db

    # 4. TestClient declenche le startup, qui utilise l'engine patche (SQLite)
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
