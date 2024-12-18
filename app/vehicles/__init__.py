"""Vehicle Module."""

from app.vehicles.database import metadata
from app.vehicles.router import router, tags
from app.vehicles.schemas import CreateVehicle, UpdateVehicle, VehicleFromDatabase

__all__ = [
    "metadata",
    "router",
    "tags",
    "CreateVehicle",
    "UpdateVehicle",
    "VehicleFromDatabase",
]
