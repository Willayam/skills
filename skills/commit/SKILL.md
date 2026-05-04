---
name: commit
description: Split all current repository changes into coherent, self-contained git commits. Use when the user asks for /commit, asks to commit everything, commit in logical chunks, split a dirty working tree into multiple commits, or prepare a clean commit series from existing changes.
---

# Commit

Turn a dirty working tree into a readable commit series where each commit has one purpose and can be reviewed or reverted on its own.

## Core rules

1. Preserve user work. Never discard, rewrite, or revert changes unless the user explicitly asks.
2. Commit everything relevant in the working tree, including untracked files and deletions, unless a change looks unsafe to commit.
3. Keep commits atomic: one behavior, one concern, one docs update, or one mechanical move per commit.
4. Do not push, amend, rebase, squash, or tag unless the user explicitly asks.
5. Stop and ask before committing secrets, large binaries, unresolved conflict markers, broken generated output, or changes whose ownership is unclear.

## Workflow

### 1. Inventory the tree

Run:

```bash
git status --short
git diff --stat
git diff --name-status
git diff --cached --name-status
```

Also inspect untracked files before adding them. Use `git diff -- <path>` for modified files and `sed`, `rg`, or file-specific tools for untracked files.

If the repository gives a target branch, compare against it for context:

```bash
git diff <target-branch>...
```

### 2. Identify commit groups

Group changes by purpose, not by file type alone.

Common groups:

- feature implementation
- bug fix
- tests for the behavior
- documentation or skill metadata
- mechanical rename, move, or formatting-only change
- generated lockfile or build artifact update paired with the source change that requires it

Avoid mixing:

- behavior changes with broad formatting
- docs-only edits with executable code
- unrelated features
- generated churn with manual source edits unless the generated file is required by that source edit

### 3. Stage one group at a time

Prefer path staging when an entire file belongs to one group:

```bash
git add -- path/to/file another/path
```

Use patch staging when one file contains multiple logical changes:

```bash
git add -p -- path/to/file
```

After staging, verify the exact commit contents:

```bash
git diff --cached --stat
git diff --cached
```

If the staged diff includes unrelated lines, unstage and split more carefully:

```bash
git restore --staged -- path/to/file
```

### 4. Commit with clear messages

Use short imperative subjects, usually under 72 characters:

```bash
git commit -m "Add logical commits skill"
```

Add a body only when the why is not obvious or the commit has multiple notable parts:

```bash
git commit -m "Refactor skill metadata loading" -m "Keeps installed skill discovery aligned with the repository layout."
```

### 5. Repeat until clean

After each commit, run:

```bash
git status --short
```

Continue grouping, staging, reviewing, and committing until no intended changes remain.

### 6. Verify the result

Review the final series:

```bash
git log --oneline --decorate -n 10
git status --short
```

Run targeted tests, lint, or formatting checks when the committed changes touch executable code. If verification is skipped, state why.

## Output format

Finish with:

- commit hashes and subjects in order
- any files intentionally left uncommitted
- verification commands run and their results
- any risks or follow-up needed
