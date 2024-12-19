import time
from collections.abc import Awaitable, Callable
from functools import partial

from fastapi import Request, Response

from app import contracts

NANOSECONDS_TO_MILLISECONDS_DIVIDER = 1e6
HEADER_NAME = "X-Process-Time-Milliseconds"


async def add_process_time_header(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    contracts.requires_not_null(request)
    contracts.requires_not_null(call_next)
    response, process_time = await measure_process_time(partial(call_next, request))
    return add_header_to_response(response, process_time)


async def measure_process_time[T](
    call_next: Callable[[], Awaitable[T]],
) -> tuple[T, float]:
    start_time = time.perf_counter_ns()
    op = await call_next()
    end_time = time.perf_counter_ns()
    return op, calculate_process_time(start_time, end_time)


def calculate_process_time(start_time: int, end_time: int) -> float:
    return (end_time - start_time) / NANOSECONDS_TO_MILLISECONDS_DIVIDER


def add_header_to_response(response: Response, process_time: float) -> Response:
    response.headers[HEADER_NAME] = f"{process_time:.3f}"
    return response
