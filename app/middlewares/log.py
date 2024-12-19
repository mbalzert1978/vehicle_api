from collections.abc import Awaitable, Callable
from http import HTTPStatus

from fastapi import Request, Response
from loguru import logger


async def logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    log_request(request)
    response = await call_next(request)
    log_response(request, response)
    return response


def log_request(request: Request) -> None:
    logger.info(create_log_message(request))


def log_response(request: Request, response: Response) -> None:
    log_function, status_message = get_log_strategy(response.status_code)
    log_function(f"{create_log_message(request)}::{status_message}")


def create_log_message(request: Request) -> str:
    return (
        f"[{request.client or "NoAddress"}]::[{request.method}]::[{request.url.path}]"
        if isinstance(request, Request)
        else ""
    )


def get_log_strategy(status_code: int) -> tuple[Callable, str]:
    match status_code:
        case _ if HTTPStatus.CONTINUE <= status_code < HTTPStatus.SWITCHING_PROTOCOLS:
            return logger.info, "INFORMATIONAL"
        case _ if HTTPStatus.OK <= status_code < HTTPStatus.MULTIPLE_CHOICES:
            return logger.info, "SUCCESS"
        case _ if HTTPStatus.MULTIPLE_CHOICES <= status_code < HTTPStatus.BAD_REQUEST:
            return logger.info, "REDIRECTION"
        case (
            _
        ) if HTTPStatus.BAD_REQUEST <= status_code < HTTPStatus.INTERNAL_SERVER_ERROR:
            return logger.error, "CLIENT_ERROR"
        case _ if HTTPStatus.INTERNAL_SERVER_ERROR <= status_code < 600:
            return logger.critical, "SERVER_ERROR"
        case _:
            return logger.warning, f"UNKNOWN STATUS CODE: {status_code}"
