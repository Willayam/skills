---
name: unconfuse
description: Audit a codebase for contradictions, inconsistent patterns, ambiguous defaults, and code-versus-doc mismatches that make AI agents guess. Use when the user says "unconfuse", wants a consistency audit, wants to reduce ambiguity, or wants the repo aligned so AI can work more confidently.
---

# Unconfuse

Make the codebase speak with one voice so the next agent can pick the right pattern on the first pass.

## When to use this skill

Use this skill when the user wants to:
- audit a specific area for conflicting patterns
- find contradictions between code and documentation
- identify ambiguous defaults or competing conventions
- remove dead conventions that still signal old patterns
- make the repository easier for AI agents to modify safely

If the user gives no focus area, ask what to audit. If the user says `full`, run the broad scan workflow below.

## Core rules

1. Code first, docs last. Discover the live patterns from source before opening `AGENTS.md`, `CLAUDE.md`, `README`, or `docs/`.
2. One obvious default. If two live approaches solve the same problem, surface the conflict and converge on one.
3. Subtract before you unify. Remove dead code, stale config, and unused conventions before migrating live code.
4. Ask before picking winners. When two live patterns compete, present the evidence and let the user choose the canonical one.

## Workflow

### 1. Scope the audit

- If the user names a focus area, stay inside it.
- If the user says `full`, start with a broad scan and identify the top 3-5 areas with the highest inconsistency.
- For broad scans, look first at places where AI agents often get mixed signals:
  - duplicate helpers for the same job
  - competing UI/component patterns
  - multiple data-fetching or state-management styles
  - schema or naming drift across files
  - stale scripts, config, or docs referencing removed behavior

### 2. Audit code first

Use local repo inspection tools. Prefer `rg` for searching and parallelize reads where it helps.

Investigation order:

1. Search source files for all variants of the pattern.
2. Count how many files use each variant.
3. Form conclusions from code alone.
4. Read docs last and compare them against the code findings.

Look for:
- conflicting patterns: two or more ways to do the same thing
- code-vs-doc mismatch: documentation says X, code does Y
- ambiguous defaults: no clear canonical path, so an agent would have to guess
- dead conventions: unused config, old imports, stale docs, obsolete scripts
- implicit knowledge: behavior that only works because of undocumented assumptions

For each finding, capture:
- severity: `HIGH`, `MEDIUM`, or `LOW`
- what is confusing
- file:line evidence for each competing pattern
- file counts for each variant when possible
- suggested next action: `CODE_FIX`, `REMOVE`, or `ASK_USER`

### 3. Report before changing live patterns

Present findings grouped by severity. For each contradiction, state:
- the competing patterns
- how many files use each one
- whether it is safe to remove immediately
- whether user input is required before changing live code

If two live patterns compete, do not silently choose one even if there is a majority. Present the evidence and ask which one should win.

### 4. Fix with tight scope

After the user approves a direction, fix one contradiction at a time in this order:

1. Remove dead patterns.
2. Align live code to the chosen pattern.
3. Add enforcement only if it is lightweight and clearly prevents regression.
4. Update documentation only after code is clear.

Fix rules:
- keep each contradiction fix atomic
- do not refactor beyond resolving the inconsistency
- do not change behavior unless the user explicitly approves it
- do not add explanatory comments to preserve dual patterns
- if a migration would touch 50+ files or cross multiple subsystems, ask before editing

### 5. Verify with a fresh pass

Re-run the same searches from scratch after edits. Do not rely on the original audit notes alone.

Verification should include:
- whether each original contradiction is gone
- whether any stale references remain
- whether new contradictions were introduced
- targeted lint, typecheck, or tests if the edits touched executable code

## Output format

Lead with findings. Keep the summary short.

Use this structure for each finding:

```md
Severity: HIGH
Area: icons
Confusion: Two live icon systems are used for the same UI surface.
Variants:
- `lucide-react` in 8 files
- custom SVG wrappers in 3 files
Evidence:
- `apps/web/src/components/nav.tsx:14`
- `apps/web/src/components/sidebar.tsx:9`
- `apps/web/src/components/icon.tsx:1`
Next action: ASK_USER
Suggested resolution: Pick one icon path, migrate the minority pattern, and remove stale wrappers.
```

If no contradictions are found, say so explicitly and note any residual risk from areas you did not inspect.
