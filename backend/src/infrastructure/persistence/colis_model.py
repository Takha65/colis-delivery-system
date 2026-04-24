"""Modele SQLAlchemy pour la table colis."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.database import Base


class ColisModel(Base):
    """Representation SQL d'un colis (separee de l'entite domaine)."""

    __tablename__ = "colis"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    tracking_number: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    poids_kg: Mapped[float] = mapped_column(Float, nullable=False)
    longueur_cm: Mapped[float] = mapped_column(Float, nullable=False)
    largeur_cm: Mapped[float] = mapped_column(Float, nullable=False)
    hauteur_cm: Mapped[float] = mapped_column(Float, nullable=False)
    rue_origine: Mapped[str] = mapped_column(String(200), nullable=False)
    ville_origine: Mapped[str] = mapped_column(String(100), nullable=False)
    code_postal_origine: Mapped[str] = mapped_column(String(20), nullable=False)
    pays_origine: Mapped[str] = mapped_column(String(50), nullable=False, default="Canada")
    lat_origine: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon_origine: Mapped[float | None] = mapped_column(Float, nullable=True)
    rue_destination: Mapped[str] = mapped_column(String(200), nullable=False)
    ville_destination: Mapped[str] = mapped_column(String(100), nullable=False)
    code_postal_destination: Mapped[str] = mapped_column(String(20), nullable=False)
    pays_destination: Mapped[str] = mapped_column(String(50), nullable=False, default="Canada")
    lat_destination: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon_destination: Mapped[float | None] = mapped_column(Float, nullable=True)
    type_colis: Mapped[str] = mapped_column(String(20), nullable=False, default="STANDARD")
    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="CREE")
    date_creation: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
