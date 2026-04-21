"""Configuration SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.shared.config import settings


class Base(DeclarativeBase):
    """Classe de base pour tous les modeles SQLAlchemy."""


engine = create_engine(settings.database_url, echo=settings.debug)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """Dependance FastAPI : fournit une session DB par requete."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
