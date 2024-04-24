"""Sqlalchemy related module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends  # noqa: TCH002
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.config import get_app_settings
from src.model.base import Base
from src.model.sql_alchemy import map_tables

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from src.crud.base import BaseRepository


settings = get_app_settings()
map_tables()


def get_session() -> Iterator[Session]:
    """
    Yield an SQLAlchemy Session object.

    Use the yielded session within a context manager for proper cleanup.

    Yields
    ------
    An SQLAlchemy Session object.
    """
    Session = sessionmaker(  # noqa: N806
        autocommit=False,
        autoflush=False,
        bind=create_engine(str(settings.database_url), pool_pre_ping=True, echo=settings.debug),
    )
    try:
        session = Session()
        yield session
    finally:
        session.close()


def get_repository(
    repo_type: type[BaseRepository],
    model_type: type[Base] | None = None,
) -> Callable[[Session], BaseRepository]:
    if model_type is None:
        model_type = Base

    def _setup_repo(
        session: Annotated[Session, Depends(get_session)],
    ) -> BaseRepository:
        return repo_type(session, model_type)

    return _setup_repo
