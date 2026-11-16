---
name: t3-worktree-cleanup
description: Nightly git worktree backup and cleanup on a machine running T3 Code. Use to set up the schedule, archive clean work idle for seven days, or review worktrees a run held back.
---

# T3 worktree cleanup

`scripts/cleanup.py` finds Git worktrees, backs up stale work, and removes recoverable checkouts.
It reads T3's state database read-only to see which threads use which worktree. A dry run is the
default. `--apply` performs the selected backup or cleanup action.

```bash
python3 ~/Development/skills/t3-worktree-cleanup/scripts/cleanup.py          # report only
python3 ~/Development/skills/t3-worktree-cleanup/scripts/cleanup.py --apply  # remove what passes
python3 ~/Development/skills/t3-worktree-cleanup/scripts/cleanup.py --prepare-archives  # stale-work report
python3 ~/Development/skills/t3-worktree-cleanup/scripts/cleanup.py --prepare-archives --apply  # push backups, never remove
```

## Seven-day archive flow

Run preparation before cleanup. Preparation considers the newest source-file modification,
checkout, index update, and activity anywhere in the associated T3 thread family. Unknown
activity holds the worktree. Running, pinned, or open threads, live processes, and open PRs
stay protected. Uncommitted, untracked, hidden, and meaningful ignored files stay for review.

For clean work idle at least seven days, preparation creates an `archive/` branch on `origin`.
The name includes the source branch, a worktree identifier, and the full commit hash. An empty
Git lease permits creation only. An existing archive branch must have exactly the same hash.
Preparation verifies the hash directly on the remote before reporting success. It never commits
files, removes worktrees, edits the T3 database, or closes PRs.

Install Gitleaks with `brew install gitleaks`. Before pushing unpublished history, preparation
scans it with Gitleaks' default rules, including older commits. Repository ignore rules cannot
disable this scan. Missing Gitleaks, scan failures, and possible secrets hold the worktree.
Secret scanning reduces risk; it cannot prove that arbitrary private information is absent.

After successful preparation, archive only the `Thread IDs` printed under
`Remote backups verified, ready for thread archive and cleanup`, using T3's
`t3_thread_organize` tool with `action: "archive"`. Check current thread state first and skip
anything that became active, pinned, or used within the last seven days. A root thread is listed only when all its existing
associated worktrees have verified backups in this run. If the archive tool is unavailable
or fails, report that fact. Never write directly to T3's database.

Then run normal `--apply` cleanup. It checks usage, clean state, and remote recovery again.
An archived thread alone is no longer enough to permit deletion. The report includes the
archive ref, commit hash, and commands to fetch and recreate each prepared worktree.
Keep archive branches until the user explicitly asks to remove them.

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
- It has a verified archive backup and its threads are archived or it has been idle for seven
  days; or it has been idle for a day and is done. Done means its commits are on the fetched
  default branch, or its merged/closed PR includes every commit and a current remote branch
  still contains them.

Everything else is held, and the report names the reason. Archiving a thread is how to let its
worktree go at the next run. Right before each removal the script checks everything again, then
runs `git worktree remove` without `--force`, so git refuses anything that changed. It stops
without removing anything if T3's database or `lsof` can't be read. If a fetch fails, nothing in
that repo counts as merged. Branches survive removal, so a removed worktree can come back with
`git worktree add <path> <branch>`. Folders git doesn't know as worktrees and registered
worktrees whose folder is gone are listed and left alone.

## Set up on a machine

1. Clone or pull this repo to `~/Development/skills`.
2. Install Gitleaks with `brew install gitleaks`. Without it, worktrees with unpushed commits are
   held instead of backed up.
3. Install Fleet's nightly job from the Fleet checkout with `/usr/bin/python3 ops/nightly.py install`.
   It runs `--prepare-archives --apply` and then `--apply` every night at 03:30, or on wake if the
   Mac slept through it. The "Nightly upkeep" section of the Fleet README describes the job.

The job can't archive T3 threads. Each Mac's T3 task "Nightly machine check" reads the job's report
and archives the threads listed under `Thread IDs`, using the checks in the archive flow above.
Schedule it in a project whose root is not a worktree, so a run doesn't create a worktree. On a
laptop, use an interval schedule. T3 skips a fixed-time run missed by more than ten minutes.

## Acting on held worktrees

When the user asks to remove something a run held, follow the gates in pstack's
`poteto-mode/playbooks/worktree-cleanup.md`. Never remove a worktree a running, pinned, or open
thread uses. For uncommitted edits, show the diff and ask. If the user wants to keep them, commit
them to a local `wip/<branch>` branch first, and leave out `node_modules` links, caches, and
anything secret or private. Name untracked files before deleting them. Report free space before and
after.
