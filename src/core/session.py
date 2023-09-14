"""Sqlalchemy related module."""
from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.model.sql_alchemy import mapper_registry, vehicle_table
from src.model.vehicle import Vehicle


class Session(Protocol):

    def __enter__(self) -> Session:
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

    def execute(self, statement: str, *arg, **kwargs) -> None:
        ...

    def get(self, *args, **kwargs) -> None:
        ...

    def close(self, *args, **kwargs) -> None:
        ...

    def commit(self, *args, **kwargs) -> None:
        ...

    def refresh(self, *args, **kwargs) -> None:
        ...

    def add(self, *args, **kwargs) -> None:
        ...


class AbstractSessionMaker(Protocol):

    def __call__(self) -> Session:
        ...


class SQLAlchemySessionMaker(AbstractSessionMaker):

    def __init__(self,
                 url: str | None = None,
                 autocommit: bool = False,
                 autoflush: bool = False,
                 echo: bool = settings.ECHO,
                 callback: Callable | None = None) -> None:
        self.autocommit = autocommit
        self.autoflush = autoflush
        self.echo = echo
        self.callback = callback or create_engine
        self.engine = self.callback(
            url or fetch_db_uri(),
            pool_pre_ping=True,
            echo=self.echo,
        )
        mapper_registry.map_imperatively(Vehicle, vehicle_table)

    def __call__(self, client: Callable | None = None) -> Session:
        session = client or sessionmaker(autocommit=self.autocommit,
                                         autoflush=self.autoflush,
                                         bind=self.engine)
        return session()


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
    return settings.DATABASE_URI


SessionLocal = SQLAlchemySessionMaker()
