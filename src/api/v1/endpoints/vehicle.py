# mypy: disable-error-code="arg-type"

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import session_factory
from src.core.error import HTTPError
from src.schemas import vehicle as schemas
from src.service import services

router = APIRouter(prefix="/vehicle", tags=["vehicle"])

log = logging.getLogger(__name__)

UNCAUGHT = "Uncaught exception"
OFFSET = 0
LIMIT = 100


@router.get("/", response_model=list[schemas.Vehicle])
def list_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008
    offset: int = OFFSET,
    limit: int = LIMIT,
) -> list[schemas.Vehicle]:

@router.get("/", response_model=list[Vehicle])
def list_vehicle(
    session: Session = Depends(get_session),  # noqa: B008
    offset: int = 0,
    limit: int = 100,
) -> list[Vehicle]:
    vehicles = CRUDBase(models.Vehicle).get_all(
        session=session,
        offset=offset,
        limit=limit,
    )
    return [Vehicle.from_orm(vehicle) for vehicle in vehicles]


    try:
        with session as db:
            return services.list_all(db, offset, limit)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.get("/{filter_by}/{value}", response_model=list[schemas.Vehicle])
def filter_vehicle(  # noqa: D417
    *,
    filter_by: services.FilterBy,
    value: str | int | bool,
    session: Session = Depends(session_factory),  # noqa: B008
) -> list[schemas.Vehicle]:


    try:
        with session as db:
            return services.filter_by(db, filter_by, value)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008,
    name: str,
    year_of_manufacture: int,
    body: dict | None = None,
    ready_to_drive: bool = False,
) -> schemas.Vehicle:


    try:
        with session as db:
            return services.create(
                db,
                name,
                year_of_manufacture,
                body,
                ready_to_drive=ready_to_drive,
            )
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.put("/{id}", response_model=schemas.Vehicle)
def update_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008
    id: int,  # noqa: A002
    update_with: schemas.VehicleUpdate,
) -> schemas.Vehicle:

    try:
        with session as db:
            return services.update(db, id, update_with)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.get("/{id}", response_model=schemas.Vehicle)
def get_vehicle(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008
    id: int,  # noqa: A002
) -> schemas.Vehicle:
    try:
        with session as db:
            return services.get(db, id)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(  # noqa: D417
    *,
    session: Session = Depends(session_factory),  # noqa: B008
    id: int,  # noqa: A002
) -> None:
    try:
        with session as db:
            services.delete(db, id)
    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        log.exception(UNCAUGHT)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e
