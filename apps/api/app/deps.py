from collections.abc import Generator

from .db.base import SessionLocal


def get_db() -> Generator:
    """
    FastAPI dependency that provides a SQLAlchemy session per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
