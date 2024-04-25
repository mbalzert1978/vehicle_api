"""FastAPI service module."""

from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection

from src.database import get_connection
from src.service.constants import Tag
from src.service.schemas import DatabaseStatus
from src.service.services import get_database_status

tags: list[str | Enum] = [Tag.SERVICE]

router = APIRouter(prefix=Tag.SERVICE, tags=tags)


@router.get("/", response_model=DatabaseStatus)
async def database_status(
    connection: Annotated[AsyncConnection, Depends(get_connection)],
) -> DatabaseStatus:
    """Check the database status."""
    try:
        await get_database_status(connection)
    except NoResultFound:
        return DatabaseStatus(status="Error")
    else:
        return DatabaseStatus(status="OK")
