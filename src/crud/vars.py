import typing

from pydantic import BaseModel

from src.model.base import Base

ModelType = typing.TypeVar("ModelType", bound=Base)
CreateSchemaType = typing.TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = typing.TypeVar("UpdateSchemaType", bound=BaseModel)
U = typing.TypeVar("U")
