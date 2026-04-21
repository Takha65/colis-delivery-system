"""Implementation SQLAlchemy du ColisRepository (Pattern Repository)."""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.application.ports import IColisRepository
from src.domain.entities import Colis
from src.domain.value_objects import TrackingNumber
from src.infrastructure.persistence.colis_mapper import to_entity, to_model
from src.infrastructure.persistence.colis_model import ColisModel


class SQLAlchemyColisRepository(IColisRepository):
    """Implementation concrete du repository avec SQLAlchemy + PostgreSQL."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, colis: Colis) -> Colis:
        existing = self._session.get(ColisModel, colis.id)
        if existing is not None:
            # Mise a jour : remplacer les attributs
            model = to_model(colis)
            for key, value in model.__dict__.items():
                if not key.startswith("_"):
                    setattr(existing, key, value)
        else:
            self._session.add(to_model(colis))
        self._session.commit()
        return colis

    def get_by_id(self, colis_id: UUID) -> Optional[Colis]:
        model = self._session.get(ColisModel, colis_id)
        return to_entity(model) if model else None

    def get_by_tracking_number(
        self, tracking_number: TrackingNumber
    ) -> Optional[Colis]:
        model = (
            self._session.query(ColisModel)
            .filter_by(tracking_number=tracking_number.valeur)
            .first()
        )
        return to_entity(model) if model else None

    def find_all(self) -> list[Colis]:
        models = self._session.query(ColisModel).all()
        return [to_entity(m) for m in models]

    def delete(self, colis_id: UUID) -> bool:
        model = self._session.get(ColisModel, colis_id)
        if model is None:
            return False
        self._session.delete(model)
        self._session.commit()
        return True
