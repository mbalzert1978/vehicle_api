import http
import typing

from fastapi import Request, Response
from loguru import logger


async def logging_middleware(
    request: Request,
    call_next: typing.Callable[[Request], typing.Awaitable[Response]],
) -> Response:
    client = request.client or None
    logger.info(f"[{client}]::{request.method}::{request.url.path}")
    response = await call_next(request)

    status = http.HTTPStatus(int(response.status_code))
    if status.is_success:
        logger.info(f"[{client}]::{request.method}::{request.url.path}::SUCCESS")
    elif status.is_client_error:
        logger.error(f"[{client}]::{request.method}::{request.url.path}::CLIENT_ERROR")
    elif status.is_server_error:
        logger.critical(f"[{client}]::{request.method}::{request.url.path}::SERVER_ERROR")

    return response
