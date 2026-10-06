#!/usr/bin/env python3
"""Create a portable Agent Skill and install it for Claude Code and Codex."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


DEFAULT_AGENTS = ("claude-code", "codex")


def normalize_name(value: str) -> str:
    name = value.strip().lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    if not name:
        raise ValueError("skill name must include at least one letter or number")
    if len(name) > 64:
        raise ValueError(f"normalized skill name is too long ({len(name)} > 64): {name}")
    return name


def validate_description(description: str) -> str:
    description = " ".join(description.split())
    if not description:
        raise ValueError("description is required")
    if len(description) > 1024:
        raise ValueError(f"description is too long ({len(description)} > 1024)")
    return description


def run(command: list[str], cwd: Path | None = None, dry_run: bool = False) -> None:
    printable = " ".join(command)
    if cwd:
        printable = f"(cd {cwd} && {printable})"
    print(printable)
    if dry_run:
        return
    subprocess.run(command, cwd=cwd, check=True)


def write_skill(skill_dir: Path, name: str, description: str, resources: list[str], force: bool) -> None:
    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists() and not force:
        raise FileExistsError(f"{skill_file} already exists; pass --force to overwrite")

    skill_dir.mkdir(parents=True, exist_ok=True)
    title = " ".join(part.capitalize() for part in name.split("-"))
    resource_lines = ""
    if resources:
        resource_lines = "\n## Resources\n\n"
        for resource in resources:
            resource_lines += f"- `{resource}/`: TODO: describe when to use this resource.\n"

    skill_file.write_text(
        f"""---
name: {name}
description: {description}
---

# {title}

## Workflow

1. TODO: Replace this with the first concrete step.
2. TODO: Add the checks, commands, or conventions that make this skill reliable.
3. TODO: State what to verify before finishing.
{resource_lines}""",
        encoding="utf-8",
    )

    for resource in resources:
        (skill_dir / resource).mkdir(exist_ok=True)


def install_command(skill_dir: Path, agents: list[str], global_scope: bool, copy: bool) -> list[str]:
    command = ["npx", "skills", "add", str(skill_dir)]
    if global_scope:
        command.append("-g")
    for agent in agents:
        command.extend(["-a", agent])
    if copy:
        command.append("--copy")
    command.append("-y")
    return command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Skill name or title. It will be normalized to lowercase hyphen-case.")
    parser.add_argument(
        "--description",
        required=True,
        help="Frontmatter description. Include what the skill does and when to use it.",
    )
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated resource directories to create: scripts,references,assets.",
    )
    parser.add_argument(
        "--source-root",
        default=None,
        help="Canonical source root. Defaults to ~/.agents/skills globally or .agents/skills with --project.",
    )
    parser.add_argument("--project", action="store_true", help="Create and install a project-local skill.")
    parser.add_argument("--agent", action="append", dest="agents", help="Agent target for skills add. Repeatable.")
    parser.add_argument("--copy", action="store_true", help="Copy instead of symlink during skills add.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing SKILL.md.")
    parser.add_argument("--no-install", action="store_true", help="Create files but skip npx skills add.")
    parser.add_argument("--dry-run", action="store_true", help="Print paths and commands without changing files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        name = normalize_name(args.name)
        description = validate_description(args.description)
        resources = [item.strip() for item in args.resources.split(",") if item.strip()]
        invalid_resources = sorted(set(resources) - {"scripts", "references", "assets"})
        if invalid_resources:
            raise ValueError(f"unsupported resources: {', '.join(invalid_resources)}")

        source_root = Path(args.source_root).expanduser() if args.source_root else None
        if source_root is None:
            source_root = Path(".agents/skills") if args.project else Path.home() / ".agents" / "skills"
        skill_dir = source_root / name
        agents = args.agents or list(DEFAULT_AGENTS)

        print(f"skill: {name}")
        print(f"source: {skill_dir}")
        print(f"agents: {', '.join(agents)}")
        print(f"scope: {'project' if args.project else 'global'}")

        if not args.dry_run:
            write_skill(skill_dir, name, description, resources, args.force)
        if not args.no_install:
            run(install_command(skill_dir, agents, not args.project, args.copy), dry_run=args.dry_run)
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
