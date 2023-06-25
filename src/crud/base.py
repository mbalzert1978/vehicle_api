from collections.abc import Sequence
from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.model.vehicle import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    def get(self, session: Session, id: int) -> ModelType | None:  # noqa: A002
        return session.get(self.model, id)

    def filter_by(
        self,
        session: Session,
        filter_by: dict[str, str | int | bool],
    ) -> Sequence[ModelType]:
        stmt = select(self.model).filter_by(**filter_by)
        return session.execute(stmt).scalars().all()

    def get_all(
        self,
        session: Session,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)
        return session.execute(stmt).scalars().all()

    def create(
        self,
        session: Session,
        *,
        to_create: CreateSchemaType,
    ) -> ModelType:
        serialized_data = jsonable_encoder(to_create)
        obj = self.model(**serialized_data)
        return write_to_database(session, obj)

    def update(
        self,
        session: Session,
        *,
        to_update: ModelType,
        update_with: UpdateSchemaType | dict,
    ) -> ModelType:
        serialized_data = jsonable_encoder(to_update)
        update_data = extract_data(update_with)
        update_fields(to_update, serialized_data, update_data)
        return write_to_database(session, to_update)

    def remove(
        self,
        session: Session,
        *,
        id: int,  # noqa: A002
    ) -> ModelType | None:
        if not (obj := session.get(self.model, id)):
            return None
        session.delete(obj)
        session.commit()
        return obj


def extract_data(update_with: UpdateSchemaType | dict) -> dict:
    return (
        update_with
        if isinstance(update_with, dict)
        else update_with.dict(exclude_unset=True)
    )


def update_fields(
    to_update: ModelType,
    serialized_data: dict,
    update_data: dict,
) -> None:
    for field in serialized_data:
        if field not in update_data:
            continue
        setattr(to_update, field, update_data[field])


def write_to_database(session: Session, to_create: ModelType) -> ModelType:
    session.add(to_create)
    session.commit()
    session.refresh(to_create)
    return to_create
