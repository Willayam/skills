---
name: create-skill
description: Create or update portable Agent Skills using the skills.sh/Agent Skills format, then install them for both Claude Code and Codex. Use when the user wants to make a new skill, scaffold a SKILL.md, package a skill for skills.sh, or ensure one skill is available in both ~/.claude/skills and ~/.codex/skills.
---

# Create Skill

Create skills as portable Agent Skills first, then install that same source into agent-specific skill directories with the `skills` CLI.

## Default Workflow

1. Clarify the skill's purpose only when the user's request does not provide enough examples to write a useful `description`.
2. Pick a lowercase hyphenated skill name under 64 characters. The folder name and `name` frontmatter must match.
3. Create one canonical source directory, usually `~/.agents/skills/<skill-name>` for a global personal skill or `.agents/skills/<skill-name>` for a project skill.
4. Write `SKILL.md` in the Agent Skills format:
   - Required frontmatter: `name`, `description`.
   - Keep `description` under 1024 characters and include both what the skill does and when to use it.
   - Prefer only portable frontmatter. Add optional fields such as `compatibility`, `license`, `metadata`, or `allowed-tools` only when they are genuinely needed.
   - Keep the body concise and procedural. Put bulky docs in `references/`, deterministic helpers in `scripts/`, and templates in `assets/`.
5. Install the same source for Claude Code and Codex:

```bash
npx skills add ~/.agents/skills/<skill-name> -g -a claude-code -a codex -y
```

For a project-local skill, run this from the project root and omit `-g`:

```bash
npx skills add .agents/skills/<skill-name> -a claude-code -a codex -y
```

6. Verify discovery:

```bash
npx skills list -a claude-code -a codex
```

## Scripted Scaffold

Use `scripts/create_skill.py` when creating a straightforward new skill. It normalizes the name, creates a spec-compliant `SKILL.md`, optionally adds resource directories, and installs the source for both agents through `npx skills add`.

```bash
python3 scripts/create_skill.py "my-skill" \
  --description "Does X. Use when the user asks for Y." \
  --resources scripts,references
```

Useful flags:

- `--project`: create `.agents/skills/<name>` in the current project and install project-local links.
- `--no-install`: scaffold only.
- `--dry-run`: print the planned paths and commands.
- `--copy`: ask `skills add` to copy instead of symlink.

After running the script, edit the generated body with task-specific workflow knowledge before treating the skill as done.

## Gotchas

- Do not maintain separate Claude and Codex copies by hand. Use one canonical source and let `npx skills add ... -a claude-code -a codex` wire it into both agents.
- For Codex global skills, the target is `~/.codex/skills`. For Claude Code global skills, the target is `~/.claude/skills`. The shared canonical source can live elsewhere, commonly `~/.agents/skills`.
- The `skills` CLI defaults to project scope. Use `-g` for global installs.
- If publishing through skills.sh, keep the skill in a GitHub repository location the CLI can discover, such as the repo root, `skills/`, `.agents/skills/`, or `.claude/skills/`.
