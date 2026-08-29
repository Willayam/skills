#!/usr/bin/env python3
"""Keep only turns that carry a stress marker, then split into chunks for the extractor."""
import re, glob, os
os.chdir(os.path.expanduser("~/Development/life/inquiry/mining"))
MARK = re.compile(r"\b(should|shouldn'?t|need to|needs to|have to|has to|must|always|never|can'?t|cannot|won'?t|hate|frustrat\w*|annoy\w*|stupid|idiot|tired|exhaust\w*|stress\w*|worried|worry|afraid|scared|fear|fail\w*|waste\w*|behind|enough|too (much|many|slow|late|long)|wtf|damn|fuck\w*|ugh|again|sick of|i feel|i'?m (so|not|just|really|tired|done)|why (do|does|did|is|are|can'?t|won'?t|would)|impossible|terrible|horrible|awful|useless|worst|ridiculous|unacceptable|disappoint\w*|embarrass\w*|guilt\w*|shame|regret|anxious|anxiety|overwhelm\w*|burn\w* out|no time|out of time|deadline|urgent|asap|hurry|rush\w*|money|expensive|broke|afford|kids?|wife|family|dad|mom|father|mother|sleep|health|weight|happy|unhappy|bliss|lonely|alone|respect|trust|blame|my fault|their fault|lazy|incompetent|wrong|mistake|broke it|broken again|still (not|doesn'?t|broken)|not working|doesn'?t work)\b", re.I)
os.makedirs("filtered", exist_ok=True)
chunks, cur, size, n = [], [], 0, 0
LIMIT = 180_000
for src in ["claude", "codex"]:
    for path in sorted(glob.glob(f"raw/{src}/*.md")):
        label = f"{src}/{os.path.basename(path)[:-3]}"
        blocks = open(path).read().split("\n### ")
        for b in blocks:
            b = b.strip()
            if not b: continue
            if not b.startswith("###"): b = "### " + b
            body = b.split("\n", 1)[1] if "\n" in b else ""
            if MARK.search(body):
                head, rest = b.split("\n", 1)
                entry = f"{head} [{label}]\n{rest}\n\n"
                cur.append(entry); size += len(entry); n += 1
                if size > LIMIT:
                    chunks.append("".join(cur)); cur, size = [], 0
if cur: chunks.append("".join(cur))
for i, c in enumerate(chunks, 1):
    open(f"filtered/chunk-{i:02d}.md", "w").write(c)
print(f"kept {n} turns in {len(chunks)} chunks")
