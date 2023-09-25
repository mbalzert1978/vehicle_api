"""Sqlalchemy related module."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, ParamSpec, Protocol, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.model.sql_alchemy import Table, mapper_registry, vehicle_table
from src.model.vehicle import Base, Vehicle

if TYPE_CHECKING:
    from collections.abc import Generator

ModelType = TypeVar("ModelType", bound=Base)
TableType = TypeVar("TableType", bound=Table)

P = ParamSpec("P")
R = TypeVar("R")


class AbstractSession(Protocol[P, R]):

    """Abstract session interface."""

    def __enter__(self) -> AbstractSession:
        """Context manager."""

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit method."""

    def execute(self, statement: str, *args: P.args, **kwargs: P.kwargs) -> R:
        """Session execute method."""

    def get(self, *args: P.args, **kwargs: P.kwargs) -> R | None:
        """Session get method."""

    def close(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Session close method."""

    def commit(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Session commit method."""

    def refresh(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Session refresh method."""

    def add(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Session add method."""

    def delete(self, *args: P.args, **kwargs: P.kwargs) -> None:
        """Session delete method."""


class AbstractSessionMaker(Protocol[ModelType, TableType]):

    """Abstract session maker interface."""

    def __call__(self) -> Generator[AbstractSession, Any, None]:
        """Session factory method."""


class SQLAlchemySessionMaker(Generic[ModelType, TableType]):

    """SQLAlchemy session maker."""

    def __init__(
        self,
        url: str,
        *,
        obj: ModelType,
        map_on: TableType,
        autocommit: bool = False,
        autoflush: bool = False,
        echo: bool = settings.ECHO,
    ) -> None:
        self.autocommit = autocommit
        self.autoflush = autoflush
        self.echo = echo
        self.engine = create_engine(url, pool_pre_ping=True, echo=self.echo)
        mapper_registry.map_imperatively(obj, map_on)

    def __call__(self) -> Generator[AbstractSession, Any, None]:
        """
        Yield an SQLAlchemy Session object.

        Use the yielded session within a context manager for proper cleanup.

        Yields
        ------
        An SQLAlchemy Session object.
        """
        Session = sessionmaker(autocommit=self.autocommit, autoflush=self.autoflush, bind=self.engine)  # noqa: N806
        try:
            session = Session()
            yield session
        finally:
            session.close()


def fetch_db_uri() -> str:
    """
    Fetch the database URI from the settings.

    Returns
    -------
    The database URI as a string.

    Raises
    ------
    ValueError: If the DATABASE_URI is not set in the .env file.

    """
    if not settings.DATABASE_URI:
        msg = "DATABASE_URI is not set in .env file."
        raise ValueError(msg)
    if not isinstance(settings.DATABASE_URI, str):
        return str(settings.DATABASE_URI)
    return settings.DATABASE_URI


SESSION_LOCAL: AbstractSessionMaker = SQLAlchemySessionMaker(fetch_db_uri(), obj=Vehicle, map_on=vehicle_table)
