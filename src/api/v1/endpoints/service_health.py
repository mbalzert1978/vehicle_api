"""FastAPI database status module."""
# mypy: disable-error-code="arg-type"
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import OperationalError

from src.api.dependencies import session_factory
from src.core.session import Session

service = APIRouter(prefix="/service", tags=["service"])

log = logging.getLogger(__name__)


@service.get("/")
def database_status(
    *,
    session: Session = Depends(session_factory),  # noqa: B008
) -> dict[str, str]:
    """
    Check the status of the database.

    Raises
    ------
    HTTPException: If the database is unavailable or an unexpected error occurs.

    Returns
    -------
    A dictionary with the status indicating that the database is functioning properly.
    """
    try:
        with session as db:
            db.execute("SELECT VERSION();")
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        ) from e
    except Exception as e:
        log.exception("Uncaught exception")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e
    else:
        return {"status": "ok"}
