"""FastAPI database status module."""
# mypy: disable-error-code="arg-type"
# ruff: noqa: B008
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import OperationalError

from src.core.session import SESSION_LOCAL, AbstractSession
from src.crud import REPOSITORY_LOCAL, AbstractRepository

service = APIRouter(prefix="/service", tags=["service"])

log = logging.getLogger(__name__)


@service.get("/")
def database_status(*,
                    session: AbstractSession = Depends(SESSION_LOCAL),
                    repository: AbstractRepository = Depends(REPOSITORY_LOCAL())) -> str:
    """Checks the database status."""
    try:
        with session as db:
            repository.execute(db, stmnt="SELECT 1=1;")
    except OperationalError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE) from e
    except Exception as e:
        log.exception("Uncaught exception")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
    else:
        return status.HTTP_200_OK
