
from framework.events.event import Event


class UserDocumentAccessed(Event):
    def __init__(self, user_id: str, datasource: str, document_id: str):
        
        super().__init__({
            "user_id": user_id,
            "datasource": datasource,
            "document_id": document_id
        })
