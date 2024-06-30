from core.shared.application.event_bus import EventBus
from core.shared.application.event_handler import EventHandler
from core.shared.domain.events import DomainEvent


class InMemoryEventBus(EventBus):
    handlers: dict[str, list[EventHandler]]
    events: list[DomainEvent]

    def __init__(self):
        self.handlers = {}
        self.events = []

    def subscribe(self, handler: EventHandler):
        self.handlers.setdefault(handler.event_name, []).append(handler)

    async def notify(self, event: DomainEvent):
        for handler in self.handlers.get(event.name, []):
            await handler.handle(event.payload)
        # FIXME: borra el evento de la lista pero lo añade a un archivo llamado events.txt, EventSourcing

    async def notify_all(self, events: list[DomainEvent]):
        for event in events:
            await self.notify(event)
            self.events.append(event)
