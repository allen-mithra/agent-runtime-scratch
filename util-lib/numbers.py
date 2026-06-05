"""Numeric helper functions."""


def clamp(value, low, high):
    """Constrain ``value`` to the inclusive range [low, high].

    >>> clamp(15, 0, 10)
    10
    >>> clamp(-3, 0, 10)
    0
    """
    if low > high:
        raise ValueError("low must not be greater than high")
    return max(low, min(value, high))


def is_prime(n):
    """Return True if ``n`` is a prime number.

    >>> is_prime(7)
    True
    >>> is_prime(1)
    False
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def mean(values):
    """Return the arithmetic mean of a non-empty iterable of numbers.

    >>> mean([1, 2, 3, 4])
    2.5
    """
    items = list(values)
    if not items:
        raise ValueError("mean() requires at least one value")
    return sum(items) / len(items)
