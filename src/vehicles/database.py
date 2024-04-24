from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Identity,
    Integer,
    MetaData,
    String,
    Table,
    Uuid,
    func,
)

from src.constants import DB_NAMING_CONVENTION

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

auth_user = Table(
    "vehicles",
    metadata,
    Column("id", Uuid, Identity(), primary_key=True),
    Column("name", String, nullable=False),
    Column("manufacturing_year", Integer, nullable=False),
    Column("body", JSON, nullable=True),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)
