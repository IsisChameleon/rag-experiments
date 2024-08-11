# application/interfaces/oauth_service.py
from abc import ABC, abstractmethod


class OAuthService(ABC):
    @abstractmethod
    def get_authorization_url(self, provider: str) -> str: pass

    @abstractmethod
    def exchange_code_for_tokens(self, provider: str, code: str) -> dict: pass
