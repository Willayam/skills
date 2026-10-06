# skills

Agent skills for Claude Code and Codex, packaged in the `skills.sh` style. Each skill is a
top-level directory with a `SKILL.md` and optional `references/`, `scripts/`, `agents/`, and
`evals/`.

## Install

```bash
npx skills add https://github.com/Willayam/skills --skill unconfuse
npx skills add https://github.com/Willayam/skills --skill advisor charlie derek elon hormozi katie marcus naval steve tony
```

## Skills

Engineering:

- `commit`: Split a dirty worktree into small, reviewable commits grouped by intent.
- `create-skill`: Create or update portable Agent Skills and install them for Claude Code and Codex.
- `unconfuse`: Audit a codebase for contradictory patterns, ambiguous defaults, and code-versus-doc mismatches.
- `codex-implementation`: Hand a scoped, well-specified change to Codex CLI, then verify its diff.
- `codex-review`: Get an independent Codex CLI review of uncommitted changes, a branch diff, or a commit.
- `codex-computer-use`: Have Codex CLI drive a browser, simulator, or running app to verify behavior.

Research:

- `scientific-research`: Find peer-reviewed studies across OpenAlex, Semantic Scholar, and PubMed, with funding and conflict-of-interest checks.

Advisors:

- `advisor`: Orchestrate several advisor lenses for big decisions.
- `charlie`: Charlie Munger on inversion, incentives, and decision quality.
- `derek`: Derek Sivers on simple, contrarian thinking.
- `elon`: Elon Musk on first principles, urgency, and the Algorithm.
- `hormozi`: Alex Hormozi on offers, pricing, sales, and revenue math.
- `katie`: Byron Katie on self-inquiry and The Work.
- `marcus`: Marcus Aurelius on Stoic perspective and emotional regulation.
- `naval`: Naval Ravikant on leverage, wealth, and long-term games.
- `steve`: Steve Jobs on product taste, simplicity, and focus.
- `tony`: Tony Robbins on outcomes, state, and massive action.
