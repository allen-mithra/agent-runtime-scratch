# todo-cli

A small, production-quality command-line todo manager written in Python with
**no third-party dependencies** (standard library only). Todos are persisted to
a local JSON file so your list survives across invocations.

## Features

- `add`, `list`, `done`, `delete`, and `clear-completed` subcommands
- Durable JSON storage with **atomic writes** (an interrupted write can't
  corrupt your existing data)
- Graceful handling of a missing or corrupt store file
- Robust input validation with clear error messages and conventional exit codes
- Clean separation between CLI parsing, domain logic, and persistence
- Full automated test suite (core operations + edge cases)

## Requirements

- Python 3.8 or newer. That's it — no packages to install.

## Install

You can run the app directly from a checkout, or install it as a command.

### Option A — run directly (no install)

```bash
cd todo-cli
./todo.py --help
# or, equivalently:
python3 todo.py --help
```

### Option B — install the `todo` command

```bash
cd todo-cli
python3 -m pip install .
todo --help
```

This installs a `todo` entry-point script (defined in `pyproject.toml`).

## Where todos are stored

By default todos live at `~/.todo/todos.json`. You can override the location:

- per-invocation with `--store PATH`, or
- globally with the `TODO_STORE` environment variable.

```bash
export TODO_STORE=./my-todos.json
todo add "Scoped to this file"
```

## Usage

All examples below assume either the installed `todo` command or `./todo.py`.

### Add a todo

```bash
$ todo add "Buy milk"
Added todo 1: Buy milk
```

Multiple words are joined automatically, so quoting is optional:

```bash
$ todo add Write the quarterly report
Added todo 2: Write the quarterly report
```

### List todos

```bash
$ todo list
[ ] 1  Buy milk
[ ] 2  Write the quarterly report
```

Completed items are shown with an `[x]` marker. An empty store prints a hint
instead of nothing.

### Mark a todo complete

```bash
$ todo done 1
Completed todo 1: Buy milk
```

### Delete a todo

```bash
$ todo delete 2
Deleted todo 2: Write the quarterly report
```

### Clear all completed todos

```bash
$ todo clear-completed
Cleared 1 completed todo(s).
```

### Version

```bash
$ todo --version
todo 1.0.0
```

## Error handling and exit codes

The CLI uses conventional exit codes so it composes well in scripts:

| Exit code | Meaning                                                        |
|-----------|----------------------------------------------------------------|
| `0`       | Success                                                        |
| `1`       | A known error: empty title, unknown id, or corrupt store file  |
| `2`       | A usage error: unknown subcommand or malformed arguments       |

Examples:

```bash
$ todo done 999
error: no todo found with id 999      # exit code 1

$ todo add ""
error: title must not be empty        # exit code 1

$ todo frobnicate
usage: todo [-h] [--version] [--store PATH] <command> ...
todo: error: argument <command>: invalid choice: 'frobnicate'   # exit code 2
```

If the store file is missing it is treated as an empty list (a clean first
run). If it exists but is corrupt, the app reports the problem and exits `1`
rather than crashing.

## Running the tests

The suite runs with the standard-library test runner (no dependencies needed):

```bash
cd todo-cli
python3 -m unittest discover -s tests -v
```

If you have `pytest` installed, it works too (configuration lives in
`pyproject.toml`):

```bash
cd todo-cli
pytest
```

## Project layout

```
todo-cli/
├── pyproject.toml        # packaging + entry point + pytest config
├── README.md
├── todo.py               # convenience launcher (no install required)
├── src/
│   └── todo/
│       ├── __init__.py   # package metadata
│       ├── errors.py     # exception hierarchy
│       ├── models.py     # Todo domain entity (+ (de)serialization)
│       ├── storage.py    # JSON persistence (atomic, corruption-aware)
│       ├── service.py    # domain logic (add/list/complete/delete/clear)
│       └── cli.py        # argument parsing + entry point
└── tests/
    ├── conftest.py / _support.py  # make `src` importable
    ├── test_storage.py
    ├── test_service.py
    └── test_cli.py
```

The layering is deliberate: `cli` depends on `service`, which depends on
`storage` and `models`; nothing lower depends on anything above it. This keeps
the domain logic fully testable in isolation from argument parsing and I/O.
