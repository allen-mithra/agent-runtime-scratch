"""Tests for the JSON persistence layer, including corruption edge cases."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import _support  # noqa: F401  (sets up sys.path)

from todo.errors import StorageError
from todo.models import Todo
from todo.storage import TodoStore


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.path = Path(self._tmp.name) / "todos.json"
        self.store = TodoStore(self.path)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_load_missing_file_returns_empty(self) -> None:
        self.assertEqual(self.store.load(), [])

    def test_load_empty_file_returns_empty(self) -> None:
        self.path.write_text("   \n", encoding="utf-8")
        self.assertEqual(self.store.load(), [])

    def test_save_then_load_round_trips(self) -> None:
        todos = [Todo(1, "a"), Todo(2, "b", completed=True)]
        self.store.save(todos)
        loaded = self.store.load()
        self.assertEqual(loaded, todos)

    def test_save_creates_parent_directory(self) -> None:
        nested = Path(self._tmp.name) / "deep" / "nested" / "todos.json"
        store = TodoStore(nested)
        store.save([Todo(1, "x")])
        self.assertTrue(nested.exists())

    def test_save_writes_pretty_json_list(self) -> None:
        self.store.save([Todo(1, "x")])
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(data, [{"id": 1, "title": "x", "completed": False}])

    def test_corrupt_invalid_json_raises_storage_error(self) -> None:
        self.path.write_text("{not json", encoding="utf-8")
        with self.assertRaises(StorageError):
            self.store.load()

    def test_corrupt_non_list_raises_storage_error(self) -> None:
        self.path.write_text('{"id": 1}', encoding="utf-8")
        with self.assertRaises(StorageError):
            self.store.load()

    def test_corrupt_record_missing_fields_raises(self) -> None:
        self.path.write_text('[{"title": "no id"}]', encoding="utf-8")
        with self.assertRaises(StorageError):
            self.store.load()

    def test_corrupt_record_bad_title_type_raises(self) -> None:
        self.path.write_text('[{"id": 1, "title": 5}]', encoding="utf-8")
        with self.assertRaises(StorageError):
            self.store.load()

    def test_corrupt_duplicate_ids_raises(self) -> None:
        self.path.write_text(
            '[{"id": 1, "title": "a"}, {"id": 1, "title": "b"}]',
            encoding="utf-8",
        )
        with self.assertRaises(StorageError):
            self.store.load()

    def test_failed_write_leaves_no_temp_files(self) -> None:
        self.store.save([Todo(1, "x")])
        leftovers = [p for p in self.path.parent.iterdir() if p.name != self.path.name]
        self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
