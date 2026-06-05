"""Command-line interface for the todo application.

This module is the only layer that deals with argument parsing, stdout/stderr,
and process exit codes. It translates the domain/storage exception hierarchy
into friendly messages and conventional exit statuses:

* ``0``  success
* ``1``  a known, user-facing error (validation, missing id, corrupt store)
* ``2``  a usage error (unknown subcommand, bad arguments) -- argparse default
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional, Sequence

from . import __version__
from .errors import TodoError
from .models import Todo
from .service import TodoService
from .storage import TodoStore

#: Environment variable allowing users (and tests) to override the store path.
STORE_ENV_VAR = "TODO_STORE"

EXIT_SUCCESS = 0
EXIT_ERROR = 1


def default_store_path() -> Path:
    """Return the default store location, honouring ``$TODO_STORE``.

    Without an override the store lives at ``~/.todo/todos.json`` so that the
    user's todos are stored in a stable, per-user location independent of the
    working directory.
    """
    override = os.environ.get(STORE_ENV_VAR)
    if override:
        return Path(override).expanduser()
    return Path.home() / ".todo" / "todos.json"


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A small command-line todo manager.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--store",
        type=Path,
        default=None,
        metavar="PATH",
        help=(
            "Path to the JSON store file "
            f"(default: ${STORE_ENV_VAR} or ~/.todo/todos.json)."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    # Require a subcommand; argparse exits with code 2 if one is missing.
    subparsers.required = True

    add_parser = subparsers.add_parser("add", help="Add a new todo.")
    add_parser.add_argument(
        "title",
        nargs="+",
        help="The todo text (multiple words are joined with spaces).",
    )
    add_parser.set_defaults(func=_cmd_add)

    list_parser = subparsers.add_parser("list", help="List all todos.")
    list_parser.add_argument(
        "--all",
        action="store_true",
        help="(default) Show every todo; kept for explicitness.",
    )
    list_parser.set_defaults(func=_cmd_list)

    done_parser = subparsers.add_parser(
        "done", help="Mark a todo as completed."
    )
    done_parser.add_argument("id", type=_positive_int, help="Id of the todo.")
    done_parser.set_defaults(func=_cmd_done)

    delete_parser = subparsers.add_parser("delete", help="Delete a todo.")
    delete_parser.add_argument("id", type=_positive_int, help="Id of the todo.")
    delete_parser.set_defaults(func=_cmd_delete)

    clear_parser = subparsers.add_parser(
        "clear-completed", help="Remove all completed todos."
    )
    clear_parser.set_defaults(func=_cmd_clear_completed)

    return parser


def _positive_int(value: str) -> int:
    """argparse type that accepts only positive integers."""
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not an integer")
    if number <= 0:
        raise argparse.ArgumentTypeError("id must be a positive integer")
    return number


# --- command handlers -------------------------------------------------------
# Each handler performs domain work and prints human-readable output. They
# return nothing; errors are raised as TodoError and handled centrally in main.


def _cmd_add(service: TodoService, args: argparse.Namespace) -> None:
    title = " ".join(args.title)
    todo = service.add(title)
    print(f"Added todo {todo.id}: {todo.title}")


def _cmd_list(service: TodoService, args: argparse.Namespace) -> None:
    todos = service.list()
    if not todos:
        print("No todos yet. Add one with: todo add \"...\"")
        return
    print(_format_todos(todos))


def _cmd_done(service: TodoService, args: argparse.Namespace) -> None:
    todo = service.complete(args.id)
    print(f"Completed todo {todo.id}: {todo.title}")


def _cmd_delete(service: TodoService, args: argparse.Namespace) -> None:
    todo = service.delete(args.id)
    print(f"Deleted todo {todo.id}: {todo.title}")


def _cmd_clear_completed(service: TodoService, args: argparse.Namespace) -> None:
    removed = service.clear_completed()
    print(f"Cleared {len(removed)} completed todo(s).")


def _format_todos(todos: List[Todo]) -> str:
    """Render todos as an aligned, human-readable list."""
    width = max(len(str(todo.id)) for todo in todos)
    lines = []
    for todo in todos:
        mark = "x" if todo.completed else " "
        lines.append(f"[{mark}] {todo.id:>{width}}  {todo.title}")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Program entry point. Returns a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    store_path = args.store if args.store is not None else default_store_path()
    service = TodoService(TodoStore(store_path))

    try:
        args.func(service, args)
    except TodoError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_ERROR

    return EXIT_SUCCESS


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
