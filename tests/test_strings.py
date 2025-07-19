import re
import typing as tp
from collections.abc import Mapping

import pytest

from joythief.strings import StringMatching, UrlString


@pytest.mark.parametrize("foo", ["foo", "fooo", "foooo", "fooooooo"])
def test_stringmatching_equal_to_string_matching_pattern(foo):
    assert StringMatching("fo{2,}") == foo


@pytest.mark.parametrize("not_foo", ["fo", "bar"])
def test_stringmatching_not_equal_to_string_not_matching_pattern(not_foo):
    assert StringMatching("fo{2,}") != not_foo


@pytest.mark.parametrize("not_str", [123, {}], ids=lambda v: type(v).__name__)
def test_stringmatching_not_equal_to_non_string(not_str):
    assert StringMatching("fo{2,}") != not_str


@pytest.mark.parametrize("foo", ["FOO", "FoO", "fOo"])
def test_stringmatching_accepts_regex_flags(foo):
    assert StringMatching("fo{2,}", flags=re.IGNORECASE) == foo


def test_stringmatching_accepts_compiled_pattern():
    pattern = re.compile("fo{2,}", flags=re.IGNORECASE)
    assert StringMatching(pattern) == "FOO"
    with pytest.raises(ValueError):
        StringMatching(pattern, flags=re.I | re.X)  # type: ignore[call-overload]


def test_stringmatching_repr():
    assert (
        repr(StringMatching("fo{2,}", flags=re.X))
        == "StringMatching(re.compile('fo{2,}', re.VERBOSE))"
    )


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
