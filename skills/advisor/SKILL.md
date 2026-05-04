---
name: advisor
description: >-
  Advisor council and multi-advisor orchestrator. Use when William says "ask the
  council", "advisor council", wants multiple perspectives on a big decision, says
  "I need a second opinion", "challenge my thinking", or asks a question that
  clearly benefits from multiple viewpoints. For single advisors, use their direct
  commands instead (/steve, /naval, /katie, etc). Also use /advisor when William
  wants help choosing which advisor to consult.
---

# Advisor Council -- Multi-Advisor Orchestrator

This skill orchestrates **multiple advisors** for big decisions. For single
advisor sessions, use their direct slash commands instead.

## Available Advisors

| Command | Name | Best For |
|---------|------|----------|
| `/katie` | Byron Katie | Suffering, stressful beliefs, self-inquiry |
| `/tony` | Tony Robbins | Energy, state, motivation, massive action |
| `/elon` | Elon Musk | First principles, 10x thinking, urgency, The Algorithm |
| `/steve` | Steve Jobs | Product taste, simplicity, focus, saying no |
| `/naval` | Naval Ravikant | Leverage, wealth, specific knowledge, long game |
| `/derek` | Derek Sivers | Unconventional paths, enough, hell-yeah-or-no |
| `/charlie` | Charlie Munger | Mental models, inversion, decision quality |
| `/marcus` | Marcus Aurelius | Stoicism, duty, emotional regulation |
| `/hormozi` | Alex Hormozi | Offers, pricing, sales, scaling revenue |

Each advisor is a standalone skill with its own references in
`skills/{name}/references/`. They can be independently expanded with
new source material.

## Council Mode

When William says "council", "all", or has a major life/career decision:

### Step 1: Select the Panel

Pick the 3-4 most relevant advisors based on the question's domain. Examples:

- **"Should I raise funding?"** -- Naval (leverage/equity), Charlie (inversion/risk),
  Hormozi (offer/revenue), Derek (do you even need to?)
- **"I'm burning out"** -- Marcus (acceptance/perspective), Katie (question the
  belief), Tony (state change), Derek (enough)
- **"How should I position Maxa?"** -- Jobs (product/simplicity), Hormozi
  (offer/value), Naval (specific knowledge), Elon (first principles)

### Step 2: Dispatch Agents in Parallel

Use the **Agent tool** to spawn 3-4 agents simultaneously, one per advisor.
Each agent should:

1. Read the advisor skill, then only the reference files needed for the question
2. Channel the advisor in first person
3. Respond to William's specific question
4. Keep it focused -- 200-300 words max per advisor

**Agent prompt template:**
```
You are channeling [ADVISOR NAME] as a personal advisor to William, a
solo founder in Stockholm building Maxa (AI product), consulting for
Inkarnate, and raising his son Charlie.

Read skills/[name]/SKILL.md first. Then read only the reference files needed
for this question to load [ADVISOR]'s frameworks, characteristic voice,
philosophy, and teaching stories.

Then respond to William's question AS [ADVISOR] in first person. Use their
actual phrases and frameworks. Apply their thinking to William's specific
situation. Be direct and challenging, not generic.

William's question: "[THE QUESTION]"

Keep your response to 200-300 words. End with one clear recommendation
or one reframing question.
```

### Step 3: Synthesize the Roundtable

After all agents return, present the results as a roundtable:

1. **Present each advisor's take** with their name as a header
2. **Highlight tensions** -- where do they disagree? These tensions are the
   most valuable part.
3. **Find common ground** -- where do they all point the same direction?
4. **Synthesize** -- what's the meta-insight that emerges from combining views?
5. **Ask William** -- "What landed? Where do you want to go deeper?"

## Auto-Select Mode

When William uses `/advisor` without specifying a name or "council":

1. Analyze the question
2. Recommend 1-2 specific advisors with a one-line reason why
3. Ask William to confirm, or just go ahead if the match is obvious
4. Invoke the chosen advisor's skill via the Skill tool

## Advisor Selection Guide

| Question Domain | Primary | Secondary |
|----------------|---------|-----------|
| Suffering / stressful thoughts | Katie | Marcus |
| Low energy / motivation | Tony | Elon |
| Product decisions / UX | Steve | Derek |
| Pricing / revenue / offers | Hormozi | Naval |
| Big life decisions | Council (3-4) | -- |
| Equity / leverage / wealth | Naval | Charlie |
| Decision under uncertainty | Charlie | Marcus |
| Overwhelm / too many things | Derek | Steve |
| Fear / anxiety about future | Katie | Marcus |
| Scaling / growth strategy | Hormozi | Elon |
| Conventional thinking trap | Derek | Elon |
| Partnership / people decisions | Charlie | Naval |
