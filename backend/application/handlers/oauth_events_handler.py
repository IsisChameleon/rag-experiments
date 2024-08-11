from application.events.user_oauth_completed import UserOAuthCompleted


def log_oauth_event(event: UserOAuthCompleted):
    print(str(event))