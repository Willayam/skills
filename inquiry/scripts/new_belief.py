#!/usr/bin/env python3
"""Create a belief file from the template with the next free id.

usage: new_belief.py --statement "..." --about self --charge 6 \
                     --date 2026-03-19 --situation "..." --quote "..." --source life/daily/2026-03-19.md
Creates the belief with its first instance. Later instances are appended by add_instance.py.
"""
import argparse, datetime, glob, os, re
VAULT = os.path.expanduser("~/Development/life/inquiry")
TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "belief-template.md")
a = argparse.ArgumentParser()
a.add_argument("--statement", required=True)
a.add_argument("--about", required=True, choices=["self", "others", "world", "past", "future"])
a.add_argument("--situation", required=True, help="one line, what was happening")
a.add_argument("--charge", type=int, default=5)
a.add_argument("--quote", default="", help="verbatim words from that moment, or empty")
a.add_argument("--source", default="live", help="file path or chat reference")
a.add_argument("--date", default=datetime.date.today().isoformat(), help="when the thought fired")
args = a.parse_args()
os.makedirs(os.path.join(VAULT, "beliefs"), exist_ok=True)
ids = [int(os.path.basename(p)[:4]) for p in glob.glob(os.path.join(VAULT, "beliefs", "[0-9][0-9][0-9][0-9]-*.md"))]
nid = f"{(max(ids) + 1) if ids else 1:04d}"
slug = "-".join(re.sub(r"[^a-z0-9 ]", "", args.statement.lower()).split()[:6]) or "belief"
body = open(TEMPLATE).read()
for k, v in {"id": nid, "statement": args.statement.replace('"', "'"), "about": args.about,
             "situation": args.situation.replace('"', "'"), "charge": args.charge, "date": args.date,
             "source": args.source, "quote": args.quote.replace('"', "'")}.items():
    body = body.replace("{" + k + "}", str(v))
path = os.path.join(VAULT, "beliefs", f"{nid}-{slug}.md")
open(path, "w").write(body)
print(path)
