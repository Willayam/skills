# Builder brief template

Copy this into the lab as `BRIEF.md`, fill in the brackets, and give each builder the shared brief plus its own direction paragraph. For round 2 and later, write `BRIEF-r<n>.md` as a delta. List what the user liked, by variant ID and screenshot path, what they rejected, and which earlier files the builder may read to lift parts. Builders must not read other round-1 variants unless the delta names them.

Before writing the brief, build a reference variant yourself, usually `v01` or the baseline, and check it. Builders copy its `<head>` and script tags. That one file settles the kit, the theme and the 390 px layout before several builders copy a mistake.

For native labs, give builders a small shared script in `kit/` next to the CSS. It draws the surroundings that don't change, such as the rest of a dialog or a page's header. It also holds every status and error message in one function. Variants then differ only in the part being designed, and copy stays the same across them. Document its API in the brief, as in the Kit section below. When a rule changes in a later round, add a new kit file instead of editing this one, so earlier rounds keep showing what the user judged.

---

# [Product] [question], round [n]

You are one of [N] designers. Each of you gets a different direction and works alone. The user will open all of them side by side, so make yours distinct, committed and finished.

## The product

[Two to four sentences: what it is, who uses it, where this screen or part sits, what it must do.]

[Native fidelity] Use the product's real look. Load `../kit/[app.css]` and the fonts in `../kit/`. Use its components' markup and classes as they appear in [paths]. Do not invent new colours, radii or fonts. The variation lives in layout, hierarchy, density, interaction and motion.

[Explore fidelity] You may set a new visual direction. Keep the brand palette in `../kit/tokens.css` and the logo and assets in `../kit/`.

## Kit

[Native labs. Name the reference variant to start from. List the kit's functions with one line each: what they draw or return, and which one owns the copy. Say which tokens builders may use for their own styles, and that they prefix selectors with their variant ID.]

## Data

Use `../kit/fixtures.js` for every number, name and date, so variants compare on design rather than data. [Data rules: units, formatting, edge cases.] Read the `data` query parameter, if present, and switch between the typical, empty and heavy fixtures.

## What your file must contain

- [Screens as hash routes: `#a`, `#b`. Or states as hash routes. Or, for a component, the live component in its real surroundings at the top, then every state frozen below it at true size. Mark them `data-part="live"` and `data-part="states"`, or similar.]
- `data-part` on these regions: [names].
- Working interactions: [list]. No dead buttons and no lorem ipsum.
- Light [and dark through `html[data-theme]` and `prefers-color-scheme`]. Use the product's tokens for every colour, never raw hex or oklch values, so dark mode follows the product's CSS.
- Correct at 1440 and 390 px wide.

## Constraints from the user

[Paste DECISIONS.md: locked parts, rejected traits, standing constraints.]

[Paste the relevant lines from references/taste.md.]

## Quality bar

- Plain UI copy in sentence case. Say what a control does. Use the fewest words that work, with no explanatory paragraphs, marketing voice, em dashes or decorative emoji.
- Use tabular numbers in columns. Nothing clips, overflows sideways or shifts layout when values change.
- Give grid columns `minmax(0, 1fr)` rather than `1fr` or `auto`. Grid items default to `min-width: auto`, so a fixed-width child pushes the page past 390 px.
- Charts are hand-built SVG or CSS. Use thin marks, quiet gridlines, selective labels and hover tooltips, and give each entity one fixed colour everywhere.
- Motion only where it earns its place: under 300 ms for UI, ease-out on entry, no bounce, and `prefers-reduced-motion` respected.
- Every control is reachable by keyboard with a visible focus ring. Hover states on everything clickable. Contrast passes.
- Avoid the generic AI look: purple gradients, identical rounded cards everywhere, emoji icons, glow and pulsing for "energy". Draw icons as inline SVG or use the product's icon set.

## Your direction

[Name]. [Axis]. [The bet in two sentences.] [Precedent, if any.]

## Output

Write exactly one file: `[lab]/variants/[vNN-name].html`, or `[lab]/sections/[slot]/[id].html` for a fragment. Start it with the `lab-meta` block from references/board.md: id, name, axis, idea, cost, model, round, parents. Do not touch any other file or the product repo.

Before reporting, open your file through the lab server. The orchestrator gives you the URL, or you run `python3 [skill]/scripts/lab.py check [lab] --ids [your id]`. Fix every issue it reports. Then take screenshots with `lab.py shoot` at 1440 and 390 and look at them. If you can't render it, say so.

[Builders in a sandbox without Chrome, such as Codex: skip check and shoot, write carefully, and say so in the report. The orchestrator or the wrapper agent runs check afterwards.]

Report in at most five lines: the file path, the idea in one sentence, how it differs from the obvious solution, one honest weakness, and whether you rendered it.
