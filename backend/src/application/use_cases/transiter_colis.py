"""Use case : faire transiter un colis vers un nouvel etat."""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.application.ports import IColisRepository
from src.application.services.event_bus import EventBus
from src.domain.entities import Colis
from src.domain.events import ColisLivreEvent, ColisTransiteEvent
from src.domain.exceptions import ColisNotFoundError


@dataclass
class TransiterColisCommand:
    colis_id: UUID
    nouvel_etat: str
    commentaire: str = ""


class TransiterColisUseCase:
    """Fait transiter un colis et publie les events correspondants."""

    def __init__(
        self,
        repository: IColisRepository,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self._repository = repository
        self._event_bus = event_bus

    def execute(self, command: TransiterColisCommand) -> Colis:
        colis = self._repository.get_by_id(command.colis_id)
        if colis is None:
            raise ColisNotFoundError(str(command.colis_id))

        statut_precedent = colis.statut
        colis.transiter_vers(command.nouvel_etat, command.commentaire)
        colis_sauve = self._repository.save(colis)

        if self._event_bus is not None:
            self._event_bus.publish(
                ColisTransiteEvent(
                    colis_id=colis_sauve.id,
                    tracking_number=colis_sauve.tracking_number.valeur,
                    statut_precedent=statut_precedent,
                    statut_nouveau=colis_sauve.statut,
                )
            )
            if colis_sauve.statut == "LIVRE":
                self._event_bus.publish(
                    ColisLivreEvent(
                        colis_id=colis_sauve.id,
                        tracking_number=colis_sauve.tracking_number.valeur,
                    )
                )

        return colis_sauve
