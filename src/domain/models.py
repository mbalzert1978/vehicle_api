"""Sqlachemy Models."""
from sqlalchemy import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    """Base Model."""

    type_annotation_map = {dict: JSON}


class Vehicle(Base):

    """Vehicle Model."""

    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(  # noqa: A003
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column()
    year_of_manufacture: Mapped[int] = mapped_column()
    body: Mapped[dict] = mapped_column()
    ready_to_drive: Mapped[bool] = mapped_column(default=False)
