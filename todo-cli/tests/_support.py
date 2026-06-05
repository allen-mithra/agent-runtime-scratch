"""Shared test setup: make the ``src`` layout importable.

Importing this module (or relying on :mod:`conftest`) ensures ``src`` is on
``sys.path`` so tests work under both ``python -m unittest`` and ``pytest``.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
