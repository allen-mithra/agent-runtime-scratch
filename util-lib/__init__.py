"""util-lib: a small collection of string and numeric helpers."""

from .numbers import clamp, is_prime, mean
from .strings import slugify, title_case, truncate

__all__ = [
    "slugify",
    "truncate",
    "title_case",
    "clamp",
    "is_prime",
    "mean",
]
