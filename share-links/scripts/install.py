#!/usr/bin/env python3
"""Set up share-links on this Mac, or remove it.

  install.py              install or update
  install.py --uninstall  remove everything except the shared files in ~/shared

It installs:
- com.share-links.server, a LaunchAgent that serves ~/shared on 127.0.0.1:4860
- `tailscale serve` on HTTPS port 8446 in front of it, so links work from every tailnet device
- com.share-links.design-lab, which keeps the design-lab server on its fixed port, when the skill is installed
- com.share-links.release, which runs release.py --apply every five minutes
- `share` in ~/.local/bin
- check_links.py as a Stop hook in ~/.claude/settings.json and ~/.codex/hooks.json
- ~/.config/share-links/config.json with the origin and the ports that stay up

Run it again after moving the skill folder. Codex runs a new hook only after you trust it in /hooks.
"""
import argparse
import json
import os
import plistlib
import shutil
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True  # Keep __pycache__ out of the skill folder.
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import CONFIG, HOME, LOGS, SCRIPTS, config  # noqa: E402

AGENTS_DIR = os.path.join(HOME, "Library/LaunchAgents")
PYTHON = "/usr/bin/python3"
LAB = os.path.join(HOME, ".claude/skills/design-lab/scripts/lab.py")
LAB_PORT = int(os.environ.get("DESIGN_LAB_PORT", "4870"))
BIN = os.path.join(HOME, ".local/bin/share")
HOOK = "%s %s" % (PYTHON, os.path.join(SCRIPTS, "check_links.py"))
HOOK_FILES = [os.path.join(HOME, ".claude/settings.json"), os.path.join(HOME, ".codex/hooks.json")]
PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def run(args, check=False):
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as e:
        out = subprocess.CompletedProcess(args, 1, "", str(e))
    if check and out.returncode != 0:
        sys.exit("%s failed: %s" % (" ".join(args), (out.stderr or out.stdout).strip()))
    return out


def tailscale():
    return shutil.which("tailscale") or "/Applications/Tailscale.app/Contents/MacOS/Tailscale"


def tailnet_name():
    try:
        name = json.loads(run([tailscale(), "status", "--json"]).stdout)["Self"]["DNSName"].rstrip(".")
        return name or None
    except (OSError, ValueError, KeyError):
        return None


def served_ports():
    """Ports `tailscale serve` exposes and the local ports behind them. Someone chose to keep those up."""
    try:
        status = json.loads(run([tailscale(), "serve", "status", "--json"]).stdout or "{}")
    except (OSError, ValueError):
        return set()
    ports = {int(p) for p in status.get("TCP", {})}
    for site in status.get("Web", {}).values():
        for handler in site.get("Handlers", {}).values():
            target = handler.get("Proxy", "")
            if target.rsplit(":", 1)[-1].rstrip("/").isdigit():
                ports.add(int(target.rsplit(":", 1)[-1].rstrip("/")))
    return ports


def label_path(label):
    return os.path.join(AGENTS_DIR, label + ".plist")


def load(label, program, **extra):
    os.makedirs(LOGS, exist_ok=True)
    plist = {
        "Label": label,
        "ProgramArguments": program,
        "EnvironmentVariables": {"PATH": PATH},
        "RunAtLoad": True,
        "StandardOutPath": os.path.join(LOGS, label.split(".")[-1] + ".log"),
        "StandardErrorPath": os.path.join(LOGS, label.split(".")[-1] + ".log"),
        **extra,
    }
    with open(label_path(label), "wb") as f:
        plistlib.dump(plist, f)
    unload(label, remove=False)
    # bootout returns before launchd has let go of the old job, so the first bootstrap can fail.
    for attempt in range(10):
        out = run(["launchctl", "bootstrap", "gui/%d" % os.getuid(), label_path(label)])
        if out.returncode == 0:
            return
        time.sleep(0.5)
    sys.exit("launchctl bootstrap %s failed: %s" % (label, out.stderr.strip()))


def unload(label, remove=True):
    run(["launchctl", "bootout", "gui/%d/%s" % (os.getuid(), label)])
    if remove and os.path.exists(label_path(label)):
        os.remove(label_path(label))


def stop_stray_lab_server():
    """The launchd copy needs the lab port. A copy lab.py started by itself may hold it."""
    for pid in run(["lsof", "-t", "-nP", "-iTCP:%d" % LAB_PORT, "-sTCP:LISTEN"]).stdout.split():
        cmd = run(["ps", "-o", "command=", "-p", pid]).stdout
        if "lab.py serve" in cmd:
            os.kill(int(pid), signal.SIGTERM)
    for _ in range(20):
        if not run(["lsof", "-t", "-nP", "-iTCP:%d" % LAB_PORT, "-sTCP:LISTEN"]).stdout.strip():
            return
        time.sleep(0.25)


def edit_hooks(path, add):
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        if not add:
            return
        data = {}
    hooks = data.get("hooks", {})
    stop = [g for g in hooks.get("Stop", []) if not any("check_links.py" in h.get("command", "") for h in g.get("hooks", []))]
    if add:
        stop.append({"hooks": [{"type": "command", "command": HOOK, "timeout": 10}]})
    if stop:
        hooks["Stop"] = stop
    else:
        hooks.pop("Stop", None)
    if hooks or "hooks" in data:
        data["hooks"] = hooks
    if not add and data == {"hooks": {}}:
        os.remove(path)  # Only this hook was in it, as in the ~/.codex/hooks.json install created.
        return
    tmp = path + ".share-links.tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def write_config(cfg):
    os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
    with open(CONFIG, "w") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")


def install():
    name = tailnet_name()
    cfg = config()
    cfg["origin"] = "https://%s:%d" % (name, cfg["https_port"]) if name else None
    cfg.setdefault("extra_ports", [])
    durable = {cfg["port"], cfg["https_port"]} | served_ports() | set(cfg["extra_ports"])
    if os.path.exists(LAB):
        durable.add(LAB_PORT)
    cfg["durable_ports"] = sorted(durable)
    write_config(cfg)
    os.makedirs(cfg["root"], exist_ok=True)

    load("com.share-links.server", [PYTHON, os.path.join(SCRIPTS, "serve.py")], KeepAlive=True, ThrottleInterval=10)
    load("com.share-links.release", [PYTHON, os.path.join(SCRIPTS, "release.py"), "--apply"], StartInterval=300)
    if os.path.exists(LAB):
        # lab.py joins the tailnet by itself once Tailscale is up, so it can start at login.
        stop_stray_lab_server()
        load("com.share-links.design-lab", [PYTHON, LAB, "serve", "--foreground", "--tailnet"],
             KeepAlive=True, ThrottleInterval=10, WorkingDirectory=HOME)

    os.makedirs(os.path.dirname(BIN), exist_ok=True)
    if os.path.lexists(BIN):
        os.remove(BIN)
    os.symlink(os.path.join(SCRIPTS, "share"), BIN)
    for path in HOOK_FILES:
        if os.path.isdir(os.path.dirname(path)):
            edit_hooks(path, add=True)

    if not name:
        print("Tailscale is not up, so links are local only. Run install.py again once it is.")
    else:
        out = run([tailscale(), "serve", "--bg", "--https=%d" % cfg["https_port"], "http://127.0.0.1:%d" % cfg["port"]])
        if out.returncode != 0:
            print("tailscale serve failed, so links are local only: %s" % (out.stderr or out.stdout).strip())
            cfg["origin"] = None
            write_config(cfg)

    print("Share root   %s" % cfg["root"])
    print("Links        %s/" % (cfg["origin"] or "http://127.0.0.1:%d" % cfg["port"]))
    print("Lasting ports %s" % ", ".join(map(str, cfg["durable_ports"])))
    print("Logs         %s" % LOGS)
    print("In Codex, open /hooks once and trust the share-links Stop hook.")


def uninstall():
    cfg = config()
    for label in ("com.share-links.server", "com.share-links.release", "com.share-links.design-lab"):
        unload(label)
    run([tailscale(), "serve", "--https=%d" % cfg["https_port"], "off"])
    if os.path.islink(BIN):
        os.remove(BIN)
    for path in HOOK_FILES:
        edit_hooks(path, add=False)
    if os.path.exists(CONFIG):
        os.remove(CONFIG)
    print("Removed. Shared files stay in %s." % cfg["root"])


def main():
    p = argparse.ArgumentParser(description="Install or remove share-links on this Mac.")
    p.add_argument("--uninstall", action="store_true")
    a = p.parse_args()
    uninstall() if a.uninstall else install()


if __name__ == "__main__":
    main()
