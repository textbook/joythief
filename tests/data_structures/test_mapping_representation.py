from collections import Counter, defaultdict
from collections.abc import Mapping

import pytest

from joythief.data_structures import DictContaining


@pytest.mark.xfail
@pytest.mark.parametrize(
    "mapping",
    [
        defaultdict(int, foo=123, bar=0, baz=789),
        Counter(foo=123, bar=0, baz=789),
        dict(foo=123, bar=0, baz=789),
        DictContaining(foo=123, bar=0, baz=789),
    ],
    ids=lambda v: type(v).__name__,
)
def test_mapping_representation(mapping: Mapping[str, int]) -> None:
    assert mapping == dict(foo=123, bar=456, qux=999)
