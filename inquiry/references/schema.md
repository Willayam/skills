# Belief file schema

One file per belief at `~/Development/life/inquiry/beliefs/NNNN-slug.md`. The id is four
digits, assigned in order, never reused. The slug is the statement, lowercased, hyphenated,
truncated to about six words.

## Frontmatter

```yaml
id: "0042"
statement: "Clients should respect my time"
about: others
root: "0007"
related: []
status: captured
charge: 7
first_seen: 2026-03-19
last_seen: 2026-08-12
current_belief: ""
instances:
  - date: 2026-03-19
    situation: "X moved the Tuesday call for the third time"
    quote: "third time he's moved it, I'm done being flexible"
    source: life/daily/2026-03-19.md
  - date: 2026-05-02
    situation: "A client booked over a blocked slot"
    quote: "why do people think my calendar is a suggestion"
    source: claude/see-computer
```

A belief is one thought. An instance is one time it fired. Every instance carries the moment
and the words from that moment. The Work is done on one instance at a time, never on the
abstraction.

| field | values | notes |
|---|---|---|
| `id` | four digit string | quoted so leading zeros survive |
| `statement` | one sentence | Katie's form. First person, present tense, one thought. Frozen after capture. |
| `about` | `self`, `others`, `world`, `past`, `future` | who or what the thought judges |
| `root` | id or empty | the deeper belief this one comes from |
| `related` | list of ids | siblings, opposites, same situation |
| `status` | see workflow.md | |
| `charge` | 1 to 10 | how much it hurts now, re-rated after each session |
| `first_seen` | date | earliest source |
| `last_seen` | date | latest source or session |
| `current_belief` | free text | what the user believes more now, after turnarounds |
| `instances` | list | one entry per time the thought fired. `date`, `situation` (one line, what was happening), `quote` (verbatim, or empty if captured live with no record), `source` (file path or chat reference). Never merged, never trimmed. |

## Body

Headings in this order. Empty sections stay in place so later sessions have a slot.

```markdown
# <statement>

## Worksheet
Judge Your Neighbor, six lines. Only for beliefs about another person.

## Sessions
### 2026-08-29, instance 2026-03-19
**Is it true?**
**Can you absolutely know that it's true?**
**How do you react, what happens, when you believe that thought?**
**Who would you be without the thought?**
**Turnarounds**
- To the self: ... (three examples)
- To the other: ... (three examples)
- To the opposite: ... (three examples)
**Truer now:**

## Notes
Anything else. Recurrences, links to daily notes, what triggered it.
```

Each session names the instance it worked. Sessions append. Nothing above is overwritten
except frontmatter fields that are meant to move (`status`, `charge`, `last_seen`,
`current_belief`, `related`, `root`) and `instances`, which only grows.
