import typing as tp

import pytest

type_only = pytest.mark.skipif(
    not tp.TYPE_CHECKING,
    reason="type-only tests that do nothing at runtime",
)
