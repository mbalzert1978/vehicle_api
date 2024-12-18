import uuid
from typing import Any, Sequence

from sqlalchemy import RowMapping, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.database import execute, fetch_all, fetch_one
from app.vehicles.database import vehicles
from app.vehicles.schemas import CreateVehicle, UpdateVehicle


async def insert_vehicle(
    conn: AsyncConnection, to_create: CreateVehicle
) -> RowMapping | None:
    insert_query = insert(vehicles).values(**to_create.model_dump()).returning(vehicles)
    return await fetch_one(conn, insert_query)


async def delete_vehicle(conn: AsyncConnection, id: uuid.UUID) -> None:
    delete_query = delete(vehicles).filter_by(id=id)
    await execute(conn, delete_query)


async def get_vehicles(
    conn: AsyncConnection, filter_on: dict[str, Any]
) -> Sequence[RowMapping]:
    select_query = select(vehicles).filter_by(**filter_on)
    return await fetch_all(conn, select_query)


async def update_vehicle(
    conn: AsyncConnection, id: uuid.UUID, update_with: UpdateVehicle
) -> None:
    update_query = (
        update(vehicles)
        .filter_by(id=id)
        .values(**update_with.model_dump(exclude_none=True))
    )
    await execute(conn, update_query)
