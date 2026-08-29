# skills

Shared agent skills packaged in the `skills.sh` style.

## Install

```bash
npx skills add https://github.com/YOUR-USERNAME/skills --skill unconfuse
npx skills add https://github.com/YOUR-USERNAME/skills --skill create-skill
npx skills add https://github.com/YOUR-USERNAME/skills --skill commit
npx skills add https://github.com/YOUR-USERNAME/skills --skill behavioral-design-audit
npx skills add https://github.com/YOUR-USERNAME/skills --skill inquiry
npx skills add https://github.com/YOUR-USERNAME/skills --skill advisor hormozi katie tony derek elon charlie marcus naval steve
```

If you publish this under a different GitHub owner or repo name, update the URL accordingly.

## Layout

```text
skills/
├── README.md
└── skills/
    ├── advisor/
    ├── behavioral-design-audit/
    ├── charlie/
    ├── commit/
    ├── create-skill/
    ├── derek/
    ├── elon/
    ├── hormozi/
    ├── inquiry/
    ├── katie/
    ├── marcus/
    ├── naval/
    ├── steve/
    ├── tony/
    └── unconfuse/
```

## Included skills

- `create-skill`: Create or update portable Agent Skills and install them for Claude Code and Codex.
- `commit`: Split all current repository changes into coherent, self-contained git commits. Invoke as `/commit`.
- `advisor`: Orchestrate multiple personal advisor lenses for big decisions.
- `behavioral-design-audit`: Audit apps or websites for behavioral design patterns, dark patterns, engagement mechanics, and ethical persuasive design.
- `charlie`: Channel Charlie Munger for inversion, incentives, and decision quality.
- `derek`: Channel Derek Sivers for simple, contrarian thinking.
- `elon`: Channel Elon Musk for first-principles, 10x thinking, urgency, and Elon's Algorithm.
- `inquiry`: Ledger of stressful beliefs worked through with The Work. Capture, mine, review, work, status.
- `hormozi`: Channel Alex Hormozi for offers, pricing, sales, and revenue math.
- `katie`: Channel Byron Katie for self-inquiry and The Work.
- `marcus`: Channel Marcus Aurelius for Stoic perspective and emotional regulation.
- `naval`: Channel Naval Ravikant for leverage, wealth, and long-term games.
- `steve`: Channel Steve Jobs for product taste, simplicity, and focus.
- `tony`: Channel Tony Robbins for outcomes, state, and massive action.
- `unconfuse`: Audit a codebase for contradictory patterns, ambiguous defaults, and code-versus-doc mismatches.
