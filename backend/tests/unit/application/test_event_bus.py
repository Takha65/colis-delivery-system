"""Tests unitaires de l'EventBus (Observer pattern)."""

from uuid import uuid4

from src.application.services.event_bus import EventBus
from src.domain.events import ColisCreeEvent, ColisLivreEvent


class TestEventBus:

    def test_subscribe_et_publish(self) -> None:
        bus = EventBus()
        recus: list = []

        def handler(event: ColisCreeEvent) -> None:
            recus.append(event)

        bus.subscribe(ColisCreeEvent, handler)
        event = ColisCreeEvent(
            colis_id=uuid4(), tracking_number="CLS-12345678", type_colis="STANDARD"
        )
        bus.publish(event)

        assert len(recus) == 1
        assert recus[0] == event

    def test_plusieurs_handlers_meme_event(self) -> None:
        bus = EventBus()
        compteur = {"a": 0, "b": 0}

        bus.subscribe(ColisCreeEvent, lambda e: compteur.update({"a": compteur["a"] + 1}))
        bus.subscribe(ColisCreeEvent, lambda e: compteur.update({"b": compteur["b"] + 1}))

        bus.publish(
            ColisCreeEvent(colis_id=uuid4(), tracking_number="CLS-12345678", type_colis="STANDARD")
        )

        assert compteur == {"a": 1, "b": 1}

    def test_handler_ne_recoit_que_son_type(self) -> None:
        bus = EventBus()
        recus_cree: list = []
        recus_livre: list = []

        bus.subscribe(ColisCreeEvent, lambda e: recus_cree.append(e))
        bus.subscribe(ColisLivreEvent, lambda e: recus_livre.append(e))

        bus.publish(
            ColisCreeEvent(colis_id=uuid4(), tracking_number="CLS-12345678", type_colis="STANDARD")
        )

        assert len(recus_cree) == 1
        assert len(recus_livre) == 0

    def test_exception_handler_bloque_pas_autres(self) -> None:
        bus = EventBus()
        recus: list = []

        def handler_qui_plante(event):
            raise RuntimeError("boom")

        def handler_normal(event):
            recus.append(event)

        bus.subscribe(ColisCreeEvent, handler_qui_plante)
        bus.subscribe(ColisCreeEvent, handler_normal)

        # publish ne doit pas lever d'exception
        bus.publish(
            ColisCreeEvent(colis_id=uuid4(), tracking_number="CLS-12345678", type_colis="STANDARD")
        )

        # Le handler normal a quand meme ete appele
        assert len(recus) == 1

    def test_clear_vide_les_handlers(self) -> None:
        bus = EventBus()
        recus: list = []
        bus.subscribe(ColisCreeEvent, lambda e: recus.append(e))
        bus.clear()

        bus.publish(
            ColisCreeEvent(colis_id=uuid4(), tracking_number="CLS-12345678", type_colis="STANDARD")
        )

        assert recus == []
