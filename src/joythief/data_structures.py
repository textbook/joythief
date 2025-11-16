import itertools
import typing as tp
from collections.abc import Hashable, Iterable, Iterator, Mapping

from .core import Matcher, MaybeMatcher
from .objects import Nothing

T = tp.TypeVar("T")


class DictContaining(Matcher[Mapping[Hashable, tp.Any]], dict[Hashable, tp.Any]):
    """Match the specified keys in a mapping, ignoring any extra keys.

    :param content: mapping or iterable of key-value pairs to include in the
        comparison

    :param \\**kwargs: additional key-value pairs to include in the comparison

    :raises ValueError: if no keys are specified (use
        :py:class:`~joythief.objects.InstanceOf` with :py:class:`dict` instead).

    .. versionadded:: 0.7.0

    .. versionchanged:: 0.8.0 added :py:meth:`optionally`.

    .. code-block:: python

        assert (
            actual
            == DictContaining([("foo", 123), ("bar", 456)], baz=InstanceOf(int))
        )

    **Note**: this subclasses :py:class:`dict` so that ``pytest`` will show the
    common and differing items. After a single comparison with a mapping, any
    keys that exist in the mapping but that are *not* specified in the matcher
    will appear to be in the matcher, with the same value. For example:

    .. code-block:: python

        >       assert DictContaining(foo=123, bar=0, baz=789) == dict(foo=123, bar=456, qux=999)
        E       AssertionError: assert DictContainin..., 'baz': 789}) == {'bar': 456, ...3, 'qux': 999}
        E
        E         Omitting 2 identical items, use -vv to show
        E         Differing items:
        E         {'bar': 0} != {'bar': 456}
        E         Left contains 1 more item:
        E         {'baz': 789}
        E         Use -v to get more diff

    """

    @tp.overload
    def __init__(self, /, **kwargs: tp.Any) -> None: ...

    @tp.overload
    def __init__(
        self, content: Mapping[Hashable, tp.Any], /, **kwargs: tp.Any
    ) -> None: ...

    @tp.overload
    def __init__(
        self, content: Iterable[tuple[Hashable, tp.Any]], /, **kwargs: tp.Any
    ) -> None: ...

    def __init__(self, content: tp.Any = None, /, **kwargs: tp.Any) -> None:
        if not content and not kwargs:
            raise ValueError("an empty DictContaining matches any mapping")
        args: tuple[tp.Any, ...] = () if content is None else (content,)
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: Hashable) -> tp.Any:
        try:
            return super().__getitem__(key)
        except KeyError as exc:
            if self._compared_to_mapping:
                return self._compared_to[key]
            raise exc

    def __iter__(self) -> Iterator[Hashable]:
        own_keys = super().__iter__()
        if self._compared_to_mapping:
            return itertools.chain(
                own_keys,
                (k for k in self._compared_to if k not in self),
            )
        return own_keys

    def compare(self, other: tp.Any) -> bool:
        if not isinstance(other, Mapping):
            return self.not_implemented
        is_equal: bool = True
        for key, value in self.items():
            if key in other:
                if self[key] != other[key]:
                    is_equal = False
            elif isinstance(value, _OptionalKey):
                _ = value == Nothing()
            else:
                is_equal = False
        return is_equal

    def represent(self) -> str:
        return f"DictContaining(**{dict.__repr__(self)})"

    @staticmethod
    def optionally(value: MaybeMatcher[T]) -> MaybeMatcher[T]:
        """Matcher factory for keys that may not be present.

        .. code-block:: python

            assert (
                actual
                == DictContaining(foo=DictContaining.optionally(123))
            )

        **Note**: this allows keys to be missing entirely, but matches the
        value strictly. For the equivalent of :py:class:`typing.Optional`, use
        :py:class:`~joythief.objects.Nullable`. These can be combined
        if required, e.g. to allow the key ``"foo"`` to be either: missing;
        present with the value ``123``; or present with the value ``None``, use:

        .. code-block:: python

            assert (
                actual
                == DictContaining(foo=DictContaining.optionally(Nullable(123)))
            )

        """
        return _OptionalKey(value)

    @property
    def _compared_to_mapping(self) -> bool:
        return self._compared_once and isinstance(self._compared_to, Mapping)


class _OptionalKey(Matcher[T]):

    _value: MaybeMatcher[T]

    def __init__(self, value: MaybeMatcher[T], /):
        super().__init__()
        self._value = value

    def compare(self, other: tp.Any) -> bool:
        return tp.cast(bool, self._value == other)

    def represent(self) -> str:
        return f"DictContaining.optionally({self._value!r})"
