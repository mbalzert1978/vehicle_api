from typing import Any

from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSON}


class Vehicle(Base):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(  # noqa: A003
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column()
    year_of_manufacture: Mapped[int] = mapped_column()
    body: Mapped[dict[str, Any]] = mapped_column()
    ready_to_drive: Mapped[bool] = mapped_column()
