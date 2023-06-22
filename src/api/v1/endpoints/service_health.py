# mypy: disable-error-code="arg-type"
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_session

router = APIRouter(prefix="/service", tags=["service"])


@router.get("/")
def database_status(
    session: Session = Depends(get_session),  # noqa: B008
):
    return {"status": "ok"}
