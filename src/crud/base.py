"""Crud Protocol."""
from collections.abc import Sequence
from typing import Protocol, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.model.vehicle import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar(
    "CreateSchemaType",
    contravariant=True,
    bound=BaseModel,
)
UpdateSchemaType = TypeVar(
    "UpdateSchemaType",
    contravariant=True,
    bound=BaseModel,
)


class CRUD(Protocol[ModelType, CreateSchemaType, UpdateSchemaType]):

    """CRUD Protocol."""

    def get(self, session: Session, id: int) -> ModelType | None:  # noqa: A002
        """Get by id."""
        ...

    def filter_by(
        self,
        session: Session,
        filter_by: dict[str, str | int | bool],
    ) -> Sequence[ModelType]:
        """Filter by dict."""
        ...

    def get_all(
        self,
        session: Session,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        """Get all."""
        ...

    def create(
        self,
        session: Session,
        *,
        to_create: CreateSchemaType,
    ) -> ModelType:
        """Create object."""
        ...

    def update(
        self,
        session: Session,
        *,
        to_update: ModelType,
        update_with: UpdateSchemaType | dict,
    ) -> ModelType:
        """Update object."""
        ...

    def remove(
        self,
        session: Session,
        *,
        id: int,  # noqa: A002
    ) -> ModelType | None:
        """Remove by id."""
        ...
