from unittest.mock import AsyncMock

import pytest
from fastapi import Response

from app.middlewares.time import (
    HEADER_NAME,
    add_header_to_response,
    calculate_process_time,
    measure_process_time,
)


@pytest.mark.asyncio()
async def test_measure_process_time_when_called_with_async_function_should_return_result_and_time():
    """
    Given: An asynchronous function mock that returns a result
    When: measure_process_time is called with an asynchronous function mock
    Then: The result should be returned and the process time should be calculated
    """
    mock_result = "test_result"
    mock_function = AsyncMock(return_value=mock_result)

    result, process_time = await measure_process_time(mock_function)

    assert result == mock_result
    assert isinstance(process_time, float)
    assert process_time > 0


@pytest.mark.parametrize(
    "start_time, end_time, expected_time",
    [
        (0, int(1e9), 1000.0),  # 1 second
        (0, int(1e6), 1.0),  # 1 millisecond
        (int(1e9), int(2e9), 1000.0),  # 1 second difference
    ],
    ids=[
        "test_calculate_process_time_when_given_one_second_difference_should_return_1000_milliseconds",
        "test_calculate_process_time_when_given_one_millisecond_difference_should_return_1_millisecond",
        "test_calculate_process_time_when_given_one_second_difference_with_offset_should_return_1000_milliseconds",
    ],
)
def test_calculate_process_time_when_given_start_and_end_times_should_return_correct_duration(
    start_time, end_time, expected_time
):
    result = calculate_process_time(start_time, end_time)
    assert result == expected_time


@pytest.mark.parametrize(
    "process_time, expected_header_value",
    [
        (1000.0, "1000.000"),
        (1.0, "1.000"),
        (0.001, "0.001"),
    ],
    ids=[
        "test_add_header_to_response_when_given_1000_milliseconds_should_add_header_with_1000_000",
        "test_add_header_to_response_when_given_1_millisecond_should_add_header_with_1_000",
        "test_add_header_to_response_when_given_0_001_milliseconds_should_add_header_with_0_001",
    ],
)
def test_add_header_to_response_when_given_process_time_should_add_correct_header(
    process_time, expected_header_value
):
    response = Response()
    result = add_header_to_response(response, process_time)

    assert result == response
    assert HEADER_NAME in result.headers
    assert result.headers[HEADER_NAME] == expected_header_value
