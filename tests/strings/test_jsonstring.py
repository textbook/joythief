import json
import typing as tp

import pytest

from joythief.core import Matcher
from joythief.strings import JsonString


@pytest.mark.parametrize(
    "expected",
    [
        123,
        "foo",
        None,
        ["foo", "bar"],
        {"foo": "bar"},
    ],
    ids=lambda v: type(v).__name__,
)
def test_jsonstring_matches_content(expected):
    assert JsonString(expected) == json.dumps(expected)


def test_jsonstring_matches_any_content():
    assert JsonString() == "{}"


@pytest.mark.parametrize(
    "actual",
    [
        pytest.param(123, id="non-string"),
        pytest.param("foo.bar", id="non-JSON"),
    ],
)
def test_jsonstring_does_not_match_non_json(actual: tp.Any):
    assert JsonString(None) != actual


def test_jsonstring_repr_shows_expected():
    assert (
        repr(JsonString({"foo": ["bar", 123]})) == "JsonString({'foo': ['bar', 123]})"
    )
    assert repr(JsonString()) == "JsonString()"


def test_type_jsonstring_matches_str() -> None:
    _: Matcher[str] = JsonString()


def test_type_jsonstring_does_not_match_other() -> None:
    _: Matcher[int] = JsonString({})  # type: ignore[assignment]
