import asyncio

from adapters.event_dispatchers.redis_event_dispatcher import RedisEventDispatcher
from application.handlers.user_access_document_events_handler import (
    UserAccessDocumentEventsHandler,
)
from redis.asyncio import Redis


async def main():
    redis_client = Redis.from_url("redis://localhost:6378")

    dispatcher = RedisEventDispatcher({"host": "localhost", "port": 6378})

    handler = UserAccessDocumentEventsHandler(redis_client)
    dispatcher.register_handler("UserDocumentAccessed", handler.handle)

    channel_name = "document_access_events"
    
    print(f"Starting to listen on channel: {channel_name}")
    await dispatcher.listen_to_events(channel_name)

if __name__ == "__main__":
    asyncio.run(main())

