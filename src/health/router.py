"""FastAPI service module."""

from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection

from src.database import get_connection
from src.health.constants import Tag
from src.health.schemas import DatabaseStatus
from src.health.services import get_database_status

tags: list[str | Enum] = [Tag.HEALTH]

router = APIRouter(prefix=Tag.HEALTH, tags=tags)


@router.get("/", response_model=DatabaseStatus)
async def database_status(
    connection: Annotated[AsyncConnection, Depends(get_connection)],
) -> DatabaseStatus:
    """Check the database status."""
    try:
        await get_database_status(connection)
    except (OSError, NoResultFound):
        return DatabaseStatus(status="ERROR")
    else:
        return DatabaseStatus(status="OK")
