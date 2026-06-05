"""End-to-end tests for the CLI layer: exit codes, output, and errors."""

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

import _support  # noqa: F401  (sets up sys.path)

from todo.cli import main


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.store = Path(self._tmp.name) / "todos.json"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_cli(self, *args):
        """Invoke main() with an explicit store; capture (code, out, err)."""
        argv = ["--store", str(self.store), *args]
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_add_and_list(self) -> None:
        code, out, _ = self.run_cli("add", "Buy", "milk")
        self.assertEqual(code, 0)
        self.assertIn("Added todo 1: Buy milk", out)

        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("Buy milk", out)
        self.assertIn("[ ]", out)

    def test_list_empty_store_message(self) -> None:
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("No todos yet", out)

    def test_done_marks_complete(self) -> None:
        self.run_cli("add", "task")
        code, out, _ = self.run_cli("done", "1")
        self.assertEqual(code, 0)
        self.assertIn("Completed todo 1", out)
        _, out, _ = self.run_cli("list")
        self.assertIn("[x]", out)

    def test_delete(self) -> None:
        self.run_cli("add", "task")
        code, out, _ = self.run_cli("delete", "1")
        self.assertEqual(code, 0)
        self.assertIn("Deleted todo 1", out)

    def test_clear_completed(self) -> None:
        self.run_cli("add", "a")
        self.run_cli("add", "b")
        self.run_cli("done", "2")
        code, out, _ = self.run_cli("clear-completed")
        self.assertEqual(code, 0)
        self.assertIn("Cleared 1", out)

    # --- error handling ----------------------------------------------------

    def test_add_empty_title_errors(self) -> None:
        code, _, err = self.run_cli("add", "   ")
        self.assertEqual(code, 1)
        self.assertIn("error:", err)
        self.assertIn("empty", err)

    def test_done_unknown_id_errors(self) -> None:
        code, _, err = self.run_cli("done", "999")
        self.assertEqual(code, 1)
        self.assertIn("no todo found with id 999", err)

    def test_delete_unknown_id_errors(self) -> None:
        code, _, err = self.run_cli("delete", "5")
        self.assertEqual(code, 1)
        self.assertIn("no todo found", err)

    def test_corrupt_store_errors_cleanly(self) -> None:
        self.store.write_text("{garbage", encoding="utf-8")
        code, _, err = self.run_cli("list")
        self.assertEqual(code, 1)
        self.assertIn("corrupt", err)

    def test_unknown_subcommand_is_usage_error(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            self.run_cli("frobnicate")
        self.assertEqual(ctx.exception.code, 2)

    def test_missing_subcommand_is_usage_error(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            self.run_cli()
        self.assertEqual(ctx.exception.code, 2)

    def test_non_integer_id_is_usage_error(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            self.run_cli("done", "abc")
        self.assertEqual(ctx.exception.code, 2)

    def test_negative_id_is_usage_error(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            self.run_cli("done", "-1")
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
