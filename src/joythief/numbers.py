import math
import typing as tp


class NaN:

    def __eq__(self, other: tp.Any) -> bool:
        if not isinstance(other, (tp.SupportsFloat, tp.SupportsIndex)):
            return NotImplemented
        return math.isnan(other)

    def __repr__(self) -> str:
        return "nan"
