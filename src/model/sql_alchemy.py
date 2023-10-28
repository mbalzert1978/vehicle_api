from sqlalchemy import JSON, Boolean, Column, Integer, String, Table
from sqlalchemy.orm import registry

mapper_registry = registry()

vehicle_table = Table(
    "vehicle",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("year_of_manufacture", Integer),
    Column("body", JSON),
    Column("ready_to_drive", Boolean),
)
