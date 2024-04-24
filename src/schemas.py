import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, model_validator


class CustomModel(BaseModel):
    model_config = ConfigDict(ser_json_timedelta="iso8601", populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {k: v.replace(microsecond=0) for k, v in data.items() if isinstance(v, datetime.datetime)}

        return {**data, **datetime_fields}

    def serialize(self, mode: Literal["json", "python"] = "json") -> dict[str, Any]:
        """Serialize the model to a dictionary.

        # Args:
        mode: The mode in which `serialize` should run. defaults to 'json'.\n
            If mode is 'json', the output will only contain JSON serializable types.\n
            If mode is 'python', the output may contain non-JSON-serializable Python objects.
        """
        return self.model_dump(mode=mode)
