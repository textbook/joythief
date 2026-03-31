import pytest

from joythief import Matcher
from joythief.strings import StringContaining
from tests.marks import type_only


@pytest.mark.parametrize("foo", ["foo", "foobar", "bazfoo", "quxfooooooo"])
def test_stringcontaining_equal_to_string_containing_substring(foo):
    assert StringContaining("foo") == foo


@pytest.mark.parametrize("not_foo", ["fo", "bar"])
def test_containing_not_equal_to_string_not_containing_substring(not_foo):
    assert StringContaining("foo") != not_foo


@pytest.mark.parametrize("not_str", [123, {}], ids=lambda v: type(v).__name__)
def test_containing_not_equal_to_non_string(not_str):
    assert StringContaining("fo{2,}") != not_str


def test_stringcontaining_repr():
    assert repr(StringContaining("foo")) == "StringContaining('foo')"


@type_only
def test_type_stringmatching_matches_str() -> None:
    _: Matcher[str] = StringContaining("foo")


@type_only
def test_type_stringmatching_does_not_match_other() -> None:
    _: Matcher[int] = StringContaining("foo")  # type: ignore[assignment]
