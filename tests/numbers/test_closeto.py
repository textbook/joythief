import typing as tp

import pytest

from joythief.core import Matcher
from joythief.numbers import CloseTo
from tests.marks import type_only


def test_closeto_equal_to_exact_value():
    assert 1.0 == CloseTo(1.0)


def test_closeto_equal_to_very_close_value():
    assert 1.0 + 1e-10 == CloseTo(1.0)


def test_closeto_not_equal_to_far_value():
    assert 1.1 != CloseTo(1.0)


def test_closeto_rel_tol_widens_match():
    assert 1.05 == CloseTo(1.0, rel_tol=0.1)


def test_closeto_rel_tol_narrows_match():
    assert 1.0 + 1e-10 != CloseTo(1.0, rel_tol=1e-12)


def test_closeto_rel_tol_alone_does_not_match_near_zero():
    assert 1e-10 != CloseTo(0.0)


def test_closeto_abs_tol_matches_near_zero():
    assert 1e-10 == CloseTo(0.0, abs_tol=1e-9)


@pytest.mark.parametrize(
    "value",
    ["1.0", {}, [], None, 1j],
    ids=lambda v: type(v).__name__,
)
def test_closeto_not_equal_to_non_numeric(value: tp.Any):
    assert value != CloseTo(1.0)


def test_closeto_equal_to_int():
    assert 1 == CloseTo(1.0)


@pytest.mark.parametrize(
    "kwargs",
    [{"rel_tol": -0.1}, {"abs_tol": -0.1}, {"rel_tol": -1e-12, "abs_tol": -1e-12}],
)
def test_closeto_rejects_negative_tolerances(kwargs: tp.Mapping[str, float]):
    with pytest.raises(ValueError, match="tolerances must be non-negative"):
        CloseTo(1.0, **kwargs)


@pytest.mark.parametrize("rel_tol", [1.0, 1.5, 100.0])
def test_closeto_rejects_rel_tol_at_or_above_one(rel_tol: float):
    with pytest.raises(ValueError, match="rel_tol must be less than 1.0"):
        CloseTo(1.0, rel_tol=rel_tol)


def test_closeto_default_repr():
    assert repr(CloseTo(1.0)) == "CloseTo(1.0)"


def test_closeto_repr_with_rel_tol():
    assert repr(CloseTo(1.0, rel_tol=0.01)) == "CloseTo(1.0, rel_tol=0.01)"


def test_closeto_repr_with_abs_tol():
    assert repr(CloseTo(1.0, abs_tol=0.1)) == "CloseTo(1.0, abs_tol=0.1)"


def test_closeto_repr_with_both_tols():
    assert (
        repr(CloseTo(1.0, rel_tol=0.01, abs_tol=0.1))
        == "CloseTo(1.0, rel_tol=0.01, abs_tol=0.1)"
    )


@type_only
def test_type_closeto_allows_float() -> None:
    _: Matcher[float] = CloseTo(1.0)


@type_only
def test_type_closeto_does_not_allow_other() -> None:
    _: Matcher[str] = CloseTo(1.0)  # type: ignore[assignment]
