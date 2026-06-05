#!/usr/bin/env python3
"""Convenience launcher so the app can be run without installation.

Usage:
    ./todo.py add "Buy milk"
    python3 todo.py list
"""

import sys
from pathlib import Path

# Make the `src` layout importable when running from a checkout.
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from todo.cli import main  # noqa: E402  (path setup must precede import)

if __name__ == "__main__":
    sys.exit(main())
