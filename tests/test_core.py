import typing as tp

import pytest

from joythief.core import Matcher, MaybeMatcher
from joythief.objects import InstanceOf
from joythief.strings import StringMatching
from tests.marks import type_only


class EqMatcher(Matcher[int]):

    _expected: int

    def __init__(self, expected: int) -> None:
        super().__init__()
        self._expected = expected

    def compare(self, other: tp.Any) -> bool:
        if not isinstance(other, int):
            return self.not_implemented
        return other == self._expected

    def represent(self) -> str:
        return f"EqMatcher({self._expected!r})"


def test_core_matcher_uses_default_repr_before_comparison():
    assert repr(EqMatcher(123)) == "EqMatcher(123)"


def test_core_matcher_uses_compared_value_after_equal_comparison():
    matcher = EqMatcher(123)
    assert matcher == 123
    assert repr(matcher) == "123"


def test_core_matcher_uses_default_repr_after_unequal_comparison():
    matcher = EqMatcher(123)
    assert matcher != 456
    assert repr(matcher) == "EqMatcher(123)"


def test_core_matcher_uses_compared_value_after_comparison_to_same_value():
    matcher = EqMatcher(123)
    assert matcher == 123
    assert matcher == 123
    assert matcher == 123
    assert repr(matcher) == "123"


def test_core_matcher_uses_default_repr_after_comparison_to_other_value():
    matcher = EqMatcher(123)
    assert matcher == 123
    assert matcher != 456
    assert matcher != 789
    assert repr(matcher) == "EqMatcher(123)"


def test_core_matcher_uses_default_matcher_after_notimplemented_comparison():
    matcher = EqMatcher(123)
    assert matcher == 123
    assert matcher != "foo"
    assert repr(matcher) == "EqMatcher(123)"


def test_core_matcher_permits_not_implemented(recwarn: pytest.WarningsRecorder):
    assert EqMatcher(123) != "str"
    assert len(recwarn.list) == 0


@type_only
def test_type_maybematcher_accepts_matcher() -> None:
    _: MaybeMatcher[str] = InstanceOf(str)


@type_only
def test_type_maybematcher_accepts_value() -> None:
    _: MaybeMatcher[str] = "some string"


@type_only
def test_type_maybematcher_does_not_accept_other_matcher() -> None:
    _: MaybeMatcher[int] = StringMatching.uuid()  # type: ignore[assignment]


@type_only
def test_type_maybematcher_does_not_accept_other_value() -> None:
    _: MaybeMatcher[str] = 123  # type: ignore[assignment]
