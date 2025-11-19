from collections.abc import Awaitable, Callable
from typing import Final

from fastapi import Request, Response
from loguru import logger

from app.middlewares.LogStrategy import LogStrategyFactory

DEFAULT_CLIENT_ADDRESS: Final[str] = "NoAddress"
LOG_MESSAGE_SEPARATOR: Final[str] = "::"


async def logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Middleware for logging HTTP requests and responses.

    Args:
        request: The incoming HTTP request.
        call_next: The next middleware or route handler.

    Returns:
        The HTTP response from the next handler.
    """
    assert isinstance(request, Request), "Request must be an instance of Request"
    assert call_next is not None, "Call next cannot be None"

    log_request(request)
    response = await call_next(request)
    log_response(request, response)

    assert isinstance(response, Response), "Response must be an instance of Response"
    return response


def log_request(request: Request) -> None:
    """Log an incoming HTTP request.

    Args:
        request: The HTTP request to log.
    """
    assert isinstance(request, Request), "Request must be an instance of Request"

    message = create_log_message(request)
    logger.info(message)


def log_response(request: Request, response: Response) -> None:
    """Log an HTTP response with appropriate log level based on status code.

    Args:
        request: The original HTTP request.
        response: The HTTP response to log.
    """
    assert isinstance(request, Request), "Request must be an instance of Request"
    assert isinstance(response, Response), "Response must be an instance of Response"

    strategy = LogStrategyFactory.new(response.status_code)
    base_message = create_log_message(request)
    full_message = f"{base_message}{LOG_MESSAGE_SEPARATOR}{strategy.status_message}"

    strategy.log_function(full_message)


def create_log_message(request: Request) -> str:
    """Create a formatted log message from an HTTP request.

    Args:
        request: The HTTP request to create a log message for.

    Returns:
        A formatted log message string.
    """
    assert isinstance(request, Request), "Request must be an instance of Request"

    client_address = request.client.host if request.client else DEFAULT_CLIENT_ADDRESS
    message = (
        f"[{client_address}]{LOG_MESSAGE_SEPARATOR}"
        f"[{request.method}]{LOG_MESSAGE_SEPARATOR}"
        f"[{request.url.path}]"
    )

    assert isinstance(message, str), "Message must be a string"
    assert message.strip(), "Message cannot be empty or whitespace"

    return message
