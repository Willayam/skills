# Board, lab files and commands

## Commands

All commands take a lab as `<slug>` (resolved in the current project), `<project>/<slug>`, or an absolute path.

| Command | What it does |
| --- | --- |
| `lab.py init <slug> --title T --scope S [--screens id:Label,...] [--parts a,b] [--slots id:Label,...] [--fidelity native\|explore]` | Creates the lab, starts the server, prints the folder and the board URL |
| `lab.py url <lab> [--tailnet]` | Starts the server if needed and prints the board URL. Run it before every link you post |
| `lab.py labs` | Every lab on this Mac, newest first. The server root `/` shows the same list |
| `lab.py list <lab>` | Variants, rounds, models and the user's verdicts |
| `lab.py check <lab> [--widths 1440,390] [--ids v03,hero-b]` | Renders each variant through headless Chrome at each width and prints problems |
| `lab.py shoot <lab> [--ids ...] [--width W] [--screens a,b] [--theme light\|dark\|both\|auto] [--full]` | Per-variant screenshots at 2x into `shots/`. Light by default, since headless Chrome otherwise follows the Mac. `--full` captures the whole page height and is the default for component and page labs. Widths under 500 render in an exact frame |
| `lab.py shoot <lab> --board [--view grid\|parts\|flow\|mix] [--cols N] [--round N]` | One contact sheet of the board |
| `lab.py stills <lab> [--ids ...] [--skip run] [--wait MS] [--size 1600] [--jobs 6]` | Freezes every visible variant in every screen into `shots/stills` and records them in `lab.json`. The grid then shows images instead of live frames. Rerun after changing a variant |
| `lab.py export <lab> <dir>` | Static copy for hosting elsewhere |
| `lab.py stop` | Stops the server. Where a LaunchAgent runs it, launchd starts it again |

Environment: `DESIGN_LAB_ROOT` (default `~/design-lab`) and `DESIGN_LAB_PORT` (default 4870). The default root always uses that port, so board links never change. If the root is not writable, as in some sandboxes, labs go to `./.design-lab`, whose server takes the next free port.

## Lab folder

```
~/design-lab/<project>/<slug>/
  lab.json        orchestrator-owned settings, described below
  BRIEF.md        shared builder brief, then BRIEF-r2.md and so on per round
  FEEDBACK.md     the user's words, verbatim, in order
  DECISIONS.md    locked, rejected, standing constraints
  kit/            product CSS, tokens, fonts, icons, fixtures
  variants/       whole variants: v00-current.html, v01-quiet-ledger.html, ...
  sections/<slot>/a.html, b.html, ...   page fragments, one folder per slot
  shots/          screenshots
  state.json      board state: verdicts, notes, pins, picks (written by the board)
```

## lab.json

```json
{
  "title": "Accounts page",
  "scope": "concept",
  "fidelity": "native",
  "round": 2,
  "rounds": [
    {"n": 1, "question": "Which overall direction?"},
    {"n": 2, "question": "Organise around accounts and entries", "note": "Built from your picks: v06 Sankey, v03 hero"}
  ],
  "widths": [1440, 1024, 390],
  "screens": [{"id": "accounts", "label": "Accounts"}, {"id": "transactions", "label": "Transactions"}],
  "parts": ["networth", "institutions", "ledger"],
  "slots": [{"id": "hero", "label": "Hero"}, {"id": "faq", "label": "FAQ"}],
  "locked": {"hero": "e"},
  "controls": {"data": ["typical", "empty", "heavy"], "state": ["rest", "hover", "open"]},
  "pageHead": ["kit/app.css", "kit/fonts.css"],
  "pageClass": "theme-light",
  "external": [{"id": "v20", "name": "In the real app", "url": "http://localhost:3000/accounts?variant=grid", "round": 3}],
  "decision": "v18, shipped in PR #3"
}
```

- `screens` are hash routes. Every variant in a concept or flow lab implements each one (`#accounts`). Use them for flow steps and component states as well.
- `parts` are `data-part` names that variants put on their main regions. They drive the Parts view and `check`.
- `slots` define a page built from fragments, in order. `locked` pins a slot to a variant.
- `controls` become selects in the board toolbar. Each value goes to every frame as a query parameter (`?data=empty&state=hover`), so one switch sets all variants to the same data or state. Variants read them with `new URLSearchParams(location.search)`.
- `view` and `part` set what the board opens on the first visit, such as `"view": "parts", "part": "live"`. Component labs open on Parts by default. A link can do the same with `?view=parts&part=live`.
- `pageHead` holds stylesheets the fragment page loads, relative to the lab folder.
- `stills` is written by `lab.py stills`. With it, Grid shows frozen images, all preloaded, and a row of state buttons. ← → or a button swaps every tile at once. Focus stays live, and More has a checkbox to play every design live in the grid. Use it for animated concept labs, where ten live frames lag and load unevenly.
- `stillWait` is virtual milliseconds to settle per screen, such as `{"door": 4000, "bets": 13000}`. A variant's `lab-meta` can override it with its own `stillWait`, needed when a screen loops. `noScreens` in `lab-meta` lists screens a variant doesn't have, and its tile says so.
- `reviewBy: "state"` ties verdicts and comments to the screen on show, stored as `v12@question`, and Copy feedback lists them under `Slide: <label>`. Use it when designs are compared one slide type at a time. The state buttons show how many designs are marked on each slide.
- `tabs` adds pages next to the designs: `[{"id": "bilder", "label": "Bilder", "src": "review/bilder.html"}]`. `src` is relative to the lab. The board forwards ← → to the page as a `{type: "step", by}` message.
- `external` lists variants that live somewhere else, such as an app route. The board frames them. Pins and part cut-outs work only if that page loads `http://127.0.0.1:4870/_lab/runtime.js`.

## Variant files

A whole variant is one HTML file in `variants/`, named `vNN-short-name.html`. It may load files from `../kit/`. Put this block in `<head>`:

```html
<script type="application/json" id="lab-meta">
{"id": "v07", "name": "Statement ledger", "axis": "printed statement made interactive",
 "idea": "Sections read like a bank statement with section balances.", "cost": "Dense on phones",
 "model": "opus", "round": 2, "parents": ["v03", "v06"], "recommended": false, "why": "", "baseline": false}
</script>
```

- `"parts": ["live", "states"]` lists the parts this variant has, when it differs from `lab.json`. `check` skips the part check for the baseline.
- `"old": true` hides a superseded variant from the default view, even if it was an agent pick. It stays under the round filter.
- `v00` is the current design with `"baseline": true`. Copy the real screen as closely as possible, or point an `external` entry at the running app.
- `axes` turns a variant into a mixer: `"axes": {"buttons": ["soft", "flat", "quiet"], "hero": ["1", "2", "3"]}`. The board shows a select per axis and reloads the variant with `?buttons=flat&hero=2`. Use it when the user is combining independent choices.
- Mark main regions with `data-part="name"`, using the names in `lab.json` `parts`.
- Theme: honour `html[data-theme="dark"]` and `html[data-theme="light"]` as well as `prefers-color-scheme`. The board sets the attribute.
- Screens: switch on `location.hash` and listen for `hashchange`.

The server injects `_lab/runtime.js` into every variant it serves. Builders never add it.

## Section fragments

A fragment is `sections/<slot>/<id>.html`, where `id` is a letter or short name. It contains one root element, a `<style>` scoped under one root class, an optional `<script>`, and the `lab-meta` block. It has no `<html>`, `<head>` or `<body>`. It uses the kit's tokens from `pageHead` and no new fonts. URLs inside it are relative to the lab folder. Recommended and `"old": true` work as they do for variants. Fragments written this way can move into production nearly unchanged.

The composed page is `_page.html?picks=hero:b,faq:a`. With `&only=hero` it renders one slot by itself.

## Board views

- **Grid.** Every variant at the chosen device width, scaled into 1 to 4 columns. Full page shows each variant's whole height.
- **Parts.** One part or slot across all variants, cropped to that part. Parts that fit render at true size.
- **Screens.** Rows are variants and columns are screens. Click a cell to open it in Focus.
- **Mix.** Slot rail on the left, composed page on the right. Picks persist and go into the copied feedback.
- **Focus.** One variant, interactive, keys ← and →. "Next to current" puts `v00` beside it.

Header line: the title and round question, the screen picker, the device switch, More and Copy feedback, which stays pinned at the top right once the page scrolls. The device switch is one segmented control with a glyph and a word per width from `lab.json`; widths of the same kind, such as two phones, show their px instead, and every option names its exact px on hover. Each design sits on its own plate with one line under it: the name, which opens Focus, and the verdict keys, which always show their words. In Focus the name moves up into the header in place of the title, and the line under the design keeps Previous, Next and the keys. More holds the view (Grid, Parts, Screens, Mix), the part, the round filter, columns, theme, shared controls, whole pages, the current design beside the open one, and filters for No and Yes. Theme colours the board as well as the designs: Auto follows the system and changes with it, Light and Dark override it.

Every variant has four buttons with matching keys: Y yes, M maybe, N no, C comment. Keys act on the tile under the pointer, or the open one. C opens a comment box under that variant. While it is open, a click inside the design ties the comment to that element, and the board records the part, the quoted text and a selector. Enter adds the comment and Esc cancels. Other keys: 1 to 9 open a variant large, O opens the one under the pointer, ← and → flip while one is open, and Esc goes back. Clicking a cell in Screens opens it large.

Two boards open on the same lab, such as a laptop and a phone, stay in step. Each one takes the other's verdicts and comments within a few seconds unless it has unsaved changes of its own.

Copy feedback puts the latest round on the clipboard in one click, for the user to paste into the chat. Each verdict and comment records the round it was made in, and only the latest round's go into the copy. Earlier rounds' marks stay on their tiles. Marks saved before the board recorded rounds count for their variant's round. It works the same in a static export. Plain http on the tailnet has no Clipboard API, so the board copies through a hidden text field there, and if the browser blocks that too it shows the text selected for a manual copy. The text lists Yes, Maybe and No, the page mix, chosen settings, then each comment with its variant, part, quoted text and selector.

On a phone, under 700 px wide, the board changes in these ways:

- Designs render at the lab's narrowest width under 700 px, or at 390 if the lab has none, until the reviewer picks another width. The device switch moves to a Width row at the top of More, and More drops Columns because the grid is one column.
- Every key has a button. Yes, Maybe, No and Comment sit under each design, its name opens Focus, Previous and Next beside the count flip, and Back returns. A tap inside the design ties an open comment to that spot.
- Buttons have 44 px touch targets and form fields use 16 px text, so iOS does not zoom.
- Focus gives the design the visible screen above the verdict row, with the idea and comments below. Screens swipes each variant's row sideways. Mix puts each slot on one row above the page.

Older labs stored keep and cut verdicts, pins and notes. The board converts them to yes, no and comments when it loads.

## Live updates

The board polls the lab every three seconds. A new or removed file re-renders the board. A changed file reloads only its own frame. Builders can write files while the user is already looking.
