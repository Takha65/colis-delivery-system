"""Implementation SQLAlchemy du ColisRepository.

Note : les operations ne committent PAS. Le commit est la responsabilite
de l'appelant (Unit of Work ou dependency FastAPI via get_db).
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.application.ports import IColisRepository
from src.domain.entities import Colis
from src.domain.value_objects import TrackingNumber
from src.infrastructure.persistence.colis_mapper import (
    historique_to_model,
    to_entity,
    to_model,
)
from src.infrastructure.persistence.colis_model import ColisModel
from src.infrastructure.persistence.historique_model import HistoriqueStatutModel


class SQLAlchemyColisRepository(IColisRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, colis: Colis) -> Colis:
        existing = self._session.get(ColisModel, colis.id)
        if existing is not None:
            model = to_model(colis)
            for key, value in model.__dict__.items():
                if not key.startswith("_"):
                    setattr(existing, key, value)
        else:
            self._session.add(to_model(colis))

        # Ajouter les nouvelles entrees d'historique
        existing_ids = {
            h.id
            for h in self._session.query(HistoriqueStatutModel)
            .filter_by(colis_id=colis.id)
            .all()
        }
        for h in colis.historique:
            if h.id not in existing_ids:
                self._session.add(historique_to_model(h))

        self._session.flush()
        return colis

    def get_by_id(self, colis_id: UUID) -> Optional[Colis]:
        model = self._session.get(ColisModel, colis_id)
        if model is None:
            return None
        historique_models = (
            self._session.query(HistoriqueStatutModel)
            .filter_by(colis_id=colis_id)
            .order_by(HistoriqueStatutModel.date_transition)
            .all()
        )
        return to_entity(model, historique_models)

    def get_by_tracking_number(
        self, tracking_number: TrackingNumber
    ) -> Optional[Colis]:
        model = (
            self._session.query(ColisModel)
            .filter_by(tracking_number=tracking_number.valeur)
            .first()
        )
        if model is None:
            return None
        historique_models = (
            self._session.query(HistoriqueStatutModel)
            .filter_by(colis_id=model.id)
            .order_by(HistoriqueStatutModel.date_transition)
            .all()
        )
        return to_entity(model, historique_models)

    def find_all(self) -> list[Colis]:
        models = self._session.query(ColisModel).all()
        return [to_entity(m) for m in models]

    def delete(self, colis_id: UUID) -> bool:
        model = self._session.get(ColisModel, colis_id)
        if model is None:
            return False
        self._session.delete(model)
        self._session.flush()
        return True
