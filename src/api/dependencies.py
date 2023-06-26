from collections.abc import Generator

from sqlalchemy.orm import Session

from src.core.session import SessionLocal


def session_factory() -> Generator[Session, None, None]:
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
