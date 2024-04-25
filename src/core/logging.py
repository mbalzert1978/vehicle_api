import logging
import sys

from asgi_correlation_id import correlation_id
from loguru import logger


def _correlation_id_filter(record) -> bool:
    record |= {"correlation_id": correlation_id.get()}
    return True


def configure_logging() -> None:
    logger.remove()
    logging.getLogger("uvicorn.error").disabled = True
    logging.getLogger("uvicorn.access").disabled = True
    fmt = "[{time}] [{correlation_id}] [{level}] - {name}:{function}:{line} :: {message}"
    logger.add(sys.stdout, format=fmt, level="INFO", filter=_correlation_id_filter)  # type:ignore[arg-type]
    logger.add(
        "logs/app.log",
        serialize=True,
        level="INFO",
        filter=_correlation_id_filter,  # type:ignore[arg-type]
        rotation="30 MB",
        retention="7 days",
    )
