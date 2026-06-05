# CLAUDE.md

## Basics

- Python interpreter is `python3`. Plain `python` is **not** on PATH in this
  environment (invoking it fails with exit 127). Use `python3` for scripts,
  `python3 -m doctest`, etc.
- `util-lib/` is a small utility package: `strings.py` (slugify, truncate,
  title_case) and `numbers.py` (clamp, is_prime, mean), re-exported from
  `__init__.py`. The directory name has a hyphen, so it is not importable as
  `util_lib` without a symlink/rename — import the modules directly or alias the
  path.

## CI & Tests

- No test framework is configured. Functions carry doctests; run them with
  `cd util-lib && python3 -m doctest strings.py numbers.py` (silent = pass).
