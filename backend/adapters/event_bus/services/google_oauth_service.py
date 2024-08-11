# adapter/servies/google_oauth_service.py
from application.interfaces.oauth_service import OAuthService


class GoogleOAuthService(OAuthService):
    def get_authorization_url(self) -> str:
        return "https://accounts.google.com/o/oauth2/auth..."

    def exchange_code_for_tokens(self, code: str) -> dict:
        # Google OAuth token exchange implementation
        return {"access_token": "google_token", "refresh_token": "google_refresh_token"}
