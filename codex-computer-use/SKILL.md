---
name: codex-computer-use
description: Ask Codex CLI (gpt-5.6-sol) to run local app verification that needs computer use: browser automation, simulators, screenshots, app launching, or independent runtime inspection. This is how gpt-5.6-sol is invoked for computer-use work. Use when the user asks Claude to have Codex test a flow, verify UI behavior, inspect a running app, capture screenshots, or report confirmation and feedback about implemented behavior that benefits from computer use functionality.
---

# Codex Computer Use

Use Codex as a separate local verification agent when the task needs real UI interaction,
screenshots, simulator/browser/device state, or an independent runtime check outside Claude's
current context.

Do not use this for ordinary code reading, typechecking, linting, or tests Claude can run
directly. Launching apps, simulators, or browsers to verify the requested work is fine without
asking; ask first only if the run could disrupt the user's environment beyond that (closing
their apps, changing system settings, acting on real accounts or data).

## Workflow

1. Create a temporary artifact directory.
2. Give Codex a self-contained prompt with the repo path, exact flow, constraints, artifact directory, and report format.
3. Run `codex exec` non-interactively.
4. Read Codex's report, inspect or reference screenshot paths, and summarize the result for the user.

Use this command shape:

```bash
ARTIFACT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/codex-computer-use.XXXXXX")"
REPORT="$ARTIFACT_DIR/report.md"
PROMPT="$ARTIFACT_DIR/prompt.md"

# Write a self-contained prompt to $PROMPT, then run:
codex exec \
  -C "$PWD" \
  --add-dir "$ARTIFACT_DIR" \
  -s danger-full-access \
  -o "$REPORT" \
  "$(cat "$PROMPT")"
```

Use `-s danger-full-access` because launching apps, simulators, and browsers needs
machine-level access. Point Codex at `$ARTIFACT_DIR` for screenshots so the paths are easy to
inspect afterward.

## Prompt Requirements

Tell Codex:

- The repo path and how to launch or reach the running app.
- The exact flow to exercise and what correct behavior looks like.
- To capture screenshots into the artifact directory at key steps.
- Not to act on real accounts, data, or system settings beyond the verification.
- To write a report with what it did, what it observed, screenshot paths, and any failures.

## Reporting Back

Read Codex's report and reference the screenshots before summarizing. Separate what Codex
confirmed working from what it flagged.

If `codex` is not installed or the command fails, report the error and offer to verify the
change directly instead.
