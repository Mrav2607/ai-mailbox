from __future__ import annotations

import uuid

from sqlalchemy import CheckConstraint, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class ProviderAccount(Base):
    """
    Connected provider account (e.g., Gmail, Outlook) with OAuth tokens.
    """

    __tablename__ = "provider_account"
    __table_args__ = (
        CheckConstraint("provider IN ('gmail','outlook')", name="provider_check"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default="gen_random_uuid()",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("app_user.id", ondelete="CASCADE")
    )
    provider: Mapped[str] = mapped_column(Text, nullable=False)
    external_user_id: Mapped[str] = mapped_column(Text, nullable=False)
    access_token: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    token_expiry: Mapped[TIMESTAMP | None] = mapped_column(TIMESTAMP(timezone=True))
    scope: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True), server_default="now()"
    )
