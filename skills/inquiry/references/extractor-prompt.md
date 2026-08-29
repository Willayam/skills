# Extractor prompt

Used by `scripts/run_extract.py`. `CHUNK_PATH` and `OUT_PATH` are substituted at run time. For journals and other prose, hand an Opus subagent the same text with the file list in place of CHUNK_PATH.

---

You are mining a chunk of William's own messages to AI coding agents (Claude Code and Codex) for stressful thoughts, in the sense Byron Katie uses in The Work. The file to read is CHUNK_PATH. Read the whole file. Each turn starts with `### <date> <project> [source]`.

Most turns are engineering instructions. That is fine. The material is in the tone and the asides. Frustration at the agent ("you keep breaking this", "why can't you just"), self-talk ("I always do this", "I'm wasting the whole day"), deadline and money pressure, comparison, fear of failure, exhaustion, judgments about coworkers, clients, or family, anything about kids, wife, health, sleep, time. Also beliefs stated as fact that carry a charge ("this should have been done weeks ago", "I can't trust the tests", "nobody else can do this").

What counts. A thought that, when believed, causes stress. Markers: should, shouldn't, need to, have to, must, always, never, can't, not enough, too much, if only, judgments of other people, complaints, fears about the future, regrets about the past, self-criticism, scarcity about time or money, needing approval, needing control. Ignore neutral instructions, plans, questions, and preferences. Ignore swearing that carries no belief. A plain bug report is not a candidate. "This is the third time and I'm done" is.

Katie's rule. Judge a specific situation, not an abstraction. Attach the specific moment when the turn gives one. Keep the statement short, in William's own words where possible, first person, present tense, in the simplest form ("X should Y", "I need Z", "I am not W"). Note that thoughts aimed at an AI agent are still real thoughts ("it should get it right the first time" is a valid worksheet line).

Write findings to OUT_PATH. Use exactly this format, one block per distinct thought. Merge near-duplicates into one block, but keep every occurrence as its own instance line. An instance is one time the thought fired. Never collapse two moments into one line.

## <statement>
- about: self | others | world | past | future
- charge: <1 to 10, your estimate from tone and repetition>
- markers: <the words that flagged it>
- instances:
  - <date> | <one line, what was happening at that moment> | "<exact quote, trimmed to the relevant sentence or two>" | <project or file>

At the bottom add `## Possible roots` with 2 to 6 deeper beliefs the surface thoughts seem to come from, each with the statements under it listed by heading text.

Quotes must be verbatim. If the chunk yields nothing real, write the file with a single line "No candidates." Plain prose. No em dashes, no colons as mid-sentence connectors, no chatbot filler, no emoji, no praise. Completeness beats polish. Do not edit any other file.
