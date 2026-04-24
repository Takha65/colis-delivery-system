"""Modele SQLAlchemy pour la table livreurs."""
from uuid import UUID, uuid4

from sqlalchemy import Float, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.database import Base


class LivreurModel(Base):
    """Representation SQL d'un livreur."""

    __tablename__ = "livreurs"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    capacite_max_kg: Mapped[float] = mapped_column(Float, nullable=False)
    position_depart_id: Mapped[str] = mapped_column(String(10), nullable=False)
