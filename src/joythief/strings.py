import re
import typing as tp


class StringMatching:
    """Matches any :py:class:`str` instance matching a regular expression.

    :param pattern: Regex pattern to match, as a string or compiled pattern.

    :param flags: Any `flags`_ to compile a :py:class:`str` pattern with

    :raises ValueError: if flags are provided with a pre-compiled pattern.

    .. _flags: https://docs.python.org/3/library/re.html#flags

    """

    _pattern: re.Pattern[str]

    @tp.overload
    def __init__(self, pattern: re.Pattern[str]): ...

    @tp.overload
    def __init__(self, pattern: str, *, flags: int = 0): ...

    def __init__(
        self,
        pattern: tp.Union[str, re.Pattern[str]],
        *,
        flags: int = 0,
    ):
        self._pattern = re.compile(pattern, flags=flags)

    def __eq__(self, other: tp.Any) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        return self._pattern.match(other) is not None

    def __repr__(self) -> str:
        return f"StringMatching({self._pattern!r})"
