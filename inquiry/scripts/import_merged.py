#!/usr/bin/env python3
"""Create belief files from accepted blocks in candidates/merged.md.

usage: import_merged.py --all                  # every block under ## Roots and ## Beliefs
       import_merged.py "I am behind" "I cannot keep a promise to myself"   # by statement
       import_merged.py --list                  # print statements and instance counts

Roots are created first so children can reference them by id. Existing beliefs with the same
statement are skipped. Instances carry over one to one.
"""
import glob, os, re, subprocess, sys
VAULT = os.path.expanduser("~/Development/life/inquiry")
HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.environ.get("INQUIRY_MERGED") or os.path.join(VAULT, "candidates", "merged.md")

def parse():
    text = open(MERGED).read()
    blocks = {}
    for sec in ("Roots", "Beliefs"):
        m = re.search(rf"^## {sec}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
        if not m: continue
        for b in re.finditer(r"^### (.+?)\n(.*?)(?=^### |\Z)", m.group(1), re.S | re.M):
            st, body = b.group(1).strip(), b.group(2)
            g = lambda k, d="": (re.search(rf"^- {k}:\s*(.+)$", body, re.M) or [None, d])[1].strip()
            inst = []
            for line in re.findall(r"^\s+- (\d{4}-\d{2}-\d{2}[^\n]*)$", body, re.M):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    date, sit = parts[0], parts[1]
                    quote = parts[2].strip().strip('"')
                    src = parts[3] if len(parts) > 3 else "unknown"
                    inst.append((date, sit, quote, src))
            blocks[st] = dict(statement=st, about=g("about", "self"), root=g("root"), charge=g("charge", "5"),
                              is_root=(sec == "Roots"), instances=inst)
    return blocks

def existing():
    out = {}
    for p in glob.glob(os.path.join(VAULT, "beliefs", "*.md")):
        t = open(p).read()
        s = re.search(r'^statement: "(.*)"$', t, re.M); i = re.search(r'^id: "(\d+)"$', t, re.M)
        if s and i: out[s.group(1)] = i.group(1)
    return out

def create(b, ids):
    if b["statement"] in ids: return ids[b["statement"]]
    inst = b["instances"] or [("", "no recorded moment", "", "merged")]
    d, sit, q, src = inst[0]
    about = b["about"] if b["about"] in ("self", "others", "world", "past", "future") else "self"
    args = ["python3", os.path.join(HERE, "new_belief.py"), "--statement", b["statement"], "--about", about,
            "--charge", re.sub(r"\D", "", b["charge"]) or "5", "--situation", sit, "--quote", q, "--source", src]
    if d: args += ["--date", d]
    path = subprocess.check_output(args, text=True).strip()
    nid = os.path.basename(path)[:4]
    for d, sit, q, src in inst[1:]:
        a = ["python3", os.path.join(HERE, "add_instance.py"), nid, "--situation", sit, "--quote", q, "--source", src]
        if d: a += ["--date", d]
        subprocess.check_call(a, stdout=subprocess.DEVNULL)
    t = open(path).read()
    dates = sorted(x[0] for x in inst if x[0])
    if dates: t = re.sub(r"^first_seen: .*$", f"first_seen: {dates[0]}", t, flags=re.M)
    if b["root"] and b["root"] in ids: t = re.sub(r'^root: ""$', f'root: "{ids[b["root"]]}"', t, flags=re.M)
    open(path, "w").write(t)
    ids[b["statement"]] = nid
    print(f"{nid}  {b['statement']}  ({len(inst)} instances)")
    return nid

blocks = parse()
if "--list" in sys.argv:
    for st, b in blocks.items(): print(f"{'root ' if b['is_root'] else '     '}{b['charge']:>2}  {len(b['instances']):>3}x  {st}")
    sys.exit()
want = list(blocks) if "--all" in sys.argv else [a for a in sys.argv[1:] if not a.startswith("--")]
missing = [w for w in want if w not in blocks]
if missing: sys.exit("not in merged.md: " + "; ".join(missing))
ids = existing()
for st in want:
    if blocks[st]["is_root"]: create(blocks[st], ids)
for st in want:
    b = blocks[st]
    if not b["is_root"]:
        if b["root"] and b["root"] not in ids and b["root"] in blocks: create(blocks[b["root"]], ids)
        create(b, ids)
subprocess.call(["python3", os.path.join(HERE, "build_index.py")])
