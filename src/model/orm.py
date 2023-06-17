from datetime import datetime
from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Brand(Base):
    __tablename__ = "brand"
    brand_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    vehicles = relationship("Vehicle", back_populates="brand")


class Color(Base):
    __tablename__ = "color"
    color_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    vehicles = relationship("Vehicle", back_populates="color")


class TransportMode(str, Enum):
    LAND = "Land"
    SEA = "Sea"
    AIR = "Air"


class TransportationMode(Base):
    __tablename__ = "transportation_mode"
    transportation_mode_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[TransportMode] = mapped_column()
    vehicles = relationship(
        "Vehicle",
        secondary="vehicle_transportation_mode",
        back_populates="transportation_modes",
    )


vehicle_transportation_mode = Table(
    "vehicle_transportation_mode",
    Base.metadata,
    Column("vehicle_id", Integer, ForeignKey("vehicle.vehicle_id")),
    Column(
        "mode_id",
        Integer,
        ForeignKey("transportation_mode.transportation_mode_id"),
    ),
)


class Address(Base):
    __tablename__ = "address"
    address_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    street: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    state: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    owner_id = mapped_column(ForeignKey("owner.owner_id"))
    owner = relationship("Owner", back_populates="address")


class Owner(Base):
    __tablename__ = "owner"
    owner_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    address = relationship("Address", back_populates="owner")
    vehicles = relationship("Vehicle", back_populates="owner")


class Vehicle(Base):
    __tablename__ = "vehicle"
    vehicle_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    model: Mapped[str] = mapped_column()
    year: Mapped[datetime] = mapped_column()
    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.brand_id"))
    brand = relationship("Brand", back_populates="vehicles")
    color_id: Mapped[int] = mapped_column(ForeignKey("color.color_id"))
    color = relationship("Color", back_populates="vehicles")
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("owner.owner_id"),
        nullable=True,
    )
    owner = relationship("Owner", back_populates="vehicles")
    transportation_modes = relationship(
        "TransportationMode",
        secondary=vehicle_transportation_mode,
        back_populates="vehicles",
    )
