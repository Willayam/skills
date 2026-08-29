# Behavioral Design Frameworks Reference

These seven frameworks serve as audit lenses for evaluating product design. Each lens reveals different aspects of how a product influences user behavior. A thorough audit applies all seven, since a design that appears benign under one framework may reveal exploitative patterns under another.

No single framework is sufficient on its own:
- Octalysis and White Hat/Black Hat map motivational drives and their ethical valence.
- SDT evaluates whether fundamental psychological needs are supported or thwarted.
- The Hook Model dissects habit-formation mechanics.
- Fogg's Behavior Model examines how motivation, ability, and prompts interact.
- Nudge Theory scrutinizes choice architecture and defaults.
- Value-Sensitive Design widens the aperture to systemic and societal impacts.

---

## Quick-Reference Comparison

| Framework | Origin | Core Question | Primary Focus | Key Ethical Metric |
|---|---|---|---|---|
| Octalysis | Yu-kai Chou | Which core drives does this product activate? | Motivational completeness and balance | Intrinsic/extrinsic drive ratio |
| Self-Determination Theory | Deci & Ryan | Are autonomy, competence, and relatedness supported? | Psychological need satisfaction | Motivation type on the continuum |
| Hook Model | Nir Eyal | How does this product form habits? | Habit loop mechanics | User value per cycle iteration |
| White Hat vs Black Hat | Yu-kai Chou | Does the user feel empowered or anxious? | Ethical valence of motivation | WH:BH ratio (target 3:1+) |
| Fogg Behavior Model | BJ Fogg | Is behavior made easier or just more pressured? | Behavior = Motivation + Ability + Prompt | Hope vs fear as primary motivator |
| Nudge Theory | Thaler & Sunstein | Do defaults serve users or the business? | Choice architecture and defaults | Ease of opting out |
| Value-Sensitive Design | Friedman & Kahn | Who is affected and are their values respected? | Systemic and societal impact | Stakeholder inclusivity |

---

## 1. Octalysis Framework

**Author:** Yu-kai Chou
**Background:** Industry-standard behavioral design framework developed over 10+ years of research, cited 3,300+ times academically, adopted by Google, LEGO, Tesla, and the UN. Maps human motivation to 8 core drives arranged in an octagon. Emphasizes Human-Focused Design over function-focused design -- the premise that systems should optimize for human motivation and feelings rather than pure efficiency.

### The 8 Core Drives

1. **Epic Meaning & Calling** -- The drive to participate in something greater than oneself. Users believe they were chosen or that their actions serve a higher purpose.
2. **Development & Accomplishment** -- The internal drive to make progress, develop skills, and overcome challenges. Requires genuine challenge; badges without effort are hollow.
3. **Empowerment of Creativity & Feedback** -- The drive to engage in creative processes, experiment, and see results. Users need autonomy to try different combinations and receive meaningful feedback.
4. **Ownership & Possession** -- The drive to own, improve, and protect things. When users feel ownership, they want to increase and defend what they have.
5. **Social Influence & Relatedness** -- The drive encompassing social acceptance, mentorship, companionship, competition, and envy. Activated by seeing others succeed or by belonging to a community.
6. **Scarcity & Impatience** -- The drive to want something because it is rare, exclusive, or not immediately obtainable. Powerful but can feel coercive.
7. **Unpredictability & Curiosity** -- The drive to find out what happens next. The core mechanic behind gambling, variable rewards, and "what if" engagement loops.
8. **Loss & Avoidance** -- The drive to avoid negative outcomes, losing progress, or missing opportunities. Creates urgency but also anxiety.

### Motivational Balance

- **Left Brain drives (2, 4, 6)** tend toward extrinsic motivation -- logic, calculation, ownership.
- **Right Brain drives (3, 5, 7)** tend toward intrinsic motivation -- creativity, social connection, curiosity.
- The best systems activate both sides. A product relying solely on extrinsic drivers will struggle with long-term engagement once rewards plateau.

### What to Look For in a Product

- Which of the 8 drives are actively present in the product experience?
- Which drives are absent or underdeveloped?
- Is the distribution balanced between left-brain and right-brain drives?
- Are the strongest drives aligned with genuine user goals or with business extraction?

### Audit Questions

- Which core drives does this product activate? List each and describe how.
- Which core drives are missing entirely? What would activating them add?
- Is the distribution balanced between intrinsic and extrinsic motivators?
- Are any drives over-relied upon to the point of being the sole engagement mechanism?
- Do users remain engaged when the dominant drive is removed (e.g., remove the leaderboard -- do users still care)?

### Positive Implementation

- Activating drives 1-3 (Epic Meaning, Accomplishment, Creativity) as primary motivators.
- Using drive 5 (Social Influence) for genuine community and mentorship.
- Balanced octagon with no single drive dominating.
- Users can articulate why they enjoy the product beyond rewards.

### Exploitative Implementation

- Over-reliance on drives 6-8 (Scarcity, Unpredictability, Loss) without White Hat balance.
- Artificial scarcity that serves the business rather than the user experience.
- Unpredictability mechanics that resemble gambling dynamics.
- Loss mechanics that punish users for healthy behavior (e.g., taking breaks).

---

## 2. Self-Determination Theory (SDT)

**Authors:** Edward Deci & Richard Ryan
**Background:** One of the most empirically validated theories of human motivation, with decades of research across education, work, health, and technology. Identifies three basic psychological needs that, when met, foster intrinsic motivation and well-being. When thwarted, usage patterns become compulsive rather than volitional.

### The Three Basic Needs

- **Autonomy** -- The need to feel in control of one's own behavior and goals. Not independence from others, but a sense that one's actions are self-endorsed rather than externally controlled.
- **Competence** -- The need to feel effective, to master challenges, and to develop skills over time. Requires optimal challenge -- not too easy (boring) and not too hard (frustrating).
- **Relatedness** -- The need to feel connected to others, to care and be cared for, to belong. Genuine social connection, not superficial social metrics.

### The Motivation Continuum

From most to least self-determined:

1. **Intrinsic motivation** -- "I enjoy this." The activity itself is rewarding. The gold standard.
2. **Identified regulation** -- "This matters to me." The activity serves a personally important goal. Still healthy.
3. **Introjected regulation** -- "I should do this." Driven by guilt, anxiety, or ego. The user feels internal pressure but it is not truly self-endorsed. Warning zone.
4. **External regulation** -- "I have to do this." Driven by rewards, punishments, or external demands. The user feels controlled. Red flag.

Products can shift users along this continuum in either direction.

### What to Look For in a Product

- Does the product give users meaningful choices, or does it prescribe a single path?
- Does the product help users develop real skills, or does it simulate progress?
- Does the product foster genuine human connection, or does it manufacture social pressure?
- What happens when a user takes a break -- is the experience welcoming or punishing?

### Audit Questions

- Does the product support autonomy? Can users choose their own goals, pace, and path? Are there penalties for taking breaks or disengaging?
- Does the product support competence? Do users develop real, transferable skills? Is feedback informational or controlling?
- Does the product support relatedness? Is social interaction genuine or metrics-driven? Do users feel belonging or comparison anxiety?
- What type of motivation does the product primarily foster? Where on the continuum do most user behaviors fall?

### Positive Implementation

- Fostering intrinsic or identified motivation as the primary engagement driver.
- Supporting all three needs simultaneously -- users feel autonomous, competent, and connected.
- Informational feedback ("Here's how you did and why") rather than controlling feedback ("You must do X to earn Y").
- Users can articulate personal goals the product helps them achieve.

### Exploitative Implementation

- Relying on introjected motivation -- streak guilt, social comparison anxiety, "you're falling behind" messaging.
- Relying on external motivation -- rewards that are only valuable within the product, punishments for disengagement.
- Thwarting autonomy -- forced engagement patterns, penalties for breaks, loss of progress for inactivity.
- Simulating competence -- inflated metrics, meaningless levels, fake mastery signals that do not reflect real skill.

---

## 3. The Hook Model

**Author:** Nir Eyal
**Background:** Describes a four-phase cycle that products use to form user habits. Introduced in "Hooked: How to Build Habit-Forming Products." The model itself is descriptive and morally neutral -- it can be applied ethically or exploitatively. Eyal later wrote "Indistractable" partly in response to criticisms about technology overuse.

### The Four Phases

1. **Trigger** -- What prompts the user to act.
   - *External triggers:* Notifications, emails, ads, calls to action. The user is pulled in from outside.
   - *Internal triggers:* Emotions, routines, situations. The user reaches for the product on their own. Internal triggers are more powerful and self-sustaining.
2. **Action** -- The simplest behavior in anticipation of a reward. Fogg's formula applies here: the action must be easy enough given the user's motivation level. Reducing friction increases action rate.
3. **Variable Reward** -- The unpredictable payoff that satisfies the trigger while leaving the user wanting more. Variability is key -- predictable rewards become boring.
4. **Investment** -- The user puts something into the product (time, data, effort, social capital) that makes the product better for them and loads the next trigger. Investment increases switching costs and commitment.

### Three Types of Variable Rewards

- **Rewards of the Tribe** -- Social validation: likes, comments, recognition, status. Driven by social connection and acceptance.
- **Rewards of the Hunt** -- Information, resources, deals. The thrill of finding something valuable. Driven by the search for material rewards.
- **Rewards of the Self** -- Mastery, completion, competence. The satisfaction of overcoming a challenge. Driven by the desire for self-improvement.

### What to Look For in a Product

- Is the full hook cycle present (trigger, action, reward, investment)?
- How many hooks run simultaneously?
- What emotions serve as internal triggers -- genuine needs or manufactured anxieties?
- Does investment genuinely improve the user's experience or primarily create lock-in?

### Audit Questions

- What triggers does the product use? Are external triggers (notifications, badges) used to build internal triggers (genuine habits), or are they a permanent crutch?
- Are variable rewards serving users or exploiting them? Do rewards deliver real value, or do they exploit dopamine responses with empty reinforcement?
- Does the action phase reduce friction for genuinely beneficial behaviors, or for compulsive checking?
- Does investment genuinely improve the product for the user, or does it primarily function as a switching cost?
- Is the full hook cycle present? How tight is the loop?

### Positive Implementation

- Internal triggers rooted in genuine user needs -- a desire to learn, create, or connect.
- Variable rewards that deliver real, lasting value (skill improvement, meaningful information, genuine relationships).
- Investment that truly makes the product better for the user over time (personalization, skill progression, content creation).
- The hook cycle serves user goals, not just engagement metrics.

### Exploitative Implementation

- Internal triggers based on anxiety, loneliness, boredom, or FOMO.
- Variable rewards that exploit dopamine responses -- infinite scroll, random reinforcement schedules, empty social validation.
- Investment as lock-in -- sunk cost mechanics, data portability barriers, social graphs that cannot be exported.
- The hook cycle optimizes for time-on-app regardless of user benefit.

---

## 4. White Hat vs Black Hat Gamification

**Author:** Yu-kai Chou (within the Octalysis framework)
**Background:** A classification system within Octalysis that divides the 8 core drives into White Hat (top of the octagon) and Black Hat (bottom of the octagon) based on how they make users feel. This is not a good/evil distinction -- Black Hat drives are powerful and sometimes necessary -- but the ratio between them determines whether the overall experience is empowering or anxiety-inducing.

### White Hat Core Drives (Top of Octagon)

- **Epic Meaning & Calling** (Drive 1)
- **Development & Accomplishment** (Drive 2)
- **Empowerment of Creativity & Feedback** (Drive 3)

White Hat drives make users feel powerful, fulfilled, and satisfied. They generate genuine, sustained motivation. However, they do not create urgency -- users feel good but may not feel compelled to act right now.

### Black Hat Core Drives (Bottom of Octagon)

- **Scarcity & Impatience** (Drive 6)
- **Unpredictability & Curiosity** (Drive 7)
- **Loss & Avoidance** (Drive 8)

Black Hat drives make users feel obsessed, anxious, or addicted. They create powerful short-term motivation and urgency. However, if users reflect on their behavior, they often feel they lost control. Sustained Black Hat dominance leads to burnout, resentment, and churn.

### Middle Drives

- **Ownership & Possession** (Drive 4) and **Social Influence & Relatedness** (Drive 5) sit in the middle and can lean White Hat or Black Hat depending on implementation.

### Best Practice: White Hat Environment, Selective Black Hat

The recommended approach is to establish a White Hat environment first -- users feel empowered, purposeful, and creative -- then use Black Hat mechanics sparingly for specific conversion or urgency moments. The user should always return to a White Hat state afterward.

### What to Look For in a Product

- Does the overall experience feel empowering or pressuring?
- After a session, do users feel accomplished or anxious?
- Are urgency mechanics (timers, limited offers, streaks) pervasive or targeted?
- Can users take breaks without penalty?

### Audit Questions

- What is the White Hat to Black Hat ratio? Count the number of White Hat mechanics vs Black Hat mechanics in the core experience loop.
- Is Black Hat used as primary or secondary motivation? If the Black Hat mechanics were removed, would users still engage?
- Do users feel empowered or anxious during and after use?
- Does the product lean on loss aversion as a primary driver? Are streak mechanics, countdown timers, or "don't miss out" messaging central to the experience?
- Report the WH:BH ratio in the audit output.

### Positive Implementation

- White Hat dominant with a WH:BH ratio of 3:1 or higher.
- Black Hat used sparingly and transparently -- limited-time events, not core engagement loops.
- Users report feeling accomplished, skilled, and purposeful.
- Taking breaks is frictionless and penalty-free.

### Exploitative Implementation

- Black Hat dominant -- the primary engagement drivers are scarcity, unpredictability, and loss.
- Constant urgency -- streaks that punish breaks, countdown timers everywhere, "last chance" messaging.
- Users report feeling unable to stop, anxious when not using the product, guilty about breaks.
- The product cannot sustain engagement without Black Hat pressure.

---

## 5. BJ Fogg Behavior Model

**Author:** BJ Fogg, Stanford Persuasive Technology Lab
**Background:** States that behavior occurs when three elements converge at the same moment: sufficient Motivation, sufficient Ability, and an effective Prompt. If any element is missing, the behavior does not happen. Also introduces the Functional Triad describing how technology persuades: as a tool (making behavior easier), as media (providing simulated experiences), and as a social actor (leveraging social dynamics).

### The Three Elements

- **Motivation** -- The user's desire to perform the behavior. Can come from pleasure/pain, hope/fear, or social acceptance/rejection. Higher motivation compensates for lower ability and vice versa.
- **Ability** -- How easy the behavior is to perform. Determined by time, money, physical effort, cognitive effort, social deviance, and routine disruption. Making behavior easier is often more effective than increasing motivation.
- **Prompt** -- The cue that triggers the behavior at the right moment. Without a prompt, even motivated and able users will not act. Prompts can be external (notifications) or internal (habits, emotions).

### Fogg's Golden Rule of Persuasive Technology

Creators should never persuade a person of something they themselves would not consent to be persuaded to do. This is the ethical boundary test for any persuasive design.

### Hope as the Ethical Motivator

Fogg asserts that hope is "probably the most ethical and empowering motivator." Products should inspire users toward positive outcomes rather than frighten them away from negative ones. Fear, guilt, and social pressure are effective motivators but carry ethical weight.

### What to Look For in a Product

- Is the product primarily making desired behavior easier (improving ability), or is it primarily increasing pressure (amplifying motivation through fear/guilt)?
- What type of motivation does the product leverage -- hope and aspiration, or fear and guilt?
- Are prompts informative and timely, or guilt-inducing and persistent?
- Does the product add friction (sludge) to behaviors the user wants but the business does not (e.g., unsubscribing, deleting account)?

### Audit Questions

- Is the product making desired behavior easier (ability) or just increasing pressure (motivation through fear/guilt)?
- What prompts does it use -- informative or guilt-inducing?
- Does the product rely on hope or fear as its primary motivator?
- Apply Fogg's Golden Rule: Would the designers consent to be persuaded in the same way?
- Is there asymmetric friction -- is signing up easier than canceling? Is engaging easier than disengaging?

### Positive Implementation

- Reducing friction for genuinely beneficial actions -- making it easier to learn, save, exercise, connect.
- Prompts that inform ("Your weekly report is ready") rather than pressure ("You're falling behind!").
- Hope-based motivation -- showing users what they could achieve, celebrating progress.
- Symmetric friction -- opting in is as easy as opting out.

### Exploitative Implementation

- Guilt-based or fear-based prompts -- "Your friends are waiting," "Don't lose your streak," "You're missing out."
- Sludge -- artificial difficulty added to actions that benefit the user but not the business (canceling, exporting data, adjusting notification settings).
- Leveraging social pressure as a primary motivator -- making users feel socially deviant for not engaging.
- Asymmetric ability -- signing up takes one click, canceling requires a phone call.

---

## 6. Nudge Theory

**Authors:** Richard Thaler & Cass Sunstein
**Background:** Rooted in the concept of "libertarian paternalism" -- since choice architecture is inevitable (someone must decide the order of options, the default settings, the framing of information), it should be designed consciously to steer people toward outcomes that benefit them. Every design decision is a nudge in some direction; the question is whether it is a deliberate, beneficial nudge or an accidental or extractive one.

### Key Principles

- **Choice preservation** -- A true nudge never removes options. Users can always opt out, choose differently, or go against the default. If opting out is prohibitively difficult, it is not a nudge but coercion.
- **Beneficial defaults** -- Default settings should reflect what most people would choose if they were fully informed, had unlimited time, and had no cognitive biases. The default is the most powerful nudge.
- **Transparency** -- Users should be able to understand that they are being nudged and why. Covert nudges that users cannot detect or evaluate are ethically suspect.
- **Conscious architecture** -- Since every design choice nudges users in some direction, designers have an obligation to be deliberate about the direction.

### Criticisms and Limitations

- **Paternalism concern** -- Assumes the designer knows what is best for the user, which may not always be true.
- **Dark nudges and sludge** -- The same principles can be used to steer users toward outcomes that benefit the company at user expense (dark nudges) or add friction to beneficial user actions (sludge).
- **Blurry ethical line** -- The boundary between helpful defaults and manipulation is genuinely difficult to draw and context-dependent.
- **Autonomy undermining** -- Even well-intentioned nudges may reduce users' capacity for autonomous decision-making over time by making choices for them.

### What to Look For in a Product

- What are the default settings? Do they serve the user's informed preference or the business's engagement metrics?
- How easy is it to change defaults? Is the settings page buried, confusing, or incomplete?
- Are there dark nudges -- design choices that steer users toward spending more money, sharing more data, or engaging more than they intend?
- Is there sludge -- unnecessary friction added to actions that benefit the user (unsubscribing, adjusting privacy settings, requesting data export)?

### Audit Questions

- What are the default settings? Do they serve users or the business?
- Can users easily find and change defaults? How many steps does it take?
- Are nudges directed toward beneficial or extractive outcomes?
- Is there sludge making user-benefiting actions harder than they should be?
- Does the choice architecture preserve genuine freedom of choice, or does it create an illusion of choice?
- Would a fully informed user make the same choices the defaults assume?

### Positive Implementation

- Defaults that serve the user's informed preference -- e.g., privacy-preserving settings as default, study reminders at user-chosen times.
- Easy opt-out from any default -- one or two steps, clearly labeled, no guilt messaging.
- Transparent architecture -- users can see and understand why options are arranged as they are.
- Nudges toward outcomes validated by user research as genuinely beneficial.

### Exploitative Implementation

- Dark nudges -- defaults that maximize data collection, engagement, or spending rather than user benefit.
- Sludge -- cancellation flows that require multiple steps, phone calls, or waiting periods. Privacy settings buried in submenus. Data export that is technically possible but practically impossible.
- Confirm-shaming -- option labels like "No, I don't want to improve" vs "Yes, sign me up."
- Illusion of choice -- all options lead to the same extractive outcome, just framed differently.

---

## 7. Value-Sensitive Design (VSD)

**Authors:** Batya Friedman & Peter Kahn
**Background:** A tripartite methodology that systematically accounts for human values in technology design. Unlike the other frameworks listed here, which focus primarily on individual user behavior and product mechanics, VSD widens the lens to systemic and societal-level impacts. It commits to three fundamental values: human well-being, justice, and dignity.

### The Three Investigation Types

- **Conceptual investigations** -- Identify all stakeholders (direct users, indirect stakeholders, non-users, future users) and the values at stake. Map potential value conflicts. This is philosophical and analytical work.
- **Empirical investigations** -- Research actual user needs, experiences, and value priorities through observation, interviews, and data. Ground the conceptual analysis in lived reality.
- **Technical investigations** -- Examine how the technology's architecture, algorithms, and design choices support or undermine identified values. Determine whether technical alternatives could better serve stakeholder values.

### Scope: Beyond the Individual User

VSD explicitly addresses impacts that other frameworks may miss:
- **Non-users** who are affected by the product without choosing to use it (e.g., children of social media users, communities affected by algorithmic decisions).
- **Vulnerable populations** including children, people with addictive tendencies, those with mental health conditions, and underserved communities.
- **Societal-level effects** including shifts in social norms, democratic participation, attention economy dynamics, and inequality.

### What to Look For in a Product

- Who benefits and who bears costs? Are costs externalized to non-users or vulnerable populations?
- Does the product account for differential impact -- does it affect some groups more negatively than others?
- Are there value conflicts between stakeholders? How are they resolved, and who decides?
- Does the product's business model create inherent conflicts with user well-being?

### Audit Questions

- Who are all stakeholders, including non-users and vulnerable populations?
- What values might be in conflict (e.g., engagement vs. well-being, personalization vs. privacy, growth vs. equity)?
- Does the design account for children, people with addictive tendencies, and underserved populations? Are there safeguards?
- Are societal-level impacts considered -- what happens if this product scales to millions of users?
- Does the business model align with or conflict with the stated user values?
- If this product's mechanics were applied to a vulnerable 14-year-old, would the designers still feel comfortable?

### Positive Implementation

- Considers all stakeholders, not just paying users. Non-user impacts are documented and mitigated.
- Prioritizes well-being over engagement metrics. Willing to sacrifice engagement for user health.
- Accounts for vulnerable populations with specific safeguards -- time limits for minors, content sensitivity controls, addiction-aware design.
- Business model aligns with user benefit (users pay for value, not attention-harvesting for advertisers).
- Regular value audits and stakeholder consultation built into the design process.

### Exploitative Implementation

- Ignores non-user impacts entirely. No consideration of how the product affects communities, families, or society.
- Exploits vulnerable populations -- targets minors with persuasive mechanics, leverages addictive tendencies for engagement, charges more to underserved communities.
- Prioritizes metrics over dignity -- treats users as data points to optimize rather than humans to serve.
- Business model inherently conflicts with user well-being (e.g., revenue scales with time-on-app, but time-on-app harms users).
- No mechanism for stakeholder feedback or value reassessment.
