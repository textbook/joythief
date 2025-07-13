import math
import typing as tp

import pytest

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
        "foo",
        float(),
    ],
)
def test_nan_not_equal_to_others(value: tp.Any):
    assert value != NaN()


def test_nan_repr_is_nan():
    assert repr(NaN()) == "nan"
