#!/usr/bin/env python3
"""Pull William's own words out of Claude Code and Codex session logs.

Writes one markdown file per Claude project and one per Codex month, user turns only,
code blocks stripped, injected context (<environment_context>, <system-reminder>, etc.) skipped.
"""
import json, os, re, sys, glob, hashlib
from collections import defaultdict
from datetime import datetime

HOME = os.path.expanduser("~")
OUT = os.path.join(HOME, "Development/life/inquiry/mining/raw")
FENCE = re.compile(r"```.*?```", re.S)
TAG = re.compile(r"<[a-zA-Z_-]+[^>]*>.*?</[a-zA-Z_-]+>", re.S)
MIN_LEN = 25

def clean(text):
    text = FENCE.sub("", text)
    text = TAG.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text

def keep(text):
    if len(text) < MIN_LEN: return False
    if text.startswith(("<", "[Request interrupted", "Caveat:", "/")): return False
    return True

seen = set()
def dedupe(text):
    h = hashlib.md5(text.encode()).hexdigest()
    if h in seen: return False
    seen.add(h); return True

def write(path, turns):
    turns.sort(key=lambda t: t[0])
    with open(path, "w") as f:
        for ts, ctx, text in turns:
            f.write(f"### {ts[:10]} {ctx}\n{text}\n\n")

# Claude Code
by_project = defaultdict(list)
for path in glob.glob(os.path.join(HOME, ".claude/projects/*/**/*.jsonl"), recursive=True):
    project = path.split("/.claude/projects/")[1].split("/")[0].replace("-Users-williamlarsten-", "").replace("-Users-williamlarsten", "home") or "root"
    try:
        for line in open(path, errors="ignore"):
            try: obj = json.loads(line)
            except Exception: continue
            if obj.get("type") != "user" or obj.get("isMeta"): continue
            msg = obj.get("message") or {}
            content = msg.get("content")
            texts = []
            if isinstance(content, str): texts.append(content)
            elif isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "text": texts.append(b.get("text", ""))
            for t in texts:
                t = clean(t)
                if keep(t) and dedupe(t):
                    by_project[project].append((obj.get("timestamp", ""), project, t))
    except Exception as e:
        print("skip", path, e, file=sys.stderr)
for project, turns in by_project.items():
    write(os.path.join(OUT, "claude", f"{project}.md"), turns)

# Codex
by_month = defaultdict(list)
for path in glob.glob(os.path.join(HOME, ".codex/sessions/**/*.jsonl"), recursive=True):
    cwd = ""
    try:
        for line in open(path, errors="ignore"):
            try: obj = json.loads(line)
            except Exception: continue
            p = obj.get("payload") or {}
            if obj.get("type") == "session_meta": cwd = os.path.basename(p.get("cwd", "")); continue
            if obj.get("type") == "event_msg" and p.get("type") == "user_message":
                t = clean(p.get("message", ""))
                if keep(t) and dedupe(t):
                    ts = obj.get("timestamp", "")
                    by_month[ts[:7]].append((ts, cwd, t))
    except Exception as e:
        print("skip", path, e, file=sys.stderr)
for month, turns in by_month.items():
    write(os.path.join(OUT, "codex", f"{month}.md"), turns)

total = sum(len(v) for v in by_project.values()) + sum(len(v) for v in by_month.values())
print(f"claude projects: {len(by_project)}, codex months: {len(by_month)}, turns: {total}")
