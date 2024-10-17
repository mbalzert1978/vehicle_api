"""Vehicle Module."""

from vehicle_api.vehicles.database import metadata
from vehicle_api.vehicles.router import router, tags
from vehicle_api.vehicles.schemas import CreateVehicle, UpdateVehicle, VehicleFromDatabase

__all__ = ["metadata", "router", "tags", "CreateVehicle", "UpdateVehicle", "VehicleFromDatabase"]
