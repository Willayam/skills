---
name: t3-worktree-cleanup
description: Weekly unattended git worktree cleanup on a machine running T3 Code. Use to set up the scheduled cleanup on a new machine, to run it by hand, or to act on worktrees a run held back.
---

# T3 worktree cleanup

`scripts/cleanup.py` finds every git worktree on the machine and removes the ones that are done.
It reads T3's state database read-only to see which threads use which worktree. A dry run is the
default, and `--apply` removes things.

```bash
python3 ~/Development/skills/t3-worktree-cleanup/scripts/cleanup.py          # report only
python3 ~/Development/skills/t3-worktree-cleanup/scripts/cleanup.py --apply  # remove what passes
```

## What it removes

Only worktrees inside an agent worktree folder are candidates. Those folders are `~/.t3/worktrees`,
`~/.codex/worktrees`, `~/.cursor/worktrees`, `~/conductor/workspaces`, and a repo's
`.claude/worktrees`. A candidate goes when all of these hold:

- No running, pinned, or open T3 thread uses it. A running delegated thread keeps its whole family
  in use.
- No process has its working directory inside it.
- It has no uncommitted edits, no files hidden by `assume-unchanged` or `skip-worktree`, and no
  untracked files. Untracked symlinks don't count.
- Every ignored file in it is build output, an env file copied in by setup, or agent scratch.
  Scratch is `.context/` and the local database `wrangler dev` keeps in `.wrangler/state`. The
  report names the scratch it deletes. Anything else ignored, like a `tmp/` of exports, holds it.
- No rebase, merge, cherry-pick, revert, or bisect is paused in it.
- It is not locked, contains no other checkout or nested git repo, and no T3 project points at it or inside it.
- Either every T3 thread that used it is archived, or it has been idle for a day and it is done.
  Done means everything in it is on the default branch, or its PR is merged or closed and holds
  every commit in it.

Everything else is held, and the report names the reason. Archiving a thread is how to let its
worktree go at the next run. Right before each removal the script checks everything again, then
runs `git worktree remove` without `--force`, so git refuses anything that changed. It stops
without removing anything if T3's database or `lsof` can't be read. If a fetch fails, nothing in
that repo counts as merged. Branches survive removal, so a removed worktree can come back with
`git worktree add <path> <branch>`. Folders git doesn't know as worktrees and registered
worktrees whose folder is gone are listed and left alone.

## Set up on a machine

1. Clone or pull this repo to `~/Development/skills`.
2. In T3, start a thread in a project whose root is not a worktree, such as a `Development`
   project at `~/Development`. Use gpt-6.1-sol at low effort and the project's root checkout.
3. In that thread, call `schedule_task` with the prompt below,
   `schedule: {"type":"interval","everyMs":604800000}`, and `bindToCurrentThread: true`. Then call
   `run_scheduled_task_now` once and check the report.

Bind it to the thread. An unbound schedule creates a new worktree from `main` for every run. Use
an interval, not a fixed time. T3 skips a fixed-time run missed by more than ten minutes, so a
sleeping laptop would miss it. An overdue interval run fires once when the app is back. The run
uses the model of the thread that called `schedule_task`.

Run prompt:

```text
Weekly worktree cleanup. Run `python3 ~/Development/skills/t3-worktree-cleanup/scripts/cleanup.py --apply` with a command timeout of at least 15 minutes, since it takes a few. Reply with its report exactly as printed, and if it failed, say what failed. Don't remove anything it held and don't clean anything else. If I later ask you to remove a held worktree, read ~/Development/skills/t3-worktree-cleanup/SKILL.md first.
```

## Acting on held worktrees

When the user asks to remove something a run held, follow the gates in pstack's
`poteto-mode/playbooks/worktree-cleanup.md`. Never remove a worktree a running, pinned, or open
thread uses. For uncommitted edits, show the diff and ask. If the user wants to keep them, commit
them to a local `wip/<branch>` branch first, and leave out `node_modules` links, caches, and
anything secret or private. Name untracked files before deleting them. Report free space before and
after.
