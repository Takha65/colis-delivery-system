"""Event Bus : implementation du pattern Observer.

Les publishers publient des evenements, les handlers s'abonnent a des
types specifiques. Aucun couplage direct entre eux.
"""

import logging
from collections import defaultdict
from typing import Callable, Type

from src.domain.events import DomainEvent

logger = logging.getLogger(__name__)

EventHandler = Callable[[DomainEvent], None]


class EventBus:
    """Bus d'evenements in-memory (Observer pattern).

    Thread-safe pour un serveur uvicorn en mode async.
    """

    def __init__(self) -> None:
        self._handlers: dict[Type[DomainEvent], list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        """Abonne un handler a un type d'evenement."""
        self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> None:
        """Publie un evenement : tous les handlers inscrits sont appeles.

        Les erreurs de handlers ne doivent pas bloquer les autres handlers
        ni remonter au publisher.
        """
        event_type = type(event)
        for handler in self._handlers.get(event_type, []):
            try:
                handler(event)
            except Exception as exc:  # pylint: disable=broad-except
                logger.error(
                    "Erreur dans le handler %s pour %s : %s",
                    handler.__name__,
                    event_type.__name__,
                    exc,
                )

    def clear(self) -> None:
        """Vide tous les handlers (utile en tests)."""
        self._handlers.clear()
