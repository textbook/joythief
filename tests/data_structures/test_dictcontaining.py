import typing as tp
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping

import pytest

from joythief.core import Matcher
from joythief.data_structures import DictContaining
from joythief.objects import InstanceOf


@pytest.mark.parametrize(
    "factory",
    [
        pytest.param(lambda: DictContaining(), id="no args"),
        pytest.param(lambda: DictContaining({}), id="empty mapping"),
        pytest.param(lambda: DictContaining([]), id="empty sequence"),
    ],
)
def test_empty_rejects(factory: Callable[[], Matcher[tp.Any]]):
    with pytest.raises(ValueError) as exc_info:
        _ = factory()
    assert exc_info.match("matches any mapping")


@pytest.mark.parametrize(
    "mapping",
    [dict(foo=123), Counter(foo=123), defaultdict(int, foo=123)],
    ids=lambda v: type(v).__name__,
)
def test_equals_matching_mapping(mapping: Mapping[str, int]):
    matcher = DictContaining(foo=123)
    assert matcher == mapping
    assert repr(matcher) == repr(mapping)


@pytest.mark.parametrize(
    "mapping",
    [dict(foo=123), Counter(foo=123), defaultdict(int, foo=123)],
    ids=lambda v: type(v).__name__,
)
def test_does_not_equal_mismatched_keys(mapping: Mapping[str, int]):
    assert DictContaining(foo=456) != mapping


@pytest.mark.parametrize(
    "mapping",
    [dict(foo=123), Counter(foo=123), defaultdict(int, foo=123)],
    ids=lambda v: type(v).__name__,
)
def test_does_not_equal_missing_keys(mapping: Mapping[str, int]):
    assert DictContaining(foo=InstanceOf(int), bar=456) != mapping


def test_repr_shows_mapping():
    assert repr(DictContaining(foo=456)) == "DictContaining(**{'foo': 456})"


def test_expands_all_sub_matchers():
    matcher = DictContaining(foo=InstanceOf(str), bar=InstanceOf(str))
    assert matcher != dict(foo=123, bar="baz")
    assert (
        repr(matcher)
        == "DictContaining(**{'foo': InstanceOf(<class 'str'>), 'bar': 'baz'})"
    )


@pytest.mark.parametrize(
    "value",
    [123, "foo", False, None],
    ids=lambda v: type(v).__name__,
)
def test_does_not_equal_non_mapping(value: tp.Any):
    assert DictContaining(foo=123) != value


def test_isinstance_of_dict():
    """To get pytest to show common/differing items."""
    assert isinstance(DictContaining(foo=123), dict)


@pytest.mark.parametrize(
    "matcher",
    [
        pytest.param(DictContaining([("foo", InstanceOf(int))]), id="sequence only"),
        pytest.param(
            DictContaining([("foo", InstanceOf(int))], bar=InstanceOf(int)),
            id="sequence and keyword",
        ),
        pytest.param(DictContaining({"foo": InstanceOf(int)}), id="mapping only"),
        pytest.param(
            DictContaining({"foo": InstanceOf(int)}, bar=InstanceOf(int)),
            id="mapping and keyword",
        ),
        pytest.param(DictContaining(foo=InstanceOf(int)), id="keyword only"),
        pytest.param(
            DictContaining([], foo=InstanceOf(int)),
            id="empty sequence and keyword",
        ),
        pytest.param(
            DictContaining({}, foo=InstanceOf(int)),
            id="empty mapping and keyword",
        ),
    ],
)
def test_supports_dict_initialisation_patterns(matcher: Matcher[tp.Any]) -> None:
    assert dict(foo=123, bar=456) == matcher


def test_supports_explicitly_optional_keys():
    matcher = DictContaining(foo=DictContaining.optionally(123))
    assert dict(foo=123) == matcher
    assert repr(matcher) == "{'foo': 123}"
    assert dict() == matcher
    assert repr(matcher) == "DictContaining(**{'foo': DictContaining.optionally(123)})"
    assert dict(foo="bar") != matcher
