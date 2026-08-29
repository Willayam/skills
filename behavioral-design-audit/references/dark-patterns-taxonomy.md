# Dark Patterns Taxonomy -- Behavioral Design Audit Reference

This document is a reference for behavioral design auditors. It catalogs 18 recognized dark patterns with definitions, severity ratings, EU Digital Services Act (DSA) compliance status, detection signals, examples, the line between legitimate and dark usage, and remediation guidance.

Use this taxonomy when auditing any digital product. For each screen, flow, or component under review, check against every pattern listed here. Patterns are ordered by the original Brignull taxonomy with additions from EU regulatory guidance.

---

## Severity Levels

| Level    | Meaning                                                                 |
|----------|-------------------------------------------------------------------------|
| Critical | Causes direct financial harm or violates explicit EU regulation. Must fix immediately. |
| High     | Manipulates user decisions or violates regulatory spirit. Fix before next release.      |
| Medium   | Nudges users in ways that may erode trust. Fix within next planning cycle.              |

---

## 1. Confirmshaming

**Definition:** Uses guilt-laden or emotionally manipulative language on decline/opt-out options to pressure users into accepting.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | Medium                                                                                      |
| EU DSA Status     | Not explicitly named, but falls under Article 25 prohibition on manipulation of user decisions |

### Detection Signals

- **Visual:** Decline button text contains value judgments, self-deprecating language, or emotional framing.
- **Behavioral:** Users report feeling guilty or pressured when declining.
- **Code:** Look for opt-out button labels containing words like "stupid," "uninformed," "miss out," "don't care," or similar emotionally loaded terms.

### Examples

- "No thanks, I prefer to stay uninformed"
- "I don't want to save money"
- "No, I enjoy paying full price"

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| "No thanks" / "Not now" / "Skip"                               | "No thanks, I hate saving money"                                  |
| Honest description of what the user will miss: "You won't receive weekly tips" | Guilt-laden framing: "No, I don't want to improve my life"       |
| Neutral tone on all options                                     | Cheerful accept button, sad or shaming decline button              |

### Remediation

- Replace all opt-out copy with neutral language: "No thanks," "Not now," "Decline," or "Skip."
- Both accept and decline options should use equivalent emotional tone.
- If describing consequences, use factual language without value judgments.

---

## 2. Roach Motel

**Definition:** Easy to get into a situation (sign up, subscribe, enable) but deliberately difficult to get out of (cancel, unsubscribe, disable). Cancellation is buried behind multiple screens, phone calls, chat agents, or retention flows.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | Critical                                                                                    |
| EU DSA Status     | Article 25 explicitly prohibits making cancellation harder than subscription                  |

### Detection Signals

- **Visual:** Cancel/unsubscribe option is missing from account settings or buried more than two levels deep.
- **Behavioral:** Cancellation requires a phone call, live chat, or mailing a letter. Retention offers interrupt the cancellation flow multiple times.
- **Code:** Compare the number of steps/screens in the signup flow versus the cancellation flow. Check for phone-only cancellation endpoints. Look for retention interstitials injected into cancel flows.

### Examples

- One-click signup but cancellation requires calling a phone number during business hours.
- Cancel button leads to a 5-step retention flow with multiple "Are you sure?" screens, each offering different deals.
- Account deletion page returns a 404 or directs to an email address.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Confirmation step: "Are you sure? You'll lose access to X"      | Four consecutive retention screens before allowing cancellation    |
| Offering a pause option alongside cancel                        | Hiding cancel behind "Contact Support"                             |
| Clearly labeled cancel button in account settings               | Cancel only available via phone call                               |

### Remediation

- Cancellation must require the same number of steps or fewer than signup.
- Provide a clearly labeled cancel option in account settings, accessible within two clicks.
- A single optional retention offer is acceptable; multiple blocking interstitials are not.
- Delete account functionality must be self-service and functional.

---

## 3. Trick Questions

**Definition:** Questions phrased in a confusing or misleading way so users give an answer they did not intend. Uses double negatives, reversed checkbox logic, or ambiguous wording.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | High                                                                                        |
| EU DSA Status     | Falls under manipulation prohibition; GDPR requires clear and unambiguous consent language    |

### Detection Signals

- **Visual:** Checkbox labels containing double negatives ("Uncheck to not receive..."). Opt-in phrasing that reads like opt-out.
- **Behavioral:** User testing reveals frequent misunderstanding of what a checkbox does.
- **Code:** Look for negation words in checkbox or toggle labels: "don't," "not," "un-," "without." Check for pre-checked boxes where checked means opting in to marketing or data sharing.

### Examples

- "Uncheck this box if you prefer not to not receive emails" (triple negative).
- Pre-checked: "I agree to receive promotional offers" placed between required terms checkboxes.
- "Do you want to opt out of not sharing your data with partners?"

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| "Send me weekly updates" (unchecked by default)                 | "Uncheck if you don't want to not receive updates"                |
| Single positive assertion per checkbox                          | Multiple clauses bundled into one checkbox                         |
| Clear, plain language                                           | Legalese or deliberately convoluted phrasing                       |

### Remediation

- Every checkbox or toggle must use a single positive assertion.
- Eliminate all double negatives.
- Marketing/data-sharing checkboxes must be unchecked by default (GDPR requirement).
- Each consent item gets its own checkbox; do not bundle unrelated consents.

---

## 4. Hidden Costs

**Definition:** Additional fees (service charges, delivery fees, taxes, "convenience" fees) are revealed only at the final checkout step, after the user has invested time and effort in the purchase flow.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | Critical                                                                                    |
| EU DSA Status     | Prohibited under EU consumer protection regulations (Consumer Rights Directive)               |

### Detection Signals

- **Visual:** Price shown on product/listing page differs from price at checkout. Fees appear in small text or as separate line items only on the payment page.
- **Behavioral:** Users abandon carts at high rates on the final checkout step (price shock).
- **Code:** Compare the price value rendered on product cards/listing pages with the total calculated at checkout. Search for fee components that only render in checkout views (e.g., `serviceFee`, `convenienceFee`, `handlingCharge`).

### Examples

- Concert ticket listed at $50 but checkout shows $50 + $12 service fee + $5 facility fee + $3 order processing fee = $70.
- Hotel rate of $120/night becomes $145 after resort fee and cleaning fee added at booking confirmation.
- Food delivery shows menu prices but adds delivery fee, small order fee, and service charge at checkout.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| "Price: $70 (includes all fees)" shown on listing                | "$50" on listing, fees revealed only at checkout                  |
| Fee breakdown visible on product page or immediately after adding to cart | Fees shown only on the final payment screen                |
| Tax disclaimer: "Prices exclude applicable sales tax"            | Unlabeled fees with vague names like "service charge"             |

### Remediation

- Display the total price including all mandatory fees on the product/listing page.
- If fees vary (e.g., delivery based on location), show a clear estimate or range upfront.
- Label every fee clearly and explain what it covers.
- If tax cannot be calculated upfront, state "plus applicable tax" on the listing.

---

## 5. Bait and Switch

**Definition:** Users set out to do one thing, but a different, undesirable outcome occurs instead. An element that appears to do X actually does Y.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | High                                                                                        |
| EU DSA Status     | Falls under prohibition on deceptive interface design                                        |

### Detection Signals

- **Visual:** Close/dismiss buttons that trigger signups or downloads. "Skip" buttons that actually submit forms. Icons whose visual meaning contradicts their function.
- **Behavioral:** Users report unexpected outcomes after clicking familiar-looking controls.
- **Code:** Audit `onClick` handlers on close icons, dismiss buttons, and "Skip" labels. Verify that the action triggered matches the button label.

### Examples

- An "X" close button on a modal that actually subscribes the user to a newsletter.
- "Skip" button that submits the form with default (company-favorable) settings.
- Windows 10 famously: clicking the "X" to close a Windows upgrade prompt triggered the upgrade.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Close button closes. Skip button skips. Submit button submits.  | Close button subscribes. Skip button submits.                     |
| Secondary actions labeled accurately ("Save Draft," "Remind Me Later") | Ambiguous labels that obscure the real action                |

### Remediation

- Every interactive element's action must match its label exactly.
- Close/dismiss controls must only close/dismiss.
- Audit all CTAs by clicking through and verifying the outcome matches the label.

---

## 6. Forced Continuity

**Definition:** A free trial or introductory offer automatically converts to a paid subscription with no warning, no reminder, and difficult cancellation.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | Critical                                                                                    |
| EU DSA Status     | Requires clear disclosure of auto-renewal terms (Consumer Rights Directive, also FTC in US)   |

### Detection Signals

- **Visual:** Trial signup flow does not clearly state when charging begins or how much will be charged. No visible reminder system before trial expiry.
- **Behavioral:** Users are surprised by charges. Support volume spikes around trial-end dates.
- **Code:** Check the trial signup flow for explicit renewal disclosure text. Search for pre-expiry reminder email templates or scheduled notification jobs. Check if cancel is accessible during the trial period.

### Examples

- "Start your free trial!" requires a credit card, auto-charges $19.99/month after 7 days with no email reminder.
- Trial end date is only shown once at signup and never again in the app or via email.
- Cancelling during a trial period requires calling support.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Clear disclosure: "After 14 days, you'll be charged $X/month"   | Renewal terms in fine print or a separate "Terms" page only       |
| Reminder email sent 3 days before trial ends                     | No reminder; user discovers charge on bank statement               |
| One-click cancel available throughout the trial                  | Cancel requires phone call or multi-step flow                      |

### Remediation

- Clearly disclose the renewal date, amount, and frequency at trial signup.
- Send at least one reminder email 3-7 days before the trial ends.
- Provide self-service cancellation accessible within two clicks throughout the trial.
- After cancellation, confirm via email that no charge will occur.

---

## 7. Friend Spam

**Definition:** Product requests access to contacts under the pretense of "finding friends" or "inviting connections" but then sends messages (email, SMS, social) to all contacts without clear, granular user consent.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | Critical                                                                                    |
| EU DSA Status     | GDPR prohibits processing third-party data without lawful basis; ePrivacy Directive restricts unsolicited electronic messages |

### Detection Signals

- **Visual:** Contact import prompts with vague descriptions like "Find your friends" without specifying what will happen to the contacts.
- **Behavioral:** After granting contact access, messages are sent without the user reviewing or approving each one. Contacts report receiving unsolicited messages.
- **Code:** Check what happens after contact permissions are granted. Look for bulk-send operations triggered by contact import. Check whether the user sees a list of contacts and explicitly selects who to message.

### Examples

- "Find friends on [App]" imports contacts, then sends "Join me on [App]!" emails to every contact without user review.
- App sends SMS invitations to all phone contacts after user taps "Connect contacts."
- LinkedIn's historic practice of importing email contacts and sending repeated invitation emails.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| User selects individual contacts to invite                      | All contacts receive messages after bulk import                    |
| Clear preview: "We'll send this message to the 3 people you selected" | Vague: "We'll help you connect with friends"               |
| No messages sent without explicit per-batch user approval        | Messages sent immediately upon contact import                      |

### Remediation

- Never send messages to imported contacts without explicit, per-message (or per-batch with preview) user approval.
- Show the exact message that will be sent before sending.
- Let users select individual contacts rather than bulk-importing and messaging all.
- Clearly disclose: "We will only contact people you explicitly select."

---

## 8. Disguised Ads

**Definition:** Advertisements designed to look like native content, navigation elements, or editorial material, making users click them without realizing they are ads.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | High                                                                                        |
| EU DSA Status     | Must be clearly labeled as advertising (Article 26, DSA)                                     |

### Detection Signals

- **Visual:** Content blocks that match the site's editorial style but link to external commercial pages. Download buttons that are actually ads. Navigation items that link to sponsored content without disclosure.
- **Behavioral:** Users click expecting editorial content or site functionality and are taken to an advertiser's page.
- **Code:** Check for ad network iframes or scripts embedded within content areas. Look for sponsored content blocks missing "Ad" or "Sponsored" labels. Audit download pages for multiple "Download" buttons where only one is real.

### Examples

- A "Download" button that is actually a Google Ad, placed next to the real download link.
- Sponsored articles styled identically to editorial content with only a small, low-contrast "Sponsored" label.
- Social media feed posts that look like friend posts but are paid promotions.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Clear "Advertisement" or "Sponsored" label, visually distinct    | Ad mimics surrounding editorial content with no label              |
| Ads have different background color or border                    | Ad is indistinguishable from native content                        |
| Single, clearly labeled download button                          | Multiple "Download" buttons, most being ads                        |

### Remediation

- All ads must carry a clear, high-contrast "Advertisement" or "Sponsored" label.
- Ads must be visually distinguishable from editorial content (different background, border, or section).
- Download pages must have exactly one clearly identified download button.
- Sponsored content must be labeled at the top, not the bottom, of the content block.

---

## 9. Privacy Zuckering

**Definition:** Users are tricked or nudged into sharing more personal data than they intend, through confusing privacy settings, opt-out-by-default sharing, or buried controls.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | Critical                                                                                    |
| EU DSA Status     | GDPR requires clear, specific, informed consent; data minimization principle; privacy by default |

### Detection Signals

- **Visual:** Privacy settings are spread across multiple pages. Sharing is enabled by default with toggles to disable. Privacy-reducing options are presented as recommendations.
- **Behavioral:** Users are unaware of how much data they are sharing. Privacy audits reveal sharing levels that exceed user expectations.
- **Code:** Audit default values of all privacy-related toggles and settings. Check if privacy settings require more than two clicks to reach. Look for data sharing enabled by default (`defaultChecked={true}`, `defaultValue="public"`).

### Examples

- Profile visibility defaults to "Public" and changing it requires navigating through four settings screens.
- "Improve your experience" toggle that actually shares browsing data with third-party advertisers.
- Privacy settings page uses "Recommended" labels on the most data-sharing options.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Privacy-first defaults: sharing is opt-in                        | Sharing enabled by default; privacy is opt-out                     |
| Single, accessible privacy settings page                         | Privacy controls scattered across many pages                       |
| Plain language: "Share your location with advertisers"           | Euphemistic: "Personalize your ad experience"                      |

### Remediation

- All data sharing must be opt-in by default (GDPR: privacy by design and by default).
- Consolidate privacy settings into a single, accessible page.
- Use plain language that clearly describes what data is shared, with whom, and why.
- Never label the most permissive setting as "Recommended."

---

## 10. Misdirection

**Definition:** Design intentionally focuses user attention on one element to distract from another. One option is made visually dominant while the alternative is minimized or hidden.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | High                                                                                        |
| EU DSA Status     | Article 25 prohibits giving more prominence to certain choices to subvert user decisions      |

### Detection Signals

- **Visual:** Accept/agree button is large, colorful, and prominent while decline/reject is small, gray, or styled as a text link. Desired action button uses primary brand color; alternative is styled to be near-invisible.
- **Behavioral:** Click-through rates on the prominent option are disproportionately high relative to user intent surveys.
- **Code:** Compare CSS properties of accept vs decline buttons: `font-size`, `padding`, `background-color`, `opacity`, `color`. Check for significantly different `z-index` or `visibility` properties. Look for decline options rendered as plain text links while accept is a styled button.

### Examples

- Cookie consent: "Accept All" is a large blue button; "Manage Preferences" is a small gray text link.
- Unsubscribe page: "Keep my subscription" is a prominent button; "Cancel" is tiny gray text at the bottom.
- App permission dialog: "Allow" is a large green button; "Don't Allow" is a small outline button.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Both options are clearly visible buttons with equal visual weight | Accept is a large colored button; decline is a tiny gray link     |
| Primary action may be visually distinguished but alternative is still clearly a button | Alternative option is nearly invisible or requires scrolling |
| Color difference is subtle; size is equal                        | Extreme contrast: bright vs invisible                              |

### Remediation

- Accept and decline options must both be rendered as buttons (not one button and one text link).
- Both options must be the same size and in close proximity.
- Color differentiation is acceptable (primary vs secondary button style) but contrast must not make either option illegible or invisible.
- The user-benefiting option (e.g., "Decline cookies") must never require scrolling to find.

---

## 11. Sneak into Basket

**Definition:** Extra items, services, insurance, or add-ons are added to the user's cart or order via pre-checked checkboxes, pre-selected radio buttons, or default-on toggles, without the user actively choosing them.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | Critical                                                                                    |
| EU DSA Status     | Explicitly prohibited (Article 22, Consumer Rights Directive: inferred consent via default options for extra payments is not valid) |

### Detection Signals

- **Visual:** Pre-checked checkboxes for add-ons (insurance, warranty, donations, premium shipping) in the checkout flow. Items in cart that the user did not add.
- **Behavioral:** Users notice unexpected items at checkout or on their receipt.
- **Code:** Search checkout components for pre-checked inputs (`defaultChecked={true}`, `checked` attribute without user interaction). Look for cart items added programmatically during checkout flow initialization. Check for hidden inputs with pre-set values for add-on products.

### Examples

- Travel booking adds travel insurance via a pre-checked box buried below the fold.
- Software installer includes a pre-selected toolbar or antivirus trial.
- E-commerce checkout pre-selects "Express Shipping (+$9.99)" over standard free shipping.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Add-ons presented as clearly unchecked options the user can select | Add-ons pre-checked so user must actively remove them            |
| Cart contains only items the user explicitly added               | Items appear in cart without user action                           |
| Upsells shown as suggestions, not defaults                       | Upsells default-on; user must notice and uncheck                   |

### Remediation

- No add-on, insurance, warranty, donation, or upgrade may be pre-selected.
- All optional purchases must require explicit user action (click/tap) to add.
- Cart must only contain items the user actively placed there.
- Audit every checkout step for pre-checked inputs or programmatically added items.

---

## 12. Price Comparison Prevention

**Definition:** Making it intentionally difficult for users to compare prices by using confusing unit pricing, incomparable plan tiers, or obfuscated cost breakdowns.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | Medium                                                                                      |
| EU DSA Status     | Not explicitly named in DSA but may fall under unfair commercial practices directive          |

### Detection Signals

- **Visual:** Pricing page uses different units across tiers (per user/month, per seat/year, per API call). Key features are listed inconsistently across plans, making side-by-side comparison difficult. Per-unit prices are hidden or require calculation.
- **Behavioral:** Users report confusion about which plan offers the best value.
- **Code:** Check pricing components for consistent unit display. Look for plans that hide certain cost components. Verify that comparison tables align features across all tiers.

### Examples

- Plan A shows a monthly price, Plan B shows an annual price divided by 12, Plan C shows a per-seat price without specifying minimum seats.
- Streaming service offers "Basic," "Standard," "Premium" but varies simultaneous streams, resolution, and ads in ways that make comparison difficult.
- SaaS pricing that requires contacting sales for any plan above the basic tier.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| All plans use the same billing unit (e.g., per user/month)       | Plans use different units to obscure comparison                    |
| Feature comparison table with aligned rows                       | Features listed in different order or with different names per plan |
| Per-unit price clearly displayed                                 | Only total price shown for volume bundles                          |

### Remediation

- Display all pricing in the same unit (e.g., all per-month or all per-year, with toggle).
- Show per-unit costs clearly when selling bundles or volume tiers.
- Use aligned comparison tables with consistent feature naming across all plans.
- If a plan requires contacting sales, show a starting price or range.

---

## 13. Nagging

**Definition:** Persistent, repeated interruptions (modals, banners, notifications, tooltips) that push users toward an action the product wants, degrading the user experience until they comply.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | Medium                                                                                      |
| EU DSA Status     | Not explicitly named but may constitute manipulation under Article 25 if persistent enough    |

### Detection Signals

- **Visual:** Same prompt/modal appears on every page load or session start. Banner persists after being dismissed. Notification badge never clears without taking the nagged action.
- **Behavioral:** Users report annoyance. Dismiss rate is high but prompt reappears.
- **Code:** Check if dismissal state is persisted (`localStorage`, cookies, database). Look for prompts that reset their dismissed state on session start, page reload, or after a timer. Count how many times the same prompt is triggered per session.

### Examples

- "Enable notifications?" prompt appears on every app open after being declined.
- "Upgrade to Premium" banner reappears on every page after being dismissed.
- App review prompt appears every three sessions regardless of prior dismissal.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Ask once, respect "No" for a reasonable period (30+ days)        | Ask on every page load or session                                  |
| "Remind me later" actually delays the prompt meaningfully        | "Remind me later" shows the same prompt 5 minutes later            |
| Maximum of 2-3 prompts with escalating intervals                 | Unlimited prompts until user complies                              |

### Remediation

- Persist dismissal state: once a user declines, do not show the same prompt for at least 30 days.
- Implement a maximum prompt count (e.g., 3 lifetime prompts for the same action).
- "Remind me later" should delay by a meaningful period (7+ days).
- Never use a notification badge that can only be cleared by performing the nagged action.

---

## 14. Obstruction

**Definition:** Deliberately making a user-benefiting process (cancellation, data export, account deletion, unsubscription) more difficult, slower, or more complex than company-benefiting processes (signup, purchase, upgrade). Also known as "sludge."

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | High                                                                                        |
| EU DSA Status     | Article 25 prohibits interfaces that make exercising rights more difficult                    |

### Detection Signals

- **Visual:** Cancel/delete/unsubscribe buttons are harder to find than subscribe/purchase buttons. User-benefiting flows have more steps, screens, or required fields than company-benefiting flows.
- **Behavioral:** Completion rates for cancellation or data export are disproportionately low. Users report giving up mid-flow.
- **Code:** Count the number of HTTP requests, screens, form fields, and clicks required for: signup vs cancel, purchase vs refund, subscribe vs unsubscribe, create account vs delete account. A significant asymmetry indicates obstruction.

### Examples

- Signup: 2 fields, 1 click. Cancel: 5 screens, 2 surveys, 1 retention offer, 1 email confirmation, 1 "processing period."
- Data export: requires filing a request that takes "up to 30 days" despite data being immediately accessible.
- Unsubscribe link leads to a login page, then a settings page, then a nested preferences page, then a confirmation page.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Cancel requires 1-2 steps with clear confirmation               | Cancel requires 5+ steps with multiple interruptions               |
| Data export is self-service and immediate                        | Data export requires a manual request and extended waiting period   |
| Unsubscribe is one click from the email                          | Unsubscribe requires logging in and navigating multiple screens    |

### Remediation

- Audit and equalize friction: user-benefiting actions should require the same or fewer steps than the corresponding company-benefiting action.
- Provide one-click unsubscribe in all marketing emails (also a legal requirement under CAN-SPAM and GDPR).
- Data export and account deletion must be self-service.
- Remove unnecessary surveys, waiting periods, and retention interstitials from exit flows.

---

## 15. False Urgency

**Definition:** Artificial time pressure created through fake countdown timers, "limited time" labels, or expiring deal notifications that are not tied to any genuine constraint.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | High                                                                                        |
| EU DSA Status     | Explicitly prohibited -- fake urgency timers not tied to real deadlines or inventory (Article 25, DSA) |

### Detection Signals

- **Visual:** Countdown timers on product or pricing pages. "Offer expires in..." banners. "Last chance!" or "Hurry!" language.
- **Behavioral:** The "limited time" offer is available indefinitely. Timer resets on page reload. The same "ending soon" promotion runs continuously.
- **Code:** Check if countdown timers reset on page reload (`Date.now()` as start vs server-side deadline). Search for hard-coded durations that restart per session. Verify if "ending soon" promotions have actual end dates in the backend.

### Examples

- "Sale ends in 2:34:15" -- timer resets to 3 hours on every page visit.
- "Only available today!" -- same message displayed every day for months.
- "This price won't last!" on a product whose price has not changed in a year.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Timer tied to a real event: "Early bird pricing ends March 15"   | Timer resets every session with no real deadline                    |
| Flash sale with genuine start and end dates                      | Perpetual "flash sale" that never ends                             |
| Ticket sales: "Registration closes in 48 hours" (real deadline)  | "Hurry! Offer expires soon!" running indefinitely                  |

### Remediation

- Only use countdown timers for genuine deadlines (event registration, real flash sales, limited inventory).
- Timers must be server-side and not reset on page reload.
- If an offer is ongoing, do not use urgency language or timers.
- Log and audit all urgency elements to verify they correspond to real constraints.

---

## 16. False Scarcity

**Definition:** Fabricated or misleading scarcity messages ("Only 2 left!" "Selling fast!") that do not reflect genuine inventory levels or demand.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | High                                                                                        |
| EU DSA Status     | Explicitly prohibited -- false scarcity messages (Article 25, DSA)                           |

### Detection Signals

- **Visual:** "Only X left in stock!" messages, especially when X is a low number. "Y people are viewing this right now" notifications. "Selling fast!" labels.
- **Behavioral:** Scarcity numbers do not change over time. The same "Only 2 left" message persists for weeks. Numbers are suspiciously round or conveniently low.
- **Code:** Check if scarcity numbers are fetched from real inventory APIs or are hard-coded/randomized. Look for `Math.random()` or static values driving "X left" displays. Verify "people viewing" counters against actual analytics data.

### Examples

- "Only 1 left!" on a product that has been "almost out of stock" for six months.
- "23 people are looking at this right now" generated by a random number function.
- "Limited edition" product that is continuously restocked.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Stock count pulled from actual inventory system                  | Hardcoded or randomized low stock numbers                          |
| "Low stock" shown only when inventory genuinely drops below threshold | "Only X left!" shown regardless of actual stock               |
| Viewer count from real analytics with reasonable refresh rate     | Viewer count from random number generator                          |

### Remediation

- Scarcity messages must be driven by real-time inventory data.
- Only display low-stock warnings when inventory genuinely falls below a defined threshold.
- Viewer/activity counts must come from actual analytics, not fabrication.
- "Limited edition" may only be used for products that are genuinely not restocked.

---

## 17. Fake Social Proof

**Definition:** Fabricated or misleading reviews, testimonials, activity notifications, or endorsements designed to create false trust and influence user decisions.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | High                                                                                        |
| EU DSA Status     | DSA requires platforms to combat fake reviews; unfair commercial practices directive prohibits misleading endorsements |

### Detection Signals

- **Visual:** Real-time activity notifications ("John from Denver just purchased...") that appear at suspiciously regular intervals. Reviews with generic language, stock photos, or implausible detail. Endorsement badges from unknown organizations.
- **Behavioral:** Activity notifications appear even during off-peak hours at the same rate. All reviews are 5-star with similar phrasing. Testimonials lack verifiable identity.
- **Code:** Check if activity notifications are driven by real transaction data or a scripted rotation. Look for review seeding scripts. Verify endorsement badges link to legitimate organizations. Check if testimonial photos are stock images (reverse image search).

### Examples

- "Sarah from London just signed up 3 minutes ago" -- generated from a list of fake names and cities on a timer.
- Product page showing exclusively 5-star reviews with identical sentence structure.
- "As seen on Forbes, TechCrunch, CNN" badges that link nowhere or reference unpaid, user-generated content.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Reviews from verified purchasers with verified purchase badges   | Fabricated reviews from fake accounts                              |
| Real-time activity from actual events, shown with reasonable delay | Scripted fake activity notifications on a timer                  |
| Press mentions that link to actual articles                      | "As seen on" badges with no verifiable source                      |

### Remediation

- Activity notifications must be driven by real, recent events.
- Reviews must include verification (verified purchase, verified user).
- Never seed or fabricate reviews, even for launch.
- Press/endorsement badges must link to the actual source.
- Implement review authenticity checks and remove identified fake reviews.

---

## 18. Forced Action

**Definition:** Requiring users to complete an unrelated or disproportionate task in order to access the functionality or content they actually want.

| Attribute         | Detail                                                                                      |
|-------------------|---------------------------------------------------------------------------------------------|
| Severity          | High                                                                                        |
| EU DSA Status     | Falls under manipulation and making access to services conditional on unrelated actions (GDPR: coupling prohibition for consent) |

### Detection Signals

- **Visual:** "Create an account to continue reading." "Share on social media to unlock this feature." "Invite 3 friends to access premium content."
- **Behavioral:** Users are blocked from core functionality until they perform an unrelated action. Feature gates appear at points of high engagement to maximize compliance.
- **Code:** Check for conditional rendering that gates content behind unrelated actions (account creation for public content, social sharing for feature access). Look for invite-gate or share-gate components. Audit whether the required action is genuinely necessary for the feature.

### Examples

- News site requires account creation to read a public article.
- App requires social media sharing to unlock a basic feature.
- Service requires inviting three friends before accessing a feature the user already paid for.
- "Allow notifications to continue" when notifications are unrelated to the task.

### Legitimate vs Dark

| Legitimate                                                      | Dark                                                              |
|-----------------------------------------------------------------|-------------------------------------------------------------------|
| Account required for personalized features (saved preferences, history) | Account required to view public content                      |
| Sharing as an optional bonus ("Share to earn extra credits")     | Sharing required to access basic features                          |
| Notification permission requested contextually when relevant     | Notification permission required to proceed with unrelated task    |

### Remediation

- Only require actions that are genuinely necessary for the requested feature.
- Account creation should be optional for consuming public content.
- Social sharing, invitations, and notifications must never gate core functionality.
- If an action is required, clearly explain why it is necessary for the specific feature.

---

## Quick Reference Table

| #  | Pattern                        | Severity | EU DSA Explicitly Prohibited | Primary Detection Method                              |
|----|--------------------------------|----------|------------------------------|-------------------------------------------------------|
| 1  | Confirmshaming                 | Medium   | No (falls under Art. 25)     | Audit decline button copy for emotional manipulation   |
| 2  | Roach Motel                    | Critical | Yes (Art. 25)                | Compare signup steps vs cancel steps                   |
| 3  | Trick Questions                | High     | No (GDPR: clear consent)     | Check for double negatives and pre-checked opt-ins     |
| 4  | Hidden Costs                   | Critical | Yes (Consumer Rights Dir.)   | Compare listing price vs checkout total                |
| 5  | Bait and Switch                | High     | No (deceptive design)        | Click all CTAs and verify outcomes match labels         |
| 6  | Forced Continuity              | Critical | Yes (auto-renewal disclosure)| Check trial flow for renewal disclosure and reminders  |
| 7  | Friend Spam                    | Critical | Yes (GDPR, ePrivacy Dir.)    | Grant contact access and observe what messages are sent |
| 8  | Disguised Ads                  | High     | Yes (Art. 26)                | Check for "Ad"/"Sponsored" labels on commercial content |
| 9  | Privacy Zuckering              | Critical | Yes (GDPR: privacy by default)| Audit default privacy settings                        |
| 10 | Misdirection                   | High     | Yes (Art. 25)                | Compare visual weight of accept vs decline options      |
| 11 | Sneak into Basket              | Critical | Yes (Consumer Rights Dir.)   | Check checkout for pre-checked add-ons                 |
| 12 | Price Comparison Prevention    | Medium   | No (unfair practices)        | Check pricing page for consistent units and clarity     |
| 13 | Nagging                        | Medium   | No (may fall under Art. 25)  | Count prompt frequency and check dismissal persistence  |
| 14 | Obstruction                    | High     | Yes (Art. 25)                | Count steps for user-benefiting vs company-benefiting actions |
| 15 | False Urgency                  | High     | Yes (Art. 25)                | Reload page and check if timer resets                  |
| 16 | False Scarcity                 | High     | Yes (Art. 25)                | Verify scarcity numbers against real inventory data     |
| 17 | Fake Social Proof              | High     | Yes (DSA, unfair practices)  | Check if activity/reviews are driven by real data       |
| 18 | Forced Action                  | High     | No (GDPR: coupling)          | Check if proceeding requires unrelated actions          |

---

## How to Use This Taxonomy in an Audit

1. **Screen-by-screen review:** Walk through every user-facing screen and flow. For each screen, scan the quick reference table and check for all 18 patterns.
2. **Flow-pair analysis:** For every company-benefiting flow (signup, purchase, enable), identify the corresponding user-benefiting flow (cancel, refund, disable) and compare friction.
3. **Code audit:** Use the code-level detection signals to search the codebase for programmatic dark patterns (pre-checked inputs, fake data generators, timer resets).
4. **Severity-based prioritization:** Address Critical patterns immediately, High patterns before the next release, and Medium patterns within the current planning cycle.
5. **Document findings:** For each detected pattern, record the pattern name, location (screen/component), severity, evidence (screenshot + code reference), and recommended fix.
