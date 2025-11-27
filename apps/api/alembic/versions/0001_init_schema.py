from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_init_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
    # Attempt to enable pgvector if installed; skip gracefully if not available
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'vector') THEN
                CREATE EXTENSION IF NOT EXISTS vector;
            ELSE
                RAISE NOTICE 'pgvector extension not installed on this server; skipping';
            END IF;
        END
        $$;
        """
    )
    op.create_table(
        "app_user",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.Text(), nullable=False, unique=True),
        sa.Column("display_name", sa.Text()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "provider_account",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("app_user.id", ondelete="CASCADE")),
        sa.Column("provider", sa.Text(), nullable=False),
        sa.Column("external_user_id", sa.Text(), nullable=False),
        sa.Column("access_token", sa.Text(), nullable=False),
        sa.Column("refresh_token", sa.Text()),
        sa.Column("token_expiry", sa.TIMESTAMP(timezone=True)),
        sa.Column("scope", sa.Text()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.CheckConstraint("provider IN ('gmail','outlook')", name="provider_check"),
    )

    op.create_table(
        "mail_thread",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("app_user.id", ondelete="CASCADE")),
        sa.Column("provider", sa.Text(), nullable=False),
        sa.Column("provider_thread_id", sa.Text(), nullable=False),
        sa.Column("subject", sa.Text()),
        sa.Column("last_message_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id", "provider", "provider_thread_id", name="uq_thread_provider"),
    )

    op.create_table(
        "mail_message",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("thread_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("mail_thread.id", ondelete="CASCADE")),
        sa.Column("provider_message_id", sa.Text(), nullable=False),
        sa.Column("sender", sa.Text()),
        sa.Column("recipient", sa.ARRAY(sa.Text())),
        sa.Column("cc", sa.ARRAY(sa.Text())),
        sa.Column("bcc", sa.ARRAY(sa.Text())),
        sa.Column("sent_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("snippet", sa.Text()),
        sa.Column("body_text", sa.Text()),
        sa.Column("body_html", sa.Text()),
        sa.Column("headers", postgresql.JSONB()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("thread_id", "provider_message_id", name="uq_msg_provider"),
    )

    op.create_table(
        "classification",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("message_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("mail_message.id", ondelete="CASCADE")),
        sa.Column("label", sa.Text()),
        sa.Column("confidence", sa.Numeric()),
        sa.Column("rationale", sa.Text()),
        sa.Column("model_version", sa.Text()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("classification_message_idx", "classification", ["message_id"]) 

    op.create_table(
        "receipt",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("message_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("mail_message.id", ondelete="CASCADE")),
        sa.Column("merchant", sa.Text()),
        sa.Column("currency", sa.Text()),
        sa.Column("subtotal", sa.Numeric()),
        sa.Column("tax", sa.Numeric()),
        sa.Column("total", sa.Numeric()),
        sa.Column("purchased_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("line_items", postgresql.JSONB()),
        sa.Column("source_confidence", sa.Numeric()),
    )

    op.create_table(
        "calendar_event",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("message_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("mail_message.id", ondelete="CASCADE")),
        sa.Column("title", sa.Text()),
        sa.Column("starts_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("ends_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("location", sa.Text()),
        sa.Column("organizer", sa.Text()),
        sa.Column("rsvp_link", sa.Text()),
    )

    op.create_table(
        "action_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("app_user.id", ondelete="CASCADE")),
        sa.Column("message_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("mail_message.id", ondelete="CASCADE")),
        sa.Column("action", sa.Text()),
        sa.Column("payload", postgresql.JSONB()),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "message_embedding",
        sa.Column("message_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("mail_message.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("embedding", postgresql.ARRAY(sa.Float())),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()")),
    )


def downgrade() -> None:
    op.drop_table("message_embedding")
    op.drop_table("action_log")
    op.drop_table("calendar_event")
    op.drop_table("receipt")
    op.drop_index("classification_message_idx", table_name="classification")
    op.drop_table("classification")
    op.drop_table("mail_message")
    op.drop_table("mail_thread")
    op.drop_table("provider_account")
    op.drop_table("app_user")
