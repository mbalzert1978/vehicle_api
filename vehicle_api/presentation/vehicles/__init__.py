"""Vehicle Module."""

from presentation.vehicles.database import metadata
from presentation.vehicles.router import router, tags
from presentation.vehicles.schemas import CreateVehicle, UpdateVehicle, VehicleFromDatabase

__all__ = ["metadata", "router", "tags", "CreateVehicle", "UpdateVehicle", "VehicleFromDatabase"]
