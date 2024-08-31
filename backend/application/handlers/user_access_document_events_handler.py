
import redis
from application.events.user_document_accessed import UserDocumentAccessed
from framework.event_handler import EventHandler


class UserAccessDocumentEventsHandler(EventHandler):
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    async def handle(self, event: UserDocumentAccessed) -> None:
        user_id = event.payload["user_id"]
        document_id = event.payload["document_id"]
        datasource  = event.payload["datasource"]
        
        key = f"DocumentAccess:datasource:{datasource}:document:{document_id}:user:{user_id}:access_count"
    
        # Increment the access count for the user-document pair
        print(f"Incrementing access count for redis key: {key}")
        await self.redis_client.incr(key)
