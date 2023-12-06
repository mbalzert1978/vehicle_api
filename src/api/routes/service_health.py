"""FastAPI database status module."""
# mypy: disable-error-code="arg-type"
# ruff: noqa: B008
import logging

from fastapi import APIRouter, Depends

from src import crud
from src.api.dependecies.database import get_repository

router = APIRouter()

log = logging.getLogger(__name__)


@router.get("/")
def database_status(
    repository: crud.AbstractRepository = Depends(get_repository(crud.SQLAlchemyRepository)),
) -> dict[str, str]:
    """Check the database status."""
    repository.execute(stmnt="SELECT 1=1;")
    return {"status": "Ok"}
