"""Immutable review-run persistence, independent of model prose and network access."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_setup import SOURCE

SCRIPT = SOURCE / "skills/pr-review/scripts/persist_report.py"
SPEC = importlib.util.spec_from_file_location("review_report", SCRIPT)
REPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORT)


class ReportTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="review-runs-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.private = self.root / "home/.copilot/engineering-workflow"
        self.worktree = self.root / "worktree"
        self.worktree.mkdir()
        self.args = dict(host="git.test", owner="sample", repository="fixture", pr="7",
                         base="a" * 40, head="b" * 40, gate="PASS", disposition="APPROVE",
                         body="Current behavior is sound.\n", reviewed_at=datetime(2026, 9, 12, 12, tzinfo=timezone.utc))

    def persist(self, **overrides):
        args = {**self.args, **overrides}
        return REPORT.persist_report(self.private, self.worktree, **args)

    def test_same_head_has_distinct_immutable_runs_even_at_identical_timestamp(self):
        first = self.persist()
        original = first.read_bytes()
        second = self.persist(body="New discussion establishes an open consequence.\n",
                              gate="UNRESOLVED", disposition="COMMENT", prior_head="a" * 40)
        third = self.persist()
        directory = self.private / "reviews/git.test/sample/fixture/pr-7" / ("b" * 40)
        self.assertEqual(first, directory / "20260912T120000000000Z.md")
        self.assertEqual(second.name, "20260912T120000000000Z-2.md")
        self.assertEqual(third.name, "20260912T120000000000Z-3.md")
        self.assertEqual(first.read_bytes(), original)
        self.assertEqual(third.read_bytes(), original)
        self.assertIn(b"New discussion", second.read_bytes())
        self.assertIn(b"Prior reviewed head: `" + b"a" * 40 + b"`", second.read_bytes())
        self.assertIn(b"Behavior gate: UNRESOLVED", second.read_bytes())
        self.assertIn(b"Recommended disposition: COMMENT", second.read_bytes())
        self.assertEqual(list(self.worktree.iterdir()), [])

    def test_concurrent_runs_never_replace_each_other(self):
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(self.persist, body=body) for body in ("First evidence", "Second evidence")]
            paths = [future.result() for future in futures]
        self.assertEqual(len(set(paths)), 2)
        self.assertEqual({path.read_text(encoding="utf-8").splitlines()[-1] for path in paths},
                         {"First evidence", "Second evidence"})

    def test_timestamp_is_utc_and_report_bytes_are_utf8_lf(self):
        path = self.persist(body="Caf\u00e9\r\nFirst\rSecond\n",
                            reviewed_at=datetime(2026, 9, 12, 5, 0, 0, 123456,
                                                 tzinfo=timezone(timedelta(hours=-7))))
        data = path.read_bytes()
        self.assertEqual(path.name, "20260912T120000123456Z.md")
        self.assertIn(b"Reviewed at: 2026-09-12T12:00:00.123456Z", data)
        self.assertTrue(data.endswith("Caf\u00e9\nFirst\nSecond\n".encode("utf-8")))
        self.assertNotIn(b"\r", data)
        self.assertFalse(data.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"Prior reviewed head", data)

    def test_invalid_identity_revisions_and_metadata_refuse_writes(self):
        cases = [{field: value} for field in ("host", "owner", "repository")
                 for value in ("..", ".", "x/y", r"x\y", "C:drive", "/absolute", "x%2fy",
                               "name.", "NUL.txt", "com1", "x\nnew", "x ", "", None)]
        cases += [{"pr": value} for value in ("0", "-1", "01", "1/2", 1, "")]
        cases += [{field: value} for field in ("base", "head", "prior_head")
                  for value in ("abc", "A" * 40, "../bad", "z" * 40, "a" * 64)]
        cases += [{"gate": "VERIFIED"}, {"disposition": "BLOCK"}, {"body": " "},
                  {"reviewed_at": datetime(2026, 9, 12)}]
        for invalid in cases:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    self.persist(**invalid)
                self.assertFalse(self.private.exists())

    def test_sha256_revision_format_is_supported_consistently(self):
        path = self.persist(base="a" * 64, head="b" * 64, prior_head="c" * 64)
        self.assertEqual(path.parent.name, "b" * 64)

    def test_worktree_containment_and_relative_roots_are_refused(self):
        for private in (self.worktree / "private", Path("relative"), self.root / "home/../private"):
            with self.subTest(private=private):
                with self.assertRaises(ValueError):
                    REPORT.persist_report(private, self.worktree, **self.args)
        with self.assertRaises(ValueError):
            REPORT.persist_report(self.private, self.root / "missing-worktree", **self.args)
        self.assertEqual(list(self.worktree.iterdir()), [])
        self.assertFalse(self.private.exists())

    def test_links_and_windows_redirection_are_refused_without_link_privileges(self):
        original = Path.lstat
        for mode, attributes in ((stat.S_IFLNK, 0), (stat.S_IFDIR, stat.FILE_ATTRIBUTE_REPARSE_POINT)):
            for linked in (self.private, self.private / "reviews"):
                def inspect(path, *args, **kwargs):
                    if path == linked:
                        return SimpleNamespace(st_mode=mode, st_file_attributes=attributes)
                    return original(path, *args, **kwargs)
                with self.subTest(mode=mode, linked=linked):
                    with patch.object(Path, "lstat", autospec=True, side_effect=inspect):
                        with self.assertRaisesRegex(ValueError, "linked or redirected"):
                            self.persist()
                    self.assertFalse(self.private.exists())

    def test_existing_nonregular_destination_and_file_parent_are_refused(self):
        first = self.persist()
        first.unlink()
        first.mkdir()
        with self.assertRaisesRegex(ValueError, "not a regular file"):
            self.persist()
        self.assertEqual(list(first.parent.iterdir()), [first])
        (self.root / "file").write_bytes(b"Preserve existing file")
        with self.assertRaisesRegex(ValueError, "parent is not a directory"):
            REPORT.persist_report(self.root / "file/child", self.worktree, **self.args)

    def test_readback_and_io_failure_do_not_claim_success(self):
        with patch.object(Path, "open", side_effect=PermissionError("fixture denied")):
            with self.assertRaisesRegex(PermissionError, "fixture denied"):
                self.persist()
        with patch.object(Path, "read_bytes", return_value=b"different bytes"):
            with self.assertRaisesRegex(OSError, "read-back differs"):
                self.persist()

    def test_cli_accepts_stdin_and_reports_failed_persistence(self):
        args = [sys.executable, str(SCRIPT), "--workflow-root", str(self.private),
                "--worktree", str(self.worktree)]
        for field in ("host", "owner", "repository", "pr", "base", "head", "gate", "disposition"):
            args += ["--" + field, self.args[field]]
        result = subprocess.run(args, input=b"Complete technical report\r\n", capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = Path(result.stdout.decode("utf-8").strip())
        self.assertTrue(report.is_file())
        self.assertTrue(report.read_bytes().endswith(b"Complete technical report\n"))
        args[args.index("--owner") + 1] = "../escape"
        result = subprocess.run(args, input=b"Complete technical report", capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"retain the complete review in chat", result.stderr)
        self.assertEqual(result.stdout, b"")


if __name__ == "__main__":
    unittest.main()
