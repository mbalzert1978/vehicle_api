# mypy: disable-error-code="arg-type"
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.dependencies import get_session
from src.crud.base import CRUDBase
from src.model import vehicle as models
from src.schemas.vehicle import Vehicle, VehicleCreate, VehicleUpdate

router = APIRouter(prefix="/vehicle", tags=["vehicle"])


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


@router.post("/", response_model=Vehicle)
def create_vehicle(
    *,
    session: Session = Depends(get_session),  # noqa: B008,
    name: str,
    year_of_manufacture: int,
    body: dict[str, Any] | None = None,
    ready_to_drive: bool = False,
) -> Vehicle:
    vehicle = CRUDBase(models.Vehicle).create(
        session=session,
        to_create=VehicleCreate(
            name=name,
            year_of_manufacture=year_of_manufacture,
            body=body,
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
