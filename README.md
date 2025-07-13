# JoyThief

Comparison is the thief of joy.

## Usage

JoyThief provides a collection of matchers which can be used for testing.

```python
from joythief.numbers import NaN


def test_my_func_with_no_arguments_returns_nan():
    assert my_func() == NaN()
```
