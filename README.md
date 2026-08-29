# skills

Shared agent skills packaged in the `skills.sh` style. Each skill is a top-level directory
containing a `SKILL.md`, plus optional `references/`, `scripts/`, `agents/`, and `evals/`.

## Install

```bash
npx skills add https://github.com/Willayam/skills --skill unconfuse
npx skills add https://github.com/Willayam/skills --skill create-skill
npx skills add https://github.com/Willayam/skills --skill commit
npx skills add https://github.com/Willayam/skills --skill behavioral-design-audit
npx skills add https://github.com/Willayam/skills --skill inquiry
npx skills add https://github.com/Willayam/skills --skill codex-implementation codex-review codex-computer-use
npx skills add https://github.com/Willayam/skills --skill advisor hormozi katie tony derek elon charlie marcus naval steve
```

## Layout

```text
skills/
├── README.md
├── advisor/
├── behavioral-design-audit/
├── charlie/
├── codex-computer-use/
├── codex-implementation/
├── codex-review/
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
- `unconfuse`: Audit a codebase for contradictory patterns, ambiguous defaults, and code-versus-doc mismatches.
- `behavioral-design-audit`: Audit apps or websites for behavioral design patterns, dark patterns, engagement mechanics, and ethical persuasive design.
- `inquiry`: Ledger of stressful beliefs worked through with The Work. Capture, mine, review, work, status.
- `codex-implementation`: Hand a scoped, well-specified change to Codex CLI, then verify its diff.
- `codex-review`: Get an independent Codex CLI review of uncommitted changes, a branch diff, or a commit.
- `codex-computer-use`: Have Codex CLI drive a browser, simulator, or running app to verify behavior.
- `advisor`: Orchestrate multiple personal advisor lenses for big decisions.
- `charlie`: Channel Charlie Munger for inversion, incentives, and decision quality.
- `derek`: Channel Derek Sivers for simple, contrarian thinking.
- `elon`: Channel Elon Musk for first-principles, 10x thinking, urgency, and Elon's Algorithm.
- `hormozi`: Channel Alex Hormozi for offers, pricing, sales, and revenue math.
- `katie`: Channel Byron Katie for self-inquiry and The Work.
- `marcus`: Channel Marcus Aurelius for Stoic perspective and emotional regulation.
- `naval`: Channel Naval Ravikant for leverage, wealth, and long-term games.
- `steve`: Channel Steve Jobs for product taste, simplicity, and focus.
- `tony`: Channel Tony Robbins for outcomes, state, and massive action.
