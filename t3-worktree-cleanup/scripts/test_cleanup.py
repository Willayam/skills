"""Exercise backup and deletion against disposable local Git remotes."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sqlite3
import tempfile
import time
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("cleanup", Path(__file__).with_name("cleanup.py"))
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.repo = self.root / "repo"
        self.remote = self.root / "remote.git"
        self.worktrees = self.root / "worktrees"
        self.path = self.worktrees / "feature"
        self.cmd("git", "init", "--bare", str(self.remote))
        self.cmd("git", "init", "-b", "main", str(self.repo))
        self.git(self.repo, "config", "user.email", "test@example.invalid")
        self.git(self.repo, "config", "user.name", "Cleanup test")
        (self.repo / "file.txt").write_text("original\n")
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-m", "Initial")
        self.git(self.repo, "remote", "add", "origin", str(self.remote))
        self.git(self.repo, "push", "origin", "main")
        self.git(self.repo, "fetch", "origin")
        self.git(self.repo, "worktree", "add", "-b", "feature", str(self.path))
        (self.path / "file.txt").write_text("unfinished feature\n")
        self.git(self.path, "commit", "-am", "Feature")
        self.wt = dict(path=str(self.path), repo=str(self.repo), branch="refs/heads/feature",
                       head=self.git(self.path, "rev-parse", "HEAD").strip())
        self.ctx = dict(uses={str(self.path): [("Feature", "settled")]},
                        project_roots=set(), cwds=set(), activity={},
                        thread_ids={str(self.path): {"thread-1"}},
                        prs={str(self.repo): {}}, main={str(self.repo): "origin/main"},
                        all_paths=[str(self.path), str(self.repo)])
        self.now = time.time() + 8 * 86400
        for p in (patch.object(cleanup, "WORKTREE_ROOTS", [self.worktrees]),
                  patch.object(cleanup.time, "time", side_effect=lambda: self.now),
                  patch.object(cleanup, "fresh_context", side_effect=lambda ctx: ctx)):
            p.start()
            self.addCleanup(p.stop)

    def cmd(self, *args):
        return subprocess.run(args, check=True, text=True, capture_output=True).stdout

    def git(self, path, *args):
        return self.cmd("git", "-C", str(path), *args)

    def test_backup_verify_remove_and_recover(self):
        self.assertFalse(cleanup.judge(self.wt, self.ctx)[0])
        self.assertIsNone(cleanup.prepare_archive(self.wt, self.ctx))
        self.assertTrue(self.path.is_dir())  # Preparation never deletes files.
        self.assertTrue(cleanup.remote_archive(self.wt))
        self.ctx["uses"][str(self.path)] = [("Feature", "archived")]
        self.ctx["activity"][str(self.path)] = self.now  # Archiving itself is recent.
        self.assertIsNone(cleanup.remove(self.wt, self.ctx))
        self.assertFalse(self.path.exists())
        self.git(self.repo, "fetch", "origin", cleanup.archive_branch(self.wt))
        self.git(self.repo, "worktree", "add", "--detach", str(self.path), self.wt["head"])
        self.assertEqual((self.path / "file.txt").read_text(), "unfinished feature\n")

    def test_dirty_and_untracked_files_never_pushed(self):
        (self.path / "file.txt").write_text("do not lose this\n")
        self.assertIn("uncommitted", cleanup.prepare_archive(self.wt, self.ctx))
        self.assertFalse(cleanup.remote_archive(self.wt))
        self.git(self.path, "restore", "file.txt")
        (self.path / "notes.txt").write_text("private notes\n")
        self.assertIn("untracked", cleanup.prepare_archive(self.wt, self.ctx))
        self.assertFalse(cleanup.remote_archive(self.wt))

    def test_recent_source_and_thread_activity_hold(self):
        self.now = (self.path / "file.txt").stat().st_mtime + 60
        self.assertIn("seven days", cleanup.archive_blocker(self.wt, self.ctx))
        self.now += 8 * 86400
        self.ctx["activity"][str(self.path)] = self.now - 60
        self.assertIn("seven days", cleanup.archive_blocker(self.wt, self.ctx))

    def test_active_and_open_pr_hold(self):
        for state in ("running", "pinned", "open"):
            self.ctx["uses"][str(self.path)] = [("Feature", state)]
            self.assertIn(state, cleanup.prepare_archive(self.wt, self.ctx))
        self.ctx["uses"][str(self.path)] = [("Feature", "settled")]
        self.ctx["prs"][str(self.repo)] = {"feature": {"state": "OPEN", "number": 7}}
        self.assertEqual(cleanup.prepare_archive(self.wt, self.ctx), "PR #7 open")

    def test_existing_conflicting_backup_is_not_overwritten(self):
        ref = "refs/heads/" + cleanup.archive_branch(self.wt)
        self.git(self.repo, "push", "origin", "main:" + ref)
        old = self.git(self.remote, "rev-parse", ref).strip()
        self.assertIn("failed", cleanup.prepare_archive(self.wt, self.ctx))
        self.assertEqual(self.git(self.remote, "rev-parse", ref).strip(), old)
        self.assertTrue(self.path.is_dir())

    def test_failed_push_does_not_allow_cleanup(self):
        hook = self.remote / "hooks" / "pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        self.assertIn("failed", cleanup.prepare_archive(self.wt, self.ctx))
        self.assertFalse(cleanup.judge(self.wt, self.ctx)[0])
        self.assertTrue(self.path.exists())

    def test_secret_in_unpublished_history_is_held(self):
        # Synthetic token, deliberately shaped like a GitHub token for the scanner.
        token = "ghp_" + "aB3dE6gH9jK2mN5pQ8sT1vW4yZ7cF0iL3oR6"
        (self.path / "credentials.txt").write_text("token=" + token + "\n")
        self.git(self.path, "add", "credentials.txt")
        self.git(self.path, "commit", "-m", "Synthetic secret fixture")
        self.git(self.path, "rm", "credentials.txt")
        self.git(self.path, "commit", "-m", "Remove fixture from tip")
        self.wt["head"] = self.git(self.path, "rev-parse", "HEAD").strip()
        self.assertIn("secret scan", cleanup.prepare_archive(self.wt, self.ctx))
        self.assertFalse(cleanup.remote_archive(self.wt))

    def test_missing_scanner_holds_unpublished_history(self):
        with patch.object(cleanup.shutil, "which", return_value=None):
            self.assertIn("gitleaks", cleanup.prepare_archive(self.wt, self.ctx))
        self.assertFalse(cleanup.remote_archive(self.wt))

    def test_remote_verification_failure_keeps_worktree(self):
        self.assertIsNone(cleanup.prepare_archive(self.wt, self.ctx))
        self.git(self.repo, "remote", "set-url", "origin", str(self.root / "missing.git"))
        self.ctx["uses"][str(self.path)] = [("Feature", "archived")]
        self.assertFalse(cleanup.judge(self.wt, self.ctx)[0])
        self.assertTrue(self.path.exists())

    def test_activity_change_before_push_is_held(self):
        def fresh(ctx):
            ctx["activity"][str(self.path)] = self.now
            return ctx
        with patch.object(cleanup, "fresh_context", side_effect=fresh):
            self.assertIn("seven days", cleanup.prepare_archive(self.wt, self.ctx))
        self.assertFalse(cleanup.remote_archive(self.wt))

    def test_archived_thread_without_remote_backup_is_held(self):
        self.ctx["uses"][str(self.path)] = [("Feature", "archived")]
        self.assertFalse(cleanup.judge(self.wt, self.ctx)[0])

    def test_kept_ignored_and_hidden_files_are_held(self):
        self.git(self.path, "update-index", "--assume-unchanged", "file.txt")
        self.assertIn("git status skips", cleanup.prepare_archive(self.wt, self.ctx))
        self.git(self.path, "update-index", "--no-assume-unchanged", "file.txt")
        exclude = Path(self.git(self.path, "rev-parse", "--git-path", "info/exclude").strip())
        exclude.write_text("private-notes.txt\n")
        (self.path / "private-notes.txt").write_text("keep me\n")
        self.assertIn("ignored files", cleanup.prepare_archive(self.wt, self.ctx))

    def test_active_thread_before_removal_keeps_verified_worktree(self):
        self.assertIsNone(cleanup.prepare_archive(self.wt, self.ctx))
        fresh = dict(self.ctx, uses={str(self.path): [("Feature", "running")]})
        with patch.object(cleanup, "fresh_context", return_value=fresh):
            self.assertIn("running", cleanup.remove(self.wt, self.ctx))
        self.assertTrue(self.path.exists())


class ThreadActivityTests(unittest.TestCase):
    def test_family_activity_and_pins_protect_sibling_worktrees(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "state.sqlite"
            with sqlite3.connect(db) as con:
                con.executescript("""
                    create table projection_projects (workspace_root text, deleted_at text);
                    create table orchestration_v2_projection_threads
                        (thread_id text, title text, payload_json text, archived_at text,
                         deleted_at text, updated_at text);
                    create table orchestration_v2_projection_runs
                        (thread_id text, status text, requested_at text, completed_at text);
                    create table orchestration_v2_projection_messages
                        (thread_id text, updated_at text);
                """)
                old, recent = "2020-01-01T00:00:00Z", "2026-10-19T20:00:00Z"
                for tid, path in (("root", "/tmp/root-wt"), ("child", "/tmp/child-wt")):
                    payload = dict(worktreePath=path, lineage=dict(rootThreadId="root"), settledAt=old)
                    con.execute("insert into orchestration_v2_projection_threads values (?, ?, ?, null, null, ?)",
                                (tid, tid, json.dumps(payload), old))
                con.execute("insert into orchestration_v2_projection_messages values (?, ?)", ("child", recent))
            with patch.object(cleanup, "DB", db):
                uses, _, activity, ids = cleanup.t3_state()
                self.assertEqual(uses[cleanup.real("/tmp/root-wt")][0][1], "settled")
                self.assertEqual(activity[cleanup.real("/tmp/root-wt")], cleanup.timestamp(recent))
                self.assertEqual(ids[cleanup.real("/tmp/child-wt")], {"root"})
                with sqlite3.connect(db) as con:
                    con.execute("update orchestration_v2_projection_threads set payload_json = json_set(payload_json, '$.pinnedAt', ?) where thread_id = 'child'", (recent,))
                uses, _, _, ids = cleanup.t3_state()
                self.assertEqual(uses[cleanup.real("/tmp/root-wt")][0][1], "pinned")
                self.assertFalse(ids)


if __name__ == "__main__":
    unittest.main()
