"""Model."""

from fastapi.encoders import jsonable_encoder

from src.model.base import Base
from src.utils.utils import utc_now


class Vehicle(Base):
    """Vehicle Model."""

    def __init__(
        self,
        name: str = "default",
        year_of_manufacture: int | None = None,
        body: dict | None = None,
        *,
        ready_to_drive: bool = False,
    ) -> None:
        self._id: int | None = None
        self.name = name
        self.year_of_manufacture = year_of_manufacture or utc_now().year
        self.body = body or {}
        self.ready_to_drive = ready_to_drive

    def model_dump(self) -> dict:
        """Dump Vehicle Model."""
        return jsonable_encoder(self, exclude_unset=True)

    def __repr__(self) -> str:
        return (
            f"Vehicle(name={self.name}, "
            f"year_of_manufacture={self.year_of_manufacture}, "
            f"body={self.body}, "
            f"ready_to_drive={self.ready_to_drive})"
        )
