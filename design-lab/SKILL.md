---
name: design-lab
description: Show design options so the user can judge them on a phone or a Mac and reply by dictating. Picks the lightest form for the question, an inline page in the T3 thread for looks, a hosted video for motion, a throwaway build with a comment bar for interaction, and a real build on a device or preview for real use. Use when the user asks for variants, options, directions, mockups or prototypes, asks to redesign something, make it look better or animate it, wants to compare designs, or sends feedback on earlier options.
---

# Design lab

The user decides by looking, often on a phone, and replies by dictating. Put the next thing in front of them within minutes. Ask one question at a time, and show only what answers it.

## Setup

`S` below is this skill's scripts folder, `~/.claude/skills/design-lab/scripts`. If `share` or `ffmpeg` is missing on this machine, run `sh $S/setup.sh`, then carry on. It installs what sharing and video need and prints anything it can't fix.

## Choose the form

| They are judging | Show it as | They reply |
|---|---|---|
| Looks: layout, type, colour, a component's states | Inline page in the thread | In chat, by letter |
| Motion: transitions, timing, anything that moves on its own | Hosted video | In chat, by letter |
| Interaction: gestures, drag, sliders, sound, anything to touch | Throwaway build at a shared link | Comment bar, pasted into chat |
| True size: a TV, a big screen, type from a distance | Full-size page at a shared link | Comment bar, pasted into chat |
| Real use: real data, the backend, device hardware | Real build on a preview deploy or their phone | In chat |

When something fits two rows, start with the lighter one. A form the user names wins.

## Choose the step

Build only what the current step needs. Never build a whole deck before the first reaction.

1. **Direction.** "What should this be?" Show 3 to 5 real bets, one key screen each. Two options that differ only in colour or copy count as one.
2. **Screen by screen.** "Which version of this screen?" Show options A to D for one screen, then the next screen. The user's picks add up to the design, so build that combination for them.
3. **Dial in.** "Is this detail right?" Show one design with every state visible at once, or 2 to 4 versions that each change one thing. Sliders sit next to the state they change, mark their defaults and write their values to the URL.
4. **Real use.** Get it on their device or a preview as soon as a leader exists.

Start at the step the request belongs to. A big UI or flow change starts at 1. A single component starts at 2 or 3.

## Inline page

Use `html_preview`, look at the PNG and console output, then call `html_render` with its `contentHeight`. Load both with ToolSearch. Outside T3, `share` the page and post the link with a screenshot.

- One question per page. Label each option A, B, C under the image, with its name.
- The frame is 728 px wide on desktop and about 360 on a phone. Use `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))` so options stack on a phone. Show components at true size.
- Frames run JavaScript, so toggles and sliders work. The page must be self-contained and under 512 KB.
- Images load from absolute paths. Local video files do not. Frames can't save anything, so no marking buttons.
- For a real screen, use stills instead of rebuilding it: `node $S/capture.mjs still /tmp/round --size 1440x900 "A Name=URL" "B Name=URL"`. Add `--full` for the page height and `--dark` for dark mode. It prints page errors and sideways scroll.

## Hosted video

Anything that moves goes in a video, recorded and hosted so it plays on the phone and the Mac:

```bash
node $S/capture.mjs clip /tmp/fan.mp4 --size 390x700 --seconds 6 \
  --run "document.querySelector('.fan').click()" "A Tight fan=a.html" "B Loose fan=b.html"
share /tmp/fan.mp4 --name fan-r1
```

The clip stacks the options, labelled and in sync, as H.264 that plays on an iPhone. Add `--speed 0.5` for a slow version of timing questions. It records no sound, so use a build for sound.

`share` prints an HTTPS tailnet URL and copies the file to `~/shared/<project>/<name>/`. In the reply, embed that copy with Markdown image syntax and its absolute path, then put the URL on the next line. A `/tmp` path disappears, so never embed one. For a simulator, use the `record` command from `device_open`.

## Throwaway build

Keep it small enough to finish quickly. Test the one interaction with fixture data, and leave out routing, auth and the rest of the app.

- **In a repo with a web build.** Add a scratch entry that imports the real components, then `bun run build -- --base ./ && share dist`. Keep it out of the diff. If that takes more than about ten minutes to get working, copy the built CSS into one HTML file instead.
- **No repo, or a new concept.** One HTML file, then `share` it.
- **Needs the backend.** Use the project's preview deploy.
- **Native.** Add a debug route behind `__DEV__` and run it on the user's phone. Use the T3 device tools for a simulator so they can watch it. Comments go in chat.

Add the comment bar to every web build. Copy `assets/comment.js` next to the page and `share` the folder:

```html
<script src="comment.js" data-title="Fan tools" data-options="A Tight fan, B Loose fan"></script>
```

The comment field stays open with the cursor in it. The user dictates a note, taps Next or the keyboard's return key to move on with the cursor kept in the field, then taps Copy all and pastes into the chat. A phone only raises its keyboard after a first tap. Picking B sets `<html data-option="B">` and fires a `labOption` event, so one page can hold every option. For separate pages use `A Tight fan=a.html`. Add `data-corner="top"` when the bar would cover what they are testing. `capture.mjs` hides the bar in stills and clips.

## Every round

- Keep `~/design-lab/<project>/<slug>/NOTES.md`: what the user said, verbatim, plus locked decisions, rejected traits and standing constraints. Read it first. Rejected traits never come back.
- Dictation garbles words. Post their feedback back as a short numbered list before building, and say which reading you took.
- Fit the product. Use its real CSS, tokens, fonts, components and realistic data, and show the current design as an option when it helps. New visual languages are opt-in. Follow [references/taste.md](references/taste.md).
- Look at what you show, at phone and desktop width, in dark mode if the product has it. Say what you did not check.
- Keep option names stable across rounds and never reuse them. Recommend one in a line.
- Say in one sentence what they are judging and what is only sample content.
- Add nothing unasked: no extra settings, features, decorative copy or explanation.
- Use parallel builders only for step 1. Use `design-lab builders` from the model configuration, and spread them across model families. Codex builders run with `-C <folder> -s workspace-write --skip-git-repo-check`, and their sandbox blocks Chrome, so capture for them. Every other step is a direct edit.

## Ship the pick

Port it onto a branch using the product's own components and tokens. Compare the build with the option at phone and desktop width, then remove the scratch code. Load the preview URL and confirm it shows the change before saying it is live. Record the pick in `NOTES.md`.

## Old board labs

Folders with a `lab.json` came from the old board. Treat their `FEEDBACK.md` and `DECISIONS.md` as the notes and carry on with the forms above. Open the board with `scripts/lab.py`, documented in `references/board.md`, only if the user asks for it by name.
