"""FastAPI database status module."""
# mypy: disable-error-code="arg-type"
# ruff: noqa: B008
import logging

from fastapi import APIRouter, Depends

from src import crud
from src.api.dependecies.database import get_repository
from src.schemas.status import DatabaseStatus

router = APIRouter()

log = logging.getLogger(__name__)


@router.get("/", response_model=DatabaseStatus)
def database_status(
    repository: crud.AbstractRepository = Depends(get_repository(crud.SQLAlchemyRepository)),
)  -> DatabaseStatus:
    """Check the database status."""
    repository.execute(stmnt="SELECT 1=1;")
    return DatabaseStatus()
