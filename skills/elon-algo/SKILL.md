---
name: elon-algo
description: Apply Elon Musk's Algorithm to anything - code, processes, workflows, systems, products, projects. Walks the 5 steps in strict order (question every requirement, delete, simplify, accelerate, automate) and, when relevant, layers in the 3 cultural ingredients (expand the product to the customer's entire experience, inject urgency and accountability, eat your own dog food). Use when asked to run the Elon algo, simplify something, audit a process for bloat, question whether something should exist, cut scope, attack a bottleneck, or rethink a system.
---

# Elon's Algorithm

Based on Jon McNeill's *The Algorithm* (Penguin Portfolio, 2026). McNeill was president of Tesla under Elon 2015 to 2018 and later applied the method at Lululemon, GM, SpaceX alumni ventures, and his incubator DVx.

Two parts:

- **Part I - The five steps.** Apply in strict order. Do not skip. Do not reorder.
- **Part II - The three cultural ingredients.** Layer these in when optimizing an organization or team, not a one-off artifact.

Works on anything: code, processes, workflows, organizations, products, features, systems, personal routines.

---

## PART I: The Five Steps

### Step 1: Question Every Requirement

**The most dangerous step to skip.** Optimizing a thing that should not exist is the most common error of a smart engineer.

Every requirement must be traceable to a **named person**, not a department. "The team decided" is not acceptable. Who on the team? Why? Requirements from smart or senior people are the most dangerous because they are the least likely to have been questioned.

#### How to execute

1. **Identify all parts.** Every component, step, rule, field, feature, role, dependency, abstraction, config option, approval gate, handoff. Nothing is exempt.
2. **For each part, find the requirement.** Trace to a real need: a user problem, a business constraint, a regulatory obligation, a technical necessity, a named person's stated decision. Read docs, history, commit messages.
3. **Flag anything where the requirement is unclear, inherited, or stale.** If you can't articulate why it exists in one sentence, it's a deletion candidate. Present:
   - What the part is
   - What requirement it might serve (best guess)
   - Why you're not confident (no documentation, nobody remembers, named generically, defensive against an impossible scenario, "just in case")
4. **Challenge "that's just how we do it."** Convention is not a requirement. Historical reasons are not current reasons.
5. **Probe apparent laws.** "You can't do that" is often a consensus, not a law. The laws of physics are less flexible, but even those have been nudged (semiconductors, gravity). Aim questioning there too.

#### Book examples

- **Tesla China (2015 to 2016):** Every Western carmaker (GM, Ford, VW, Apple) accepted China's joint-venture equity requirement. Elon refused and sent McNeill to Beijing. After 14 months of negotiation, Tesla got the first 100% foreign-owned auto plant in China (Gigafactory Shanghai). The "requirement" wasn't a law, it was a norm.
- **Giga-casting the chassis (Doug Field):** Tesla's body shop had 300+ welded parts, half the factory's capital cost. Field rolled a Matchbox car across a table: one cast piece, top and bottom. Automakers "knew" you couldn't cast large parts (heat, splatter, molds exploding). They tested on reject wheel rims, then larger. Final chassis: 3 parts instead of 300. Five to seven year lead over competitors.
- **TrueMotion (McNeill, pre-Tesla):** Stanford had given up on distinguishing driver vs. passenger phone via GPS ("does not exist"). Brad Cordova questioned it by changing the frame: used motion sensors to map the path into the car. Drivers maneuver behind the wheel with a distinct signature. Patented. Became the model Tesla now uses for insurance.
- **Cyber-insurance (Cork):** Lululemon (holds no payment data, Stripe does) and Lyft (bank accounts, passports, IDs) both paid $7M/year because insurers grouped by employee count. One-size-fits-all that applies to everyone is a signal that nobody has dug into the data. McNeill turned it into a company.

#### Output

```
## Step 1: Requirement Audit

### Confirmed requirements
- [part]: [one-sentence reason it must exist, named source]

### Flagged (deletion candidates)
- [part]: best guess is [X], but [reason for doubt]
```

**Do not move to Step 2 until every requirement has a verdict.**

---

### Step 2: Delete Every Possible Step

> "If you're not adding things back at least 10% of the time, you're not deleting enough."

The best part is no part. The best process step is no step. Every part carries cost, failure modes, and time. The default bias in most organizations is to add. Your job is to subtract.

#### How to execute

1. **For each QUESTION or CUT item from Step 1, propose full deletion.** Not optimization. Deletion.
2. **Map every step.** McNeill's method: sticky notes on a wall, one per step. If done right, you'll fill the wall. Most managers can't list their own process.
3. **Circle every step the customer doesn't pay for.** Accounting reviews, performance reviews, internal handoffs: ripe for removal. Aim to cut 80%. You'll end up adding back maybe 10%. That's the point: you found the limit.
4. **The robot exercise.** Imagine teaching every step to a highly advanced but entirely ignorant robot. You must explain every element in excruciating detail. The tedium of this tunes you to the minutiae - you start spotting shortcuts, duplication, and steps that can fold into each other.
5. **Run the "delete a step" contest.** Ask colleagues: find one step to eliminate. Maybe it's duplicative. Maybe it was created for a defunct status quo and hung on.

#### Book examples

- **Raptor engine:** Between v1 and v2, SpaceX deleted hundreds of parts entirely. Not simplified. Removed from existence.
- **Tesla e-commerce (2015 to 2017):** 64 clicks to buy a car. Elon set stretch goal: 10. Cut choices from 300,000+ configurations to 2 packages, questioned every loan signature (bank lawyers, not regulators, drove 90% of them), got Ally + US Bank to a one-paragraph loan, pulled in Experian for prefill. Final: 12 clicks. Sales up 20x over 10 months.
- **Hurricane Irma (2017):** Karim Bousta (global service) pushed an OTA battery-range unlock to 2,000 Florida Tesla owners during evacuation without approval. His decision rule (Elon's three conditions for autonomy): (1) won't hurt or kill anyone, (2) won't break the law, (3) won't cost the company millions. Within those bounds, improvise. Deleting the approval chain saved lives and made the press.
- **Zumi (McNeill/Ganesh at DVx):** The only bad step at a restaurant is waiting for the check. 20 minutes of idle table, servers running cards instead of selling wine. Ganesh's childhood memory: his father's club in Chennai, walk out, monthly bill. Zumi replicated that. Restaurant business up 20% at first London trial.

**Do not move to Step 3 until deletions are decided.**

---

### Step 3: Simplify and Optimize

> "The most common error of a smart engineer is to optimize a thing that should not exist."

Only work on what survived Steps 1 and 2. Optimization before subtraction is wasted motion.

#### How to execute

1. **Agree on the goal.** McNeill: "The first order of business in a meeting is to agree on the goal." Half the time, people in the room aren't on the same page. Anyone tangential leaves.
2. **Reduce to essentials.** Fewer moving parts, less code, fewer tools, fewer dependencies, fewer choices.
3. **Innovation by subtraction.** Stretch goal forces subtraction. Tesla tried to cut 30-day onboarding to 2 hours. They couldn't, so they deleted the whole training program and replaced it with one sentence: *"Be so great they'll talk about you at dinner."* Then the service manager bought groceries for a customer's kids during a labor emergency. "You asked us to make them talk about us at dinner."
4. **Solve systemically, not locally.** Nikki Monterroso (delivery) was running around the factory fixing paint scratches one-by-one. She and Cameron Wetherbee invented a $15 rain jacket for cars in transit. Eliminated 99% of scratches costing $100+ each. Systemic fix, not a bigger quality-control team.
5. **Find a simplifier.** The most valuable people break problems down to 1 or 2 key elements. Hire them or sit near them. McNeill's mantra: "Simplifiers are accelerators."

#### Book examples

- **Alinea (Michelin 3-star, Chicago):** Chef Grant Achatz optimized every arm and hand motion at each station. Equipment bolted to the floor only after the optimum layout was found. Three-step dish prep complete in seconds. Immense complexity hidden behind apparent ease.
- **Tesla delivery prep:** 6 hours/car to 4 minutes/car, by breaking the process into manageable chunks (vacuum, wash, buff, glass, wipe) with staffing matched to cycle time per pitch.
- **Cash velocity:** If company A takes 15 days to produce a car and company B takes 5, company B needs 1/3 the working capital. Simplification isn't just pretty. It's a balance sheet weapon.

**Do not move to Step 4 until simplifications are decided.**

---

### Step 4: Accelerate Cycle Time

> "Every process can be speeded up. But do not do this until you have worked through the first three steps."

Speed is growth. Faster cycle time = higher throughput with the same fixed resources. It also exposes quality and process issues you couldn't see before, giving you the next target.

#### How to execute

1. **Measure cycle time end to end.** Clock starts when the customer initiates, ends when delivered. Not the time you spend. The time the customer waits.
2. **Compare cycle time to "touch time."** Touch time is the time the thing is actually being worked on. McNeill's wife's car: 4 weeks cycle time, 8 hours of billed labor. The gap is the opportunity. (Later he started Sterling Collision Repair around this: 18 days to 18 hours.)
3. **Aim for 50% speedup per iteration.** Not 5%. A stretch target shows you exactly where the current process breaks. That's where to work.
4. **Accelerate by parallelizing.** Sequential relay-race processes are where most slack lives. At Lululemon, the Olympic team ran design, logistics, and manufacturing concurrently instead of in sequence: 18 months went to 4 months.
5. **Go to the source of the bottleneck.** Lululemon dye samples bounced between Canada and Asia for weeks. Designer + supply-chain lead flew together to the source factory. Back-and-forths went from weeks to minutes.

#### Book examples

- **Tesla Vehicle Plan (Neal Suidan, 2018):** Excel-based S&OP meetings replaced with a real-time data platform. Car-production cycle time fell 14 days to under 6. Scaled Model 3 from 20K/quarter to 500K.
- **GM Hummer EV (Josh Tavel, Mary Barra):** Traditional auto development: 4 years. Small autonomous team reporting direct to the president: 19 months. GM's new-model norm went from 2 to 4 years down to 12 to 14 months.
- **Lululemon Olympics:** 4 months to design, manufacture, and deliver modular Olympic uniforms. Designers body-scanned athletes; supply chain tested fabrics in simulated Beijing weather. Parallel, not serial. Sold out in hours.

**Do not move to Step 5 until acceleration decisions are made.**

---

### Step 5: Automate Last

> "I've made the mistake of trying to automate something that should not exist, or automating a process step that should have been deleted."

Automation is expensive, rigid, and locks in whatever process exists. If you automate a flawed process, you get an expensive, fast, rigid system that does the wrong thing.

#### How to execute

1. **Only automate what survived Steps 1 to 4.** The process must be stable, simple, and fast before code is written.
2. **Hand-run the process first.** Amazon ran packing by hand. DoorDash took restaurant orders by phone and fulfilled them manually. Tesla built Model 3 by hand in a sprung tent (Jerome Guillen) when the over-automated Alien Dreadnought crashed. Learn the process by doing it, then encode what you learned.
3. **House-before-walls discipline.** McNeill's analogy: architect vs. contractor. Contractors want to pour foundations before the design is done. Changes afterward are expensive or impossible. Hold off the coders until the design is locked.
4. **Rank automation by effort-to-impact.** Time saved by automation vs. time to build and maintain. Scripts, cron, webhooks, CI/CD, Claude skills, MCP tools: start simple.

#### Book examples

- **Alien Dreadnought (2017):** Elon over-automated the Model 3 line. Robots crashed into each other, cars fell off trays. Jerome Guillen built a long tent, hand-assembled cars, removed 50% of steps through observation. 75 cars in week 1, 750 by week 6. Elon publicly: "Excessive automation at Tesla was a mistake. My mistake. Humans are underrated."
- **Curbee (McNeill at DVx):** Manually ran a mobile car-repair business in Sunnyvale for 7 months (Excel, Google Forms, Google Maps). Only after 2 years of learning did they build software. Now in 500+ dealerships.

---

### Radical Rethinking (the whole algorithm, applied end-to-end)

When all five steps are applied to one problem, breakthrough solutions emerge that no single step would have produced.

**Tesla service centers, 2015, $300M saved.** Service centers were maxed out, 30-day waits in the US. Building 100 more was $300M McNeill didn't have. Chris Sullivan (Palo Alto service manager) ran the Algorithm:

- **Q:** Did customers have to schedule? Did they have to bring the car in at all? (Step 1)
- **Delete:** Customer-service person as intermediary; the technician talks to the customer directly. (Step 2)
- **Simplify:** Four lanes by size. Senior tech triages at the curb before the coffee is done. 80% of cars fixed in 20 minutes. (Step 3)
- **Accelerate:** No building visit = no wait. (Step 4)
- **Automate:** Outfit returned "lemon" Teslas as a mobile repair fleet. House calls. Later: espresso machines in the service vans. (Step 5)

The goal isn't "finished the checklist." The goal is to arrive at a configuration that the status quo would call impossible.

---

## PART II: The Three Cultural Ingredients

These are what McNeill calls the "secret sauce." The cultural conditions without which the five steps don't take root. Layer these in when optimizing an organization, team, or ongoing operation.

### Ingredient 1: Expand the Product to the Customer's Entire Experience

Define your product as **everything the customer touches**, not just the thing you ship. Every friction point in that expanded view is an opportunity.

- **Tesla:** The product isn't the car. It's shopping, financing, charging, servicing, and trading it in. Expanding into charging infrastructure, insurance (1/3 of cash flow at peak), subscription autopilot, and battery-range unlocks each added recurring revenue and made the core product better.
- **Stash (Brandon Krieg):** The product isn't the personal-finance app. It's financial literacy. Built an AI investing coach so customers could get advice the rich take for granted.
- **GM Chevy Bolt:** Mark Reuss asked "are our cars *fun*?" Added customizable snap-on dashboard (inspired by Chinese EVs). Fun is part of the product.

**How to apply:** List every moment in the customer's lifecycle. For each, ask: is this effortful or delightful? Can we remove it, own it, or monetize it?

### Ingredient 2: Inject Urgency and Accountability

Weekly cadence, CEO-level presence, unambiguous ownership. This is, in McNeill's view, the single most powerful ingredient.

- **Elon's weekly meetings:** Every Tuesday, engineers reported on the 2 to 3 most pressing problems. The CEO knows the material deeply enough to ask sharp questions and demand results.
- **Democratizes + hierarchizes at once.** CEO works side-by-side with engineers on the problem, but also demands results. Can't be fooled. This combination drives problem-solving.
- **DVx stage-gate:** Every startup has weekly 1:1s. Monthly CEO report. Ventures that miss metrics get killed quickly. "What milestone are we working toward, and what's standing in the way?"
- **Stash's AI coach (Brandon Krieg):** CEO returned to founder mode, pulled a small team ("Ninjas"), weekly deliverables, 1 month to prototype, shipped early 2025.

**How to apply:** Pick the biggest problem. Assemble a small group involved in a way that matters. Set action + goal. Meet in a week with a progress report. That's the entire mechanism.

### Ingredient 3: Eat Your Own Dog Food

Use your product the way customers do. Regularly. As an executive, especially.

- **Elon missed the Tesla follow-up gap** because he didn't take test drives himself. McNeill took 8 test drives at 8 different stores (different emails per store). Zero callbacks. Found 5,000 similar orphaned buyers. Halted all test drives until follow-up happened. Sales spiked within days.
- **JB Straubel's rule:** Each executive pulls a car off the factory lot each night, drives home, emails feedback by morning. Drove rapid improvements in software, ride, and roof-glass tint.
- **Celeste Burgoyne / McNeill cross-visit:** Lululemon and Tesla executives visited each other's stores (employees didn't know them). Unvarnished observations. Still doing it years later.
- **20% rule:** McNeill spends one day a week (20%) away from the desk, in some part of the customer journey.
- **Mary Barra (GM):** A GM product in the driveway for months-long evaluations. Lyriq's "ignition button" vestige spotted and removed.
- **McNeill's doctrine:** Anytime a customer needs YouTube to figure out your product, the design needs a tweak.

**How to apply:** Schedule 20% of your time outside the office, in the customer's experience. Write up observations. Share with the relevant leader. Repeat.

---

## Session Format

### Opening

When invoked, ask William **what** he wants to optimize. Anything qualifies: a feature, a codebase, a project, a routine, a workflow, a business process. Then read the relevant files or get the concrete details. Do real research before presenting anything.

### Per step

```
## Step N: [Name]

> [Elon's quote for this step]

### What I found
[Concrete analysis based on actual code / docs / data, not theory]

### Recommendations
| Item | Verdict | Reasoning |
|------|---------|-----------|
| ... | KEEP / QUESTION / CUT / SIMPLIFY / ACCELERATE / AUTOMATE | ... |

### Your call
[Specific decision point for William]
```

### Closing

```
## Results

### Deleted
- [what was removed]

### Simplified
- [what was made simpler]

### Accelerated
- [what was made faster]

### Automated
- [what was automated]

### Cultural ingredients applied (if relevant)
- Expanded product view: [...]
- Urgency/accountability: [...]
- Eat own dog food: [...]

### Net result
[Before vs. after. Fewer parts, less cost, faster cycle, less manual work.]
```

Then remind William: **"Now go back to Step 1."** The Algorithm is a loop, not a one-pass process. Last year's advances are this year's norms. There's always another layer of dumb requirements to find.

---

## Rules

- **Never skip steps. Never reorder.** The sequence IS the algorithm.
- **One step at a time.** Complete each before starting the next. Get William's decision before advancing.
- **Do real analysis.** Read code, check configs, review docs. Don't philosophize.
- **Be specific.** "Simplify the API" is useless. "Delete /legacy endpoint, zero calls in 90 days" is useful.
- **Attach names to requirements.** "The team decided" is not acceptable. Who? Why?
- **Bias toward deletion.** When in doubt, cut. You can add it back.
- **If William wants to jump ahead, redirect.** "Let's make sure this should exist first."
- **Radical rethinking is the target, not a bonus.** A pass that only trims 5% means Step 1 wasn't done aggressively enough.
- **The goal is not perfection. It's ruthless simplicity.**
