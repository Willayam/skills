#!/usr/bin/env python3
"""Rebuild ~/Development/life/inquiry/index.md from belief frontmatter. Also validates fields."""
import glob, os, re, sys, datetime
VAULT = os.path.expanduser("~/Development/life/inquiry")
STATUSES = ["captured", "worksheet", "questioned", "turned", "quiet", "recurring"]
ABOUT = ["self", "others", "world", "past", "future"]

def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m: return None
    fm, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^[a-z_]+:", line):
            key, _, val = line.partition(":")
            val = val.strip().strip('"')
            fm[key] = [] if val in ("", "[]") and key in ("instances", "related") else val
        elif key == "instances" and line.strip().startswith("- date:"):
            fm["instances"].append(line.split("date:", 1)[1].strip())
        elif key == "related" and line.strip().startswith("- "):
            fm["related"].append(line.strip()[2:].strip('"'))
    return fm

beliefs, errors = [], []
for path in sorted(glob.glob(os.path.join(VAULT, "beliefs", "*.md"))):
    fm = frontmatter(open(path).read())
    name = os.path.basename(path)
    if not fm: errors.append(f"{name}: no frontmatter"); continue
    for f in ("id", "statement", "about", "status", "charge"):
        if not fm.get(f): errors.append(f"{name}: missing {f}")
    if fm.get("status") not in STATUSES: errors.append(f"{name}: bad status {fm.get('status')}")
    if fm.get("about") not in ABOUT: errors.append(f"{name}: bad about {fm.get('about')}")
    try: fm["charge"] = int(fm.get("charge", 0))
    except ValueError: errors.append(f"{name}: charge not a number"); fm["charge"] = 0
    fm["file"] = name
    fm["n"] = len(fm.get("instances") or [])
    if fm["n"] == 0: errors.append(f"{name}: no instances")
    beliefs.append(fm)

by_id = {b["id"]: b for b in beliefs}
def link(b): return f"[{b['id']} {b['statement']}](beliefs/{b['file']})"
open_ = sorted([b for b in beliefs if b["status"] in ("captured", "recurring")], key=lambda b: -b["charge"])
out = [f"# Inquiry\n\nGenerated {datetime.date.today().isoformat()} by build_index.py. Do not edit.\n"]
if open_:
    b = open_[0]
    out.append(f"## Now\n\n{link(b)}, charge {b['charge']}, {b['about']}, fired {b['n']} times, last {b.get('last_seen','')}.\n")
out.append("## By status\n")
for s in STATUSES:
    rows = sorted([b for b in beliefs if b["status"] == s], key=lambda b: -b["charge"])
    if not rows: continue
    out.append(f"### {s} ({len(rows)})\n")
    for b in rows:
        out.append(f"- {link(b)} · charge {b['charge']} · {b['n']}x · {b['about']}" + (f" · root {b['root']}" if b.get("root") else ""))
    out.append("")
roots = [b for b in beliefs if any(c.get("root") == b["id"] for c in beliefs)]
if roots:
    out.append("## Roots\n")
    for r in sorted(roots, key=lambda b: -b["charge"]):
        out.append(f"- {link(r)} · {r['status']} · charge {r['charge']}")
        for c in sorted([c for c in beliefs if c.get("root") == r["id"]], key=lambda b: -b["charge"]):
            out.append(f"  - {link(c)} · {c['status']} · charge {c['charge']}")
    out.append("")
shifted = [b for b in beliefs if b.get("current_belief")]
if shifted:
    out.append("## What shifted\n")
    for b in shifted: out.append(f"- {link(b)} → {b['current_belief']}")
    out.append("")
if errors:
    out.append("## Validation\n"); out += [f"- {e}" for e in errors]
os.makedirs(VAULT, exist_ok=True)
open(os.path.join(VAULT, "index.md"), "w").write("\n".join(out) + "\n")
print(f"{len(beliefs)} beliefs, {len(errors)} errors")
sys.exit(1 if errors else 0)
