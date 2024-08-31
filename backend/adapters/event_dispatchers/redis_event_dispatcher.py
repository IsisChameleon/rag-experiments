import asyncio
import json
import random
from typing import Any, Callable, Dict

import redis.asyncio as redis
from framework.event_dispatcher import EventDispatcher
from framework.event_handler import EventHandler
from framework.events.event import Event

# class EventDispatcherConfig():
#     def __init__(self, retry_attempts: int = 3):

#         self.handlers: Dict[str, EventHandler] = {}
#         self.retry_attempts = retry_attempts

#     @staticmethod
#     def from_toml(self, toml_string: str):
#         config = toml.loads(toml_string)
#         retry_attempts = config.get("retry_attempts", 3)
#         return EventDispatcherConfig(retry_attempts)

# class RedisEventDispatcherConfig(EventDispatcherConfig):
#     def __init__(self, redis_url: str, retry_attempts: int = 3):
#         super().__init__(retry_attempts)
#         self.redis_url = redis_url


class RedisEventDispatcher(EventDispatcher):
    def __init__(self, redis_kwargs: str, retry_attempts: int = 3, base_delay: float = 0.1, max_delay: float = 10.0):
        self.redis = redis.Redis(**redis_kwargs)
        self.handlers: Dict[str, EventHandler] = {}
        self.retry_attempts = retry_attempts
        self.base_delay = base_delay
        
        self.max_delay = max_delay

    def register_handler(self, event_name: str, handler: Callable[[Event], Any]) -> None:
        self.handlers[event_name] = handler


    async def _dispatch(self, event: Event) -> None:
        handler = self.handlers.get(event.get_name())
        if not handler:
            return  # No handler for this event

        for attempt in range(self.retry_attempts):
            try:
                await handler(event)
                return  # Event processed successfully
            except Exception:
                if attempt == self.retry_attempts - 1:
                    await self._store_in_error_queue(event)
                    return
                delay = min(self.base_delay * (2 ** attempt) + random.uniform(0, 0.1 * (2 ** attempt)), self.max_delay)
                await asyncio.sleep(delay)

    async def _store_in_error_queue(self, event: 'Event') -> None:
        await self.redis.rpush('error_queue', self.serialize_event(event))

    async def listen_to_events(self, channel_name: str) -> None:
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel_name)

        async for message in pubsub.listen():
            if message['type'] == 'message':
                event_data = message['data']
                event = self.deserialize_event(event_data)
                await self._dispatch(event)

    def serialize_event(self, event: Event) -> str:
        # Serialize the event to a JSON string
        event_data = {
            "name": event.get_name(),
            "payload": event.payload
        }
        return json.dumps(event_data)

    def deserialize_event(self, event_data: str) -> Event:
        # Deserialize the event data from a JSON string
        event_dict = json.loads(event_data)
        event_name = event_dict["name"]
        payload = event_dict["payload"]

        event_class = self.get_event_class(event_name)
        return event_class(**payload)

    def get_event_class(self, event_name: str):
        # This method returns the Event class based on the event name
        if event_name == "UserOAuthCompleted":
            from application.events.user_oauth_completed import UserOAuthCompleted
            return UserOAuthCompleted
        elif event_name == "UserDocumentAccessed":
            from application.events.user_document_accessed import UserDocumentAccessed
            return UserDocumentAccessed

        raise NotImplementedError(f"Event class for {event_name} not found")
