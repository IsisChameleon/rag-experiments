from abc import ABC, abstractmethod

from framework.events.event import Event


class EventHandler(ABC):
    @abstractmethod
    async def handle(self, event: Event) -> None:
        pass
