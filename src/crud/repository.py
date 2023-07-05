"""Repository for CRUD operations on a model."""
from __future__ import annotations

from typing import TYPE_CHECKING, Generic

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from src.domain import types

if TYPE_CHECKING:
    from collections.abc import Sequence

    from sqlalchemy.orm import Session


def factory(model: type[types.ModelType]) -> CRUDRepository:
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


class CRUDRepository(
    Generic[types.ModelType, types.CreateSchemaType, types.UpdateSchemaType],
):

    """Repository for CRUD operations on a model with SQLAlchemy ORM."""

    def __init__(self, model: type[types.ModelType]) -> None:
        self.model = model

    def get(
        self,
        session: Session,
        id: int,  # noqa: A002
    ) -> types.ModelType | None:
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
        return session.get(self.model, id)

    def filter_by(
        self,
        session: Session,
        filter_by: dict,
    ) -> Sequence[types.ModelType]:
        """
        Filter model instances based on the provided criteria.

        Args:
        ----
        session: An SQLAlchemy Session object.
        filter_by: A dictionary containing the filter criteria.
        The keys represent the column names, and the values represent the filter values.

        Returns:
        -------
            A sequence of model instances that match the filter criteria.

        """
        stmt = select(self.model).filter_by(**filter_by)
        return session.execute(stmt).scalars().all()

    def get_all(
        self,
        session: Session,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[types.ModelType]:
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
        stmt = select(self.model).offset(offset).limit(limit)
        return session.execute(stmt).scalars().all()

    def create(
        self,
        session: Session,
        *,
        to_create: types.CreateSchemaType,
    ) -> types.ModelType:
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

    def update(
        self,
        session: Session,
        *,
        to_update: types.ModelType,
        update_with: types.UpdateSchemaType | dict,
    ) -> types.ModelType:
        """
        Update a model instance with new data.

        Args:
        ----
        session: An SQLAlchemy Session object.
        to_update: The model instance to update.
        update_with: The data to update the model instance with.

        Returns:
        -------
        The updated model instance.

        """
        serialized_data = jsonable_encoder(to_update)
        update_data = extract_data(update_with)
        update_fields(to_update, serialized_data, update_data)
        return write_to_database(session, to_update)

    def remove(
        self,
        session: Session,
        *,
        id: int,  # noqa: A002
    ) -> types.ModelType | None:
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


def extract_data(update_with: types.UpdateSchemaType | dict) -> dict:
    """
    Extract the update data from the given object.

    Args:
    ----
    update_with: The object containing the update data.

    Returns:
    -------
    The extracted update data as a dictionary.

    """
    return (
        update_with
        if isinstance(update_with, dict)
        else update_with.dict(exclude_unset=True)
    )


def update_fields(
    to_update: types.ModelType,
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


def write_to_database(
    session: Session,
    to_create: types.ModelType,
) -> types.ModelType:
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
