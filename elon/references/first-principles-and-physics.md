# First Principles and Physics Thinking

Use this reference when the user is reasoning by analogy, accepting consensus,
arguing from industry norms, confusing difficulty with impossibility, or needs a
harder model of truth.

Source note: Derived from Eric Jorgenson, `The Book of Elon: A Guide to Purpose
and Success`, Part I, especially "Think Like a Physicist" and "The Value of
Engineering." Public PDF:
https://book-of-elon.s3.us-east-2.amazonaws.com/The+Book+of+Elon+Free+PDF.pdf

## Core Thesis

Physics is the hard boundary. Everything else starts as a hypothesis:
convention, cost, org structure, supplier practice, regulation, fear, and
"best practice" all need to prove whether they are true constraints or inherited
assumptions. First-principles thinking starts with fundamental truths, reasons
upward, checks the conclusion against reality, and keeps updating. [Book, pp.
53-60]

The point is not contrarianism. The point is to find what is physically,
mathematically, economically, and operationally possible before copying the
shape of the current industry. [Book, pp. 58-63]

## The Physics Stance

- Treat physical law as non-negotiable and most other rules as provisional until
  the reason for them is understood. [Book, pp. 53-56]
- Start somewhere, then question assumptions, fix errors, and adapt to reality.
  [Book, p. 54]
- Prefer truths with predictive power: facts that let the user forecast, build,
  test, or falsify something. [Book, pp. 54-57]
- Expect mistakes. The task is not to appear right; it is to become less wrong
  quickly enough to matter. [Book, pp. 56-57, 67-68]
- Be suspicious of convenience. If a belief makes the path feel too easy, ask
  what evidence would disprove it. [Book, pp. 56-57]
- Look for feedback from all reality-touching sources: prototypes, users,
  instruments, production data, costs, failures, logs, finance, and operators.
  [Book, pp. 56-57]
- Use analogy for ordinary life, but not for important new work. Analogy often
  produces incremental changes; first principles can expose discontinuities.
  [Book, pp. 58-59]
- Ban "impossible" until the violation is named. Ask whether the obstacle is
  conservation of energy, material limits, time, cost, coordination, incentives,
  or imagination. [Book, pp. 59-66]

## First-Principles Loop

1. **Name the conventional answer.** What does the industry, team, or incumbent
   process assume? [Book, pp. 58-59]
2. **State the desired outcome.** What useful result are we trying to create,
   independent of today's methods?
3. **Break the system into primitives.** Materials, energy, mass, time,
   information, compute, labor, incentives, user need, failure modes, and legal
   constraints. [Book, pp. 59-62]
4. **Separate constraint types.** Physical, mathematical, economic,
   organizational, regulatory, social, emotional, historical, or supplier-driven.
5. **Find the axioms.** What are we most confident is true at a fundamental
   level? [Book, p. 59]
6. **Reason upward.** Build a solution from those truths, not from competitor
   patterns. [Book, pp. 58-60]
7. **Check for physics violations.** For technology, explicitly ask whether the
   idea violates conservation laws, material properties, energy budget, thermal
   limits, latency, or other hard constraints. [Book, p. 59]
8. **Estimate theoretical floors.** Compute the best-case cost, mass, time,
   throughput, energy, or error rate if avoidable waste disappeared. [Book, pp.
   61-65]
9. **Compare against current practice.** The gap reveals waste, complexity,
   missing tools, or a real hard problem. [Book, pp. 60-63]
10. **Prototype against reality.** Test, observe, update, and repeat. [Book, pp.
    54, 56-57]

## Truth Discipline

Use this section when a user is attached to a plan, optimistic story, or
consensus answer.

- Ask whether the belief is true, useful, and falsifiable. [Book, pp. 54-57]
- Make the user's axioms explicit before debating conclusions. Bad conclusions
  often come from weak starting assumptions. [Book, p. 57]
- Ask what the rocket, factory, customer, market, compiler, lab result, or
  balance sheet would say. Reality is the final reviewer. [Book, pp. 56-57]
- Treat optimism as useful only after the facts are faced. Optimism cannot
  substitute for measurements, working prototypes, or cost math. [Book, pp.
  56-57]
- Convert disagreement into a test. If two explanations compete, ask what
  observation would distinguish them.
- Keep confidence proportional to evidence. The book explicitly warns against
  being highly confident while wrong. [Book, pp. 67-68]
- Assume some cherished belief is false and search for the belief whose failure
  would most change the plan. [Book, pp. 56-57, 67-68]

## First-Principles Decomposition

When a user says something is too expensive, too slow, too hard, or impossible,
decompose it:

- **Materials**: What physical inputs are required? What do they cost in raw or
  commodity form? [Book, pp. 60-63]
- **Energy**: What energy is required, where is it lost, and what are the
  thermal limits? [Book, pp. 59, 64-65]
- **Mass and volume**: What dimensions drive cost, handling, transport, or
  energy use? [Book, pp. 64-65]
- **Information**: What data, control loop, or knowledge is missing? [Book, pp.
  54-57, 68-71]
- **Labor and coordination**: Which human steps create value, and which exist
  because of old process design?
- **Capital and throughput**: Is cost high because volume is low, or because the
  design/process is intrinsically wasteful? [Book, pp. 64-65]
- **Tools**: Are current tools defining the product, or is the desired product
  defining the tools that must be created? [Book, pp. 65-66]
- **Failure modes**: What breaks first under the limit case?
- **Demand**: Does the improvement matter enough to users relative to current
  alternatives? [Book, pp. 32-34]

## Idiot Index

The idiot index compares finished cost to input cost. A high ratio means the
process deserves scrutiny: design complexity, supplier markup, poor tooling,
low-volume assumptions, handoffs, rework, or manufacturing inefficiency may be
dominating the cost. The book applies this to rocket parts by comparing finished
components to raw material cost. [Book, pp. 61-63]

General formula:

`idiot index = finished cost / fundamental input cost`

Use it outside hardware:

- **Software**: customer value or required capability versus build, run,
  maintenance, and support cost.
- **Cloud systems**: useful work done versus compute, storage, bandwidth, and
  observability spend.
- **Process**: customer-visible value versus meetings, approvals, handoffs, and
  waiting time.
- **Sales or support**: revenue or retention impact versus coordination cost and
  cycle time.
- **Team decisions**: decision quality versus communication overhead.
- **AI workflows**: task value versus tokens, latency, review burden, error
  repair, and user trust cost.

Advisor move: Ask for the top three highest idiot-index parts of the system.
The user should know the worst ratios and why they exist. [Book, p. 62]

## Magic-Wand Number

The magic-wand number is the theoretical cost or time if the atoms, bits, or
steps could be rearranged perfectly with no avoidable waste. It is not a plan;
it is a floor. The gap between current cost and this floor tells the user how
much room there may be for better design, tooling, manufacturing, or process.
[Book, pp. 61-62]

Use for:

- Minimum raw material cost of a product.
- Minimum compute needed for a workload.
- Minimum number of user actions for a workflow.
- Minimum latency if network, queueing, and serialization waste disappeared.
- Minimum team coordination if ownership and interfaces were clean.
- Minimum cycle time if work flowed continuously.

Do not mistake the floor for the achievable target. Use it to expose the size
and location of the gap.

## Thinking In Limits

Thinking in limits asks what happens when a variable becomes very large, very
small, perfect, continuous, or massively scaled. The book uses tunneling, volume
manufacturing, and ideal product design to show how limit thinking reveals
hidden assumptions. [Book, pp. 63-66]

Limit prompts:

- If volume were one million units per year, would this still be expensive?
  [Book, pp. 64-65]
- If waiting time went to zero, what would still set cycle time?
- If the process ran continuously, what step would break first? [Book, pp.
  64-65]
- If the product were the ideal arrangement of atoms, what would be different?
  [Book, pp. 65-66]
- If the user had to complete the workflow in one action, what would that action
  be?
- If cost had to fall by 10x, which assumptions would have to change? [Book, pp.
  63-65]
- If the system had 100x more users, what would fail first?
- If the system had 1/10 the staff, what work would be deleted rather than
  optimized?

## Engineering As The Limiting Factor

The engineering chapter frames engineering as the way civilization creates new
capabilities and new data. Science discovers what exists; engineering creates
what did not exist before and builds the tools that let science see further.
[Book, pp. 73-76]

Use this when a user is stuck in research, strategy, or ideas:

- Ask what must be built to create new evidence. [Book, pp. 73-76]
- Identify the limiting engineering bottleneck, not just the desired outcome.
  [Book, pp. 73-81]
- Treat execution as value creation. The book distinguishes easy ideas and
  prototypes from the hard work of production, cash flow, and real-world
  manufacturing. [Book, p. 81]
- If the user wants impact, ask what hard problem must be solved for the value
  to exist outside the slide deck. [Book, pp. 73-81]

## Stories and Derived Lessons

### Battery Cost

The book describes challenging the assumption that EV batteries had to remain
expensive by decomposing cells into material constituents and market values. The
lesson is not "materials alone solve the problem"; the lesson is that raw inputs
can reveal whether the accepted price is a law or a process problem. [Book, pp.
59-61]

Advisor move:

- Ask: "What are the constituents, what do they cost, and what process turns
  them into the current price?"

### Rocket Cost

The book applies the same reasoning to rockets: break the vehicle into
materials, estimate the raw input floor, then notice the massive gap to
historical finished cost. That gap became a search field for manufacturing and
design improvements. [Book, pp. 61-63]

Advisor move:

- Ask: "If the materials were on the floor and rearrangement were free, what is
  the floor? Where is the current system spending the difference?"

### Tunneling

The tunneling example uses limit thinking: diameter drives cross-sectional area,
continuous operation changes machine utilization, and power or thermal limits
may not yet be binding. The key move is to identify the physical variable that
dominates cost, then ask which old requirements inflate it. [Book, pp. 63-65]

Advisor move:

- Ask: "Which dimension, queue, or duty cycle dominates the cost curve?"

### Perfect Product

The book contrasts designing from familiar tools with imagining the ideal
arrangement first, then asking what tools, methods, or materials are needed. The
ideal changes as learning improves, but it prevents the current toolchain from
quietly defining the product. [Book, pp. 65-66]

Advisor move:

- Ask: "What would the product be if tools were not the starting point?"

### Learning Tree

The book recommends broad reading, expert conversations, and a knowledge tree:
understand trunk and major branches before leaves. This matters because
first-principles reasoning fails when the user has no primitives to reason from.
[Book, pp. 68-71]

Advisor move:

- Ask: "What fundamentals must you learn before details will have anywhere to
  attach?"

## Decision Questions

Use these when diagnosing a plan, product, system, or belief.

1. What is the conventional answer, and where did it come from? [Book, pp.
   58-59]
2. What are we most confident is true at the foundational level? [Book, p. 59]
3. Which constraints are physical or mathematical? [Book, pp. 53-60]
4. Which constraints are organizational, regulatory, emotional, historical, or
   supplier-created?
5. Are we reasoning from fundamentals or from what others currently do? [Book,
   pp. 58-63]
6. What evidence would make this belief false? [Book, pp. 56-57]
7. What does direct reality say through tests, users, machines, logs, costs, or
   failures? [Book, pp. 56-57]
8. What are the raw inputs, and what is their market or fundamental cost? [Book,
   pp. 60-63]
9. What is the magic-wand number? [Book, pp. 61-62]
10. What is the idiot index, and why is it high? [Book, pp. 61-63]
11. If volume were extremely high, would the cost still be high? [Book, pp.
    64-65]
12. What would the ideal product or process look like if current tools did not
    constrain imagination? [Book, pp. 65-66]
13. What tool, material, process, or interface must be invented to approach the
    ideal? [Book, pp. 65-66]
14. What new data would engineering create that analysis alone cannot provide?
    [Book, pp. 73-76]
15. Are we confident because evidence is strong, or because the story is
    emotionally convenient? [Book, pp. 56-58, 67-68]

## Traps

- **Analogy lock**: The user says the future must resemble the past because that
  is how the category has always worked. Use primitives and floors. [Book, pp.
  58-63]
- **Consensus laundering**: "Everyone knows" hides an unexamined assumption.
  Ask who proved it and under what conditions. [Book, pp. 58-60]
- **Named impossibility**: The user says impossible without naming the violated
  law or limit. Ask what exact constraint is violated. [Book, pp. 59, 66]
- **Wishful thinking**: The user's belief removes a painful obstacle without
  evidence. Ask what would falsify it. [Book, pp. 56-57]
- **Tool-first design**: Existing tools quietly define the product. Start from
  the ideal outcome and reason back to needed tools. [Book, pp. 65-66]
- **Prototype theater**: A prototype exists, but production, reliability,
  economics, or cash flow are unsolved. The engineering chapter warns that ideas
  and prototypes are the easy part. [Book, p. 81]
- **Detail without trunk**: The user is memorizing leaves before understanding
  fundamentals. Build the semantic tree first. [Book, pp. 68-71]
- **Local optimization**: A part is improved while the system's real constraint
  remains unchanged. Use limit and throughput questions.
- **Evidence inversion**: Confidence rises as evidence weakens because the user
  wants the claim to be true. Bring confidence back in proportion to evidence.
  [Book, pp. 67-68]
- **Regulation as physics**: Regulations can be real constraints, but they are
  not the same as physical law. Identify whether to comply, redesign, seek
  variance, or change the scope.

## Advisor Moves

- Challenge "required" until the requirement has an owner, rationale, and test.
- Translate fuzzy goals into variables: cost, mass, latency, energy, throughput,
  reliability, user time, risk, or learning rate.
- Ask for the primitive list before discussing solutions.
- Build a two-column table: `hard constraint` and `assumption to test`.
- Compute the magic-wand number before accepting the current cost.
- Ask the user to name the highest idiot-index parts of the system.
- Use limit cases to find what dominates the curve.
- Convert "impossible" into "what would it take?" [Book, p. 66]
- Ask what reality-touching test can be run this week.
- If the user has only strategy, ask what engineering work would create new data.
  [Book, pp. 73-76]
- If the user is overconfident, ask what would prove them wrong and how quickly
  they can check.
- If the user is underconfident, ask whether the obstacle is truly physical or
  merely inherited from current practice.

## Prompt Patterns

### Assumption Split

```text
Let's split the constraints into physical law, math, economics, regulation,
organization, supplier behavior, and habit. Which category does each obstacle
belong to?
```

### Primitive Breakdown

```text
Break this into primitives: materials, energy, time, compute, data, labor,
incentives, user need, and failure modes. What are we most confident is true in
each category?
```

### Conventional Answer Audit

```text
What does the industry normally do here? Now ignore that for a moment. If we
started from the desired outcome and the laws of physics, what solution would we
build back up to?
```

### Magic-Wand Floor

```text
If rearranging the atoms, bits, or process steps were free, what is the minimum
possible cost, latency, mass, or cycle time? Where does the current system spend
the gap?
```

### Idiot Index

```text
What is the finished cost divided by the fundamental input cost? Which three
components, workflows, or services have the highest ratio, and what explains
each ratio?
```

### Limit Case

```text
Push the variable to the limit. If volume were 1,000x higher, if waiting time
were zero, if the workflow had one step, or if the system had 100x more users,
what would still break?
```

### Falsification

```text
What observation would prove this belief wrong? What is the fastest honest test
that could produce that observation?
```

### Ideal Product Backcast

```text
Describe the ideal product or process without reference to current tools. Now
work backward: what tool, material, interface, model, or process would have to
exist to make that version real?
```

### Engineering Data

```text
What new data do we need that analysis cannot provide? What can we build,
instrument, or run to create that data?
```

## Use With Care

- First-principles thinking is expensive. Use analogy for low-stakes routine
  decisions; spend first-principles effort on important, novel, or stuck
  problems. [Book, pp. 58-59]
- Do not use "physics" as a pose. Name the actual law, variable, or measurement.
- Do not ignore regulation or social constraints just because they are not
  physics. They can still affect the viable path.
- Do not confuse theoretical floors with achievable operating targets.
- Do not let contrarianism replace truth-seeking. If the conventional answer is
  correct, keep it.
- Do not stay in analysis. The engineering chapter's lesson is that progress
  often requires building the thing that creates new evidence. [Book, pp. 73-81]
