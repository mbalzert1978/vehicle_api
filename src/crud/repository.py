"""Repository for CRUD operations on a model."""
from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, text

from src.model.valueobject import ValueObject
from src.model.vehicle import Base

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
T = TypeVar("T")


def factory(model: type[ModelType]) -> CRUDRepository:
    """
    Create a CRUDRepository instance for a given model type.

    Args:
    ----
    model: The model type for which the CRUDRepository instance is created.

    Returns:
    -------
    A CRUDRepository instance.

    """
    return CRUDRepository(model)


class CRUDRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Repository for CRUD operations on a model with SQLAlchemy ORM."""

    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    def execute(self, session: Session, *, stmnt: str) -> None:
        session.execute(text(stmnt))

    def get(self,
            session: Session,
            *,
            id: ValueObject,
            default: T | None = None) -> ModelType | T:
        """
        Retrieve a model instance by its ID.

        Args:
        ----
        session: An SQLAlchemy Session object.
        id: The ID of the model instance to retrieve.

        Returns:
        -------
        The model instance if found, or None if not found.

        """
        return result if (result := session.get(self.model, id)) else default

    def list( # noqa: A003
            self,
            session: Session,
            *,
            filter_by: dict | None = None) -> Sequence[ModelType]:
        """
        Retrieve multiple model instances with optional offset and limit.

        Args:
        ----
        session: An SQLAlchemy Session object.
        offset: The number of results to skip from the beginning.
        limit: The maximum number of results to retrieve.

        Returns:
        -------
        A sequence of model instances.

        """
        stmt = select(self.model).filter_by(**filter_by or {})
        return session.execute(stmt).scalars().all()

    def create(self, session: Session, *,
               to_create: CreateSchemaType) -> ModelType:
        """
        Create a new model instance.

        Args:
        ----
        session: An SQLAlchemy Session object.
        to_create: The data to create the model instance.

        Returns:
        -------
        The created model instance.

        """
        serialized_data = jsonable_encoder(to_create)
        obj = self.model(**serialized_data)
        return write_to_database(session, obj)

    def update(self, session: Session, *, to_update: ModelType,
               data: UpdateSchemaType) -> ModelType:
        """
        Update a model instance with new data.

        Args:
        ----
        session: An SQLAlchemy Session object.
        to_update: The model instance to update.
        data: The data to update the model instance with.

        Returns:
        -------
        The updated model instance.

        """
        serialized_data = jsonable_encoder(to_update)
        update_data = extract_data(data)
        update_fields(to_update, serialized_data, update_data)
        return write_to_database(session, to_update)

    def delete(self, session: Session, *, id: ValueObject) -> ModelType | None:
        """
        Remove a model instance by its ID.

        Args:
        ----
        session: An SQLAlchemy Session object.
        id: The ID of the model instance to remove.

        Returns:
        -------
        The removed model instance if found, or None if not found.

        """
        if not (obj := session.get(self.model, id)):
            return None
        session.delete(obj)
        session.commit()
        return obj


def extract_data(update_with: UpdateSchemaType | dict) -> dict:
    """
    Extract the update data from the given object.

    Args:
    ----
    update_with: The object containing the update data.

    Returns:
    -------
    The extracted update data as a dictionary.

    """
    return (update_with if isinstance(update_with, dict) else update_with.dict(
        exclude_unset=True))


def update_fields(
    to_update: ModelType,
    serialized_data: dict,
    update_data: dict,
) -> None:
    """
    Update the fields of a model instance with new data.

    Args:
    ----
    to_update: The model instance to update.
    serialized_data: The serialized data of the model instance.
    update_data: The data containing the fields to update.

    Returns:
    -------
    None

    """
    for field in serialized_data:
        if field not in update_data:
            continue
        setattr(to_update, field, update_data[field])


def write_to_database(session: Session, to_create: ModelType) -> ModelType:
    """
    Write a model instance to the database.

    Args:
    ----
    session: An SQLAlchemy Session object.
    to_create: The model instance to write to the database.

    Returns:
    -------
    The written model instance.

    """
    session.add(to_create)
    session.commit()
    session.refresh(to_create)
    return to_create
