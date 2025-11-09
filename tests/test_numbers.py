import math
import typing as tp

import pytest

from joythief.core import Matcher
from joythief.numbers import NaN


@pytest.fixture(
    params=[
        pytest.param(math.nan, id="math.nan"),
        pytest.param(float("nan"), id='float("nan")'),
    ]
)
def nan(request: pytest.FixtureRequest) -> float:
    return tp.cast(float, getattr(request, "param"))


def test_nan_equal_to_nan(nan: float):
    assert nan == NaN()


@pytest.mark.parametrize(
    "value",
    [
        123,
        1.23,
        13j,
        "foo",
    ],
    ids=lambda v: type(v).__name__,
)
def test_nan_not_equal_to_others(value: tp.Any):
    assert value != NaN()


def test_nan_repr_is_nan():
    assert repr(NaN()) == "NaN()"


def test_type_nan_allows_float() -> None:
    _: Matcher[float] = NaN()


def test_type_nan_allows_int() -> None:
    _: Matcher[float] = NaN()


def test_type_nan_does_not_allow_other() -> None:
    _: Matcher[str] = NaN()  # type: ignore[assignment]
