from typing import AsyncGenerator, Sequence

from sqlalchemy import CursorResult, Delete, Insert, RowMapping, Select, Update
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine

from src.config import get_settings

DATABASE_URL = str((settings := get_settings()).DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.ENVIRONMENT.is_debug,
    pool_size=10,
    pool_pre_ping=True,
    echo_pool=settings.ENVIRONMENT.is_debug,
)


async def get_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with engine.begin() as conn:
        yield conn
        await conn.close()


async def fetch_one(conn: AsyncConnection, select_query: Select | Insert | Update) -> RowMapping | None:
    cursor: CursorResult = await conn.execute(select_query)
    return cursor.mappings().one_or_none()


async def fetch_all(conn: AsyncConnection, select_query: Select | Insert | Update) -> Sequence[RowMapping]:
    cursor: CursorResult = await conn.execute(select_query)
    return cursor.mappings().all()


async def execute(conn: AsyncConnection, select_query: Insert | Update | Delete) -> None:
    await conn.execute(select_query)
