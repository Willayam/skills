#!/usr/bin/env python3
"""Append an instance to an existing belief and update last_seen and status.

usage: add_instance.py 0042 --date 2026-08-29 --situation "..." --quote "..." --source live
"""
import argparse, datetime, glob, os, re, sys
VAULT = os.path.expanduser("~/Development/life/inquiry")
a = argparse.ArgumentParser()
a.add_argument("id")
a.add_argument("--date", default=datetime.date.today().isoformat())
a.add_argument("--situation", required=True)
a.add_argument("--quote", default="")
a.add_argument("--source", default="live")
args = a.parse_args()
paths = glob.glob(os.path.join(VAULT, "beliefs", f"{args.id}-*.md"))
if len(paths) != 1: sys.exit(f"belief {args.id} not found")
path = paths[0]; t = open(path).read()
entry = (f'  - date: {args.date}\n    situation: "{args.situation.replace(chr(34), chr(39))}"\n'
         f'    quote: "{args.quote.replace(chr(34), chr(39))}"\n    source: {args.source}\n')
head, sep, body = t.partition("\n---\n")
if "instances:" not in head: sys.exit("no instances key in frontmatter")
# insert after the last instance line (instances block runs to the next top-level key or end)
lines = head.split("\n"); i = lines.index("instances:") + 1
while i < len(lines) and (lines[i].startswith("  ") or lines[i] == ""): i += 1
lines.insert(i, entry.rstrip("\n"))
head = "\n".join(lines)
head = re.sub(r"^last_seen: .*$", f"last_seen: {args.date}", head, flags=re.M)
m = re.search(r"^status: (\w+)$", head, re.M)
if m and m.group(1) in ("turned", "quiet"):
    head = head.replace(m.group(0), "status: recurring")
open(path, "w").write(head + sep + body)
print(path)
