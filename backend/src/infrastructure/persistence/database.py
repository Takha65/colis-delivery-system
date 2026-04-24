"""Configuration SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.shared.config import settings


class Base(DeclarativeBase):
    """Classe de base pour tous les modeles SQLAlchemy."""


engine = create_engine(settings.database_url, echo=settings.debug)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """Dependance FastAPI : fournit une session DB par requete.

    La session commit automatiquement a la fin d'une requete reussie
    et rollback si une exception survient.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
