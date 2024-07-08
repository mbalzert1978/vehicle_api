import typing

from fastapi import Request, Response
from loguru import logger
from presentation.utils.utils import is_client_error, is_server_error, is_success


async def logging_middleware(
    request: Request,
    call_next: typing.Callable[[Request], typing.Awaitable[Response]],
) -> Response:
    client = request.client or None
    logger.info(f"[{client}]::{request.method}::{request.url.path}")
    response = await call_next(request)

    if is_success(response.status_code):
        logger.info(f"[{client}]::{request.method}::{request.url.path}::SUCCESS")
    elif is_client_error(response.status_code):
        logger.error(f"[{client}]::{request.method}::{request.url.path}::CLIENT_ERROR")
    elif is_server_error(response.status_code):
        logger.critical(f"[{client}]::{request.method}::{request.url.path}::SERVER_ERROR")

    return response
