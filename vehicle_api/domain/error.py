import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class Error:
    """Errors."""

    code: str
    description: str = ""

    @classmethod
    def none(cls) -> "Error":
        return cls(code="none", description="")

    @classmethod
    def internal_server_error(cls, description: str) -> "Error":
        return cls(code="500", description=description)

    @classmethod
    def bad_request(cls, description: str) -> "Error":
        return cls(code="400", description=description)
