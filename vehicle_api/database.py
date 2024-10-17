from http import HTTPStatus
from typing import Any, AsyncGenerator, Sequence

from fastapi import HTTPException
from sqlalchemy import (
    CursorResult,
    Executable,
    Insert,
    MetaData,
    RowMapping,
    Select,
    Update,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from vehicle_api.config import get_settings
from vehicle_api.constants import DB_NAMING_CONVENTION

DATABASE_URL = str((settings := get_settings()).DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.ENVIRONMENT.is_debug,
    pool_size=10,
    pool_pre_ping=True,
    echo_pool=settings.ENVIRONMENT.is_debug,
)

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


async def get_connection() -> AsyncGenerator[AsyncConnection, None]:
    try:
        async with engine.begin() as conn:
            yield conn
    except (SQLAlchemyError, OSError) as exc:
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(exc)) from exc


async def fetch_one(conn: AsyncConnection, select_query: Select | Insert | Update) -> RowMapping | None:
    cursor: CursorResult = await conn.execute(select_query)
    return cursor.mappings().one_or_none()


async def fetch_all(conn: AsyncConnection, select_query: Select | Insert | Update) -> Sequence[RowMapping]:
    cursor: CursorResult = await conn.execute(select_query)
    return cursor.mappings().all()


async def execute(conn: AsyncConnection, select_query: Executable) -> CursorResult[Any]:
    return await conn.execute(select_query)
