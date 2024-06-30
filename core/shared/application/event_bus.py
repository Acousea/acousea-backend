from abc import ABC, abstractmethod

from core.shared.application.event_handler import EventHandler
from core.shared.domain.events import DomainEvent


class EventBus(ABC):
    @abstractmethod
    def subscribe(self, handler: EventHandler):
        pass

    @abstractmethod
    def notify(self, event: DomainEvent):
        pass

    @abstractmethod
    def notify_all(self, events: list[DomainEvent]):
        pass
