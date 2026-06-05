## Build Python deliverables against the standard library only

The Philosophy
This container's Python has no package installer — `pip` is absent both as a
binary and as a module, so nothing third-party can be installed mid-run.
Reaching for a popular framework first and discovering the gap later wastes
turns and forces a rewrite. Treating the stdlib as the whole toolbox up front
turns a constraint into a clean, idiomatic design instead of a fallback.

Do's
- Do verify the toolchain before depending on it: a quick `python3 -m pip --version` reveals the gap immediately.
- Do reach for stdlib equivalents by default: `argparse` for CLIs, `json` for storage, `unittest` for tests, `dataclasses` for models.
- Do run tests with `python3 -m unittest discover -s tests` and keep them pytest-compatible (plain `TestCase`, a `conftest.py` for path setup) so they work either way.
- Do make `src`-layout packages importable in tests via a `conftest.py`/`_support.py` `sys.path` insert rather than requiring an editable install.

Don'ts
- Don't assume `pip`, `pytest`, or any third-party package is present — installation will fail.
- Don't write a test suite that only runs under `pytest`; if pytest is missing the whole suite becomes unrunnable here.
