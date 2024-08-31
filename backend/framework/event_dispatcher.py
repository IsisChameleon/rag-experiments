from abc import ABC, abstractmethod
from typing import List

from framework.events.event import Event


class EventDispatcher(ABC):

    @abstractmethod
    async def _dispatch(self, event: Event) -> None:
        """Dispatch the event to the appropriate handler."""
        pass

    @abstractmethod
    async def listen_to_events(self, channel_names: List[str]) -> None:
        """Subscribe to a channel and listen for incoming events."""
        pass
