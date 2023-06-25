# mypy: disable-error-code="arg-type"

from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_session
from src.crud.base import CRUDBase
from src.model import vehicle as models
from src.schemas.vehicle import Vehicle, VehicleCreate, VehicleUpdate

router = APIRouter(prefix="/vehicle", tags=["vehicle"])

UNPROCESSABLE = "unprocessable value, not a"


class FilterBy(str, Enum):
    NAME = "name"
    YEAR_OF_MANUFACTURE = "year_of_manufacture"
    READY_TO_DRIVE = "ready_to_drive"


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


@router.get("/{filter_by}/{value}", response_model=list[Vehicle])
def filter_vehicle(
    filter_by: FilterBy,
    value: str | int | bool,
    session: Session = Depends(get_session),  # noqa: B008
) -> list[Vehicle]:
    match filter_by:
        case FilterBy.NAME:
            if not isinstance(value, str):
                raise HTTPException(
                    status_code=422,
                    detail=f"{UNPROCESSABLE} string.",
                )
            vehicles = CRUDBase(models.Vehicle).filter_by(
                session=session,
                filter_by={"name": value},
            )
        case FilterBy.YEAR_OF_MANUFACTURE:
            if not isinstance(value, int):
                raise HTTPException(
                    status_code=422,
                    detail=f"{UNPROCESSABLE} integer.",
                )
            vehicles = CRUDBase(models.Vehicle).filter_by(
                session=session,
                filter_by={"year_of_manufacture": value},
            )
        case FilterBy.READY_TO_DRIVE:
            if not isinstance(value, bool):
                raise HTTPException(
                    status_code=422,
                    detail=f"{UNPROCESSABLE} boolean.",
                )
            vehicles = CRUDBase(models.Vehicle).filter_by(
                session=session,
                filter_by={"ready_to_drive": value},
            )
    return [Vehicle.from_orm(vehicle) for vehicle in vehicles]


@router.post("/", response_model=Vehicle)
def create_vehicle(
    *,
    session: Session = Depends(get_session),  # noqa: B008,
    name: str,
    year_of_manufacture: int,
    body: dict | None = None,
    ready_to_drive: bool = False,
) -> Vehicle:
    vehicle = CRUDBase(models.Vehicle).create(
        session=session,
        to_create=VehicleCreate(
            name=name,
            year_of_manufacture=year_of_manufacture,
            body=body or {},
            ready_to_drive=ready_to_drive,
        ),
    )
    return Vehicle.from_orm(vehicle)


@router.put("/{id}", response_model=Vehicle)
def update_vehicle(
    *,
    session: Session = Depends(get_session),  # noqa: B008
    id: int,  # noqa: A002
    update_with: VehicleUpdate,
) -> Vehicle:
    if not (to_update := CRUDBase(models.Vehicle).get(session=session, id=id)):
        raise HTTPException(status_code=404, detail="Vehicle not found.")

    to_update = CRUDBase(models.Vehicle).update(
        session=session,
        to_update=to_update,
        update_with=update_with,
    )
    return Vehicle.from_orm(to_update)


@router.get("/{id}", response_model=Vehicle)
def get_vehicle(
    *,
    session: Session = Depends(get_session),  # noqa: B008
    id: int,  # noqa: A002
) -> Vehicle:
    if not (vehicle := CRUDBase(models.Vehicle).get(session=session, id=id)):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    return Vehicle.from_orm(vehicle)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    *,
    session: Session = Depends(get_session),  # noqa: B008
    id: int,  # noqa: A002
) -> None:
    if not CRUDBase(models.Vehicle).remove(session=session, id=id):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
