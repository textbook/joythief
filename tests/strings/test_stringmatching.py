import re
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from joythief.strings import StringMatching


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
    "value",
    [
        pytest.param(str(uuid4()).lower(), id="lowercase"),
        pytest.param(str(uuid4()).upper(), id="uppercase"),
    ],
)
def test_stringmatching_uuid_preset_matches_uuid(value):
    matcher = StringMatching.uuid()
    assert matcher == value
    assert repr(matcher) == repr(value)


@pytest.mark.parametrize(
    "value",
    [
        "foo.bar",
        pytest.param(f"foo {uuid4()} bar", id="string containing UUID"),
        123,
        datetime.now(),
    ],
    ids=lambda v: type(v).__name__,
)
def test_stringmatching_uuid_preset_does_not_match_non_uuid(value):
    assert StringMatching.uuid() != value


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(datetime.now().isoformat(), id="isoformat"),
        pytest.param(datetime.now(tz=timezone.utc).isoformat(), id="isoformat UTC"),
        pytest.param(str(datetime.now()), id="str"),
        pytest.param(str(datetime.now(tz=timezone.utc)), id="str UTC"),
        pytest.param(
            datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z"),
            id="isoformat Zulu",
        ),
    ],
)
def test_stringmatching_iso8601_preset_matches_timestamp(value):
    matcher = StringMatching.iso8601()
    assert matcher == value
    assert repr(matcher) == repr(value)


@pytest.mark.parametrize(
    "value",
    [
        pytest.param(
            f"foo {datetime.now().isoformat()} bar",
            id="string containing isoformat",
        ),
        "foo.bar",
        [],
    ],
    ids=lambda v: type(v).__name__,
)
def test_stringmatching_iso8601_preset_does_not_match_non_timestamp(value):
    assert StringMatching.iso8601() != value
