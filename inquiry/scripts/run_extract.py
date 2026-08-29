#!/usr/bin/env python3
"""Run the extractor prompt over every filtered chunk with codex exec (gpt-5.6-sol), N at a time."""
import glob, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.expanduser("~/Development/life/inquiry/mining")
SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = os.path.join(os.path.dirname(HERE), "candidates")
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True); os.makedirs(CAND, exist_ok=True)
prompt = open(os.path.join(SKILL, "references", "extractor-prompt.md")).read().split("---\n", 1)[1]
def run(chunk):
    n = os.path.basename(chunk)[:-3]
    out = os.path.join(CAND, f"transcripts-{n}.md")
    if os.path.exists(out) and os.path.getsize(out) > 0: return f"{n} skip"
    p = prompt.replace("CHUNK_PATH", chunk).replace("OUT_PATH", out)
    with open(os.path.join(HERE, "logs", f"{n}.log"), "w") as log:
        rc = subprocess.call(["codex", "exec", "-C", os.path.dirname(HERE), "-s", "workspace-write",
                              "-o", os.path.join(HERE, "logs", f"{n}.last.md"), p], stdout=log, stderr=subprocess.STDOUT)
    line = f"{n} exit {rc}"
    with open(os.path.join(HERE, "logs", "summary.log"), "a") as s: s.write(line + "\n")
    return line
chunks = sorted(glob.glob(os.path.join(HERE, "filtered", "chunk-*.md")))
with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as ex:
    for r in ex.map(run, chunks): print(r, flush=True)
with open(os.path.join(HERE, "logs", "summary.log"), "a") as s: s.write("DONE\n")
