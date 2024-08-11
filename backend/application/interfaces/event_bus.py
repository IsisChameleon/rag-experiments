from abc import ABC, abstractmethod

from application.events.event import Event


class EventBus(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None:
        pass

    @abstractmethod
    def subscribe(self, event_name: str, handler) -> None:
        pass
