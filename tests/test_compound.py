import pytest

from joythief.compound import AllOf, AnyOf
from joythief.strings import JsonString, StringMatching


def test_allof_false_if_none_match():
    assert "foo" != AllOf(StringMatching(r"^{}$"), JsonString())


def test_allof_false_if_any_do_not_match():
    assert "foo" != AllOf(StringMatching(r"fo+"), JsonString())


def test_allof_true_if_all_match():
    assert "{}" == AllOf(StringMatching(r"^{}$"), JsonString())


def test_allof_repr_shows_matches():
    matcher = AllOf(JsonString(), StringMatching(r"fo+"))
    assert "foo" != matcher
    assert repr(matcher) == "AllOf(JsonString(), 'foo')"


def test_allof_requires_some_matchers():
    with pytest.raises(TypeError):
        _ = AllOf()


def test_allof_warns_on_single_matcher():
    with pytest.warns(UserWarning):
        _ = AllOf(JsonString())


def test_anyof_false_if_none_match():
    assert "foo" != AnyOf(StringMatching(r"^{}$"), JsonString())


def test_anyof_true_if_any_match():
    assert "foo" == AnyOf(StringMatching(r"fo+"), JsonString())


def test_anyof_true_if_all_match():
    assert "{}" == AnyOf(StringMatching(r"^{}$"), JsonString())


def test_anyof_requires_some_matchers():
    with pytest.raises(TypeError):
        _ = AnyOf()


def test_anyof_warns_on_single_matcher():
    with pytest.warns(UserWarning):
        _ = AnyOf(JsonString())
