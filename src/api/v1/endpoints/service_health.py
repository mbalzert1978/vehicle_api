# mypy: disable-error-code="arg-type"
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from src.api.dependencies import get_session

service = APIRouter(prefix="/service", tags=["service"])


@service.get("/")
def database_status(
    session: Session = Depends(get_session),  # noqa: B008
) -> dict[str, str]:
    try:
        session.execute(text("SELECT VERSION();"))
    except OperationalError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        ) from e
    else:
        return {"status": "ok"}
