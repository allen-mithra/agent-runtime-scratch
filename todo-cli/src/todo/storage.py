"""JSON-file persistence for todos.

The store is a single JSON file containing a list of todo records, e.g.::

    [{"id": 1, "title": "Buy milk", "completed": false}]

Design points:

* A missing file is treated as an empty store (first run is not an error).
* A corrupt or structurally invalid file raises :class:`StorageError` rather
  than crashing with a raw traceback, so the CLI can report it cleanly.
* Writes are atomic: data is written to a temporary file in the same directory
  and then renamed over the target, so an interrupted write cannot truncate or
  corrupt an existing store.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import List

from .errors import StorageError
from .models import Todo


class TodoStore:
    """Loads and saves a list of :class:`Todo` objects from a JSON file."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)

    def load(self) -> List[Todo]:
        """Return the persisted todos.

        Returns an empty list if the file does not exist. Raises
        :class:`StorageError` if the file exists but cannot be read or does not
        contain a valid list of todo records.
        """
        if not self.path.exists():
            return []

        try:
            raw = self.path.read_text(encoding="utf-8")
        except OSError as exc:
            raise StorageError(f"could not read store file {self.path}: {exc}") from exc

        if raw.strip() == "":
            # An empty file is a benign edge case; treat it as an empty store.
            return []

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise StorageError(
                f"store file {self.path} is corrupt (invalid JSON): {exc}"
            ) from exc

        if not isinstance(data, list):
            raise StorageError(
                f"store file {self.path} is corrupt: expected a list of todos"
            )

        todos = [Todo.from_dict(item) for item in data]

        ids = [todo.id for todo in todos]
        if len(set(ids)) != len(ids):
            raise StorageError(
                f"store file {self.path} is corrupt: duplicate todo ids"
            )

        return todos

    def save(self, todos: List[Todo]) -> None:
        """Persist ``todos`` to disk atomically.

        Raises :class:`StorageError` if the destination directory cannot be
        created or the file cannot be written.
        """
        payload = json.dumps([todo.to_dict() for todo in todos], indent=2)

        directory = self.path.parent
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise StorageError(
                f"could not create directory {directory}: {exc}"
            ) from exc

        # Write to a temp file in the same directory, then atomically replace.
        try:
            fd, tmp_name = tempfile.mkstemp(
                dir=str(directory), prefix=".todo-", suffix=".tmp"
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(payload)
                    handle.write("\n")
                os.replace(tmp_name, self.path)
            except BaseException:
                # Clean up the temp file on any failure so we don't leak it.
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass
                raise
        except OSError as exc:
            raise StorageError(
                f"could not write store file {self.path}: {exc}"
            ) from exc
