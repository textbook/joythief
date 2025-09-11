import pytest

from joythief.compound import All, Any
from joythief.strings import JsonString, StringMatching


def test_all_false_if_none_match():
    assert "foo" != All(StringMatching(r"^{}$"), JsonString())


def test_all_false_if_any_do_not_match():
    assert "foo" != All(StringMatching(r"fo+"), JsonString())


def test_all_true_if_all_match():
    assert "{}" == All(StringMatching(r"^{}$"), JsonString())


def test_all_repr_shows_matches():
    matcher = All(JsonString(), StringMatching(r"fo+"))
    assert "foo" != matcher
    assert repr(matcher) == "All(JsonString(), 'foo')"


def test_all_requires_some_matchers():
    with pytest.raises(TypeError):
        _ = All()


def test_all_warns_on_single_matcher():
    with pytest.warns(UserWarning):
        _ = All(JsonString())


def test_any_false_if_none_match():
    assert "foo" != Any(StringMatching(r"^{}$"), JsonString())


def test_any_true_if_any_match():
    assert "foo" == Any(StringMatching(r"fo+"), JsonString())


def test_any_true_if_all_match():
    assert "{}" == Any(StringMatching(r"^{}$"), JsonString())


def test_any_requires_some_matchers():
    with pytest.raises(TypeError):
        _ = Any()


def test_any_warns_on_single_matcher():
    with pytest.warns(UserWarning):
        _ = Any(JsonString())
