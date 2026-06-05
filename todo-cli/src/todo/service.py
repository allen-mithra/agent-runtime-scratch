"""Domain logic for managing todos.

The service owns all business rules (id assignment, validation, state changes)
and delegates persistence to a :class:`~todo.storage.TodoStore`. It is
deliberately free of any CLI/printing concerns so it can be unit-tested and
reused independently of the command-line front end.
"""

from __future__ import annotations

from typing import List

from .errors import TodoNotFoundError, ValidationError
from .models import Todo
from .storage import TodoStore

# Guard against absurdly long titles silently filling the store file.
MAX_TITLE_LENGTH = 1000


class TodoService:
    """High-level operations over the persisted collection of todos."""

    def __init__(self, store: TodoStore) -> None:
        self._store = store

    def list(self) -> List[Todo]:
        """Return all todos in id order."""
        return sorted(self._store.load(), key=lambda todo: todo.id)

    def add(self, title: str) -> Todo:
        """Create a new todo with the given title and persist it.

        Raises:
            ValidationError: if ``title`` is empty or too long.
        """
        clean_title = self._normalize_title(title)

        todos = self._store.load()
        next_id = max((todo.id for todo in todos), default=0) + 1
        todo = Todo(id=next_id, title=clean_title, completed=False)
        todos.append(todo)
        self._store.save(todos)
        return todo

    def complete(self, todo_id: int) -> Todo:
        """Mark the todo with ``todo_id`` as completed and persist it.

        Returns the updated todo. Completing an already-completed todo is
        idempotent. Raises :class:`TodoNotFoundError` if no such id exists.
        """
        todos = self._store.load()
        todo = self._find(todos, todo_id)
        todo.completed = True
        self._store.save(todos)
        return todo

    def delete(self, todo_id: int) -> Todo:
        """Remove the todo with ``todo_id`` and persist the change.

        Returns the removed todo. Raises :class:`TodoNotFoundError` if no such
        id exists.
        """
        todos = self._store.load()
        todo = self._find(todos, todo_id)
        todos = [item for item in todos if item.id != todo_id]
        self._store.save(todos)
        return todo

    def clear_completed(self) -> List[Todo]:
        """Delete all completed todos and persist the change.

        Returns the list of todos that were removed (may be empty).
        """
        todos = self._store.load()
        removed = [todo for todo in todos if todo.completed]
        if removed:
            remaining = [todo for todo in todos if not todo.completed]
            self._store.save(remaining)
        return removed

    @staticmethod
    def _find(todos: List[Todo], todo_id: int) -> Todo:
        for todo in todos:
            if todo.id == todo_id:
                return todo
        raise TodoNotFoundError(todo_id)

    @staticmethod
    def _normalize_title(title: str) -> str:
        clean = title.strip()
        if not clean:
            raise ValidationError("title must not be empty")
        if len(clean) > MAX_TITLE_LENGTH:
            raise ValidationError(
                f"title must be at most {MAX_TITLE_LENGTH} characters"
            )
        return clean
