import typing as tp

T = tp.TypeVar("T")

Type = tp.Union[type[T], tuple[type[T], ...]]


class InstanceOf(tp.Generic[T]):

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
