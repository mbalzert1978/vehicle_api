from collections.abc import Generator
from dataclasses import dataclass
from http import HTTPStatus
from typing import Final, Protocol

from loguru import logger

UNKNOWN_STATUS_CODE_UPPER_BOUND: Final[int] = 600
STATUS_INFORMATIONAL: Final[str] = "INFORMATIONAL"
STATUS_SUCCESS: Final[str] = "SUCCESS"
STATUS_REDIRECTION: Final[str] = "REDIRECTION"
STATUS_CLIENT_ERROR: Final[str] = "CLIENT_ERROR"
STATUS_SERVER_ERROR: Final[str] = "SERVER_ERROR"


class LogFunction(Protocol):
    """Protocol for logging functions."""

    def __call__(self, message: str) -> None: ...


@dataclass(frozen=True, slots=True)
class LogStrategy:
    """Immutable data class representing a logging strategy."""

    log_function: LogFunction
    status_message: str

    def __iter__(self) -> Generator[tuple[LogFunction, str], None, None]:
        """Allow unpacking of LogStrategy into its components.

        Args:
            None

        Yields:
            A tuple containing the log function and status message.
        """
        assert self.log_function is not None, "Log function should be set"
        assert self.status_message, "Status message should be set"
        yield from (self.log_function, self.status_message)


class LogStrategyFactory:
    """Factory for creating log strategies based on HTTP status codes."""

    @staticmethod
    def new(status_code: int) -> LogStrategy:
        """Create a log strategy for the given status code.

        Args:
            status_code: HTTP status code to determine logging strategy for.

        Returns:
            LogStrategy instance with appropriate log function and message.
        """
        assert isinstance(status_code, int), "Status code must be an integer"

        match status_code:
            case _ if HTTPStatus.CONTINUE <= status_code < HTTPStatus.OK:
                strategy = LogStrategy(logger.info, STATUS_INFORMATIONAL)
            case _ if HTTPStatus.OK <= status_code < HTTPStatus.MULTIPLE_CHOICES:
                strategy = LogStrategy(logger.info, STATUS_SUCCESS)
            case _ if (
                HTTPStatus.MULTIPLE_CHOICES <= status_code < HTTPStatus.BAD_REQUEST
            ):
                strategy = LogStrategy(logger.info, STATUS_REDIRECTION)
            case _ if (
                HTTPStatus.BAD_REQUEST <= status_code < HTTPStatus.INTERNAL_SERVER_ERROR
            ):
                strategy = LogStrategy(logger.error, STATUS_CLIENT_ERROR)
            case _ if (
                HTTPStatus.INTERNAL_SERVER_ERROR
                <= status_code
                < UNKNOWN_STATUS_CODE_UPPER_BOUND
            ):
                strategy = LogStrategy(logger.critical, STATUS_SERVER_ERROR)
            case _:
                strategy = LogStrategy(
                    logger.warning, f"UNKNOWN STATUS CODE: {status_code}"
                )

        assert strategy is not None, "Log strategy should be created"
        return strategy
