import typing as tp
from datetime import date, datetime

import pytest

from joythief import Matcher
from joythief.objects import Anything, InstanceOf


class NewType:
    pass


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("foo"),
        pytest.param(123),
        pytest.param([]),
        pytest.param({}),
    ],
    ids=lambda v: type(v).__name__,
)
def test_instanceof_single_type_value_matches_type(value: tp.Any):
    assert value == InstanceOf(type(value))
    assert value != InstanceOf(NewType)


def test_instanceof_single_type_repr():
    assert (
        repr(InstanceOf(NewType)) == "InstanceOf(<class 'tests.test_objects.NewType'>)"
    )


def test_instanceof_single_type_handles_inheritance():
    assert datetime.now() == InstanceOf(date)
    assert date.today() != InstanceOf(datetime)


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(3j),
        pytest.param(2.34),
        pytest.param(123),
    ],
    ids=lambda v: type(v).__name__,
)
def test_instanceof_multiple_types_matches_any(value: tp.Any):
    assert value == InstanceOf((complex, float, int))


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("foo"),
        pytest.param([]),
        pytest.param({}),
    ],
    ids=lambda v: type(v).__name__,
)
def test_instanceof_multiple_types_does_not_match_other(value: tp.Any):
    assert value != InstanceOf((complex, float, int))


def test_instanceof_multiple_types_repr():
    assert (
        repr(InstanceOf((complex, float, int)))
        == "InstanceOf((<class 'complex'>, <class 'float'>, <class 'int'>))"
    )


@pytest.mark.parametrize(
    "type_, value",
    [
        pytest.param(str, "foo", id="single"),
        pytest.param((list, tuple), [], id="multiple"),
    ],
)
def test_instanceof_nullable_allows_none(type_: type[tp.Any], value: tp.Any):
    assert value == InstanceOf(type_, nullable=True)
    assert None == InstanceOf(type_, nullable=True)


def test_instanceof_nullable_repr():
    assert (
        repr(InstanceOf(int, nullable=True))
        == "InstanceOf(<class 'int'>, nullable=True)"
    )


@pytest.mark.parametrize(
    "value",
    [
        123,
        [],
        4.56,
        {},
        date.today(),
    ],
    ids=lambda v: type(v).__name__,
)
def test_any_matches_anything(value):
    matcher: Matcher[tp.Any] = Anything()
    assert matcher == value
    assert repr(matcher) == repr(value)


def test_any_default_repr():
    assert repr(Anything()) == "Anything()"
