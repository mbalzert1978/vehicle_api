import uuid
from typing import Any, Sequence

from sqlalchemy import Connection, RowMapping, delete, insert, select, update

from app.database import execute, fetch_all, fetch_one
from app.vehicles.database import vehicles
from app.vehicles.schemas import CreateVehicle, UpdateVehicle


def insert_vehicle(conn: Connection, to_create: CreateVehicle) -> RowMapping | None:
    insert_query = insert(vehicles).values(**to_create.model_dump()).returning(vehicles)
    return fetch_one(conn, insert_query)


def delete_vehicle(conn: Connection, id: uuid.UUID) -> None:
    delete_query = delete(vehicles).filter_by(id=id)
    execute(conn, delete_query)


def get_vehicles(conn: Connection, filter_on: dict[str, Any]) -> Sequence[RowMapping]:
    select_query = select(vehicles).filter_by(**filter_on)
    return fetch_all(conn, select_query)


def update_vehicle(conn: Connection, id: uuid.UUID, update_with: UpdateVehicle) -> None:
    update_query = (
        update(vehicles)
        .filter_by(id=id)
        .values(**update_with.model_dump(exclude_none=True))
    )
    execute(conn, update_query)
