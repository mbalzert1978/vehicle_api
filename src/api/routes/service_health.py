"""FastAPI database status module."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from src import crud
from src.api.dependecies.database import get_repository
from src.schemas.status import DatabaseStatus

router = APIRouter()

log = logging.getLogger(__name__)


@router.get("/", response_model=DatabaseStatus)
def database_status(
    repository: Annotated[crud.AbstractRepository, Depends(get_repository(crud.SQLAlchemyRepository))],
) -> DatabaseStatus:
    """Check the database status."""
    repository.execute(stmnt="SELECT 1=1;")
    return DatabaseStatus()
