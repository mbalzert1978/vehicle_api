import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from asgi_correlation_id import correlation_id
from loguru import logger

# Constants
LOG_FORMAT: Final[str] = (
    "[{time}] [{correlation_id}] [{level}] - {name}:{function}:{line} :: {message}"
)
LOG_LEVEL: Final[str] = "INFO"
LOG_FILE_PATH: Final[str] = "logs/app.log"
LOG_ROTATION_SIZE: Final[str] = "30 MB"
LOG_RETENTION_PERIOD: Final[str] = "7 days"
UVICORN_ERROR_LOGGER: Final[str] = "uvicorn.error"
UVICORN_ACCESS_LOGGER: Final[str] = "uvicorn.access"


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    """Configuration for application logging."""

    format_string: str
    level: str
    log_file_path: Path
    rotation_size: str
    retention_period: str
    serialize_file: bool
    enable_uvicorn_logging: bool


class LoggingConfigFactory:
    """Factory for creating logging configuration instances."""

    @staticmethod
    def new() -> LoggingConfig:
        """Create a new logging configuration with default settings.

        Returns:
            A new LoggingConfig instance with default values.
        """
        log_file_path = Path(LOG_FILE_PATH)

        result = LoggingConfig(
            format_string=LOG_FORMAT,
            level=LOG_LEVEL,
            log_file_path=log_file_path,
            rotation_size=LOG_ROTATION_SIZE,
            retention_period=LOG_RETENTION_PERIOD,
            serialize_file=True,
            enable_uvicorn_logging=False,
        )

        assert isinstance(result, LoggingConfig), (
            "Result must be a LoggingConfig instance"
        )
        assert result.format_string.strip(), "Format string cannot be empty"
        assert result.level.strip(), "Log level cannot be empty"

        return result


class LoggingConfigurator:
    """Configurator for application logging setup."""

    @staticmethod
    def configure(config: LoggingConfig) -> None:
        """Configure application logging with the given configuration.

        Args:
            config: The logging configuration to apply.
        """
        assert isinstance(config, LoggingConfig), (
            "Config must be a LoggingConfig instance"
        )
        assert config.format_string.strip(), "Format string cannot be empty"
        assert config.level.strip(), "Log level cannot be empty"

        LoggingConfigurator._remove_default_handlers()
        LoggingConfigurator._disable_uvicorn_logging(config.enable_uvicorn_logging)
        LoggingConfigurator._add_console_handler(config)
        LoggingConfigurator._add_file_handler(config)

    @staticmethod
    def _remove_default_handlers() -> None:
        """Remove all default loguru handlers."""
        logger.remove()

    @staticmethod
    def _disable_uvicorn_logging(enable_uvicorn: bool) -> None:
        """Disable uvicorn loggers if requested.

        Args:
            enable_uvicorn: Whether to enable uvicorn logging.
        """
        assert isinstance(enable_uvicorn, bool), "Enable uvicorn must be a boolean"

        if enable_uvicorn:
            return
        logging.getLogger(UVICORN_ERROR_LOGGER).disabled = True
        logging.getLogger(UVICORN_ACCESS_LOGGER).disabled = True

    @staticmethod
    def _add_console_handler(config: LoggingConfig) -> None:
        """Add console logging handler.

        Args:
            config: The logging configuration to use.
        """
        assert isinstance(config, LoggingConfig), (
            "Config must be a LoggingConfig instance"
        )

        logger.add(
            sys.stdout,
            format=config.format_string,
            level=config.level,
            filter=_correlation_id_filter,
        )

    @staticmethod
    def _add_file_handler(config: LoggingConfig) -> None:
        """Add file logging handler.

        Args:
            config: The logging configuration to use.
        """
        assert isinstance(config, LoggingConfig), (
            "Config must be a LoggingConfig instance"
        )
        assert isinstance(config.log_file_path, Path), (
            "Log file path must be a Path instance"
        )

        # Ensure log directory exists
        config.log_file_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            str(config.log_file_path),
            serialize=config.serialize_file,
            level=config.level,
            filter=_correlation_id_filter,
            rotation=config.rotation_size,
            retention=config.retention_period,
        )


def _correlation_id_filter(record: dict[str, Any]) -> bool:
    """Add correlation ID to log record.

    Args:
        record: The log record to modify.

    Returns:
        Always True to include the record in logging.
    """
    assert isinstance(record, dict), "Record must be a dictionary"

    current_correlation_id = correlation_id.get()
    record["correlation_id"] = current_correlation_id

    assert "correlation_id" in record, "Correlation ID must be added to record"

    return True


def configure_logging() -> None:
    """Configure application logging with default settings."""
    config = LoggingConfigFactory.new()
    LoggingConfigurator.configure(config)

    assert config is not None, "Configuration must be created"
