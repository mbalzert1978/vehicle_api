import pytest

from app import contracts
from app.contracts import (
    ArgumentNull,
    ArgumentNullOrEmpty,
    ArgumentNullOrWhiteSpace,
    ArgumentTypeMismatch,
)


def test_requires_not_null_when_given_none_should_raise_argument_null():
    with pytest.raises(ArgumentNull, match="Argument cannot be None."):
        contracts.requires_not_null(None)


def test_requires_not_null_when_given_non_none_value_should_not_raise_exception():
    contracts.requires_not_null("Not None")
    contracts.requires_not_null(42)
    contracts.requires_not_null([])


@pytest.mark.parametrize(
    "value, exception, message",
    [
        (None, ArgumentNull, "Argument cannot be None."),
        ("", ArgumentNullOrEmpty, "Argument cannot be empty."),
        ("   ", ArgumentNullOrWhiteSpace, "Argument cannot be null or whitespace."),
        ([], ArgumentNullOrEmpty, "Argument cannot be empty."),
        ({}, ArgumentNullOrEmpty, "Argument cannot be empty."),
    ],
    ids=[
        "test_requires_not_null_not_empty_when_given_none_should_raise_argument_null",
        "test_requires_not_null_not_empty_when_given_empty_string_should_raise_argument_null_or_empty",
        "test_requires_not_null_not_empty_when_given_whitespace_string_should_raise_argument_null_or_whitespace",
        "test_requires_not_null_not_empty_when_given_empty_list_should_raise_argument_null_or_empty",
        "test_requires_not_null_not_empty_when_given_empty_dict_should_raise_argument_null_or_empty",
    ],
)
def test_requires_not_null_not_empty_when_given_invalid_input_should_raise_appropriate_exception(
    value, exception, message
):
    with pytest.raises(exception, match=message):
        contracts.requires_not_null_not_empty(value)


def test_requires_not_null_not_empty_when_given_valid_input_should_not_raise_exception():
    contracts.requires_not_null_not_empty("Not empty")
    contracts.requires_not_null_not_empty([1, 2, 3])
    contracts.requires_not_null_not_empty({"key": "value"})


@pytest.mark.parametrize(
    "value, expected_type",
    [
        ("string", str),
        (42, int),
        (3.14, float),
        ([], list),
        ({}, dict),
    ],
    ids=[
        "test_requires_type_when_given_string_and_str_type_should_not_raise_exception",
        "test_requires_type_when_given_integer_and_int_type_should_not_raise_exception",
        "test_requires_type_when_given_float_and_float_type_should_not_raise_exception",
        "test_requires_type_when_given_list_and_list_type_should_not_raise_exception",
        "test_requires_type_when_given_dict_and_dict_type_should_not_raise_exception",
    ],
)
def test_requires_type_when_given_matching_type_should_not_raise_exception(
    value, expected_type
):
    contracts.requires_type(value, expected_type)


@pytest.mark.parametrize(
    "value, expected_type, error_message",
    [
        ("string", int, "Expected argument of type int, got str."),
        (42, str, "Expected argument of type str, got int."),
        (3.14, list, "Expected argument of type list, got float."),
    ],
    ids=[
        "test_requires_type_when_given_string_for_int_type_should_raise_argument_type_mismatch",
        "test_requires_type_when_given_int_for_str_type_should_raise_argument_type_mismatch",
        "test_requires_type_when_given_float_for_list_type_should_raise_argument_type_mismatch",
    ],
)
def test_requires_type_when_given_mismatched_type_should_raise_argument_type_mismatch(
    value, expected_type, error_message
):
    with pytest.raises(ArgumentTypeMismatch, match=error_message):
        contracts.requires_type(value, expected_type)
