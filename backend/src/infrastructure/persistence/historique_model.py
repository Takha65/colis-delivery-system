"""Modele SQLAlchemy pour l'historique des statuts."""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.database import Base


class HistoriqueStatutModel(Base):
    """Representation SQL d'une entree d'historique."""

    __tablename__ = "historique_statuts"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    colis_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("colis.id", ondelete="CASCADE"), nullable=False
    )
    statut_precedent: Mapped[str] = mapped_column(String(20), nullable=False)
    statut_nouveau: Mapped[str] = mapped_column(String(20), nullable=False)
    date_transition: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    commentaire: Mapped[str] = mapped_column(String(500), nullable=False, default="")
