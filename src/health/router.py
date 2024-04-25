"""FastAPI service module."""

from enum import Enum

from fastapi import APIRouter
from sqlalchemy.exc import NoResultFound

from src.database import engine
from src.health.constants import Tag
from src.health.schemas import DatabaseStatus
from src.health.services import get_database_status

tags: list[str | Enum] = [Tag.HEALTH]

router = APIRouter(prefix=Tag.HEALTH, tags=tags)


@router.get("/", response_model=DatabaseStatus)
async def database_status() -> DatabaseStatus:
    """Check the database status."""
    try:
        async with engine.connect() as connection:
            await get_database_status(connection)
    except (OSError, NoResultFound):
        return DatabaseStatus(status="ERROR")
    else:
        return DatabaseStatus(status="OK")
