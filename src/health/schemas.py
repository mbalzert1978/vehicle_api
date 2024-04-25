from pydantic import BaseModel, Field


class DatabaseStatus(BaseModel):
    status: str = Field(default="Ok")
