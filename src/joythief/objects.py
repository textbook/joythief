"""Matchers for general object types."""

import typing as tp

from joythief.core import Matcher

T = tp.TypeVar("T")

Type = tp.Union[type[T], tuple[type[T], ...]]


class InstanceOf(Matcher[T]):
    """Matches any instance of the specified type(s).

    This matcher compares the received value using
    :py:func:`isinstance`, so accepts either a single type or a tuple
    of types. With :code:`nullable` set to :py:const:`True`, the
    received value can also be :py:const:`None`.

    Originally formulated for `this answer`_.

    .. _this answer: https://stackoverflow.com/a/64973325/3001761

    """

    _nullable: bool
    _type: Type[T]

    def __init__(self, type_: Type[T], *, nullable: bool = False):
        self._nullable = nullable
        self._type = type_

    def __eq__(self, other: tp.Any) -> bool:
        type_: tuple[type[tp.Any], ...] = (
            self._type if isinstance(self._type, tuple) else (self._type,)
        )
        if self._nullable:
            type_ = type_ + (type(None),)
        return isinstance(other, type_)

    def __repr__(self) -> str:
        return (
            f"InstanceOf({self._type!r}"
            f"{', nullable=True' if self._nullable else ''})"
        )
