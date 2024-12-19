"""Vehicle Module."""

from app.vehicles.database import metadata
from app.vehicles.router import router
from app.vehicles.schemas import CreateVehicle, UpdateVehicle, VehicleFromDatabase

__all__ = [
    "metadata",
    "router",
    "CreateVehicle",
    "UpdateVehicle",
    "VehicleFromDatabase",
]
