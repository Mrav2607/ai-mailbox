from .celery_app import celery_app

@celery_app.task
def classify_message(message_id: int) -> dict:
    return {"message_id": message_id, "label": "other", "score": 0.0}
