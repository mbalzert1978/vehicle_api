from collections.abc import Generator

from sqlalchemy.orm import Session

from src.core.session import SessionLocal


def get_session() -> Generator[Session, None, None]:
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
