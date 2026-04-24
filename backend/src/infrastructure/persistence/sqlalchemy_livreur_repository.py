"""Implementation SQLAlchemy du LivreurRepository.

Note : les operations ne committent PAS. Le commit est la responsabilite
de l'appelant (Unit of Work ou dependency FastAPI via get_db).
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.application.ports import ILivreurRepository
from src.domain.entities import Livreur
from src.infrastructure.persistence.livreur_model import LivreurModel


class SQLAlchemyLivreurRepository(ILivreurRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, livreur: Livreur) -> Livreur:
        existing = self._session.get(LivreurModel, livreur.id)
        if existing is not None:
            existing.nom = livreur.nom
            existing.capacite_max_kg = livreur.capacite_max_kg
            existing.position_depart_id = livreur.position_depart_id
        else:
            model = LivreurModel(
                id=livreur.id,
                nom=livreur.nom,
                capacite_max_kg=livreur.capacite_max_kg,
                position_depart_id=livreur.position_depart_id,
            )
            self._session.add(model)
        self._session.flush()  # force l'INSERT sans committer
        return livreur

    def get_by_id(self, livreur_id: UUID) -> Optional[Livreur]:
        model = self._session.get(LivreurModel, livreur_id)
        if model is None:
            return None
        return Livreur(
            id=model.id,
            nom=model.nom,
            capacite_max_kg=model.capacite_max_kg,
            position_depart_id=model.position_depart_id,
        )

    def find_all(self) -> list[Livreur]:
        models = self._session.query(LivreurModel).all()
        return [
            Livreur(
                id=m.id,
                nom=m.nom,
                capacite_max_kg=m.capacite_max_kg,
                position_depart_id=m.position_depart_id,
            )
            for m in models
        ]
