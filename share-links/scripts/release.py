#!/usr/bin/env python3
"""Stop processes left running in T3 worktrees that are done, so their ports and memory free up.

  release.py           report what would stop
  release.py --apply   stop it

A worktree is done when every T3 thread that uses it is settled, archived or deleted and none is
running or pinned, or when T3 deleted its folder. A running delegated thread keeps its whole family
in use, and a delegated child must be settled itself. Worktrees no thread names are left alone.

Only orphans stop. An orphan's parent chain reaches launchd without passing an app, a launchd job,
an agent runtime (claude, codex, cursor-agent), tmux, screen, zellij, mosh or sshd. A live agent
session's own processes sit under the T3 app, so they stay. T3 ends those with the session. A dev
server started with nohup or `( ... &)` is an orphan, and so is anything that outlived its session.

The unit that stops is the highest process tied to the worktree and everything under it. A process
is tied when its working directory or its command line is inside the worktree. If anything in that
tree is an agent, a shell host or tied to a worktree still in use, the whole tree stays. Otherwise
each process gets SIGTERM, then SIGKILL after five seconds. Freeing the worktree's processes also lets the weekly
t3-worktree-cleanup run remove the folder, since it holds any worktree a process is using.
"""
import argparse
import datetime
import os
import re
import signal
import sqlite3
import subprocess
import sys
import time

HOME = os.path.expanduser("~")
WORKTREES = os.path.realpath(os.path.join(HOME, ".t3/worktrees"))
DB = os.path.join(HOME, ".t3/userdata/statev2.sqlite")
ACTIVE_RUN_STATES = ("queued", "preparing", "starting", "running", "waiting")
OWNERS = {"tmux", "screen", "zellij", "sshd", "sshd-session", "mosh-server"}
# A running agent is work in progress, not a leftover. Its servers become orphans once it exits.
AGENTS = {"codex", "claude", "cursor-agent", "t3-claude"}
# Folder names only, so a path in `-v <worktree>:/app` or `<worktree>,` still names the worktree itself.
TIED = re.compile(re.escape(WORKTREES) + r"/([A-Za-z0-9._-]+)/([A-Za-z0-9._-]+)")


def run(args, timeout=60):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)


def done_worktrees():
    """(worktrees every T3 thread is done with, worktrees any thread names). (None, None) when T3's
    database can't be trusted."""
    try:
        con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True, timeout=10)
    except sqlite3.Error:
        return None, None
    try:
        marks = ",".join("?" * len(ACTIVE_RUN_STATES))
        running = {r[0] for r in con.execute(
            "select distinct thread_id from orchestration_v2_projection_runs where status in (%s)" % marks,
            ACTIVE_RUN_STATES)}
        threads = {}
        for tid, wt, root, rel, archived, deleted, settled, pinned in con.execute(
            """select thread_id, json_extract(payload_json,'$.worktreePath'),
                      coalesce(json_extract(payload_json,'$.lineage.rootThreadId'), thread_id),
                      json_extract(payload_json,'$.lineage.relationshipToParent'),
                      archived_at, deleted_at,
                      json_extract(payload_json,'$.settledAt'), json_extract(payload_json,'$.pinnedAt')
               from orchestration_v2_projection_threads"""):
            threads[tid] = dict(wt=wt, root=root, rel=rel, archived=archived, deleted=deleted, settled=settled, pinned=pinned)
    except sqlite3.Error:
        return None, None
    finally:
        con.close()
    if not any(t["wt"] for t in threads.values()):
        return None, None  # The format changed, so nothing counts as settled.

    running_roots = {threads[t]["root"] for t in running if t in threads}
    pinned_roots = {t["root"] for t in threads.values() if t["pinned"] and not t["deleted"]}
    busy, done, known = set(), set(), set()
    for tid, t in threads.items():
        if not t["wt"]:
            continue
        wt = os.path.realpath(t["wt"])
        known.add(wt)
        r = threads.get(t["root"])
        if tid in running or t["root"] in running_roots:
            busy.add(wt)
        elif t["deleted"]:
            done.add(wt)
        elif r is None or t["root"] in pinned_roots:
            busy.add(wt)
        elif not (r["deleted"] or r["archived"] or r["settled"]):
            busy.add(wt)
        # A delegated child thread settles by itself. Only a provider's subagents follow their root.
        elif tid != t["root"] and t["rel"] != "subagent" and not (t["archived"] or t["settled"]):
            busy.add(wt)
        else:
            done.add(wt)
    return done - busy, known


def processes():
    procs = {}
    for line in run(["ps", "-axo", "pid=,ppid=,uid=,command="]).stdout.splitlines():
        parts = line.split(None, 3)
        if len(parts) < 3:
            continue
        procs[int(parts[0])] = dict(ppid=int(parts[1]), uid=int(parts[2]), cmd=parts[3] if len(parts) > 3 else "")
    out = run(["lsof", "-a", "-u", str(os.getuid()), "-d", "cwd", "-Fpn"], timeout=120).stdout
    pid = None
    for line in out.splitlines():
        if line.startswith("p"):
            pid = int(line[1:])
        elif line.startswith("n") and pid in procs:
            procs[pid]["cwd"] = line[1:]
    return procs


def listening_ports():
    ports, pid = {}, None
    for line in run(["lsof", "-nP", "-a", "-u", str(os.getuid()), "-iTCP", "-sTCP:LISTEN", "-Fpn"]).stdout.splitlines():
        if line.startswith("p"):
            pid = int(line[1:])
        elif line.startswith("n"):
            ports.setdefault(pid, set()).add(line[1:].rsplit(":", 1)[-1])
    return ports


def launchd_jobs():
    jobs = set()
    for line in run(["launchctl", "list"]).stdout.splitlines()[1:]:
        first = line.split("\t", 1)[0]
        if first.isdigit():
            jobs.add(int(first))
    return jobs


def worktrees_of(proc):
    found = {m.group(0) for m in TIED.finditer(proc["cmd"])}
    cwd = proc.get("cwd", "")
    if cwd.startswith(WORKTREES + "/"):
        found.add("/".join(cwd.split("/")[: WORKTREES.count("/") + 3]))
    return found


def names(proc):
    """The program's name and its first argument's, so `node .../codex exec` counts as codex.
    ps shows a detached screen as SCREEN and an ssh session as `sshd-session: user@ttys001`."""
    return {os.path.basename(t).rstrip(":").lower() for t in proc["cmd"].split()[:2]}


def owned(pid, procs, jobs, me):
    """True when something other than launchd answers for this process: an app, a job, a shell host."""
    p, first, seen = pid, True, set()
    while p > 1 and p in procs and p not in seen:
        seen.add(p)
        if p in jobs or p in me or names(procs[p]) & (OWNERS | AGENTS):
            return True
        # An app above this process owns it. An app that is itself the orphan, like a test browser, does not.
        # Python.app is only how macOS packages the interpreter, so a Python parent is not an app.
        if not first and ".app/Contents/MacOS/" in procs[p]["cmd"] and "/Python.app/" not in procs[p]["cmd"]:
            return True
        first = False
        p = procs[p]["ppid"]
    return False


def ancestors(pid, procs):
    chain, p = set(), pid
    while p > 1 and p in procs and p not in chain:
        chain.add(p)
        p = procs[p]["ppid"]
    return chain


def plan():
    done, known = done_worktrees()
    procs = processes()
    jobs = launchd_jobs()
    me = ancestors(os.getpid(), procs)
    uid = os.getuid()

    def released(wt):
        if done is not None and wt in done:
            return True
        # A missing folder only counts for a path T3 created. A path in some command line can be anything.
        return not os.path.isdir(wt) and (done is None or wt in known)

    def holds(p):
        """True for a process that must keep running, which keeps the whole tree it sits in."""
        wts = worktrees_of(procs[p])
        return p in me or p in jobs or bool(names(procs[p]) & (OWNERS | AGENTS)) or bool(wts and not all(released(w) for w in wts))

    tied = {}
    for pid, proc in procs.items():
        if proc["uid"] != uid:
            continue
        wts = worktrees_of(proc)
        # A process tied to any worktree still in use stays, even if it also names a released one.
        if wts and all(released(w) for w in wts):
            tied[pid] = sorted(wts)[0]

    roots = {}
    for pid, wt in tied.items():
        if owned(pid, procs, jobs, me):
            continue
        top = pid
        while procs[top]["ppid"] in tied and not owned(procs[top]["ppid"], procs, jobs, me):
            top = procs[top]["ppid"]
        roots[top] = wt
    # A tied process can sit below an untied one that sits below another top. Stop each tree once.
    roots = {t: wt for t, wt in roots.items() if not (ancestors(procs[t]["ppid"], procs) & set(roots))}

    children = {}
    for pid, proc in procs.items():
        children.setdefault(proc["ppid"], []).append(pid)
    groups = []
    for top, wt in sorted(roots.items()):
        tree, stack = [], [top]
        while stack:
            p = stack.pop()
            tree.append(p)
            stack.extend(children.get(p, []))
        # Stopping part of a tree can still break what holds it, like a wrapper waiting on codex to write a report.
        held = next((p for p in tree if holds(p)), None)
        reason = "folder is gone" if not os.path.isdir(wt) else "threads are done"
        groups.append(dict(worktree=wt, reason=reason, pids=tree, held=held))
    return groups, procs, done is None


def stop(pids):
    for p in pids:
        try:
            os.kill(p, signal.SIGTERM)
        except OSError:
            pass
    deadline = time.time() + 5
    alive = list(pids)
    while alive and time.time() < deadline:
        time.sleep(0.25)
        alive = [p for p in alive if exists(p)]
    for p in alive:
        try:
            os.kill(p, signal.SIGKILL)
        except OSError:
            pass
    return alive


def exists(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def main():
    p = argparse.ArgumentParser(description="Stop orphaned processes in T3 worktrees that are done.")
    p.add_argument("--apply", action="store_true", help="stop them, instead of only reporting")
    a = p.parse_args()

    groups, procs, blind = plan()
    for g in [g for g in groups if g["held"]]:
        if not a.apply:
            print("keeping %s, because %d is still in use: %s" % (
                g["worktree"].replace(HOME, "~"), g["held"], procs[g["held"]]["cmd"][:120]))
    groups = [g for g in groups if not g["held"]]
    if blind and (groups or not a.apply):
        print("T3's database could not be read, so only worktrees whose folder is gone count.", file=sys.stderr)
    if not groups:
        if not a.apply:
            print("Nothing to stop.")
        return
    ports = listening_ports()
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for g in groups:
        freed = sorted({port for pid in g["pids"] for port in ports.get(pid, ())}, key=int)
        print("%s %s %s (%s)%s" % (
            stamp, "stopping" if a.apply else "would stop", g["worktree"].replace(HOME, "~"), g["reason"],
            ", frees port " + ", ".join(freed) if freed else ""))
        for pid in g["pids"]:
            print("  %d %s" % (pid, procs[pid]["cmd"][:160]))
        if a.apply:
            left = stop(g["pids"])
            if left:
                print("  sent SIGKILL to %s" % ", ".join(map(str, left)))
    sys.stdout.flush()


if __name__ == "__main__":
    main()
