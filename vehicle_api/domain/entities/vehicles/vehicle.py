import dataclasses

from vehicle_api.domain.entities.vehicles.year import Year
from vehicle_api.domain.shared.aggregate import AggregateRoot


@dataclasses.dataclass(slots=True, eq=False)
class Vehicle(AggregateRoot):
    name: str
    manufacture_year: Year
    is_drivable: bool
