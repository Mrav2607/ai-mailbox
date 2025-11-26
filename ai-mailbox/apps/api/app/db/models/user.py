from __future__ import annotations

import uuid

from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class AppUser(Base):
    """
    End users of the mailbox app. Matches alembic table app_user.
    """

    __tablename__ = "app_user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default="gen_random_uuid()",
    )
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False, index=True)
    display_name: Mapped[str | None] = mapped_column(Text, nullable=True)
