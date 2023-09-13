"""FastAPI database status module."""
# mypy: disable-error-code="arg-type"
# ruff: noqa: B008
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import OperationalError

from src.api.dependencies import session_factory
from src.core.session import Session
from src.crud import REPOSITORY_FACTORY, AbstractRepository

service = APIRouter(prefix="/service", tags=["service"])

log = logging.getLogger(__name__)


@service.get("/")
def database_status(
    *,
    session: Session = Depends(session_factory),
    repository: AbstractRepository = Depends(REPOSITORY_FACTORY),
) -> dict[str, str]:
    """Checks the database status."""
    try:
        with session as db:
            repository.execute(db, stmnt="SELECT VERSION();")
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, ) from e
    except Exception as e:
        log.exception("Uncaught exception")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, ) from e
    else:
        return {"status": "ok"}
