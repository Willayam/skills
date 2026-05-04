# Organization, The Algorithm, and Urgency

Use this reference for process audits, codebase simplification, org design,
meetings, communication, timelines, and automation decisions.

## Core Thesis

Most systems are slower and more complex than physics requires. The cure is not
more process. The cure is to question requirements, delete aggressively,
simplify, accelerate, and automate only after the system deserves automation.

## The Algorithm

Run these steps in strict order:

1. **Question every requirement.** Each requirement needs an owner and a reason.
   Requirements from smart people are especially dangerous because others stop
   questioning them.
2. **Delete every possible part or process.** If nothing ever has to be added
   back, deletion was too timid.
3. **Simplify and optimize what remains.** Never optimize something that should
   not exist.
4. **Accelerate cycle time.** Speed matters after the work is necessary and
   simple.
5. **Automate last.** Automation locks in the process. Do not automate waste.

## Requirement Audit Template

```md
## Requirement Audit

### Confirmed
- [part/process/rule]: required because [reason], owned by [person/source].

### Questionable
- [part/process/rule]: appears to serve [guess], but evidence is weak because
  [reason].

### Delete Candidates
- [part/process/rule]: no current owner, customer value, legal need, safety
  need, or technical necessity found.
```

## Organization Design

- Let information travel by the shortest useful path.
- Do not force work through chains of command when direct communication solves
  the problem faster.
- Organizational boundaries show up in products as duplicated parts, awkward
  interfaces, and "box inside a box" design.
- Design, engineering, and manufacturing should be close enough that mistakes
  hurt immediately and get fixed immediately.
- Acronyms, jargon, and invented labels tax communication. Use plain terms
  unless the acronym is widely understood and genuinely saves time.

## Failure Culture

- Innovation requires permission to make non-catastrophic mistakes.
- Incentives should reward useful experiments and fast correction.
- Do not punish smart, motivated people for honest failures in unknown terrain.
- Do remove persistent low effort, low motivation, or reality-denial.
- Failure is useful only if it creates learning and changes the next iteration.

## Simplicity

- Complexity is a tax on speed, reliability, cost, and learning.
- The best part is no part; the best process is no process.
- Ask for the design necessity of every component and every step.
- Overdelete first, then add back only what reality proves necessary.
- Give teams one clear metric when focus is drifting.

## Urgency

- Time is the only non-replaceable resource.
- Speed is both offense and defense. Faster iteration compounds.
- Long timelines often mean serialized dependencies. Run independent work in
  parallel.
- For urgent critical items, review progress daily until the constraint breaks.
- If a timeline is too long, break the problem into building, power, cooling,
  supply, staffing, approvals, and other true constraints; then solve them in
  parallel where possible.

## Meeting Rules

- Delete large meetings unless they provide value to almost everyone present.
- Delete recurring meetings once the urgent need passes.
- Leave meetings where you are not adding value.
- Replace status theater with direct work on the bottleneck.

## Automation Rules

- Hand-run or manually inspect the process first.
- Automate only after deletion, simplification, and acceleration.
- Prefer small scripts and tight feedback loops before large platforms.
- Automating a bad process creates a fast bad process.

## Advisor Moves

- Start with "what requirement does this serve?"
- Ask "who owns this requirement?" not "which department wants it?"
- Make deletion candidates explicit and concrete.
- Refuse to jump to tooling until the workflow is necessary and simple.
- Turn vague urgency into a measurable cycle-time target.
