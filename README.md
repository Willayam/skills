# skills

Shared agent skills packaged in the `skills.sh` style.

## Install

```bash
npx skills add https://github.com/willayam/skills --skill unconfuse
npx skills add https://github.com/willayam/skills --skill create-skill
npx skills add https://github.com/willayam/skills --skill advisor hormozi katie tony derek elon elon-algo charlie marcus naval steve
```

If you publish this under a different GitHub owner or repo name, update the URL accordingly.

## Layout

```text
skills/
├── README.md
└── skills/
    ├── advisor/
    ├── charlie/
    ├── create-skill/
    ├── derek/
    ├── elon/
    ├── elon-algo/
    ├── hormozi/
    ├── katie/
    ├── marcus/
    ├── naval/
    ├── steve/
    ├── tony/
    └── unconfuse/
```

## Included skills

- `create-skill`: Create or update portable Agent Skills and install them for Claude Code and Codex.
- `advisor`: Orchestrate multiple personal advisor lenses for big decisions.
- `charlie`: Channel Charlie Munger for inversion, incentives, and decision quality.
- `derek`: Channel Derek Sivers for simple, contrarian thinking.
- `elon`: Channel Elon Musk for first-principles, 10x thinking, and urgency.
- `elon-algo`: Apply Elon's Algorithm to systems, processes, code, products, and workflows.
- `hormozi`: Channel Alex Hormozi for offers, pricing, sales, and revenue math.
- `katie`: Channel Byron Katie for self-inquiry and The Work.
- `marcus`: Channel Marcus Aurelius for Stoic perspective and emotional regulation.
- `naval`: Channel Naval Ravikant for leverage, wealth, and long-term games.
- `steve`: Channel Steve Jobs for product taste, simplicity, and focus.
- `tony`: Channel Tony Robbins for outcomes, state, and massive action.
- `unconfuse`: Audit a codebase for contradictory patterns, ambiguous defaults, and code-versus-doc mismatches.
