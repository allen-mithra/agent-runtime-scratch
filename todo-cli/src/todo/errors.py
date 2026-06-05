"""Exception hierarchy for the todo application.

Keeping the exceptions in one place lets the CLI layer translate domain and
storage failures into clean, user-facing error messages and exit codes without
leaking tracebacks.
"""

from __future__ import annotations


class TodoError(Exception):
    """Base class for all expected, user-facing errors."""


class ValidationError(TodoError):
    """Raised when user-supplied input is invalid (e.g. an empty title)."""


class TodoNotFoundError(TodoError):
    """Raised when an operation references a todo id that does not exist."""

    def __init__(self, todo_id: int) -> None:
        super().__init__(f"no todo found with id {todo_id}")
        self.todo_id = todo_id


class StorageError(TodoError):
    """Raised when the store file cannot be read, parsed, or written."""
