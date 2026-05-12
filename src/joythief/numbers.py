"""Matchers for `numeric types`_ (e.g. :py:class:`float`).

.. _numeric types: https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex

"""

import math
import typing as tp

from joythief.core import Matcher


class CloseTo(Matcher[float]):
    """Matches any numeric value approximately equal to an expected value.

    Comparison is delegated to :py:func:`math.isclose`, so the same
    `tolerance semantics`_ apply: the relative tolerance is the maximum
    allowed difference relative to the larger absolute value of the inputs,
    and the absolute tolerance is the minimum allowed difference - useful
    when comparing values near zero.

    :param expected: the value to compare against.
    :param rel_tol: relative tolerance, defaulting to ``1e-09``. Must be
      less than ``1.0``.
    :param abs_tol: absolute tolerance, defaulting to ``0.0``.

    :raises ValueError: if either tolerance is negative, or ``rel_tol`` is
      not less than ``1.0``.

    .. _tolerance semantics: https://docs.python.org/3/library/math.html#math.isclose

    """

    _expected: float
    _rel_tol: tp.Optional[float]
    _abs_tol: tp.Optional[float]

    def __init__(
        self,
        expected: float,
        *,
        rel_tol: tp.Optional[float] = None,
        abs_tol: tp.Optional[float] = None,
    ):
        super().__init__()
        if (rel_tol is not None and rel_tol < 0) or (
            abs_tol is not None and abs_tol < 0
        ):
            raise ValueError("tolerances must be non-negative")
        if rel_tol is not None and rel_tol >= 1.0:
            raise ValueError("rel_tol must be less than 1.0")
        self._expected = expected
        self._rel_tol = rel_tol
        self._abs_tol = abs_tol

    def compare(self, other: tp.Any) -> bool:
        if not isinstance(other, (int, float)):
            return self.not_implemented
        return math.isclose(
            other,
            self._expected,
            rel_tol=1e-09 if self._rel_tol is None else self._rel_tol,
            abs_tol=0.0 if self._abs_tol is None else self._abs_tol,
        )

    def represent(self) -> str:
        parameters = [repr(self._expected)]
        if self._rel_tol is not None:
            parameters.append(f"rel_tol={self._rel_tol!r}")
        if self._abs_tol is not None:
            parameters.append(f"abs_tol={self._abs_tol!r}")
        return f"CloseTo({', '.join(parameters)})"


class NaN(Matcher[float]):
    """Matches any :py:class:`float` instance representing NaN.

    `IEEE 754`_ NaN (*"not a number"*) instances are, by definition, not
    equal to each other. This matcher compares equal to e.g.
    :py:data:`math.nan` or :code:`float("nan")` using
    :py:func:`math.isnan`.

    Originally formulated for `this answer`_.

    .. _IEEE 754: https://en.wikipedia.org/wiki/IEEE_754
    .. _this answer: https://stackoverflow.com/a/79699116/3001761

    """

    def compare(self, other: tp.Any) -> bool:
        if not isinstance(other, float):
            return self.not_implemented
        return math.isnan(other)

    def represent(self) -> str:
        return super().represent()
