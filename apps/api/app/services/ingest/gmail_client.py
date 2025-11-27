class GmailClient:
    def __init__(self, token: str | None = None):
        self.token = token

    def list_messages(self, user_id: str) -> list[dict]:
        # Placeholder
        return []
