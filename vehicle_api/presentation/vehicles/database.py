from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Table,
    Uuid,
    func,
)

from presentation.database import metadata

vehicles = Table(
    "vehicles",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("name", String, nullable=False),
    Column("manufacturing_year", Integer, nullable=False),
    Column("is_drivable", Boolean, nullable=True),
    Column("body", JSON, nullable=True),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)
