import time
from collections.abc import Awaitable, Callable
from functools import partial
from typing import Final

from fastapi import Request, Response

NANOSECONDS_TO_MILLISECONDS_DIVIDER: Final[float] = 1_000_000.0
HEADER_NAME: Final[str] = "X-Process-Time-Milliseconds"
DECIMAL_PLACES_PRECISION: Final[int] = 3


async def add_process_time_header(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Add process time header to HTTP response.

    Args:
        request: The incoming HTTP request.
        call_next: The next middleware or route handler.

    Returns:
        The HTTP response with added process time header.
    """
    assert isinstance(request, Request), "Request must be an instance of Request"
    assert call_next is not None, "Call next cannot be None"

    response, process_time = await measure_process_time(partial(call_next, request))
    result = add_header_to_response(response, process_time)

    assert isinstance(result, Response), "Result must be an instance of Response"
    assert HEADER_NAME in result.headers, "Process time header must be present"

    return result


async def measure_process_time[T](
    call_next: Callable[[], Awaitable[T]],
) -> tuple[T, float]:
    """Measure the execution time of an async operation.

    Args:
        call_next: The async operation to measure.

    Returns:
        A tuple containing the operation result and execution time in milliseconds.
    """
    assert call_next is not None, "Call next cannot be None"

    start_time = time.perf_counter_ns()
    assert isinstance(start_time, int), "Start time must be an integer"

    operation_result = await call_next()

    end_time = time.perf_counter_ns()
    assert isinstance(end_time, int), "End time must be an integer"
    assert end_time >= start_time, (
        "End time must be greater than or equal to start time"
    )

    process_time = calculate_process_time(start_time, end_time)

    assert isinstance(process_time, float), "Process time must be a float"
    assert process_time >= 0, "Process time must be non-negative"

    return operation_result, process_time


def calculate_process_time(start_time: int, end_time: int) -> float:
    """Calculate process time in milliseconds from nanosecond timestamps.

    Args:
        start_time: Start timestamp in nanoseconds.
        end_time: End timestamp in nanoseconds.

    Returns:
        Process time in milliseconds.
    """
    assert isinstance(start_time, int), "Start time must be an integer"
    assert isinstance(end_time, int), "End time must be an integer"
    assert end_time >= start_time, (
        "End time must be greater than or equal to start time"
    )

    time_difference = end_time - start_time
    process_time = time_difference / NANOSECONDS_TO_MILLISECONDS_DIVIDER

    assert isinstance(process_time, float), "Process time must be a float"
    assert process_time >= 0, "Process time must be non-negative"

    return process_time


def add_header_to_response(response: Response, process_time: float) -> Response:
    """Add process time header to HTTP response.

    Args:
        response: The HTTP response to modify.
        process_time: Process time in milliseconds.

    Returns:
        The modified HTTP response with process time header.
    """
    assert isinstance(response, Response), "Response must be an instance of Response"
    assert isinstance(process_time, float), "Process time must be a float"
    assert process_time >= 0, "Process time must be non-negative"

    response.headers[HEADER_NAME] = f"{process_time:.{DECIMAL_PLACES_PRECISION}f}"

    assert HEADER_NAME in response.headers, "Process time header must be present"

    return response
