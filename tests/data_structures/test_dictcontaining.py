import typing as tp
from collections import Counter, defaultdict
from collections.abc import Mapping

import pytest

from joythief.data_structures import DictContaining
from joythief.objects import InstanceOf


def test_empty_rejects():
    with pytest.raises(ValueError) as exc_info:
        _ = DictContaining()
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
