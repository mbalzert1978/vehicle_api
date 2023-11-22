"""FastAPI database status module."""
# mypy: disable-error-code="arg-type"
# ruff: noqa: B008
import logging
from typing import Literal, cast

from fastapi import APIRouter, Depends, status

from src.core.session import SESSION_LOCAL, AbstractSession
from src.crud import REPOSITORY_LOCAL, AbstractRepository

service = APIRouter(prefix="/service", tags=["service"])

log = logging.getLogger(__name__)


@service.get("/")
def database_status(
    *,
    session: AbstractSession = Depends(SESSION_LOCAL),
    repository: AbstractRepository = Depends(REPOSITORY_LOCAL()),
) -> Literal[200]:
    """Check the database status."""
    with session as db:
        repository.execute(db, stmnt="SELECT 1=1;")
        return cast(Literal[200], status.HTTP_200_OK)
