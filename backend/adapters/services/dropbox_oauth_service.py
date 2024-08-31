from application.interfaces.oauth_service import OAuthService


class DropboxOAuthService(OAuthService):
    def get_authorization_url(self) -> str:
        return "https://www.dropbox.com/oauth2/authorize..."

    def exchange_code_for_tokens(self, code: str) -> dict:
        # Dropbox OAuth token exchange implementation
        return {"access_token": "dropbox_token", "refresh_token": "dropbox_refresh_token"}
