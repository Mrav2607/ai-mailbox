from __future__ import annotations

import uuid

from sqlalchemy import Text, Numeric, TIMESTAMP, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Classification(Base):
    """
    LLM or heuristic classification results per message.
    """

    __tablename__ = "classification"
    __table_args__ = (Index("classification_message_idx", "message_id"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default="gen_random_uuid()",
    )
    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("mail_message.id", ondelete="CASCADE")
    )
    label: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[Numeric | None] = mapped_column(Numeric)
    rationale: Mapped[str | None] = mapped_column(Text)
    model_version: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default="now()"
    )
