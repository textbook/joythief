from __future__ import annotations

import typing as tp
from abc import ABC, abstractmethod

if tp.TYPE_CHECKING:
    from typing_extensions import TypeAlias

T = tp.TypeVar("T")


class Matcher(tp.Generic[T], ABC):
    """Defines the core requirements for any matcher.

    - Must be comparable for equality with anything.
    - Must have a sensible representation.

    """

    @abstractmethod
    def __eq__(self, other: tp.Any) -> bool: ...

    @abstractmethod
    def __repr__(self) -> str: ...


MaybeMatcher: TypeAlias = tp.Union[T, Matcher[T]]
"""Either ``T`` or a matcher of ``T``."""
