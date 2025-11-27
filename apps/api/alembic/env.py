import os
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Ensure app package is importable when running alembic from the apps/api directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from app.db.base import Base  # noqa: E402
# Import models so metadata is populated for autogenerate
import app.db.models  # noqa: F401,E402

config = context.config
section = config.get_section(config.config_ini_section) or {}
section["sqlalchemy.url"] = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/ai_mailbox"
)

# Use ORM metadata for autogenerate (kept in sync with alembic revision 0001)
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    context.configure(url=section["sqlalchemy.url"], literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(section, prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
