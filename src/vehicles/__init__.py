"""Vehicle Module."""

from src.vehicles.database import metadata
from src.vehicles.router import router, tags
from src.vehicles.schemas import CreateVehicle, UpdateVehicle, VehicleFromDatabase

__all__ = ["metadata", "router", "tags", "CreateVehicle", "UpdateVehicle", "VehicleFromDatabase"]
