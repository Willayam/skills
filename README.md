# skills

Shared agent skills packaged in the `skills.sh` style.

## Install

```bash
npx skills add https://github.com/willayam/skills --skill unconfuse
npx skills add https://github.com/willayam/skills --skill create-skill
```

If you publish this under a different GitHub owner or repo name, update the URL accordingly.

## Layout

```text
skills/
├── README.md
└── skills/
    ├── create-skill/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── scripts/
    │       └── create_skill.py
    └── unconfuse/
        ├── SKILL.md
        └── agents/
            └── openai.yaml
```

## Included skills

- `create-skill`: Create or update portable Agent Skills and install them for Claude Code and Codex.
- `unconfuse`: Audit a codebase for contradictory patterns, ambiguous defaults, and code-versus-doc mismatches.
