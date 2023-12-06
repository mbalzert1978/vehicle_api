# ruff: noqa: A003, A002
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, overload


if TYPE_CHECKING:
    from collections.abc import Sequence


class AbstractRepository[ModelType, CreateSchemaType, UpdateSchemaType](Protocol):
    model: ModelType
    """The abstract repository protocol."""

    @staticmethod
    def execute(*, stmnt: str) -> None:
        """
        Execute a statement in the database.

        Parameters
        ----------
        session : Session
            the database session object.
        stmnt : str
            the statement to execute.
        """

    def create(self, *, to_create: CreateSchemaType) -> ModelType:
        """
        Create a ModelType object in the database.

        Parameters
        ----------
        session : Session
            the database session object.
        to_create : CreateSchemaType
            the CreateSchemaType object to create.

        Returns
        -------
        ModelType
            the ModelType object.
        """

    @overload
    def get(self, *, id: int) -> ModelType:
        ...

    @overload
    def get[U](self, *, id: int, default: U) -> ModelType | U:
        ...

    @overload
    def get[U](self, *, id: int, default: U | None = None) -> ModelType | U:
        """
        Get a ModelType object from the database.

        Parameters
        ----------
        session : Session
            the database session object.
        id : int
            the id of the ModelType object.
        default : T | None, optional
            the default value to return if the ModelType object is not found.
            The default value is None.

        Returns
        -------
        ModelType | T
            the ModelType object or the default value.
        """

    def list(self, *, filter_by: dict | None = None) -> Sequence[ModelType]:
        """
        Get a list of ModelType objects from the database.

        Parameters
        ----------
        session : Session
            the database session object.
        filter_by : dict | None, optional
            the filter by dictionary. The default value is None.

        Returns
        -------
        Sequence[ModelType]
            the list of ModelType objects.
        """

    def update(
        self,
        *,
        to_update: ModelType,
        data: UpdateSchemaType,
    ) -> ModelType:
        """
        Update a ModelType object in the database.

        Parameters
        ----------
        session : Session
            the database session object.
        to_update : ModelType
            the ModelType object to update.
        data : UpdateSchemaType
            the data to update the ModelType object.

        Returns
        -------
        ModelType
            the updated ModelType object.
        """

    def delete(self, *, id: int) -> ModelType | None:
        """
        Delete a ModelType object from the database.

        Parameters
        ----------
        session : Session
            the database session object.
        id : int
            the id of the ModelType object.
        """
