from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.deps import get_db
from app.db.models import MailThread, MailMessage, Classification

router = APIRouter(prefix="/mail")


@router.get("/triage")
def get_triage(
    user_id: UUID,
    bucket: str = "needs_reply",
    limit: int = 50,
    db: Session = Depends(get_db),
) -> dict:
    """
    Fetch recent threads for a user with latest classification label.
    """
    threads = (
        db.execute(
            select(MailThread)
            .where(MailThread.user_id == user_id)
            .order_by(desc(MailThread.last_message_at.nullslast()), desc(MailThread.created_at))
            .limit(limit)
        )
        .scalars()
        .all()
    )

    thread_ids = [t.id for t in threads]
    messages = (
        db.execute(
            select(MailMessage)
            .where(MailMessage.thread_id.in_(thread_ids))
            .order_by(desc(MailMessage.sent_at.nullslast()), desc(MailMessage.created_at))
        )
        .scalars()
        .all()
        if thread_ids
        else []
    )
    latest_classifications = (
        db.execute(
            select(Classification)
            .where(Classification.message_id.in_([m.id for m in messages]))
            .order_by(desc(Classification.created_at))
        )
        .scalars()
        .all()
        if messages
        else []
    )
    classifications_by_msg = {}
    for cls in latest_classifications:
        if cls.message_id not in classifications_by_msg:
            classifications_by_msg[cls.message_id] = cls

    messages_by_thread: dict[UUID, list[MailMessage]] = {}
    for message in messages:
        messages_by_thread.setdefault(message.thread_id, []).append(message)

    items = []
    for thread in threads:
        msg_list = messages_by_thread.get(thread.id, [])
        latest_message = msg_list[0] if msg_list else None
        classification = classifications_by_msg.get(latest_message.id) if latest_message else None
        items.append(
            {
                "thread_id": str(thread.id),
                "subject": thread.subject,
                "last_message_at": thread.last_message_at,
                "latest_message_snippet": latest_message.snippet if latest_message else None,
                "classification": {
                    "label": classification.label if classification else None,
                    "confidence": float(classification.confidence) if classification and classification.confidence is not None else None,
                },
            }
        )
    return {"bucket": bucket, "items": items}


@router.get("/thread/{thread_id}")
def get_thread(thread_id: UUID, db: Session = Depends(get_db)) -> dict:
    thread = db.get(MailThread, thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    messages = (
        db.execute(
            select(MailMessage)
            .where(MailMessage.thread_id == thread_id)
            .order_by(desc(MailMessage.sent_at.nullslast()), desc(MailMessage.created_at))
        )
        .scalars()
        .all()
    )
    return {
        "thread": {
            "id": str(thread.id),
            "subject": thread.subject,
            "provider": thread.provider,
            "last_message_at": thread.last_message_at,
        },
        "messages": [
            {
                "id": str(m.id),
                "sent_at": m.sent_at,
                "sender": m.sender,
                "snippet": m.snippet,
                "body_text": m.body_text,
            }
            for m in messages
        ],
    }
