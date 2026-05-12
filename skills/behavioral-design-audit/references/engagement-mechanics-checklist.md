# Engagement Mechanics Checklist

Reference for auditing 16 engagement mechanics in consumer apps. Each mechanic includes detection methods, a 1-5 quality scale, ethical checklists, common pitfalls, and best practices.

Use this checklist to evaluate whether an app's engagement patterns serve users or exploit them.

---

## Summary Table

| # | Mechanic | Primary Detection | Ethical Risk Level |
|---|----------|-------------------|--------------------|
| 1 | Streaks | Streak counter, flame icons, consecutive day tracking | Medium |
| 2 | Progress Bars | Completion percentages, skill trees, mastery indicators | Low-Medium |
| 3 | XP & Level Systems | XP counters, level badges, level-up animations | Medium |
| 4 | Leaderboards | Ranking tables, league tiers, friend comparisons | Medium-High |
| 5 | Daily Rewards / Login Bonuses | Daily reward popups, calendar markers, escalating displays | Medium-High |
| 6 | Variable / Mystery Rewards | Mystery boxes, spin-the-wheel, random bonus multipliers | High |
| 7 | Social Validation (Kudos/Reactions) | Like/reaction buttons, activity feeds, kudos notifications | Medium |
| 8 | Challenges & Events | Challenge banners, event countdowns, themed content | Low-Medium |
| 9 | Hearts / Energy / Lives System | Heart counters, "out of hearts" screens, regeneration timers | High |
| 10 | Push Notifications | Notification content, frequency, timing, personalization | Medium-High |
| 11 | Session-End Celebrations | Congratulations screens, XP summaries, completion animations | Low |
| 12 | Adaptive Difficulty | Difficulty indicators, performance-based content selection | Low |
| 13 | Spaced Repetition | Review prompts, memory strength indicators, due-for-review items | Very Low |
| 14 | Social Sharing | Share buttons on achievements, shareable cards, social post generators | Medium |
| 15 | Achievement Badges | Badge collections, achievement galleries, profile displays | Low-Medium |
| 16 | Team / Group Mechanics | Team challenges, group leaderboards, collaborative goals | Medium |

---

## Standard Ethical Checklist

Every mechanic is evaluated against these five questions:

1. **Serves user goals?** -- Does this mechanic help the user achieve what they came to the product for?
2. **Customizable / opt-out?** -- Can users adjust or disable this mechanic without penalty?
3. **Transparent mechanism?** -- Is it clear to the user how this mechanic works and why it exists?
4. **Passes Regret Test?** -- Would the user, reflecting a week later, feel good about behavior this mechanic drove?
5. **Passes Transparency Test?** -- If the full design intent were published, would the company be proud of it?

---

## 1. Streaks

### Definition
Track consecutive days or sessions of engagement. Streaks leverage loss aversion (fear of breaking the chain), sunk cost (days already invested), identity (becoming "someone who does this daily"), and social proof (others maintaining theirs) simultaneously.

### Detection Signals

**UI indicators:**
- Streak counter displayed on home screen
- Flame, fire, or calendar icons
- Streak milestone celebrations (7 days, 30 days, 100 days)
- Streak freeze or shield options
- Streak recovery offers (often paid)

**Code patterns:**
Search for: `streak`, `consecutiveDays`, `dailyLogin`, `streakFreeze`, `streakCount`, `currentStreak`, `longestStreak`, `streakProtection`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Simple counter only -- no milestones, no protection, no context |
| 2 | Counter + milestone markers (7-day, 30-day celebrations) |
| 3 | + Freeze protection so a single miss does not reset everything |
| 4 | + Celebrations + sharing on milestones, visual streak history |
| 5 | + Customizable goals (not forced daily) + gentle handling of breaks |

### Ethical Checklist

- [ ] **Serves user goals?** Does maintaining the streak correlate with genuine skill or habit building?
- [ ] **Customizable / opt-out?** Can users set their own frequency goal (e.g., 3x/week instead of daily)?
- [ ] **Transparent mechanism?** Does the app explain what counts toward maintaining the streak?
- [ ] **Passes Regret Test?** Would users who maintained a streak for months feel it was worthwhile?
- [ ] **Passes Transparency Test?** Would publishing "we use loss aversion to drive daily opens" be acceptable?

### Common Issues
- Streak guilt when broken, leading to negative association with the product
- Anxiety about maintaining the streak overshadowing actual learning or engagement
- Feeling obligated rather than motivated -- the streak becomes the reason, not the activity
- Paid streak recovery creating a monetization incentive to NOT protect streaks well
- No distinction between meaningful engagement and a token daily open

### Best Practice
Duolingo-style implementation with freezes, celebration on milestones, and gentle break messaging. When a user returns after a break, show "Welcome back!" not "You lost your streak!" Offer flexible goal setting (practice 3 days a week vs. every day). The streak should reinforce a habit the user wants, not create one the product wants.

---

## 2. Progress Bars

### Definition
Visual representation of advancement toward a goal. Progress bars leverage the Zeigarnik Effect -- the cognitive tendency to remember and feel compelled to complete unfinished tasks. A partially filled bar creates a psychological urge to fill it.

### Detection Signals

**UI indicators:**
- Horizontal or circular bars showing completion percentage
- Skill trees with filled/unfilled nodes
- Section mastery indicators
- Profile completeness meters
- Chapter or lesson completion trackers

**Code patterns:**
Search for: `progressBar`, `completion`, `percentage`, `mastery`, `skillLevel`, `progressPercent`, `completionRate`, `masteryLevel`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Single linear bar showing overall completion |
| 2 | Segmented or sectioned bar (per topic, per chapter) |
| 3 | + Non-linear progression (faster early progress to build momentum) |
| 4 | + Multiple dimensions of progress (mastery, coverage, retention) |
| 5 | + Meaningful milestones + user-set goals tied to genuine outcomes |

### Ethical Checklist

- [ ] **Serves user goals?** Does the progress metric represent genuine advancement toward the user's objective?
- [ ] **Customizable / opt-out?** Can users choose which progress dimensions matter to them?
- [ ] **Transparent mechanism?** Is it clear how progress percentage is calculated?
- [ ] **Passes Regret Test?** Does reaching 100% correspond to actual competence or completion?
- [ ] **Passes Transparency Test?** Would publishing the progress calculation formula be acceptable?

### Common Issues
- Misleading progress percentages (80% complete but 80% of the difficulty remains)
- Artificially slow progress in later stages to drive more engagement sessions
- Progress bars that never reach 100% because new content keeps being added
- Progress inflation to make users feel good without corresponding skill gain
- Multiple overlapping progress indicators creating confusion

### Best Practice
LinkedIn profile completeness model -- clear, actionable, tied to genuine value. Each step toward completion should provide real benefit. Progress should be honest: if a user is 30% through material, show 30%, not 60%. Use multiple dimensions (coverage vs. mastery) to provide a nuanced picture.

---

## 3. XP & Level Systems

### Definition
Numerical progress representation through experience points and tiered levels. XP provides granular, immediate feedback on every action. Levels provide clear milestones and identity markers. Together they create a dual-speed reward system: constant micro-rewards (XP) and periodic macro-rewards (level-ups).

### Detection Signals

**UI indicators:**
- XP counters incrementing after actions
- Level badges or indicators on profile
- Level-up animations and celebrations
- XP multipliers or bonus XP events
- XP breakdown by activity type

**Code patterns:**
Search for: `xp`, `experiencePoints`, `level`, `levelUp`, `xpMultiplier`, `xpGained`, `totalXp`, `levelThreshold`, `xpBonus`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | XP counter only -- numbers go up with no context or meaning |
| 2 | + Levels with names or tiers that provide identity |
| 3 | + Weighted XP by difficulty (harder questions earn more) |
| 4 | + Level-gated content or features that make levels meaningful |
| 5 | + Meaningful level progression tied to actual skill with calibrated thresholds |

### Ethical Checklist

- [ ] **Serves user goals?** Does XP earned correlate with genuine learning or skill development?
- [ ] **Customizable / opt-out?** Can users hide XP/levels if they find them distracting?
- [ ] **Transparent mechanism?** Is it clear how XP is calculated and what determines level thresholds?
- [ ] **Passes Regret Test?** Would a Level 50 user feel their level reflects real capability?
- [ ] **Passes Transparency Test?** Would publishing the XP formula and level curve be acceptable?

### Common Issues
- XP inflation making numbers meaningless (earning 10,000 XP per session)
- Levels disconnected from actual skill (Level 30 user who cannot perform basic tasks)
- Early levels too easy and late levels impossibly slow, creating a misleading initial experience
- XP for trivial actions (opening app, visiting settings) diluting the signal
- Multiplier events creating urgency that disrupts natural usage patterns

### Best Practice
Early levels should be quick (endowed progress effect -- get users past the "beginner" identity fast). Difficulty should scale so XP per session stays roughly constant. Level names should provide identity ("Expert," "Master") that users feel proud of. XP should weight difficulty: a hard problem solved correctly should earn significantly more than an easy one.

---

## 4. Leaderboards

### Definition
Rank users by performance metrics. Leaderboards leverage social comparison theory -- the human tendency to evaluate ourselves by comparing to others. They can motivate top performers but demoralize the majority.

### Detection Signals

**UI indicators:**
- Ranking tables showing user position
- League tiers (Bronze, Silver, Gold, Diamond)
- Friend comparison views
- "Top X%" badges or notifications
- Weekly reset countdowns
- Promotion/demotion indicators

**Code patterns:**
Search for: `leaderboard`, `ranking`, `league`, `tier`, `weeklyReset`, `promotion`, `demotion`, `rank`, `topUsers`, `leagueStanding`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Global leaderboard only -- demoralizing for 90%+ of users |
| 2 | + Friend leaderboard for relevant comparison |
| 3 | + Tiered leagues with ~30 matched users per group |
| 4 | + Weekly resets with promotion/demotion between tiers |
| 5 | + Opt-out option + appropriate skill matching + team-based options |

### Ethical Checklist

- [ ] **Serves user goals?** Does competition enhance the user's core objective or distract from it?
- [ ] **Customizable / opt-out?** Can users opt out of leaderboards without losing features?
- [ ] **Transparent mechanism?** Is the ranking algorithm and matching logic clear?
- [ ] **Passes Regret Test?** Would bottom-ranked users feel the leaderboard helped them?
- [ ] **Passes Transparency Test?** Would publishing the matching algorithm be acceptable?

### Common Issues
- Global leaderboards where the top is unreachable, demotivating 90%+ of users
- No opt-out for users who find competition stressful or counterproductive
- Mismatched skill levels in the same league creating unfair comparisons
- Leaderboards rewarding time spent over skill (whoever grinds most wins)
- Rankings based on total XP rather than efficiency or improvement

### Best Practice
Duolingo tiered leagues with approximately 30 matched users, weekly resets, and promotion/demotion. Small groups make top-3 feel achievable. Weekly resets give fresh starts. Matching by activity level (not just skill) keeps competition fair. Always offer an opt-out path.

---

## 5. Daily Rewards / Login Bonuses

### Definition
Rewards granted for daily engagement, often escalating over consecutive days. Creates a simple behavioral loop: open app, receive reward, close app (or stay to use reward). Escalating rewards add sunk-cost pressure -- missing a day resets the escalation.

### Detection Signals

**UI indicators:**
- Daily reward popup on app open
- Calendar UI with reward markers for each day
- Escalating reward displays (Day 1: 10 coins, Day 7: 100 coins)
- "Claim" buttons
- Countdown to next reward

**Code patterns:**
Search for: `dailyReward`, `loginBonus`, `dailyBonus`, `consecutiveDay`, `claimReward`, `dailyClaim`, `rewardCalendar`, `loginStreak`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Same reward every day -- minimal effort, minimal value |
| 2 | Escalating rewards over consecutive days |
| 3 | + Meaningful rewards (unlocks content, not just points) |
| 4 | + Reward tied to useful content (daily challenge, featured lesson) |
| 5 | + Rewards that directly serve learning or core goals |

### Ethical Checklist

- [ ] **Serves user goals?** Does the daily reward encourage meaningful engagement or just app opens?
- [ ] **Customizable / opt-out?** Can users disable the popup without losing progress?
- [ ] **Transparent mechanism?** Is the reward schedule visible and predictable?
- [ ] **Passes Regret Test?** Would users feel good about opening the app just to claim a reward?
- [ ] **Passes Transparency Test?** Would publishing "we give daily rewards to boost DAU metrics" be acceptable?

### Common Issues
- Hollow rewards that add no real value (cosmetic currency with nothing to spend it on)
- Missed-day anxiety and guilt from breaking the consecutive chain
- The reward becoming the only reason to open the app
- Escalating rewards creating outsized pressure to not miss a single day
- Login bonus popup blocking access to actual content

### Best Practice
Daily challenge with educational value rather than a pure reward handout. The "reward" should be the activity itself -- a curated daily question set, a new concept to explore, or a targeted review session. The act of engagement should BE the reward, not a hollow token attached to it.

---

## 6. Variable / Mystery Rewards

### Definition
Unpredictable reward delivery following a variable ratio schedule. This is the most psychologically potent reward pattern -- the same mechanism that makes slot machines compelling. Creates anticipation and constant engagement through the uncertainty of when and what the next reward will be.

### Detection Signals

**UI indicators:**
- Mystery boxes or loot boxes
- "Spin the wheel" mechanics
- Surprise reward popups
- Random bonus XP multipliers
- "Lucky" or "rare" reward indicators
- Chest/crate opening animations

**Code patterns:**
Search for: `randomReward`, `mysteryBox`, `bonusXp`, `surpriseReward`, `Math.random` paired with rewards, `lootBox`, `rareReward`, `rewardChance`, `dropRate`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Pure random rewards -- no connection to effort or achievement |
| 2 | Rewards weighted by effort (more effort = better odds) |
| 3 | + Celebratory but not manipulative (surprise confetti, not slot reels) |
| 4 | + Tied to genuine achievement (bonus for exceptional performance) |
| 5 | + Transparent randomization + educational value + never paid |

### Ethical Checklist

- [ ] **Serves user goals?** Does the variable reward enhance the core experience or create compulsion?
- [ ] **Customizable / opt-out?** Can users disable surprise elements?
- [ ] **Transparent mechanism?** Are probabilities disclosed? Is it clear this is random?
- [ ] **Passes Regret Test?** Would users feel manipulated if they understood the variable ratio schedule?
- [ ] **Passes Transparency Test?** Would publishing "we use slot-machine psychology" be acceptable?

**Additional ethical flags specific to this mechanic:**
- [ ] Distinct from gambling mechanics (no real-money purchase of random outcomes)?
- [ ] Age-appropriate for the target audience?
- [ ] Not creating compulsive checking behavior?
- [ ] Probabilities transparent and published?
- [ ] Never requires payment for random outcomes?

### Common Issues
- Gambling-like mechanics that exploit the same neural pathways as slot machines
- Paid loot boxes or mystery boxes (widely considered predatory, banned in some jurisdictions)
- Creating compulsive checking behavior ("maybe this time I'll get the rare reward")
- Children and young users particularly vulnerable to variable ratio exploitation
- Opaque probabilities that hide how unlikely good outcomes are

### Best Practice
Surprise celebration for genuine achievement, not paid randomized rewards. A student who gets 10 questions right in a row might get a surprise animation -- the reward celebrates the accomplishment, not the other way around. Never charge money for randomized outcomes. Always make probabilities transparent if randomization exists.

---

## 7. Social Validation (Kudos / Reactions)

### Definition
Quick social feedback mechanisms -- likes, kudos, reactions, high-fives, and similar lightweight social interactions. They provide validation, create reciprocity loops, and build community connection through minimal-effort social gestures.

### Detection Signals

**UI indicators:**
- Like or reaction buttons on activities or achievements
- Activity feeds showing others' reactions to your work
- Notification of received kudos or reactions
- Reaction counts or summaries
- "X people cheered you on" messages

**Code patterns:**
Search for: `kudos`, `reaction`, `like`, `socialFeed`, `activityFeed`, `cheer`, `highFive`, `encouragement`, `socialNotification`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Simple like button with count |
| 2 | + Multiple reaction types (cheers, high-fives, encouragement) |
| 3 | + Activity feed showing friends' progress and reactions |
| 4 | + Reciprocal encouragement prompts (congratulate friend on milestone) |
| 5 | + Meaningful social connection, not just validation metrics |

### Ethical Checklist

- [ ] **Serves user goals?** Does social feedback enhance motivation toward the user's actual objective?
- [ ] **Customizable / opt-out?** Can users disable social features without penalty?
- [ ] **Transparent mechanism?** Is it clear who sees what and how the feed is curated?
- [ ] **Passes Regret Test?** Would users feel good about time spent giving/checking reactions?
- [ ] **Passes Transparency Test?** Would publishing "we show reaction counts to drive reciprocal engagement" be acceptable?

### Common Issues
- Validation becoming the primary motivator instead of the actual activity
- Anxiety about not receiving reactions or receiving fewer than peers
- Social comparison spirals (seeing others get more kudos)
- Feed algorithms optimizing for engagement over user wellbeing
- Creating obligation to react to others (reciprocity pressure)

### Best Practice
Strava kudos model -- encouraging, reciprocal, but not count-obsessed. Kudos are given freely, received warmly, but never prominently counted or ranked. The social layer should feel like a supportive community, not a popularity contest. No public counts. No "X gave more kudos than you" comparisons.

---

## 8. Challenges & Events

### Definition
Time-limited or themed activities that create focused engagement periods. Challenges introduce novelty, urgency, and variety into a routine product experience. Events create shared temporal experiences that build community.

### Detection Signals

**UI indicators:**
- Challenge banners or featured challenge sections
- Event countdowns or timers
- Special challenge tracks separate from main content
- Themed visual changes (seasonal events, special editions)
- Leaderboards specific to the challenge

**Code patterns:**
Search for: `challenge`, `event`, `tournament`, `weeklyChallenge`, `timeLimit`, `eventStart`, `eventEnd`, `challengeGoal`, `seasonalEvent`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Simple challenges ("answer 10 questions today") |
| 2 | + Themed challenges with story or narrative context |
| 3 | + Progressive difficulty within the challenge |
| 4 | + Team challenges enabling cooperative engagement |
| 5 | + Educational value + genuine time constraints (not manufactured urgency) |

### Ethical Checklist

- [ ] **Serves user goals?** Does the challenge push users toward meaningful engagement?
- [ ] **Customizable / opt-out?** Can users ignore challenges without FOMO pressure?
- [ ] **Transparent mechanism?** Are time constraints real or manufactured?
- [ ] **Passes Regret Test?** Would users feel the challenge time was well spent?
- [ ] **Passes Transparency Test?** Would publishing "we create fake urgency to drive sessions" be acceptable?

### Common Issues
- Fake urgency (countdown timers that reset, "limited time" events that recur constantly)
- Challenge fatigue from too-frequent or overlapping challenges
- Challenges disconnected from the core product value (do X unrelated things for a badge)
- FOMO exploitation -- making users feel they will miss out permanently
- Challenge difficulty miscalibration (too easy = boring, too hard = frustrating)

### Best Practice
Pre-exam prep events tied to real dates (actual test dates create genuine urgency). Weekend challenges with educational themes that reinforce core learning. Challenges should feel like special opportunities, not constant pressure. Frequency should be low enough that each one feels noteworthy.

---

## 9. Hearts / Energy / Lives System

### Definition
A limited resource that depletes with use (typically through mistakes or sessions) and regenerates over time or can be replenished via purchase. This is the core monetization mechanic in many freemium apps -- it gates continued engagement behind either patience or payment.

### Detection Signals

**UI indicators:**
- Heart, energy, or life counter (usually in the header)
- "Out of hearts" or "no energy" blocking screens
- Timer showing when next heart/energy regenerates
- "Buy more hearts" or "refill energy" purchase prompts
- "Watch ad for a heart" offers
- Premium subscription pitched as "unlimited hearts"

**Code patterns:**
Search for: `hearts`, `lives`, `energy`, `regeneration`, `cooldown`, `limitedAttempts`, `heartCount`, `refillHearts`, `energyTimer`, `unlimitedHearts`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Hard paywall -- no free refill path, must pay to continue |
| 2 | Time-based regeneration (wait X hours for one heart) |
| 3 | + Earn hearts through effort (perfect lesson = earn a heart back) |
| 4 | + Reasonable limits + always-free path to continued use |
| 5 | + System serves learning goals (mistakes are consequential) not just monetization |

### Ethical Checklist

- [ ] **Serves user goals?** Does limiting play make mistakes more meaningful for learning, or just drive purchases?
- [ ] **Customizable / opt-out?** Can users fully engage for free with reasonable time investment?
- [ ] **Transparent mechanism?** Is it clear how hearts are lost, earned, and regenerated?
- [ ] **Passes Regret Test?** Would users who purchased hearts feel the purchase was fair?
- [ ] **Passes Transparency Test?** Would publishing "we frustrate users into paying" be acceptable?

**Additional ethical flags specific to this mechanic:**
- [ ] Is regeneration time reasonable (not punishingly long)?
- [ ] Can users fully engage for free without hitting walls daily?
- [ ] Are "watch ad" alternatives available and functional?
- [ ] Is the system tuned for learning (mistakes matter) or revenue (mistakes cost)?

### Common Issues
- Pure monetization mechanic disguised as game design ("mistakes should have consequences")
- Frustration-driven conversion -- intentionally frustrating free users to force payment
- Blocking learning behind a paywall (running out of hearts mid-lesson)
- Regeneration times tuned for revenue, not user experience
- Heart loss on genuinely difficult content punishing effort

### Best Practice
If used at all, mistakes should be learning moments, not monetization triggers. A heart lost should prompt review of the mistake, not a purchase screen. The free path should allow a full daily learning session without hitting the wall. Consider whether this mechanic is necessary at all -- many successful education apps thrive without it.

---

## 10. Push Notifications

### Definition
External triggers sent to the user's device to drive re-engagement. Notifications are the most direct line of communication between product and user, making them both the most powerful engagement tool and the most invasive when misused.

### Detection Signals

**UI indicators:**
- Notification content (informational vs. guilt-based vs. promotional)
- Notification frequency (daily, multiple daily, weekly)
- Timing patterns (morning, evening, based on user activity)
- Personalization level (generic vs. contextual)
- Notification settings granularity

**Code patterns:**
Search for: `pushNotification`, `notification`, `reminder`, `sendNotification`, `notificationSchedule`, `notificationChannel`, `pushToken`, `reminderTime`, `notificationPermission`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Generic blasts to all users at fixed times |
| 2 | Timed to individual user activity patterns |
| 3 | + Personalized content referencing user's specific progress |
| 4 | + Genuinely valuable information (not just "come back" reminders) |
| 5 | + User-controlled frequency + genuinely useful content + respectful tone |

### Ethical Checklist

- [ ] **Serves user goals?** Does the notification help the user achieve their goal, or just serve engagement metrics?
- [ ] **Customizable / opt-out?** Can users granularly control notification types and frequency?
- [ ] **Transparent mechanism?** Is it clear why the notification was sent and what triggers it?
- [ ] **Passes Regret Test?** Would users feel the notification was a welcome reminder, not an interruption?
- [ ] **Passes Transparency Test?** Would publishing "we send guilt-based notifications to boost DAU" be acceptable?

### Common Issues
- Guilt-based messaging ("Your streak is about to end!" "You're falling behind!")
- Excessive frequency creating notification fatigue and eventual app deletion
- Passive-aggressive tone ("We miss you..." "Your friends are pulling ahead...")
- Ignoring user timezone, schedule, or do-not-disturb preferences
- All-or-nothing notification settings (either all notifications or none)
- Notifications that provide no value, only urgency

### Best Practice
Personalized timing based on when the user actually engages. Valuable content in the notification itself (today's word, a quick fact, progress summary). User-controlled frequency with granular options. No guilt, no passive aggression. Respect system-level quiet hours. The notification should make the user glad they received it.

---

## 11. Session-End Celebrations

### Definition
Positive feedback and summary delivered at the end of each engagement session. These serve as the final emotional impression of the session, heavily influencing the Peak-End Rule -- people judge experiences largely by how they felt at the end.

### Detection Signals

**UI indicators:**
- Congratulations or "great job" screens after completing a session
- XP earned summaries
- Streak update confirmations
- Achievement unlock announcements at session end
- "Session complete" screens with stats
- Preview of what comes next

**Code patterns:**
Search for: `sessionEnd`, `celebration`, `sessionSummary`, `completionScreen`, `sessionComplete`, `endScreen`, `sessionStats`, `congratulations`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Simple "done" or "session complete" screen |
| 2 | XP earned summary with basic stats |
| 3 | + Progress visualization + streak update + comparison to previous |
| 4 | + Personalized insights ("You improved 15% in vocabulary") |
| 5 | + Genuine mastery feedback + preview of what is next (Zeigarnik for return) |

### Ethical Checklist

- [ ] **Serves user goals?** Does the celebration reflect genuine progress toward the user's objective?
- [ ] **Customizable / opt-out?** Can users skip the celebration screen if they prefer?
- [ ] **Transparent mechanism?** Are the stats shown accurate and meaningful?
- [ ] **Passes Regret Test?** Would users feel the celebration was earned and honest?
- [ ] **Passes Transparency Test?** Would publishing "we use Peak-End Rule to create positive final impressions" be acceptable?

### Common Issues
- Over-the-top celebration for minimal effort (feels hollow and patronizing)
- No celebration at all (session ends abruptly, feels unrewarding)
- Ending on a negative note (hearts lost, mistakes made, streak warnings)
- Celebration screen blocking quick exit (dark pattern)
- Stats that are misleading or meaningless

### Best Practice
Never end on a negative. Show genuine progress honestly. Preview what comes next to create positive anticipation for return (leveraging Zeigarnik Effect constructively). Celebrate proportionally to effort -- a 5-minute easy session gets a lighter celebration than a 30-minute challenging one. Allow quick dismissal for users who want to move on.

---

## 12. Adaptive Difficulty

### Definition
Adjusting challenge level based on user performance to maintain flow state -- the psychological zone between boredom (too easy) and anxiety (too hard) where engagement and learning are maximized. This is one of the most pro-user engagement mechanics when done well.

### Detection Signals

**UI indicators:**
- Difficulty indicators on content
- "This was adjusted for you" or "personalized" messaging
- Performance-based content selection
- Difficulty settings with "recommended" option
- Smooth transitions between easy and hard content

**Code patterns:**
Search for: `difficulty`, `adaptive`, `skillLevel`, `performanceBased`, `questionDifficulty`, `adaptiveAlgorithm`, `difficultyLevel`, `userSkill`, `irt`, `abilityEstimate`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Fixed difficulty -- same for all users |
| 2 | Manual difficulty selection (easy/medium/hard) |
| 3 | Basic adaptive system (easy/medium/hard) based on recent performance |
| 4 | Continuous real-time adjustment maintaining ~70-80% success rate |
| 5 | + Transparent adaptation + user override + clear explanation of why |

### Ethical Checklist

- [ ] **Serves user goals?** Does adaptation help the user learn more effectively?
- [ ] **Customizable / opt-out?** Can users override the algorithm and choose their own difficulty?
- [ ] **Transparent mechanism?** Does the user know difficulty is being adjusted and roughly how?
- [ ] **Passes Regret Test?** Would users feel the adaptive system helped them improve?
- [ ] **Passes Transparency Test?** Would publishing "we adjust difficulty to keep you in flow state" be acceptable?

### Common Issues
- Adjustments too slow (user is frustrated or bored for too long before system adapts)
- Adjustments not transparent (user does not know why content suddenly got easier/harder)
- No user control or override (algorithm knows best, user cannot choose)
- Using adaptation to artificially inflate success rates (making everything easy to feel good)
- Narrow difficulty band that does not challenge advanced users enough

### Best Practice
Real-time adjustment keeping the user in the flow channel (approximately 70-80% success rate). Be transparent about adaptation -- "We're giving you harder questions because you're doing well" builds trust and motivation. Always allow user override for those who want more challenge or easier practice.

---

## 13. Spaced Repetition

### Definition
Algorithmically optimized review scheduling based on forgetting curves. Items the user knows well are reviewed less frequently; items the user struggles with appear more often. This is the gold standard of ethical engagement in education -- it drives retention AND requires regular engagement, aligning product goals with user goals perfectly.

### Detection Signals

**UI indicators:**
- "Review" or "practice" prompts for previously learned material
- Memory strength indicators (strong/weak/due for review)
- "Due for review" item counts
- Review session as a distinct mode
- Forgetting curve visualizations

**Code patterns:**
Search for: `spacedRepetition`, `forgettingCurve`, `reviewInterval`, `dueDate`, `ease`, `easeFactor`, `interval`, `repetition`, `sm2`, `fsrs`, `anki`, `leitner`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Fixed review schedule (review everything every X days) |
| 2 | Basic spaced intervals (expanding intervals but not performance-adjusted) |
| 3 | SM-2 or similar proven algorithm with performance-adjusted intervals |
| 4 | + Performance-adjusted ease factors + mature/young card distinction |
| 5 | + Transparent science explanation + user-adjustable parameters + proven efficacy data |

### Ethical Checklist

- [ ] **Serves user goals?** Does the review schedule optimize for long-term retention?
- [ ] **Customizable / opt-out?** Can users adjust review load and parameters?
- [ ] **Transparent mechanism?** Does the app explain the science behind spaced repetition?
- [ ] **Passes Regret Test?** Would users feel the review sessions genuinely helped retention?
- [ ] **Passes Transparency Test?** Would publishing "we schedule reviews based on forgetting curves" be a proud statement?

### Common Issues
- Fake spaced repetition that is actually just random review with a spaced repetition label
- Not explaining the science to users (missed opportunity for buy-in and trust)
- Review fatigue when too many items become due simultaneously
- No user control over review load or timing
- Algorithm not validated against actual retention data

### Best Practice
Anki-style SM-2 or FSRS algorithm with transparent scheduling. Explain the science to users -- understanding WHY they are reviewing builds intrinsic motivation. Allow dose control (how many reviews per day). Document and show dose-dependent improvement data. This is one mechanic where the engagement pattern and the user benefit are perfectly aligned.

---

## 14. Social Sharing

### Definition
Features enabling users to share achievements, progress, or content to external social platforms. When done well, sharing is identity expression ("this is who I am"). When done poorly, it is spam generation.

### Detection Signals

**UI indicators:**
- Share buttons on achievements, milestones, or completions
- Shareable cards or images auto-generated with user stats
- Social post generators with pre-written copy
- "Share to [platform]" integration
- Year-in-review or wrapped-style summaries

**Code patterns:**
Search for: `share`, `socialShare`, `shareCard`, `generateShareImage`, `shareToTwitter`, `shareToInstagram`, `shareableContent`, `wrappedSummary`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Basic share button with plain text |
| 2 | Formatted share content with stats |
| 3 | + Visual share cards or images |
| 4 | + Identity-rich content (Spotify Wrapped style) that users genuinely want to share |
| 5 | + Genuinely share-worthy content + privacy-respecting + no friend spam |

### Ethical Checklist

- [ ] **Serves user goals?** Does sharing provide genuine value (identity expression, social connection)?
- [ ] **Customizable / opt-out?** Is sharing strictly opt-in with no pressure or prompting?
- [ ] **Transparent mechanism?** Is it clear exactly what will be shared and to whom?
- [ ] **Passes Regret Test?** Would users feel good about what they shared a week later?
- [ ] **Passes Transparency Test?** Would publishing "we prompt sharing to acquire new users virally" be acceptable?

### Common Issues
- Friend spam (auto-posting, contact harvesting, "invite friends" pressure)
- Over-prompting to share (share button after every minor achievement)
- Sharing as obligation rather than genuine desire
- Contact list harvesting disguised as "find friends"
- Shared content that is embarrassing or reveals too much
- No preview of what will be shared before posting

### Best Practice
Spotify Wrapped model -- users WANT to share because the content reflects their identity and is visually compelling. Share prompts should appear only at genuinely share-worthy moments (major milestones, annual reviews). Always show a preview before sharing. Never access contacts without explicit permission. Never auto-post anything.

---

## 15. Achievement Badges

### Definition
Visual rewards for completing specific milestones or challenges. Badges serve as trophies, identity markers, and progress documentation. They work best when they represent genuine accomplishment and worst when they are participation ribbons.

### Detection Signals

**UI indicators:**
- Badge or trophy collections/galleries
- Achievement unlock notifications
- Badge display on user profiles
- Tiered badges (bronze, silver, gold variants)
- Locked/unlocked badge previews
- Progress toward next badge

**Code patterns:**
Search for: `badge`, `achievement`, `trophy`, `milestone`, `unlock`, `achievementUnlock`, `badgeEarned`, `badgeProgress`, `badgeTier`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Participation badges (earned for showing up, not achieving) |
| 2 | Effort-based badges (complete X sessions, answer Y questions) |
| 3 | + Skill-based badges (achieve X% accuracy, master a topic) |
| 4 | + Tiered badges (bronze/silver/gold) representing increasing mastery |
| 5 | + Badges for genuine mastery + meaningfully displayed + few enough to be special |

### Ethical Checklist

- [ ] **Serves user goals?** Do badges represent accomplishments the user is genuinely proud of?
- [ ] **Customizable / opt-out?** Can users hide or de-emphasize the badge system?
- [ ] **Transparent mechanism?** Are badge criteria clear and visible before earning?
- [ ] **Passes Regret Test?** Would users display their badges proudly, not dismissively?
- [ ] **Passes Transparency Test?** Would publishing "we give badges to create collection completionism" be acceptable?

### Common Issues
- Meaningless badges that everyone gets (the PBL fallacy -- points, badges, leaderboards without substance)
- Badges without genuine challenge, devaluing the entire system
- Badge fatigue from receiving too many -- when everything is special, nothing is
- Badges disconnected from actual skill or accomplishment
- Badge collection becoming the goal instead of the underlying learning

### Best Practice
Fewer badges, but each one meaningful. Badges should be earned through genuine challenge, and a user should feel proud to have one. Display should be optional but desirable. Think of academic honors, not participation trophies. Tiered systems (bronze/silver/gold) add depth without adding clutter. Criteria should be visible before earning so users can aspire to them.

---

## 16. Team / Group Mechanics

### Definition
Cooperative engagement features where groups work toward shared goals. Team mechanics leverage belonging, accountability, and collective identity to drive engagement. They shift motivation from "I should practice" to "my team is counting on me."

### Detection Signals

**UI indicators:**
- Team or group challenge interfaces
- Group leaderboards
- Collaborative goal trackers (team has done X of Y)
- Study group features
- Team chat or communication
- Club or group membership

**Code patterns:**
Search for: `team`, `group`, `collaborative`, `clubGoal`, `teamChallenge`, `studyGroup`, `groupMember`, `teamScore`, `collectiveGoal`

### Quality Scale (1-5)

| Score | Implementation |
|-------|---------------|
| 1 | Simple team label -- users grouped but not cooperating |
| 2 | Team leaderboard (team score = sum of individual scores) |
| 3 | + Collaborative goals (team collectively works toward a shared target) |
| 4 | + Team communication and encouragement features |
| 5 | + Genuine cooperation that enhances individual outcomes + fair contribution tracking |

### Ethical Checklist

- [ ] **Serves user goals?** Does team membership enhance the individual's learning or engagement?
- [ ] **Customizable / opt-out?** Can users participate individually without penalty?
- [ ] **Transparent mechanism?** Is it clear how team goals work and how contributions are tracked?
- [ ] **Passes Regret Test?** Would users feel the team dynamic was supportive, not pressuring?
- [ ] **Passes Transparency Test?** Would publishing "we use social obligation to drive engagement" be acceptable?

### Common Issues
- Free-rider problem (some members contribute nothing, others carry the team)
- Social pressure to perform creating anxiety rather than motivation
- Teams feeling like just another leaderboard with extra steps
- Forced team membership without opt-out
- Teams formed randomly without shared goals or interests
- No mechanism to handle inactive or toxic team members

### Best Practice
Strava clubs model -- collective goals create belonging, and individual contribution is valued but not pressured. Teams should form around shared interests or goals (study the same subject, preparing for the same test). Contribution should be visible but not punitive. The team should make the experience more enjoyable, not more obligatory. Always offer solo participation as a first-class option.

---

## Usage Notes

When auditing a product, work through each of the 16 mechanics:

1. **Detect**: Is this mechanic present? Use UI and code detection signals.
2. **Score**: Rate the implementation quality on the 1-5 scale.
3. **Evaluate**: Run through the 5 standard ethical checklist questions.
4. **Flag**: Identify any common issues that are present.
5. **Recommend**: Suggest improvements toward the best practice benchmark.

Mechanics with ethical risk levels of "High" (Variable/Mystery Rewards, Hearts/Energy/Lives) deserve extra scrutiny. These mechanics have the highest potential for user harm and the strongest history of exploitative implementation.

Mechanics with ethical risk levels of "Very Low" or "Low" (Spaced Repetition, Adaptive Difficulty, Session-End Celebrations) are inherently more aligned with user interests. Poor implementation is still possible but the design intent is typically pro-user.

The goal of a behavioral design audit is not to eliminate engagement mechanics but to ensure they serve users rather than exploit them. Every mechanic on this list can be implemented ethically or exploitatively -- the difference is in the details.
