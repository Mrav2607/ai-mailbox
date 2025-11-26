from .celery_app import celery_app

@celery_app.task
def ingest_gmail_messages(user_id: int) -> str:
    return f"Ingested messages for user {user_id} (placeholder)"
