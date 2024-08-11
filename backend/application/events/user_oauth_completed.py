from application.events.event import Event


class UserOAuthCompleted(Event):
    def __init__(self, user_id: str, provider: str):
        self.user_id = user_id
        self.provider = provider

    def __str__(self) -> str:
        return "UserOAuthCompleted for " + self.user_id + " with provider " + self.provider
    
    def get_name(self) -> str:
        return "UserOAuthCompleted"