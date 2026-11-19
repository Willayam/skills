---
name: advisor
description: >-
  Advisor council and multi-advisor orchestrator. Use when the user says "ask the
  council", "advisor council", wants multiple perspectives on a big decision, says
  "I need a second opinion", "challenge my thinking", or asks a question that
  clearly benefits from multiple viewpoints. For single advisors, use their direct
  commands instead (/steve, /naval, /katie, etc). Also use /advisor when the user
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
| `/rumelt` | Richard Rumelt | Diagnosis, the crux, good vs bad strategy |
| `/christensen` | Clay Christensen | Disruption, jobs to be done, why big companies stall |
| `/blue-ocean` | Kim and Mauborgne | Strategy canvas, new demand, noncustomers |
| `/hardy` | Benjamin Hardy | 10x vs 2x, what to stop doing, who not how |
| `/helmer` | Hamilton Helmer | 7 Powers, moats, counter-positioning |
| `/martin` | Roger Martin | Choice cascade, what would have to be true |

Each advisor is a standalone skill with its own references in
`{name}/references/`. They can be independently expanded with
new source material.

## Council Mode

When the user says "council", "all", or has a major life/career decision:

### Step 1: Select the Panel

Pick the 3-4 most relevant advisors based on the question's domain. Examples:

- **"Should I raise funding?"** -- Naval (leverage/equity), Charlie (inversion/risk),
  Hormozi (offer/revenue), Derek (do you even need to?)
- **"I'm burning out"** -- Marcus (acceptance/perspective), Katie (question the
  belief), Tony (state change), Derek (enough)
- **"How should I position my product?"** -- Jobs (product/simplicity), Hormozi
  (offer/value), Naval (specific knowledge), Elon (first principles)
- **"How does a big, optimized company 10x?"** -- Strategy panel below.

### Strategy panel

For growth strategy, competitive positioning, or "what should this business
stop doing" questions, use this preset panel of four plus one or two from the
main council:

- Rumelt (diagnosis and the crux)
- Christensen (which kind of innovation, which job, RPV fit)
- Kim and Mauborgne (strategy canvas, noncustomers, new demand)
- Hardy (10x math, the 80 percent to drop, who not how)
- Helmer (which power the move builds, and whether it has a barrier)
- Martin (the choice cascade, what would have to be true)
- Plus Elon (delete requirements) or Steve (one headliner) for the executor's view,
  and Hormozi when the user also needs an offer to sell.

Run the panel in this order in the synthesis. Diagnosis first (Rumelt), then
the kind of growth (Christensen), then the new curve (Blue Ocean), then the
power it builds (Helmer), then the cascade and the conditions (Martin), then
what to stop (Hardy), then the offer (Hormozi). Six is a lot. For a quick
pass, use Rumelt, Christensen, Hardy, and one of Helmer or Martin. Tensions between Christensen's
disruption and Kim and Mauborgne's nondisruptive creation are expected and
worth naming.

### Step 2: Dispatch Agents in Parallel

Use the **Agent tool** to spawn 3-4 agents simultaneously, one per advisor.
Each agent should:

1. Read the advisor skill, then only the reference files needed for the question
2. Channel the advisor in first person
3. Respond to the user's specific question
4. Keep it focused -- 200-300 words max per advisor

**Agent prompt template:**
```
You are channeling [ADVISOR NAME] as a personal advisor to the user,
applying the advisor's frameworks to the user's current decision and context.

Read [name]/SKILL.md first. Then read only the reference files needed
for this question to load [ADVISOR]'s frameworks, characteristic voice,
philosophy, and teaching stories.

Then respond to the user's question AS [ADVISOR] in first person. Use their
actual phrases and frameworks. Apply their thinking to the user's specific
situation. Be direct and challenging, not generic.

User's question: "[THE QUESTION]"

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
5. **Ask the user** -- "What landed? Where do you want to go deeper?"

## Auto-Select Mode

When the user uses `/advisor` without specifying a name or "council":

1. Analyze the question
2. Recommend 1-2 specific advisors with a one-line reason why
3. Ask the user to confirm, or just go ahead if the match is obvious
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
| Scaling / growth strategy | Strategy panel | Hormozi, Elon |
| Plan is goals with no diagnosis | Rumelt | Charlie |
| Big company cannot grow from its core | Christensen | Blue Ocean |
| Competing on the same axes as everyone | Blue Ocean | Steve |
| What to stop doing to grow | Hardy | Derek |
| Is this advantage durable | Helmer | Charlie |
| Plan is initiatives with budgets, no bet | Martin | Rumelt |
| Conventional thinking trap | Derek | Elon |
| Partnership / people decisions | Charlie | Naval |
