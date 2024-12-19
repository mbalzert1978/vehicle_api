"""FastAPI service module."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncConnection

from app.database import get_connection
from app.health.schemas import DatabaseStatus
from app.health.services import get_database_status

router = APIRouter(prefix="/health", tags=["Health"])


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
