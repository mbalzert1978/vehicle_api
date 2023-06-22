# mypy: disable-error-code="arg-type"
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_session
from src.crud.base import CRUDBase
from src.model import vehicle as models
from src.schemas.vehicle import (
    Vehicle,
    VehicleCreate,
    VehicleData,
    VehicleUpdate,
)

router = APIRouter(prefix="/vehicle", tags=["vehicle"])


@router.get("/", response_model=list[Vehicle])
def list_vehicle(
    session: Session = Depends(get_session),  # noqa: B008
    offset: int = 0,
    limit: int = 100,
) -> list[Vehicle]:
    vehicle = CRUDBase(models.Vehicle).get_all(
        session=session,
        offset=offset,
        limit=limit,
    )
    return [Vehicle.from_orm(v) for v in vehicle]


@router.post("/", response_model=Vehicle)
def create_vehicle(
    *,
    session: Session = Depends(get_session),  # noqa: B008,
    name: str,
    year_of_manufacture: int,
    body: VehicleData | None = None,
    ready_to_drive: bool = False,
) -> Vehicle:
    vehicle = CRUDBase(models.Vehicle).create(
        session=session,
        to_create=VehicleCreate(
            name=name,
            year_of_manufacture=year_of_manufacture,
            body=body or VehicleData(),
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
    if not (vehicle := CRUDBase(models.Vehicle).get(session=session, id=id)):
        raise HTTPException(status_code=404, detail="Vehicle not found.")

    vehicle = CRUDBase(models.Vehicle).update(
        session=session,
        to_update=vehicle,
        update_with=update_with,
    )
    return Vehicle.from_orm(vehicle)


@router.get("/{id}", response_model=Vehicle)
def read_vehicle(
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
