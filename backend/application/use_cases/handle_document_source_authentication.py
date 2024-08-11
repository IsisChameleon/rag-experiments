from typing import List

from application.events.user_oauth_completed import UserOAuthCompleted
from application.interfaces.document_service import DocumentService
from application.interfaces.event_bus import EventBus
from application.interfaces.oauth_service import OAuthService
from domain.models.User import User


class HandleDocumentSourceAuthentication:
    def __init__(self, oauth_service: OAuthService, document_retrieval_service: DocumentService, event_bus: EventBus):
        self.oauth_service = oauth_service
        self.document_retrieval_service = document_retrieval_service
        self.event_bus = event_bus

    def handle_callback(self, code: str, user: User) -> List[str]:
        tokens = self.oauth_service.exchange_code_for_tokens(code)
        user.access_token = tokens['access_token']
        user.refresh_token = tokens.get('refresh_token')

        event = UserOAuthCompleted(user.user_id, self.oauth_service.__class__.__name__)
        self.event_bus.publish(event)
