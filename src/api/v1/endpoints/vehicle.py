from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.model import vehicle as models
from src.schemas.vehicle import Vehicle, VehicleCreate, VehicleUpdate

router = APIRouter()


@router.get("/", response_model=list[Vehicle])
def list_vehicle(
    session: Session = Depends(deps.get_db),
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
    session: Session = Depends(deps.get_db),
    to_create: VehicleCreate,
) -> Vehicle:
    vehicle = CRUDBase(models.Vehicle).create(
        session=session,
        to_create=to_create,
    )
    return Vehicle.from_orm(vehicle)


@router.put("/{id}", response_model=Vehicle)
def update_vehicle(
    *,
    session: Session = Depends(deps.get_db),
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
    session: Session = Depends(deps.get_db),
    id: int,
) -> Vehicle:
    if not (vehicle := CRUDBase(models.Vehicle).get(session=session, id=id)):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
    return Vehicle.from_orm(vehicle)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    *,
    session: Session = Depends(deps.get_db),
    id: int,
) -> None:
    if not CRUDBase(models.Vehicle).remove(session=session, id=id):
        raise HTTPException(status_code=404, detail="Vehicle not found.")
