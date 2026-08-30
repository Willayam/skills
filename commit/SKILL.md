---
name: commit
description: Split an existing dirty worktree into small, reviewable Git commits grouped by intent. Use when the user asks for /commit, to commit logical chunks, split changes into commits, make atomic commits, or clean up a working tree into meaningful commits without changing unrelated work.
---

# /commit

Turn a dirty worktree into a short series of commits that each explain one coherent change.

## When to Use

Use this skill when the user asks to:

- `/commit`
- commit current changes in logical chunks
- split a large diff into atomic commits
- create clean commits from mixed staged, unstaged, or untracked work
- prepare a branch for review by organizing local changes

Do not use this skill for history rewriting, squashing, rebasing, pushing, or opening a PR unless the user explicitly asks for those actions too.

## Core Rules

1. Preserve user work. Never discard, overwrite, or revert changes just to make staging easier.
2. Commit by intent, not by file type. A commit should answer "what behavior or artifact changed?".
3. Keep each commit independently understandable and preferably independently buildable.
4. Inspect the staged diff before every commit.
5. Use the repository's existing commit-message style when one is visible.
6. Stop and ask before committing secrets, unrelated personal files, huge generated artifacts, or changes whose purpose cannot be inferred.

## Workflow

### 1. Establish Context

Inspect the repository state before staging anything:

```bash
git status --short
git branch --show-current
git log --oneline -5
git diff --stat
git diff
git diff --cached
```

If the repo has contributor or agent instructions, read the relevant files before committing. If there are already staged changes, treat them as user-selected until proven otherwise; inspect them and avoid mixing new content into them accidentally.

### 2. Classify the Diff

Group changes by durable intent. Common buckets:

- product behavior or bug fix
- tests for that behavior
- documentation for changed behavior
- mechanical formatting or generated lockfile updates
- build configuration or dependency changes
- preparatory refactor with no behavior change

Prefer combining tests with the behavior they verify. Split tests only when they cover multiple independent behavior changes or when the repository's norm is separate test commits.

Flag anything suspicious before committing:

- secrets, tokens, credentials, private keys, or `.env` files
- local editor files, machine-specific paths, caches, logs, or screenshots
- generated files that are not normally checked in
- unrelated changes in the same file that require hunk-level staging

### 3. Plan the Commit Order

Write a short commit plan before staging:

1. prerequisite config, schema, or dependency changes
2. refactors that make later behavior changes small
3. behavior changes with their tests
4. docs or examples that depend on the final behavior
5. mechanical cleanup or generated artifacts, if they must be committed separately

If two commits would not make sense independently, merge them. If one commit has more than one reason to change, split it.

### 4. Stage Precisely

Use pathspecs for cleanly separated files:

```bash
git add path/to/file
```

Use interactive or patch staging for mixed files:

```bash
git add -p path/to/file
```

For untracked files, inspect contents before staging:

```bash
sed -n '1,220p' path/to/file
git add path/to/file
```

After staging each chunk, verify exactly what will be committed:

```bash
git diff --cached --stat
git diff --cached
git status --short
```

If the staged diff includes unrelated content, unstage only the mistaken paths or hunks and restage carefully. Do not use destructive reset or checkout commands.

### 5. Verify the Chunk

Run the narrowest meaningful checks before each commit when feasible:

```bash
git diff --check --cached
```

For code changes, prefer the repo's formatter, typecheck, tests, and validators that apply to the staged chunk. If checks are expensive, run targeted checks per commit and a broader check after the final commit.

If verification fails, fix the issue in the appropriate chunk before committing. If a fix belongs to an earlier staged chunk, adjust the staging so the final commit remains coherent.

### 6. Commit

Match the existing message style from recent commits. If there is no clear style, use a concise imperative subject:

```bash
git commit -m "Add note validation for article titles"
```

Good subjects name the intent. Avoid vague subjects such as:

- `update files`
- `fix stuff`
- `misc changes`
- `wip`

Use a body when the reason is not obvious from the diff, when there are tradeoffs, or when validation context matters.

### 7. Repeat and Final Check

Repeat classification, staging, verification, and commit until all intended changes are committed.

After the final commit, run:

```bash
git status --short
git log --oneline -5
```

If any changes remain, explain whether they were intentionally left uncommitted and why.

## Final Response

Report:

- commit hashes and subjects, in order
- checks run and whether they passed
- any files or changes intentionally left uncommitted
- any risks, skipped checks, or follow-up needed
