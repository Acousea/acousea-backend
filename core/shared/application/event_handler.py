from abc import ABC, abstractmethod
from typing import ClassVar, Generic, TypeVar

EventPayload = TypeVar("EventPayload")


class EventHandler(ABC, Generic[EventPayload]):
    event_name: ClassVar[str] = ""

    @abstractmethod
    def handle(self, payload: EventPayload):
        pass
