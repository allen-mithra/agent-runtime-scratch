# util-lib

A small Python utility library of string and numeric helpers.

## Installation / usage

The package is a plain Python package. Import the helpers directly:

```python
from util_lib import slugify, truncate, title_case, clamp, is_prime, mean
```

> Note: directory is named `util-lib`. To import it as `util_lib`, place it on
> your path under an importable name (e.g. symlink or rename to `util_lib`), or
> import the modules individually.

## String helpers (`strings.py`)

### `slugify(text)`
Convert a string into a URL-friendly slug. Lowercases the text, replaces runs
of non-alphanumeric characters with single hyphens, and strips leading/trailing
hyphens.

```python
slugify("Hello, World!")   # -> 'hello-world'
```

### `truncate(text, length, suffix="...")`
Truncate `text` to at most `length` characters. If the text is longer than
`length`, it is cut and `suffix` is appended so the total length does not exceed
`length`. Raises `ValueError` if `length` is negative.

```python
truncate("hello world", 8)   # -> 'hello...'
```

### `title_case(text)`
Capitalize the first letter of each word and lowercase the rest. Words are split
on whitespace and rejoined with single spaces.

```python
title_case("the QUICK brown fox")   # -> 'The Quick Brown Fox'
```

## Numeric helpers (`numbers.py`)

### `clamp(value, low, high)`
Constrain `value` to the inclusive range `[low, high]`. Raises `ValueError` if
`low > high`.

```python
clamp(15, 0, 10)   # -> 10
clamp(-3, 0, 10)   # -> 0
```

### `is_prime(n)`
Return `True` if `n` is a prime number, `False` otherwise.

```python
is_prime(7)   # -> True
is_prime(1)   # -> False
```

### `mean(values)`
Return the arithmetic mean of a non-empty iterable of numbers. Raises
`ValueError` if the iterable is empty.

```python
mean([1, 2, 3, 4])   # -> 2.5
```
