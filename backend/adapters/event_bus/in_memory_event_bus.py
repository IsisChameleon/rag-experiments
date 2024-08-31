from application.interfaces.event_bus import EventBus
from framework.events.event import Event


class InMemoryEventBus(EventBus):
    def __init__(self):
        self.subscribers = {}

    def publish(self, event: Event) -> None:
        event_name = event.get_name()
        if event_name in self.subscribers:
            for handler in self.subscribers[event_name]:
                handler(event)

    def subscribe(self, event_name: str, handler) -> None:
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(handler)