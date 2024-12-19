from collections.abc import Generator, Sequence
from http import HTTPStatus
from typing import Any

from fastapi import HTTPException
from sqlalchemy import (
    Connection,
    CursorResult,
    Executable,
    Insert,
    MetaData,
    RowMapping,
    Select,
    Update,
    create_engine,
)
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.constants import DB_NAMING_CONVENTION

DATABASE_URL = str((settings := get_settings()).DATABASE_URL)

engine = create_engine(
    DATABASE_URL,
    echo=settings.ENVIRONMENT.is_debug,
    pool_size=10,
    pool_pre_ping=True,
    echo_pool=settings.ENVIRONMENT.is_debug,
)

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


def get_connection() -> Generator[Connection, None]:
    try:
        with engine.begin() as conn:
            yield conn
    except (SQLAlchemyError, OSError) as exc:
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc)) from exc


def fetch_one(
    conn: Connection, select_query: Select | Insert | Update
) -> RowMapping | None:
    cursor: CursorResult = conn.execute(select_query)
    return cursor.mappings().one_or_none()


def fetch_all(
    conn: Connection, select_query: Select | Insert | Update
) -> Sequence[RowMapping]:
    cursor: CursorResult = conn.execute(select_query)
    return cursor.mappings().all()


def execute(conn: Connection, select_query: Executable) -> CursorResult[Any]:
    return conn.execute(select_query)
