"""pytest configuration: ensure the ``src`` layout is importable.

This makes ``import todo`` work without an editable install when the suite is
run via pytest. (``python -m unittest`` relies on the same logic in
``_support``.)
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
