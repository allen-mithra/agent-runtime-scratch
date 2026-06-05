"""Tests for the domain service: core operations and edge cases."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import _support  # noqa: F401  (sets up sys.path)

from todo.errors import TodoNotFoundError, ValidationError
from todo.service import MAX_TITLE_LENGTH, TodoService
from todo.storage import TodoStore


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        path = Path(self._tmp.name) / "todos.json"
        self.service = TodoService(TodoStore(path))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    # --- add ---------------------------------------------------------------

    def test_add_assigns_sequential_ids(self) -> None:
        first = self.service.add("one")
        second = self.service.add("two")
        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_add_strips_whitespace(self) -> None:
        todo = self.service.add("  spaced  ")
        self.assertEqual(todo.title, "spaced")

    def test_add_empty_title_raises(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.add("   ")

    def test_add_overlong_title_raises(self) -> None:
        with self.assertRaises(ValidationError):
            self.service.add("x" * (MAX_TITLE_LENGTH + 1))

    def test_add_persists_across_instances(self) -> None:
        self.service.add("persisted")
        # A fresh service over the same file should see the data.
        reloaded = TodoService(self.service._store)
        self.assertEqual(len(reloaded.list()), 1)

    def test_ids_continue_after_deletion(self) -> None:
        self.service.add("one")
        self.service.add("two")
        self.service.delete(2)
        third = self.service.add("three")
        # Max id was 1 after deleting 2, so next is 2 again -- but never clashes.
        self.assertEqual(third.id, 2)
        ids = [t.id for t in self.service.list()]
        self.assertEqual(len(ids), len(set(ids)))

    # --- list --------------------------------------------------------------

    def test_list_empty_store(self) -> None:
        self.assertEqual(self.service.list(), [])

    def test_list_sorted_by_id(self) -> None:
        self.service.add("a")
        self.service.add("b")
        ids = [t.id for t in self.service.list()]
        self.assertEqual(ids, [1, 2])

    # --- complete ----------------------------------------------------------

    def test_complete_marks_done(self) -> None:
        todo = self.service.add("task")
        updated = self.service.complete(todo.id)
        self.assertTrue(updated.completed)
        self.assertTrue(self.service.list()[0].completed)

    def test_complete_is_idempotent(self) -> None:
        todo = self.service.add("task")
        self.service.complete(todo.id)
        again = self.service.complete(todo.id)
        self.assertTrue(again.completed)

    def test_complete_unknown_id_raises(self) -> None:
        with self.assertRaises(TodoNotFoundError):
            self.service.complete(999)

    def test_complete_on_empty_store_raises(self) -> None:
        with self.assertRaises(TodoNotFoundError):
            self.service.complete(1)

    # --- delete ------------------------------------------------------------

    def test_delete_removes_todo(self) -> None:
        todo = self.service.add("task")
        removed = self.service.delete(todo.id)
        self.assertEqual(removed.id, todo.id)
        self.assertEqual(self.service.list(), [])

    def test_delete_unknown_id_raises(self) -> None:
        self.service.add("task")
        with self.assertRaises(TodoNotFoundError):
            self.service.delete(42)

    def test_delete_only_targets_one(self) -> None:
        self.service.add("a")
        self.service.add("b")
        self.service.delete(1)
        ids = [t.id for t in self.service.list()]
        self.assertEqual(ids, [2])

    # --- clear-completed ---------------------------------------------------

    def test_clear_completed_removes_only_done(self) -> None:
        self.service.add("a")
        b = self.service.add("b")
        self.service.complete(b.id)
        removed = self.service.clear_completed()
        self.assertEqual([t.id for t in removed], [b.id])
        remaining = [t.title for t in self.service.list()]
        self.assertEqual(remaining, ["a"])

    def test_clear_completed_when_none_done(self) -> None:
        self.service.add("a")
        removed = self.service.clear_completed()
        self.assertEqual(removed, [])
        self.assertEqual(len(self.service.list()), 1)

    def test_clear_completed_on_empty_store(self) -> None:
        self.assertEqual(self.service.clear_completed(), [])


if __name__ == "__main__":
    unittest.main()
