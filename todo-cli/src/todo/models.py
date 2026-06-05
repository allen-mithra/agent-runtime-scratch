"""Domain model for a single todo item."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .errors import StorageError


@dataclass
class Todo:
    """A single todo item.

    Attributes:
        id: Stable, unique, positive integer identifier.
        title: Human-readable description (always non-empty, stripped).
        completed: Whether the item has been marked done.
    """

    id: int
    title: str
    completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dict suitable for JSON encoding."""
        return {"id": self.id, "title": self.title, "completed": self.completed}

    @classmethod
    def from_dict(cls, data: Any) -> "Todo":
        """Build a :class:`Todo` from decoded JSON, validating its shape.

        Raises:
            StorageError: if ``data`` is not a well-formed todo record. This is
                surfaced as a storage (not validation) problem because it means
                the persisted file is corrupt rather than that the user typed
                something wrong.
        """
        if not isinstance(data, dict):
            raise StorageError("todo record is not an object")

        raw_id = data.get("id")
        # bool is a subclass of int; reject it explicitly so True/False ids fail.
        if not isinstance(raw_id, int) or isinstance(raw_id, bool) or raw_id <= 0:
            raise StorageError(f"todo record has an invalid id: {raw_id!r}")

        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            raise StorageError(f"todo {raw_id} has an invalid title")

        completed = data.get("completed", False)
        if not isinstance(completed, bool):
            raise StorageError(f"todo {raw_id} has an invalid 'completed' flag")

        return cls(id=raw_id, title=title, completed=completed)
