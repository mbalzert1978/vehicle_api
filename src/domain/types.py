"""types Module."""
from typing import TypeVar

from pydantic import BaseModel

from src.domain.models import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel, covariant=True)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReturnSchemaType = TypeVar("ReturnSchemaType", bound=BaseModel)
