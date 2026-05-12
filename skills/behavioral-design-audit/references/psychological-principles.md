# Psychological Principles in Product Design

Reference document for the behavioral design audit skill. Covers 12 psychological principles commonly employed in product design, with guidance on detecting them, distinguishing ethical from exploitative applications, and assessing severity when misused.

---

## Quick-Reference Summary

| # | Principle | Primary Detection Signal | Misuse Severity |
|---|-----------|--------------------------|-----------------|
| 1 | Variable Ratio Reinforcement | Randomized rewards, mystery bonuses, "spin the wheel" mechanics | Critical |
| 2 | Loss Aversion | Streak penalties, progress decay, expiration countdowns | High |
| 3 | Endowed Progress Effect | Onboarding checklists starting partially complete | Medium |
| 4 | Commitment & Consistency | Goal-setting during onboarding, "you committed to X" reminders | High |
| 5 | Zeigarnik Effect | Partially completed progress bars, "X remaining" messaging | Medium |
| 6 | FOMO (Fear of Missing Out) | Time-sensitive content, "only X spots left," countdown timers | High |
| 7 | Social Comparison | Leaderboards, percentile rankings, friend activity feeds | High |
| 8 | Peak-End Rule | Session-end celebration screens, post-activity summaries | Medium |
| 9 | Flow State | Adaptive difficulty, infinite scroll, removed stopping points | High |
| 10 | Sunk Cost Effect | "You've been with us for 2 years," total hours/XP displays | High |
| 11 | Identity Investment | Shareable identity cards, year-in-review, "Your" language | Medium-High |
| 12 | Overjustification Effect | Points/badges for naturally enjoyable activities | High (in education) |

---

## 1. Variable Ratio Reinforcement

**Origin:** B.F. Skinner

### Definition

Rewards delivered after unpredictable numbers of actions. Produces the highest and most consistent response rates of all reinforcement schedules. Dopamine is released in anticipation of the reward, not at the moment the reward is received.

### Detection Signals

- Randomized rewards
- Mystery bonuses
- "Spin the wheel" mechanics
- Unpredictable content feeds
- Pull-to-refresh with variable results

### Ethical Use

- Surprise celebration animations for genuine achievements
- Randomized daily challenges with educational value

### Exploitative Use

- Slot machine mechanics
- Loot boxes
- Infinite scroll feeds optimized for dopamine
- Notification patterns designed to create checking habits

### Misuse Severity

**Critical** -- directly linked to addictive behavior patterns; activates the same neural pathways as gambling.

### Audit Questions

- Are variable rewards tied to genuine value or purely to engagement?
- Could this pattern create compulsive checking behavior?

---

## 2. Loss Aversion

**Origin:** Daniel Kahneman & Amos Tversky

### Definition

The psychological pain of losing is approximately twice as powerful as the pleasure of an equivalent gain. People expend disproportionate effort to avoid losses.

### Detection Signals

- Streak mechanics with loss penalties
- Progress decay from inactivity
- "Your items expire" countdowns
- Rank demotion warnings
- Sunk cost messaging

### Ethical Use

- Gentle reminders about maintaining progress
- Streak freezes as a safety net

### Exploitative Use

- Harsh streak penalties causing anxiety
- Aggressive progress decay
- Guilt-based re-engagement ("You lost your 47-day streak!")

### Misuse Severity

**High** -- creates anxiety, compulsive usage, and feelings of obligation.

### Audit Questions

- Is loss messaging the primary or secondary motivator?
- Do users feel motivated or anxious?

---

## 3. Endowed Progress Effect

**Origin:** Nunes & Dreze (2006)

### Definition

People are more motivated to complete a goal when they feel they have already made progress. In the classic car wash experiment, customers given a loyalty card with 2 of 10 stamps pre-filled completed the card at a 34% rate, versus 19% for those given a blank 8-stamp card -- identical effort required.

### Detection Signals

- Onboarding checklists starting partially complete
- Profiles shown at 20% instead of 0%
- Pre-awarded progress points

### Ethical Use

- Acknowledging genuine completed steps (account created, profile set up)
- Starting at Level 1 not Level 0

### Exploitative Use

- Fake progress to create sunk cost
- Misleading completion percentages
- Artificial advancement to drive purchase

### Misuse Severity

**Medium** -- manipulates perception but does not typically create anxiety.

### Audit Questions

- Does the endowed progress reflect genuine accomplishment or is it fabricated?

---

## 4. Commitment & Consistency

**Origin:** Robert Cialdini

### Definition

Once people make an initial commitment, they are more likely to continue investing to maintain consistency. Four factors amplify the effect: the commitment is active, public, effortful, and freely chosen.

### Detection Signals

- Goal-setting during onboarding
- "You committed to X" reminders
- Escalating commitment sequences (foot-in-the-door technique)
- Public goal sharing
- Investment displays ("You've spent 42 hours")

### Ethical Use

- Helping users set and track genuinely desired goals
- Celebrating consistency with personal objectives

### Exploitative Use

- Weaponizing past commitments against users
- Using sunk cost messaging to prevent cancellation
- Escalating commitments beyond original intent

### Misuse Severity

**High** -- exploits the psychological need for self-consistency.

### Audit Questions

- Are commitments genuinely chosen by users?
- Is past commitment used to support or trap users?

---

## 5. Zeigarnik Effect

**Origin:** Bluma Zeigarnik

### Definition

People remember incomplete tasks better than completed ones. The brain keeps unfinished tasks "open" in working memory, creating psychological tension and an urge for closure.

### Detection Signals

- Partially completed progress bars
- "You have X remaining" messaging
- Cliffhanger content
- Unfinished session reminders
- Incomplete daily challenges shown prominently

### Ethical Use

- Showing genuine progress toward meaningful goals
- Resuming where the user left off

### Exploitative Use

- Artificially creating open loops to drive return visits
- Splitting naturally complete experiences into fragments
- Manipulating task boundaries to maximize uncompleted items

### Misuse Severity

**Medium** -- creates mild compulsion but less anxiety than loss aversion.

### Audit Questions

- Are the "incomplete" items genuinely meaningful to the user or artificially fragmented?

---

## 6. FOMO (Fear of Missing Out)

**Origin:** Driven by loss aversion combined with the need for social belonging

### Definition

The brain releases stress hormones when detecting potential social exclusion. FOMO drives more app engagement than any other single psychological trigger.

### Detection Signals

- "Your friends are active right now"
- Time-sensitive content
- Disappearing stories/content
- "Only X spots left"
- Countdown timers
- Social activity notifications

### Ethical Use

- Informing users about genuinely time-limited opportunities they have expressed interest in

### Exploitative Use

- Artificial scarcity
- Fake urgency timers
- Social pressure to engage
- Creating anxiety about missing out on manufactured events

### Misuse Severity

**High** -- creates anxiety that impairs judgment and wellbeing; especially harmful for young users.

### Audit Questions

- Is the scarcity or urgency real?
- Does missing the event cause genuine loss or just manufactured anxiety?

---

## 7. Social Comparison

**Origin:** Leon Festinger (1954)

### Definition

People understand their own abilities by comparing themselves to others. Two types exist: upward comparison ("they're ahead of me") drives aspiration but can cause anxiety; downward comparison ("I'm ahead of them") boosts confidence.

### Detection Signals

- Leaderboards
- Rank displays
- "X people completed this"
- Percentile rankings
- Friend activity feeds
- "You're in the top X%"

### Ethical Use

- Tiered leagues with similar-level peers
- Optional friend comparisons
- Celebrating collective progress

### Exploitative Use

- Global leaderboards that demoralize 90% of users
- Constant comparison notifications
- Competitive framing of non-competitive activities

### Misuse Severity

**High** -- can cause discouragement, anxiety, and disengagement among struggling users.

### Audit Questions

- Does comparison motivate or demoralize?
- Can users opt out?
- Are comparison groups appropriately matched?

---

## 8. Peak-End Rule

**Origin:** Daniel Kahneman

### Definition

People judge experiences by the most intense moment (peak) and how they ended, not by the average. The remembering self -- not the experiencing self -- makes decisions about whether to return.

### Detection Signals

- Session-end celebration screens
- Post-activity summaries
- Strategically placed "wow moments"
- Reward delivery at end of sessions

### Ethical Use

- Ensuring sessions end on positive notes
- Celebrating genuine achievements
- Providing satisfying summaries

### Exploitative Use

- Masking a poor overall experience with an artificially exciting ending
- Ending on negative notes (lost streak, failed attempt) to drive anxiety-based return

### Misuse Severity

**Medium** -- manipulates memory of experience quality.

### Audit Questions

- Does the ending reflect genuine value delivered?
- Are negative endings used to drive guilt-based return?

---

## 9. Flow State

**Origin:** Mihaly Csikszentmihalyi

### Definition

Complete absorption in an activity where time disappears and self-consciousness vanishes. Six conditions are required: challenge-skill balance, clear goals, immediate feedback, sense of control, deep concentration, and autotelic nature (the activity is its own reward).

### Detection Signals

- Adaptive difficulty
- Distraction-free modes
- Immediate feedback loops
- Minimal UI during core activity
- Clear micro-goals

### Ethical Use

- Designing core experiences (practice, learning) for flow with appropriate challenge, minimal distraction, and immediate feedback

### Exploitative Use

- Using flow to trap users in infinite sessions (infinite scroll, auto-play)
- Removing natural stopping points
- Exploiting flow's time-distortion effect

### Misuse Severity

**High** -- users can lose hours without awareness, especially when combined with variable rewards.

### Audit Questions

- Does flow serve the user's goals or the company's engagement metrics?
- Are there natural stopping points?

---

## 10. Sunk Cost Effect

**Origin:** Related to loss aversion but specifically about past investment

### Definition

People continue investing in something because of what they have already invested, not because of the future value it provides. The more invested, the harder it becomes to walk away -- even when walking away is the rational choice.

### Detection Signals

- "You've been with us for 2 years" messages
- Total hours/questions/XP displays
- Progress investment reminders during cancellation flows

### Ethical Use

- Celebrating genuine milestones and progress
- Data portability so investment is not wasted

### Exploitative Use

- Showing investment totals during cancellation to prevent leaving
- Making data non-portable
- Using past investment as emotional leverage

### Misuse Severity

**High** -- traps users in products they want to leave.

### Audit Questions

- Is investment data shown to celebrate or to prevent departure?
- Can users take their data with them?

---

## 11. Identity Investment

**Origin:** Popularized by the Spotify Wrapped pattern

### Definition

When a product becomes part of how users define themselves, switching costs become existential rather than merely practical. Data tracking is reframed as personal narrative.

### Detection Signals

- "Your" language everywhere
- Shareable identity cards
- Personality/type classifications
- Year-in-review features
- Percentile identity ("top 0.5% of listeners")
- Profile customization

### Ethical Use

- Helping users understand their patterns
- Celebrating genuine identity milestones
- Making data useful for self-reflection

### Exploitative Use

- Creating artificial tribal identity to increase switching costs
- Weaponizing identity against the user ("You're a 365-day streaker, don't break it now")

### Misuse Severity

**Medium-High** -- exploits self-concept and creates emotional switching costs.

### Audit Questions

- Does identity investment serve self-knowledge or platform lock-in?
- Is the identity genuine or manufactured?

---

## 12. Overjustification Effect

**Origin:** Edward Deci (1971)

### Definition

When external rewards are given for intrinsically enjoyable activities, intrinsic motivation can diminish. After rewards are removed, people engage in the activity less than they did before rewards were ever introduced.

### Detection Signals

- Points/badges/rewards for activities users would do naturally
- Reward systems that shift focus from content to mechanics
- Declining engagement when reward systems change

### Ethical Use

- Using rewards for scaffolding (onboarding) then fading them as intrinsic motivation develops
- Rewards that acknowledge skill rather than mere participation

### Exploitative Use

- Making learning contingent on reward collection
- Creating dependency on external validation
- Gamifying to the point where the game overshadows the content

### Misuse Severity

**High in education** -- can permanently undermine intrinsic motivation to learn.

### Audit Questions

- Could users enjoy this activity without the rewards?
- Do rewards enhance or replace intrinsic interest?
