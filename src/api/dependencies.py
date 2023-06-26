"""Dependencies module."""
from collections.abc import Generator

from sqlalchemy.orm import Session

from src.core.session import SessionLocal


def session_factory() -> Generator[Session, None, None]:
    """
    Yield an SQLAlchemy Session object.

    Yields
    ------
    An SQLAlchemy Session object.

    Raises
    ------
    None

    Returns
    -------
    None

    Notes
    -----
    Use the yielded session within a context manager for proper cleanup.

    """
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
