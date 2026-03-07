# skills

Shared agent skills packaged in the `skills.sh` style.

## Install

```bash
npx skills add https://github.com/willayam/skills --skill unconfuse
```

If you publish this under a different GitHub owner or repo name, update the URL accordingly.

## Layout

```text
skills/
├── README.md
└── skills/
    └── unconfuse/
        ├── SKILL.md
        └── agents/
            └── openai.yaml
```

## Included skills

- `unconfuse`: Audit a codebase for contradictory patterns, ambiguous defaults, and code-versus-doc mismatches.
