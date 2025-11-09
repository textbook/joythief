import typing as tp
from typing import Mapping

import pytest

from joythief.core import Matcher
from joythief.strings import StringMatching, UrlString


@pytest.mark.parametrize(
    "attributes",
    [
        pytest.param(dict(hostname="google.com"), id="hostname only"),
        pytest.param(dict(scheme="https"), id="scheme only"),
        pytest.param(dict(path="/search"), id="path only"),
        pytest.param(
            dict(hostname="google.com", path="/search"), id="hostname and path"
        ),
        pytest.param(
            dict(scheme="https", hostname="google.com"), id="scheme and hostname"
        ),
        pytest.param(dict(query=dict(q=["my search"])), id="query only"),
    ],
)
def test_urlstring_matches_url(attributes: Mapping[str, tp.Any]):
    assert UrlString(**attributes) == "https://google.com/search?q=my%20search"


def test_urlstring_tolerates_missing_query():
    assert UrlString(query=dict(foo=["bar"])) != "https://example.com"


def test_urlstring_retains_blank_query_params():
    assert UrlString(query=dict(foo=[""])) == "https://example.com?foo="


@pytest.mark.parametrize("non_str", [1.23, []], ids=lambda v: type(v).__name__)
def test_urlstring_does_not_match_non_str(non_str):
    assert UrlString(scheme="https", hostname="example.com") != non_str


def test_urlstring_requires_some_attributes():
    with pytest.raises(TypeError) as exc_info:
        UrlString()

    exc_info.match(r"^A UrlString with no arguments matches any string$")


def test_urlstring_accepts_string_matchers():
    matcher = UrlString(hostname=StringMatching(r"^google\."))
    assert matcher == "https://google.com"
    assert matcher == "https://google.co.uk"
    assert matcher != "https://example.com"


@pytest.mark.parametrize(
    "arguments, expected",
    [
        pytest.param(
            dict(hostname="example.com", scheme="https"),
            "UrlString(scheme='https', hostname='example.com')",
            id="scheme before hostname",
        ),
        pytest.param(
            dict(hostname="example.com", path="/some/path"),
            "UrlString(hostname='example.com', path='/some/path')",
            id="hostname before path",
        ),
        pytest.param(
            dict(query=dict(foo=["bar"]), path="/some/path"),
            "UrlString(path='/some/path', query={'foo': ['bar']})",
            id="path before query",
        ),
    ],
)
def test_urlstring_repr_shows_parameters_in_sensible_order(
    arguments: Mapping[str, tp.Any],
    expected: str,
):
    assert repr(UrlString(**arguments)) == expected


def test_type_urlstring_matches_str() -> None:
    _: Matcher[str] = UrlString(hostname="localhost:4200")


def test_type_urlstring_does_not_match_other() -> None:
    _: Matcher[int] = UrlString(scheme="https")  # type: ignore[assignment]
