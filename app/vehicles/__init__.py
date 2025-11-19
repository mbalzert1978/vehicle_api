"""Vehicle Module."""

from app.vehicles.router import router
from app.vehicles.schemas import CreateVehicle, UpdateVehicle, VehicleFromDatabase

__all__ = [
    "router",
    "CreateVehicle",
    "UpdateVehicle",
    "VehicleFromDatabase",
]
