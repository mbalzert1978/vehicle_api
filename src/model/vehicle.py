from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Vehicle(Base):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(  # noqa: A003
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column()
    year_of_manufacture: Mapped[int] = mapped_column()
    body: Mapped[str] = mapped_column()
    ready_to_drive: Mapped[bool] = mapped_column()
