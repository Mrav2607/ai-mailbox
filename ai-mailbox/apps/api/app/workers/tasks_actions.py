from .celery_app import celery_app

@celery_app.task
def create_unsubscribe_draft(thread_id: int) -> str:
    return f"Drafted unsubscribe for thread {thread_id} (placeholder)"
