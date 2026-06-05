# agent-runtime-scratch

Throwaway target for agent-runtime e2e smoke tests. Deliverables land in their
own subdirectories.

## Basics

- The runtime container ships Python 3.11 **without `pip`** (no `pip` binary and
  no `pip` module). Only the standard library is available — no third-party
  packages can be installed. Build Python deliverables dependency-free.

## Architecture

- `todo-cli/` — a dependency-free Python command-line todo manager. Layered as
  `cli` → `service` → (`storage`, `models`), with an `errors` exception
  hierarchy. Source lives under `todo-cli/src/todo/`; a `todo.py` launcher at
  `todo-cli/` runs it without installation.

## CI & Tests

- `todo-cli/` tests use the stdlib `unittest` runner (pytest is not installed):
  `cd todo-cli && python3 -m unittest discover -s tests -v`. Tests put `src` on
  `sys.path` via `tests/conftest.py` / `tests/_support.py`, so no install is
  needed to run them.
