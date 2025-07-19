# JoyThief

[![CI](https://github.com/textbook/joythief/actions/workflows/push.yml/badge.svg)](https://github.com/textbook/joythief/actions/workflows/push.yml)
[![Docs](https://app.readthedocs.org/projects/joythief/badge/?version=latest)](https://joythief.readthedocs.io/en/latest/)
[![Coverage Status](https://coveralls.io/repos/github/textbook/joythief/badge.svg?branch=main)](https://coveralls.io/github/textbook/joythief?branch=main)

Comparison is the thief of joy.

## Usage

JoyThief provides a collection of matchers which can be used for testing.

```python
from joythief.numbers import NaN


def test_my_func_with_no_arguments_returns_nan():
    assert my_func() == NaN()
```
