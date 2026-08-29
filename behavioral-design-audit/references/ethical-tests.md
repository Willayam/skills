# Ethical Tests for Behavioral Design Auditing

This reference documents 10 ethical tests to apply when auditing a product's behavioral design. Each test provides a structured framework for evaluating whether engagement mechanics, persuasive features, and design patterns are ethical, manipulative, or somewhere in between.

## Quick-Reference Summary

| # | Test Name | Source | Core Question |
|---|-----------|--------|---------------|
| 1 | Regret Test | Nir Eyal | Would users still engage if they fully understood the mechanism? |
| 2 | Transparency Test | Persuasion Knowledge Model | Does the feature work equally well when users understand why it exists? |
| 3 | Autonomy Test | Self-Determination Theory (Deci & Ryan) | Does the user feel they are choosing to engage, or compelled to engage? |
| 4 | Fogg's Golden Rule | BJ Fogg | Would the creators consent to be persuaded this way by their own design? |
| 5 | Manipulation Matrix | Nir Eyal | Does the maker use the product AND does it improve users' lives? |
| 6 | Alignment Test | Ethical Engagement Design | Do business metrics improve when and because user outcomes improve? |
| 7 | Calm Technology Test | Amber Case | Does this require the smallest possible amount of attention to deliver value? |
| 8 | Value-Sensitive Design Test | Friedman & Kahn | Does this design respect well-being, justice, and dignity for all stakeholders? |
| 9 | EU DSA Compliance Test | Digital Services Act Article 25 | Does this interface deceive, manipulate, or distort free decision-making? |
| 10 | Informed User Test | Persuasion Knowledge Model | Are we helping users do what they want, or getting them to do what we want? |

---

## Test 1: The Regret Test

### Source
Nir Eyal, author of *Hooked* and *Indistractable*. Eyal proposed this test as a practical litmus test for distinguishing persuasion from manipulation in product design.

### Core Question
"If people knew everything the product designer knows, would they still execute the intended behavior? Are they likely to regret doing this?"

### Procedure
1. Identify each engagement mechanic in the product (streaks, notifications, rewards, social pressure, progress systems, urgency cues, etc.).
2. For each mechanic, imagine the user has complete information about why it exists and how it works -- the internal product documents, the growth metrics it targets, the psychological principle it exploits.
3. With that full knowledge, ask: Would the user still choose to engage with this feature?
4. Then ask: After engaging, would the user feel good about the time/money/attention they spent, or would they feel manipulated?
5. Document which features pass and which fail this thought experiment.

### Pass/Partial/Fail Criteria
- **Pass:** Users would not regret the behavior even with full transparency. The feature delivers genuine value that the user would endorse even after understanding the design intent behind it.
- **Partial:** Some features pass (e.g., spaced repetition reminders) while others would cause regret (e.g., guilt-inducing streak loss messages).
- **Fail:** The core engagement loop relies on user ignorance of the mechanism. If users knew how it worked, they would disengage or feel deceived.

### Example Scenario
A test prep app sends a push notification: "You're on a 14-day streak! Don't break it now!" The user opens the app and does a quick practice session not because they want to learn but because they fear losing the streak. If the user understood that the streak counter was designed specifically to trigger loss aversion and increase DAU, would they still value it? If the answer is "they'd feel manipulated," the feature fails the Regret Test. Compare this to a notification that says "Your last practice session improved your verbal score by 8% -- want to keep that momentum going?" which is more likely to pass because it connects engagement to genuine progress.

---

## Test 2: The Transparency Test

### Source
Derived from the Persuasion Knowledge Model (Friestad & Wright, 1994). The PKM describes how people develop knowledge about persuasion tactics and how that knowledge changes their response to those tactics.

### Core Question
"Would this design decision work equally well (or better) if the user understands exactly why it exists?"

### Procedure
1. For each feature or engagement mechanic, articulate its purpose out loud as if explaining it to the user. For example: "We show you a streak counter because spaced repetition works better with consistent daily practice."
2. Evaluate the user's likely reaction to hearing that explanation. Does it sound helpful, or does it sound manipulative?
3. Categorize the feature:
   - **Enhanced by transparency:** Spaced repetition becomes more effective when users understand the science behind it. Progress tracking is more motivating when users know why it matters.
   - **Neutral to transparency:** The feature works the same whether or not users understand the design rationale.
   - **Undermined by transparency:** The feature loses its effectiveness when users recognize the mechanism. Guilt-based streaks get less compelling. Fake scarcity becomes obvious.
4. Features in the third category are manipulative by this test's definition.

### Pass/Partial/Fail Criteria
- **Pass:** The feature becomes more compelling when users understand how and why it works. Transparency strengthens engagement.
- **Partial:** The feature works the same whether or not users understand it. Transparency neither helps nor hurts.
- **Fail:** The feature loses effectiveness when users understand how it works. This is a strong signal of manipulation, because it means the feature depends on the user not recognizing the persuasion tactic.

### Example Scenario
A language learning app uses spaced repetition to schedule review sessions. When users are told "We schedule your reviews based on the forgetting curve -- you'll see words right before you'd forget them, which is the most efficient way to build long-term memory," users engage more enthusiastically because they trust the system. This passes. Compare this to a feature that shows "3 other users are studying right now!" when the number is fabricated. If users knew it was fake social proof, they would distrust the app. This fails.

---

## Test 3: The Autonomy Test

### Source
Self-Determination Theory (SDT) by Edward Deci and Richard Ryan. SDT identifies autonomy, competence, and relatedness as fundamental human psychological needs. When products support autonomy, motivation is intrinsic and sustainable. When products undermine autonomy, motivation is extrinsic and fragile.

### Core Question
"Does the user feel they are choosing to engage, or feeling compelled to engage?"

### Procedure
1. **Check opt-in and customization:** Can users customize or disable engagement features (notifications, streaks, leaderboards, social features) without penalty? Are these features opt-in by default, or opt-out?
2. **Check break tolerance:** What happens when a user takes a break? Is the break punished (streak reset, lost progress, guilt messages)? Or is it accommodated (streak freeze, "welcome back" messaging, no penalty)?
3. **Check disengagement cost:** How hard is it to reduce engagement? Can users downgrade, pause, or leave without friction? Is the cancellation flow straightforward or does it use dark patterns (multiple confirmation screens, guilt trips, hidden options)?
4. **Check notification control:** Can users set notification frequency and type? Are defaults respectful (few, relevant) or aggressive (many, frequent)?
5. **Check extrinsic pressure signals:** Look for language like "Don't let your friends down," "You'll lose your progress," "Last chance!" These signal autonomy-undermining design.

### Pass/Partial/Fail Criteria
- **Pass:** All engagement features are opt-in, customizable, and there are no penalties for breaks. Users have granular control over their experience. Disengagement is frictionless.
- **Partial:** Some features are customizable but others impose guilt or penalties. For example, users can control notifications but streaks are reset punitively.
- **Fail:** Primary engagement relies on loss aversion, guilt, or compulsion. Users feel trapped, and reducing engagement is costly or punishing.

### Example Scenario
A fitness app allows users to set their own workout goals, choose which notifications they receive, and pause their streak for vacation without penalty. When a user misses a day, the app says "Rest days are important too. Ready when you are." This passes. Compare this to a fitness app that resets a 90-day streak to zero after one missed day, sends "You've lost your streak!" push notifications, and requires navigating three screens of "Are you sure?" prompts to turn off notifications. This fails.

---

## Test 4: Fogg's Golden Rule

### Source
BJ Fogg, founder of the Stanford Behavior Design Lab and creator of the Fogg Behavior Model. Fogg's Golden Rule of habit-forming technology states: "Never build something you wouldn't want to be persuaded by yourself."

### Core Question
"Would the creators of this product consent to be persuaded in the same way by their own design?"

### Procedure
1. For each persuasive feature in the product (notifications, reward systems, social comparisons, urgency mechanics, subscription flows, cancellation processes), put yourself in the position of the design team.
2. Ask: Would the designers accept receiving these notifications at this frequency?
3. Ask: Would the designers accept this cancellation flow if they wanted to leave a competing product?
4. Ask: Would the designers find these reward mechanics enjoyable or manipulative if they encountered them in a product they use daily?
5. Ask: Would the designers be comfortable showing this feature to their family and explaining how it works?
6. If the answer to any of these is "no," the feature violates Fogg's Golden Rule.

### Pass/Partial/Fail Criteria
- **Pass:** Designers would genuinely want this experience for themselves. They would be proud to explain every feature to their family and would happily use their own product daily.
- **Partial:** Some features pass (the core learning experience) but others seem designed for someone the designers consider less sophisticated than themselves.
- **Fail:** Designers clearly build features they would find annoying, manipulative, or disrespectful if they encountered them as users. The team builds for "users" but not for "people like us."

### Example Scenario
A productivity app's team uses their own app daily and finds the task-scheduling feature genuinely helpful. However, the growth team added a "Your productivity dropped 15% this week" notification designed to trigger anxiety and re-engagement. When the PM receives this notification on their own phone, they find it stressful and unhelpful, and they mute it. If the team mutes their own notification, it fails Fogg's Golden Rule -- they are building something they would not consent to be persuaded by.

---

## Test 5: The Manipulation Matrix

### Source
Nir Eyal, from *Hooked: How to Build Habit-Forming Products*. The Manipulation Matrix is a two-axis framework for classifying the ethical standing of habit-forming products.

### Core Question
"Does the maker use the product AND does it materially improve users' lives?"

### Procedure
1. **Axis 1 -- Maker Uses Product:** Determine whether the product team genuinely uses their own product. Not as a dogfooding exercise, but as real users who depend on it. Do they use it the way their target users use it?
2. **Axis 2 -- Materially Improves Users' Lives:** Determine whether the product measurably improves user outcomes. This means real improvements: better test scores, healthier habits, saved time, learned skills -- not just "engagement" or "time spent in app."
3. **Classify into quadrant:**
   - **Facilitator (uses + improves):** The maker believes in the product and it delivers real value. This is the ethical quadrant.
   - **Entertainer (uses + does not improve):** The maker enjoys the product but it doesn't materially improve lives (e.g., games, social media). Acceptable but worth scrutiny.
   - **Peddler (does not use + improves):** The product improves lives but the team doesn't use it themselves. Questionable -- they may not truly understand the user experience.
   - **Dealer (does not use + does not improve):** The maker would never use the product and it doesn't improve lives. This is the unethical quadrant.

### Pass/Partial/Fail Criteria
- **Pass:** The product falls in the Facilitator quadrant. The team uses the product and it demonstrably improves user outcomes.
- **Partial:** The product falls in the Entertainer or Peddler quadrant. It has some ethical standing but is missing one of the two key criteria.
- **Fail:** The product falls in the Dealer quadrant. The team does not use the product and it does not improve users' lives. The product exists solely to extract value from users.

### Example Scenario
A test prep app is built by a team of former students who use the app themselves to stay sharp and who track user score improvements as their north star metric. Users who complete the program measurably improve their test scores. This is a Facilitator -- it passes. Compare this to a social media app whose executives limit their own children's screen time on the platform while optimizing for maximum time-on-app for other people's children. The team does not use the product the way users do, and the product does not improve users' lives. This is a Dealer -- it fails.

---

## Test 6: The Alignment Test

### Source
Ethical Engagement Design frameworks, synthesized from multiple sources including Tristan Harris (Center for Humane Technology), Joe Edelman (Meaning Alignment), and the broader Time Well Spent movement.

### Core Question
"Do business metrics improve when and because user outcomes improve?"

### Procedure
1. **Map business KPIs:** List all primary business metrics: DAU, MAU, retention, session length, conversion rate, revenue, LTV.
2. **Map user outcomes:** List all intended user outcomes: test score improvement, skill acquisition, goal completion, knowledge retention, satisfaction.
3. **Draw connections:** For each business KPI, determine whether it improves when users achieve their goals, or whether it improves independently of (or inversely to) user success.
4. **Identify misalignment:** Look for cases where:
   - The business benefits from users spending more time than necessary (session length as KPI when efficiency would serve users better).
   - The business benefits from users failing (a prep course that profits more from repeat customers than from students who pass on the first attempt).
   - The business benefits from user anxiety (re-engagement driven by fear of falling behind rather than genuine desire to learn).
5. **Score alignment:** What percentage of business KPIs are directly aligned with user outcomes?

### Pass/Partial/Fail Criteria
- **Pass:** Revenue and retention are directly tied to user goal achievement. The product succeeds when users succeed. For example, a test prep app where revenue correlates with score improvement and course completion.
- **Partial:** Some metrics are aligned (retention correlates with learning outcomes) but others are not (session length is optimized beyond what learning requires).
- **Fail:** Business success is decoupled from or inversely correlated with user wellbeing. The product extracts attention, money, or data regardless of whether users benefit.

### Example Scenario
A test prep app charges a subscription and tracks "user score improvement" as its primary success metric. When users improve their scores and pass their exams, they tell friends, driving organic growth. The business does better when users do better. This passes. Compare this to a test prep app that earns more revenue when students fail and re-subscribe for another cycle. The business has a perverse incentive to keep students "almost ready" but never fully prepared. This fails.

---

## Test 7: The Calm Technology Test

### Source
Amber Case, based on the Calm Technology principles originally articulated by Mark Weiser and John Seely Brown at Xerox PARC. Case's framework argues that the best technology requires the minimum possible attention from users to deliver its value.

### Core Question
"Does this technology require the smallest possible amount of attention to deliver its value?"

### Procedure
1. **Audit notifications:** For each notification the product sends, ask: Is this necessary? Does it inform the user about something they need to know right now? Could it be batched, delayed, or delivered passively instead?
2. **Audit animations and visual elements:** For each animation, badge, counter, or visual cue, ask: Does this serve the user's task or does it demand attention for the product's benefit?
3. **Audit prompts and interruptions:** For each modal, popup, interstitial, or prompt, ask: Could the same value be delivered without interrupting the user's flow?
4. **Assess peripheral vs. focal attention:** Does the product use peripheral awareness appropriately (e.g., a subtle progress indicator) or does it constantly demand focal attention (e.g., flashing badges, urgent-looking counters)?
5. **Measure cognitive load:** Does the product feel like it adds stress to the user's life, or does it feel like a calm, reliable tool?

### Pass/Partial/Fail Criteria
- **Pass:** The product delivers value with minimal attention demand. Notifications are rare and relevant. Visual design is clean and focused. The product uses peripheral awareness appropriately and does not compete aggressively for focal attention.
- **Partial:** Some unnecessary attention demands exist (badge counters, occasional irrelevant notifications) but the core experience is calm and focused on user tasks.
- **Fail:** The product aggressively competes for attention far beyond what its value requires. It uses red badges, frequent push notifications, attention-grabbing animations, and urgency cues to demand focal attention disproportionate to the value it delivers.

### Example Scenario
A weather app displays current conditions on a home screen widget (peripheral awareness) and only sends push notifications for severe weather alerts (genuine urgency). Users get weather information with minimal cognitive demand. This passes. Compare this to a weather app that sends daily push notifications ("It's 72 degrees today!"), displays a red badge on the app icon at all times, and opens with a full-screen interstitial ad before showing the forecast. The attention demand far exceeds the value delivered. This fails.

---

## Test 8: The Value-Sensitive Design Test

### Source
Batya Friedman and Peter Kahn, University of Washington. Value-Sensitive Design (VSD) is a theoretically grounded approach to technology design that accounts for human values in a principled and comprehensive manner throughout the design process.

### Core Question
"Does this design respect human well-being, justice, and dignity for all stakeholders?"

### Procedure
1. **Identify all stakeholders:** List every group affected by the product, including:
   - Primary users (people who use the product directly).
   - Secondary users (people who interact with primary users and are affected indirectly, such as parents of child users).
   - Non-users (people who are affected by the product's existence even though they do not use it).
   - Vulnerable populations (children, people with addictive tendencies, people with anxiety disorders, financially stressed populations, underserved communities).
2. **For each stakeholder group, assess:**
   - **Autonomy:** Does the design respect their ability to make free choices?
   - **Non-exploitation:** Does the design avoid exploiting their vulnerabilities (developmental stage, cognitive biases, financial stress, addictive tendencies)?
   - **Dignity:** Does the design treat them with respect, not as targets to be manipulated?
   - **Informed consent:** Do they understand how the product affects them?
3. **Check for externalized harm:** Does the product benefit primary users at the expense of non-users or vulnerable populations?
4. **Check for differential impact:** Does the product affect different populations differently, and are those differences accounted for in the design?

### Pass/Partial/Fail Criteria
- **Pass:** The design accounts for all stakeholders including vulnerable populations. Safeguards exist for children, people with addictive tendencies, and other at-risk groups. Harm is not externalized.
- **Partial:** The design serves primary users well but ignores some stakeholder impacts. For example, the app works well for adults but has no safeguards for teenage users who may be more susceptible to social comparison.
- **Fail:** The design exploits vulnerable populations or externalizes harm. For example, a product that targets compulsive behavior patterns in people with addictive tendencies, or that profits from children's inability to distinguish ads from content.

### Example Scenario
A test prep app for high school students includes: time-limit reminders ("You've been studying for 2 hours -- take a break"), parental visibility into study time (without exposing individual answers), no social comparison leaderboards for students under 16, and an "exam anxiety" mode that removes countdown timers during practice. The app proactively considers vulnerable populations (stressed teens, students with test anxiety) and designs safeguards. This passes. Compare this to a test prep app that ranks students publicly, sends "You're falling behind your classmates" notifications to teenagers, and has no time-limit suggestions, actively exploiting adolescent social anxiety to drive engagement. This fails.

---

## Test 9: The EU DSA Compliance Test

### Source
European Union Digital Services Act (DSA), specifically Article 25 which prohibits online platforms from designing, organizing, or operating their interfaces in a way that deceives, manipulates, or materially distorts users' ability to make free and informed decisions (commonly referred to as the prohibition on "dark patterns").

### Core Question
"Does this interface deceive, manipulate, or materially distort users' ability to make free and informed decisions?"

### Procedure
Check systematically for each of the following DSA-prohibited patterns:
1. **Asymmetric friction:** Is cancellation significantly harder than subscription? Does opting out of data collection require more steps than opting in?
2. **Visual prominence bias:** Are choices the company prefers made visually prominent (large, colorful, primary position) while user-protective choices are de-emphasized (small, grey, hidden)?
3. **Nagging:** Does the product repeatedly request something the user has already declined? Are dismissed prompts shown again after a short interval?
4. **Preselection/default manipulation:** Are payment options, data sharing toggles, or subscription tiers pre-checked or pre-selected in the company's favor?
5. **Fake urgency/scarcity:** Does the product display countdown timers, "limited availability" messages, or "act now" prompts that are artificial?
6. **False social proof:** Does the product display fabricated user counts, fake reviews, or misleading activity indicators?
7. **Confirm-shaming:** Does declining an option use guilt-inducing language ("No, I don't want to improve my score")?
8. **Hidden information:** Are costs, commitments, or consequences buried in fine print or revealed only after the user has invested effort?

### Pass/Partial/Fail Criteria
- **Pass:** No DSA-prohibited patterns detected. The interface treats all choices symmetrically, presents information clearly, and respects user decisions without nagging or manipulation.
- **Partial:** Minor instances found that are easily correctable. For example, a slightly asymmetric cancellation flow or one instance of visual prominence bias in a settings page.
- **Fail:** Core UX patterns violate DSA Article 25. The product relies on dark patterns for conversion, retention, or monetization.

### Example Scenario
A subscription app allows users to cancel with two taps (Settings > Cancel Subscription > Confirm), the same number of taps required to subscribe. The cancellation button is the same size and visual weight as other options. No "Are you sure?" guilt screens. No "Here's what you'll lose" fear messaging. Subscription and cancellation are symmetric. This passes. Compare this to an app where subscribing takes one tap but cancelling requires navigating to a hidden settings page, clicking through four confirmation screens with guilt-inducing copy ("You'll lose access to 500 hours of content"), and finally sending an email to customer support. This fails.

---

## Test 10: The Informed User Test

### Source
Derived from the Persuasion Knowledge Model (Friestad & Wright, 1994). This test operationalizes the PKM's insight that persuasion attempts are ethical when they help people achieve their own goals, and manipulative when they redirect people toward the persuader's goals.

### Core Question
"Are we helping users do what they already want to do, or getting them to do what we want them to do?"

### Procedure
1. **List user-stated goals:** What do users say they want from this product? (Learn a language, pass a test, get fit, stay informed.)
2. **List company goals:** What does the company optimize for? (DAU, session length, subscription conversion, retention, ad revenue.)
3. **For each engagement feature, classify:**
   - **User-serving:** The feature directly helps users achieve their stated goals. A spaced repetition algorithm serves the user's goal of learning efficiently.
   - **Company-serving:** The feature primarily serves company metrics. An infinite scroll feed serves session length, not the user's goal.
   - **Dual-serving:** The feature serves both. A well-designed streak can serve both the user's consistency goal and the company's retention metric.
4. **Apply the knowledge test:** For each feature, ask: If the user knew this feature existed primarily to serve the company's goals, would they still want it? If users would reject the feature upon understanding its true purpose, it is manipulative.
5. **Calculate the ratio:** What percentage of engagement features are user-serving vs. company-serving?

### Pass/Partial/Fail Criteria
- **Pass:** Features clearly serve user-stated goals. Company benefits (revenue, retention, growth) are a natural byproduct of users achieving their goals. Users would endorse every feature if they understood its purpose.
- **Partial:** A mix of user-serving and company-serving features. The core product serves users, but some engagement mechanics are primarily company-serving (e.g., aggressive upsell prompts, notification frequency optimized for DAU rather than learning).
- **Fail:** Core features primarily serve company metrics at the user's expense. The product is optimized for engagement, not for user outcomes. Features that users would reject if they understood the purpose are central to the experience.

### Example Scenario
A test prep app includes a study planner that schedules sessions based on the user's exam date and available time, a progress dashboard showing score improvement over time, and practice tests that adapt difficulty to the user's level. All of these features serve the user's goal of passing their exam. The company benefits because satisfied users subscribe longer and refer friends. This passes. Compare this to a test prep app that includes: an infinite feed of "study tips" articles designed to maximize session length (not learning), daily push notifications timed for maximum open rates rather than optimal study times, and a leaderboard that triggers social anxiety to prevent churn. These features serve the company's engagement metrics at the expense of the user's study efficiency. This fails.
