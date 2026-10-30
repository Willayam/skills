#!/usr/bin/env python3
"""Stop hook for Claude Code and Codex. Sends a reply back once if it links a server that won't stay up.

It reads the hook's JSON on stdin and checks `last_assistant_message`. A link counts when its host is
this Mac, the LAN or the tailnet and its port is not in `durable_ports`. A loopback link always
counts, because it won't open on the user's phone. Code blocks and inline code are skipped, since
nobody clicks those. A reply that was already sent back (`stop_hook_active`)
always passes, so the agent can keep a link on purpose.
"""
import ipaddress
import json
import os
import re
import sys
import urllib.parse

sys.dont_write_bytecode = True  # Keep __pycache__ out of the skill folder.
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import config  # noqa: E402

URL = re.compile(r"https?://(?:\[[0-9a-f:.]+\]|[^\s<>()\[\]\"'`*/]+)[^\s<>()\[\]\"'`*]*", re.I)
CODE = re.compile(r"```.*?```|~~~.*?~~~|`[^`\n]*`", re.S)
PRIVATE = [ipaddress.ip_network(n) for n in (
    "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16", "100.64.0.0/10", "169.254.0.0/16", "fd00::/8", "fe80::/10")]


def loopback(host):
    host = host.lower().strip("[]")
    if host in ("localhost", "0.0.0.0") or host.endswith(".localhost"):
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def local(host):
    host = host.lower().strip("[]")
    # A name with no dot is a MagicDNS or LAN short name, like williams-mac-mini.
    if loopback(host) or "." not in host or host.endswith((".local", ".ts.net")):
        return True
    try:
        return any(ipaddress.ip_address(host) in n for n in PRIVATE)
    except ValueError:
        return False


def dead_links(text, durable):
    found = []
    for raw in URL.findall(CODE.sub(" ", text)):
        url = raw.rstrip(".,;:!?")
        try:
            parts = urllib.parse.urlsplit(url)
            port = parts.port or (443 if parts.scheme.lower() == "https" else 80)
        except ValueError:
            continue
        host = parts.hostname
        if host and local(host) and (port not in durable or loopback(host)) and url not in found:
            found.append(url)
    return found


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return
    if event.get("stop_hook_active"):
        return
    links = dead_links(event.get("last_assistant_message") or "", set(config()["durable_ports"]))
    if not links:
        return
    reason = (
        "Your reply links addresses that won't open later or on the user's phone: "
        + ", ".join(links)
        + ". A dev server stops when this session ends, its worktree is deleted or the Mac restarts, and a "
        "loopback address only opens on this Mac. The user often opens links hours later, from their phone. "
        "Where a tailnet URL exists for the same page, link that instead. For a page, build or image, run "
        "`share <file-or-folder>` and link the URL it prints. For a design lab, link what `lab.py url <lab> --tailnet` prints. "
        "If the page needs a live server, keep the link but say it needs one, give the command that starts it, and add a "
        "screenshot. If you are only naming an address, put it in backticks. Then send the reply again."
    )
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    main()
