#!/usr/bin/env python3
"""Design lab helper. One server on a fixed port serves every lab under the lab root.

Standard library only, Python 3.9+. Lab root: $DESIGN_LAB_ROOT, else ~/design-lab.

  lab.py init <slug | project/slug> [--title T] [--scope concept|flow|component|page|system]
                 [--screens id:Label,...] [--parts a,b] [--slots id:Label,...] [--fidelity native|explore]
  lab.py url <lab> [--tailnet]       start the server if needed, print the board URL
  lab.py serve [--tailnet]           start the server if needed, print the root URL
  lab.py stop
  lab.py labs                        every lab, newest first
  lab.py list <lab>                  variants with verdicts
  lab.py check <lab> [--widths 1440,390] [--ids v01,v02]
  lab.py shoot <lab> [--ids ...] [--round N] [--screens a,b] [--width W] [--height H] [--full] [--theme light|dark|both|auto]
                     [--board] [--cols N] [--view V]
  lab.py export <lab> <outdir>
  lab.py project                     the project name used for labs started from this directory
"""
import argparse
import datetime
import glob
import html as htmllib
import http.server
import json
import os
import re
import shutil
import signal
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD_DIR = os.path.join(SKILL_DIR, "assets", "board")
DEFAULT_PORT = int(os.environ.get("DESIGN_LAB_PORT", "4870"))
DEFAULT_ROOT = os.path.abspath(os.path.expanduser("~/design-lab"))
# The share-links skill installs this LaunchAgent to keep the default root's server up across restarts.
LAUNCH_AGENT = "com.share-links.design-lab"
META_RE = re.compile(r'<script[^>]*id=["\']lab-meta["\'][^>]*>(.*?)</script>', re.S | re.I)
RUNTIME_TAG = '<script src="/_lab/runtime.js" data-lab-runtime defer></script>'
EARLY_TAG = ("<script data-lab-early>window.__labErrors=[];addEventListener('error',function(e){var t=e.target;"
             "if(t&&t!==window&&(t.src||t.href)){__labErrors.push('failed to load '+(t.src||t.href))}"
             "else{__labErrors.push('script error: '+(e.message||e.error))}},true);"
             "addEventListener('unhandledrejection',function(e){__labErrors.push('unhandled rejection: '+((e.reason&&e.reason.message)||e.reason))});"
             "(function(c){console.error=function(){__labErrors.push('console.error: '+[].map.call(arguments,String).join(' ').slice(0,200));"
             "return c.apply(console,arguments)}})(console.error);</script>")
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome", "chromium", "chromium-browser",
]


def lab_root():
    root = os.environ.get("DESIGN_LAB_ROOT") or os.path.expanduser("~/design-lab")
    try:
        os.makedirs(root, exist_ok=True)
        probe = os.path.join(root, ".write-probe")
        open(probe, "w").close()
        os.remove(probe)
        return os.path.abspath(root)
    except OSError:
        fallback = os.path.abspath(".design-lab")
        os.makedirs(fallback, exist_ok=True)
        print("lab root %s is not writable here, using %s" % (root, fallback), file=sys.stderr)
        return fallback


# Labs have written this as an object as well as a string. An object must not break every listing.
def decision_text(decision):
    if isinstance(decision, dict):
        return ", ".join(str(v) for v in (decision.get("pick"), decision.get("where") or decision.get("note")) if v)
    return str(decision or "")


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def read_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


WRITE_LOCK = threading.Lock()


def write_json(path, data):
    with WRITE_LOCK:
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", prefix=".tmp-", suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)


def to_int(v, default=1):
    try:
        return int(v)
    except (TypeError, ValueError):
        m = re.search(r"\d+", str(v))
        return int(m.group(0)) if m else default


def git(*args):
    try:
        return subprocess.run(["git"] + list(args), capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def project_name():
    remote = git("remote", "get-url", "origin")
    if remote:
        return re.sub(r"\.git$", "", remote.rstrip("/").split("/")[-1].split(":")[-1])
    common = git("rev-parse", "--path-format=absolute", "--git-common-dir")
    if common:
        return os.path.basename(os.path.dirname(common.rstrip("/")))
    return os.path.basename(os.getcwd()) or "scratch"


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "lab"


def resolve_lab(arg, must_exist=True):
    root = lab_root()
    if os.path.isabs(arg) or arg.startswith("."):
        d = os.path.abspath(arg)
    elif "/" in arg:
        d = os.path.join(root, arg)
    else:
        d = os.path.join(root, slugify(project_name()), arg)
        if must_exist and not os.path.isfile(os.path.join(d, "lab.json")):
            hits = glob.glob(os.path.join(root, "*", arg, "lab.json"))
            if len(hits) == 1:
                d = os.path.dirname(hits[0])
    if must_exist and not os.path.isfile(os.path.join(d, "lab.json")):
        raise SystemExit("no lab at %s" % d)
    return d


def lab_path(d):
    """URL path of a lab, with a trailing slash. Labs outside the root are not served."""
    rel = os.path.relpath(d, lab_root())
    if rel.startswith(".."):
        raise SystemExit("%s is outside the lab root %s" % (d, lab_root()))
    return "/" + urllib.parse.quote(rel.replace(os.sep, "/")) + "/"


# ---------------------------------------------------------------- lab data

def file_meta(path, rel, default_id):
    meta = {"id": default_id, "name": ""}
    m = re.match(r"(v\d+)[-_]?(.*)", default_id)
    if m:
        meta = {"id": m.group(1), "name": m.group(2).replace("-", " ").strip()}
    try:
        with open(path, errors="ignore") as f:
            head = f.read(300000)
        found = META_RE.search(head)
        if found:
            parsed = json.loads(found.group(1))
            if isinstance(parsed, dict):
                meta.update(parsed)
            else:
                meta["metaError"] = "lab-meta is not a JSON object"
    except (OSError, ValueError) as e:
        meta["metaError"] = str(e)
    meta["file"] = rel
    try:
        meta["mtime"] = os.path.getmtime(path)
    except OSError:
        pass
    return meta


def collect(d):
    lab = read_json(os.path.join(d, "lab.json"), {})
    variants = []
    vdir = os.path.join(d, "variants")
    if os.path.isdir(vdir):
        for name in sorted(os.listdir(vdir)):
            if name.endswith(".html") and not name.startswith("_"):
                variants.append(file_meta(os.path.join(vdir, name), "variants/" + name, os.path.splitext(name)[0]))
    for ext in lab.get("external", []):
        variants.append(dict(ext, external=True))
    variants.sort(key=lambda v: (to_int(v.get("round", 1)), str(v.get("id"))))
    seen = {}
    for v in variants:
        if v["id"] in seen:
            v["duplicate"] = seen[v["id"]]
        seen.setdefault(v["id"], v.get("file") or v.get("url"))
    slots = []
    sdir = os.path.join(d, "sections")
    declared = [s if isinstance(s, dict) else {"id": s} for s in lab.get("slots", [])]
    names = [s["id"] for s in declared]
    if os.path.isdir(sdir):
        names += sorted(n for n in os.listdir(sdir) if os.path.isdir(os.path.join(sdir, n)) and n not in names)
    for sid in names:
        decl = next((s for s in declared if s["id"] == sid), {"id": sid})
        frags = []
        fdir = os.path.join(sdir, sid)
        if os.path.isdir(fdir):
            for name in sorted(os.listdir(fdir)):
                if name.endswith(".html") and not name.startswith("_"):
                    frags.append(file_meta(os.path.join(fdir, name), "sections/%s/%s" % (sid, name), os.path.splitext(name)[0]))
        frags.sort(key=lambda v: (to_int(v.get("round", 1)), str(v.get("id"))))
        slots.append({"id": sid, "label": decl.get("label", sid), "variants": frags})
    return {"lab": lab, "variants": variants, "slots": slots, "dir": d,
            "state": read_json(os.path.join(d, "state.json"), {})}


def all_labs():
    root = lab_root()
    out = []
    for path in glob.glob(os.path.join(root, "*", "*", "lab.json")) + glob.glob(os.path.join(root, "*", "lab.json")):
        d = os.path.dirname(path)
        lab = read_json(path, {})
        vcount = len(glob.glob(os.path.join(d, "variants", "*.html"))) + len(glob.glob(os.path.join(d, "sections", "*", "*.html")))
        stamps = [os.path.getmtime(p) for p in glob.glob(os.path.join(d, "*")) + glob.glob(os.path.join(d, "variants", "*"))]
        rounds = [to_int(lab.get("round", 1))]
        for f in glob.glob(os.path.join(d, "variants", "*.html")) + glob.glob(os.path.join(d, "sections", "*", "*.html")):
            rounds.append(to_int(file_meta(f, "", "x").get("round", 1)))
        out.append({"dir": d, "path": lab_path(d), "title": lab.get("title", os.path.basename(d)), "scope": lab.get("scope", ""),
                    "round": max(rounds), "variants": vcount, "decision": decision_text(lab.get("decision")),
                    "updated": max(stamps) if stamps else 0})
    out.sort(key=lambda x: -x["updated"])
    return out


# ---------------------------------------------------------------- init

def cmd_init(a):
    arg = a.lab if "/" in a.lab or os.path.isabs(a.lab) else "%s/%s" % (slugify(project_name()), slugify(a.lab))
    d = resolve_lab(arg, must_exist=False)
    for sub in ("variants", "shots", "kit"):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    path = os.path.join(d, "lab.json")
    lab = read_json(path, {})
    lab.setdefault("title", a.title or os.path.basename(d).replace("-", " "))
    lab.setdefault("scope", a.scope)
    lab.setdefault("fidelity", a.fidelity)
    lab.setdefault("created", now())
    lab.setdefault("source", os.getcwd())
    lab.setdefault("round", 1)
    lab.setdefault("rounds", [{"n": 1, "question": ""}])
    lab.setdefault("widths", [1440, 1024, 390])
    if a.screens:
        lab["screens"] = [dict(zip(("id", "label"), (s.split(":", 1) + [s])[:2])) for s in a.screens.split(",")]
    lab.setdefault("screens", [])
    if a.parts:
        lab["parts"] = [p.strip() for p in a.parts.split(",") if p.strip()]
    lab.setdefault("parts", [])
    if a.slots:
        lab["slots"] = [dict(zip(("id", "label"), (s.split(":", 1) + [s])[:2])) for s in a.slots.split(",")]
        os.makedirs(os.path.join(d, "sections"), exist_ok=True)
        for s in lab["slots"]:
            os.makedirs(os.path.join(d, "sections", s["id"]), exist_ok=True)
    lab.setdefault("controls", {})
    lab.setdefault("pageHead", [])
    lab.setdefault("external", [])
    write_json(path, lab)
    for name, text in (("FEEDBACK.md", "# Feedback ledger\n\nEverything the user said about this lab, verbatim and in order. Newest at the bottom.\n"),
                       ("DECISIONS.md", "# Decisions\n\n## Locked\n\n## Rejected, do not bring back\n\n## Standing constraints\n")):
        p = os.path.join(d, name)
        if not os.path.exists(p):
            with open(p, "w") as f:
                f.write(text)
    print(d)
    info = ensure_server(False)
    print(info["url"].rstrip("/") + lab_path(d))


# ---------------------------------------------------------------- server

class Handler(http.server.SimpleHTTPRequestHandler):
    root = "."
    hosts = set()

    def log_message(self, fmt, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def host_ok(self):
        # Reject other Host names so a DNS-rebinding page can't read the labs.
        if (self.headers.get("Host") or "").lower() in self.hosts:
            return True
        self.send_error(403, "unknown host")
        return False

    def fs_path(self, urlpath):
        rel = os.path.normpath(urllib.parse.unquote(urlpath)).lstrip("/")
        if rel.startswith("..") or rel == ".":
            return self.root if rel == "." else None
        return os.path.join(self.root, rel)

    def lab_for(self, urlpath):
        prefix = urlpath.split("/_lab/")[0] if "/_lab/" in urlpath else urlpath
        d = self.fs_path(prefix)
        while d and d.startswith(self.root) and d != self.root:
            if os.path.isfile(os.path.join(d, "lab.json")):
                return d
            d = os.path.dirname(d)
        return None

    def send_bytes(self, body, ctype, code=200):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, data, code=200):
        self.send_bytes(json.dumps(data, ensure_ascii=False).encode(), "application/json; charset=utf-8", code)

    def send_file(self, path, inject=False, early=False):
        if not path or not os.path.isfile(path):
            return self.send_error(404)
        ctype = self.guess_type(path)
        with open(path, "rb") as f:
            body = f.read()
        if (inject or early) and path.endswith(".html"):
            text = body.decode("utf-8", errors="replace")
            if inject and "data-lab-runtime" not in text:
                i = text.lower().rfind("</body>")
                text = text[:i] + RUNTIME_TAG + text[i:] if i >= 0 else text + RUNTIME_TAG
            if early:
                m = re.search(r"<head[^>]*>", text, re.I)
                text = text[:m.end()] + EARLY_TAG + text[m.end():] if m else EARLY_TAG + text
            body = text.encode()
            ctype = "text/html; charset=utf-8"
        self.send_bytes(body, ctype)

    def do_GET(self):
        if not self.host_ok():
            return
        parsed = urllib.parse.urlparse(self.path)
        p = parsed.path
        check = "labcheck=1" in parsed.query
        if p == "/" or p == "/index.html":
            return self.send_bytes(root_index().encode(), "text/html; charset=utf-8")
        if p.endswith("/_lab/api/lab"):
            d = self.lab_for(p)
            return self.send_json(collect(d)) if d else self.send_json({"error": "no lab"}, 404)
        if "/_lab/" in p:
            rest = os.path.normpath(p.split("/_lab/", 1)[1]).lstrip("./")
            return self.send_file(os.path.join(BOARD_DIR, rest))
        local = self.fs_path(p)
        if local and os.path.isdir(local):
            if not p.endswith("/"):
                self.send_response(301)
                self.send_header("Location", p + "/")
                self.end_headers()
                return
            if os.path.isfile(os.path.join(local, "lab.json")):
                return self.send_file(os.path.join(BOARD_DIR, "index.html"))
            return self.send_error(404)
        if p.endswith("/_page.html") and self.lab_for(p):
            return self.send_file(os.path.join(BOARD_DIR, "page.html"), early=check)
        # Fragments are pasted into _page.html, which already runs the runtime.
        return self.send_file(local, inject="/sections/" not in p, early=check)

    def do_POST(self):
        if not self.host_ok():
            return
        origin = self.headers.get("Origin")
        if origin and urllib.parse.urlparse(origin).netloc.lower() != (self.headers.get("Host") or "").lower():
            return self.send_json({"error": "cross-origin request refused"}, 403)
        if "application/json" not in (self.headers.get("Content-Type") or ""):
            return self.send_json({"error": "JSON only"}, 415)
        p = urllib.parse.urlparse(self.path).path
        d = self.lab_for(p)
        if not d:
            return self.send_json({"error": "no lab"}, 404)
        n = int(self.headers.get("Content-Length") or 0)
        try:
            data = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self.send_json({"error": "bad json"}, 400)
        if p.endswith("/_lab/api/state"):
            write_json(os.path.join(d, "state.json"), data)
            return self.send_json({"ok": True})
        return self.send_json({"error": "unknown endpoint"}, 404)


def root_index():
    rows = []
    for lab in all_labs():
        when = datetime.datetime.fromtimestamp(lab["updated"]).strftime("%Y-%m-%d %H:%M") if lab["updated"] else ""
        project = lab["path"].strip("/").split("/")[0]
        rows.append('<tr><td>%s</td><td><a href="%s">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
            htmllib.escape(project), lab["path"], htmllib.escape(lab["title"]), htmllib.escape(lab["scope"]),
            lab["round"], lab["variants"], htmllib.escape(lab["decision"]), when))
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Design labs</title><style>
:root{color-scheme:light dark}body{margin:0;font:14px/1.45 system-ui,-apple-system,sans-serif;background:Canvas;color:CanvasText}
main{max-width:1100px;margin:0 auto;padding:40px 20px}h1{font-size:22px;margin:0 0 4px}p{color:GrayText;margin:0 0 24px}
table{width:100%%;border-collapse:collapse}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid color-mix(in srgb,CanvasText 14%%,transparent)}
th{font-size:12px;color:GrayText;font-weight:600}td:nth-child(5),td:nth-child(4){font-variant-numeric:tabular-nums}a{color:inherit}
</style></head><body><main><h1>Design labs</h1><p>Every lab on this machine, newest first. Root: %s</p>
<table><thead><tr><th>Project</th><th>Lab</th><th>Scope</th><th>Round</th><th>Variants</th><th>Decision</th><th>Updated</th></tr></thead>
<tbody>%s</tbody></table></main></body></html>""" % (htmllib.escape(lab_root()), "".join(rows) or '<tr><td colspan="7">No labs yet.</td></tr>')


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True
    # A board loads every variant at once. The default backlog of 5 drops
    # connections, so pages come up without their kit scripts or CSS.
    request_queue_size = 128


def port_free(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


def tailnet():
    for exe in ("tailscale", "/Applications/Tailscale.app/Contents/MacOS/Tailscale"):
        try:
            out = subprocess.run([exe, "status", "--json"], capture_output=True, text=True, timeout=5).stdout
            data = json.loads(out)
            ip = (data.get("Self", {}).get("TailscaleIPs") or [None])[0]
            name = (data.get("Self", {}).get("DNSName") or "").rstrip(".")
            if ip:
                return ip, name
        except (OSError, ValueError, subprocess.SubprocessError):
            continue
    return None, None


def state_file():
    return os.path.join(lab_root(), ".server.json")


def listener(port):
    """The pid listening on 127.0.0.1:port, or None."""
    try:
        out = subprocess.run(["lsof", "-t", "-nP", "-iTCP@127.0.0.1:%d" % port, "-sTCP:LISTEN"],
                             capture_output=True, text=True, timeout=5).stdout.split()
        return int(out[0]) if out else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def launch_agent():
    """launchctl's target for the LaunchAgent that runs the default root's server, if this Mac has one."""
    if lab_root() != DEFAULT_ROOT:
        return None
    target = "gui/%d/%s" % (os.getuid(), LAUNCH_AGENT)
    try:
        loaded = subprocess.run(["launchctl", "print", target], capture_output=True, timeout=5).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return None
    return target if loaded else None


def server_info():
    info = read_json(state_file(), None)
    if not info:
        return None
    try:
        os.kill(info["pid"], 0)
    except OSError:
        return None
    try:
        with urllib.request.urlopen(info["url"] + "_lab/ping.txt", timeout=1.5) as r:
            if r.status == 200:
                return info
    except Exception:
        pass
    # A slow ping, or a sandbox that blocks it, is not a dead server. Starting a second one moved board
    # links to a new port. Trust the state file only if its pid is the one listening.
    return info if listener(info["port"]) == info["pid"] else None


def ensure_server(want_tailnet, port=None):
    info = server_info()
    if info and (info.get("shareUrl") or not want_tailnet):
        return info
    agent = None if port else launch_agent()
    if agent:
        # launchd runs this server. A second copy would fight it for the port, so ask launchd instead.
        if not info:
            subprocess.run(["launchctl", "kickstart", agent], capture_output=True, timeout=10)
        for _ in range(150):  # launchd waits 10 seconds before it restarts a job that just exited.
            info = server_info()
            if info:
                return info
            time.sleep(0.1)
        raise SystemExit("the %s LaunchAgent did not start the lab server" % LAUNCH_AGENT)
    if info:
        os.kill(info["pid"], signal.SIGTERM)
        time.sleep(0.4)
    args = [sys.executable, os.path.abspath(__file__), "serve", "--foreground"]
    if want_tailnet:
        args.append("--tailnet")
    if port:
        args += ["--port", str(port)]
    root = lab_root()
    log = open(os.path.join(root, ".server.log"), "a")
    env = dict(os.environ, DESIGN_LAB_ROOT=root)
    subprocess.Popen(args, stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True, cwd=root, env=env)
    for _ in range(60):
        time.sleep(0.1)
        info = server_info()
        if info:
            return info
    raise SystemExit("lab server did not start, see %s" % os.path.join(lab_root(), ".server.log"))


def run_server(want_tailnet, port):
    root = lab_root()
    ip, name = tailnet() if want_tailnet else (None, None)
    # The default root keeps one port so board links never change. Another root, like a sandbox's
    # ./.design-lab, takes the next free port.
    walk = not port and root != DEFAULT_ROOT
    port = port or DEFAULT_PORT
    while not (port_free("127.0.0.1", port) and (not ip or port_free(ip, port))):
        if not walk:
            raise SystemExit("port %d is taken, so the lab server can't start. lab.py url finds the running one." % port)
        port += 1
    Handler.root = root
    Handler.hosts = {"127.0.0.1:%d" % port, "localhost:%d" % port}
    server = Server(("127.0.0.1", port), Handler)
    info = {"pid": os.getpid(), "port": port, "url": "http://127.0.0.1:%d/" % port, "root": root, "started": now()}

    def listen_on_tailnet(ip, name):
        Handler.hosts.add("%s:%d" % (ip, port))
        if name:
            Handler.hosts.add("%s:%d" % (name.lower(), port))
            Handler.hosts.add("%s:%d" % (name.split(".")[0].lower(), port))
        threading.Thread(target=Server((ip, port), Handler).serve_forever, daemon=True).start()
        info["shareUrl"] = "http://%s:%d/" % (name or ip, port)
        write_json(state_file(), info)

    def wait_for_tailnet():
        # At login launchd can start this before Tailscale is up. Join the tailnet once it is.
        while True:
            time.sleep(10)
            ip, name = tailnet()
            if ip:
                try:
                    return listen_on_tailnet(ip, name)
                except OSError:
                    pass

    write_json(state_file(), info)
    if ip:
        listen_on_tailnet(ip, name)
    elif want_tailnet:
        threading.Thread(target=wait_for_tailnet, daemon=True).start()
    print(info["url"], flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def cmd_serve(a):
    if a.foreground:
        return run_server(a.tailnet, a.port)
    info = ensure_server(a.tailnet, a.port)
    print(info["url"])
    if info.get("shareUrl"):
        print(info["shareUrl"])


def cmd_url(a):
    d = resolve_lab(a.lab)
    info = ensure_server(a.tailnet)
    print(info["url"].rstrip("/") + lab_path(d))
    if info.get("shareUrl"):
        print(info["shareUrl"].rstrip("/") + lab_path(d))


def cmd_stop(a):
    info = server_info()
    if not info:
        print("not running")
        return
    os.kill(info["pid"], signal.SIGTERM)
    print("stopped", info["url"])


def cmd_labs(a):
    for lab in all_labs():
        when = datetime.datetime.fromtimestamp(lab["updated"]).strftime("%Y-%m-%d") if lab["updated"] else ""
        print("%s  %-44s r%-2s %3d variants  %s%s" % (when, lab["path"].strip("/"), lab["round"], lab["variants"], lab["title"],
                                                       ("  [" + lab["decision"] + "]") if lab["decision"] else ""))


def cmd_list(a):
    data = collect(resolve_lab(a.lab))
    verdicts = data["state"].get("variants", {})
    for v in data["variants"]:
        s = verdicts.get(v["id"], {})
        print("%-5s %-5s r%-2s %-30s %-12s %s" % (s.get("verdict") or "", v["id"], v.get("round", 1), (v.get("name") or "")[:30],
                                                str(v.get("model", ""))[:12], v.get("axis", "")))
        if v.get("duplicate"):
            print("      warning: id %s is also used by %s" % (v["id"], v["duplicate"]))
    for slot in data["slots"]:
        marks = []
        for f in slot["variants"]:
            verdict = verdicts.get("%s:%s" % (slot["id"], f["id"]), {}).get("verdict")
            marks.append(f["id"] + ("(%s)" % verdict if verdict else ""))
        print("slot %s: %s" % (slot["id"], ", ".join(marks) or "empty"))
    picks = data["state"].get("compose") or {}
    if picks:
        print("page mix: " + ", ".join("%s=%s" % kv for kv in picks.items()))


# ---------------------------------------------------------------- checks and screenshots

def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        if not os.path.isabs(c) and shutil.which(c):
            return shutil.which(c)
    return None


def chrome(args, timeout=90):
    exe = find_chrome()
    if not exe:
        raise SystemExit("no Chrome or Chromium found. Use your own browser tool instead.")
    profile = tempfile.mkdtemp(prefix="lab-chrome-")
    try:
        return subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                               "--no-default-browser-check", "--user-data-dir=" + profile] + args,
                              capture_output=True, text=True, timeout=timeout)
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def targets(d, data, a, base):
    ids = set(a.ids.split(",")) if getattr(a, "ids", None) else None
    screens = a.screens.split(",") if getattr(a, "screens", None) else [s["id"] for s in data["lab"].get("screens", [])] or [""]
    for v in data["variants"]:
        if ids and v["id"] not in ids:
            continue
        if getattr(a, "round", None) and str(v.get("round", 1)) != str(a.round):
            continue
        src = v.get("url") or (base + v["file"])
        for scr in screens:
            yield v["id"], scr, src, v
    for slot in data["slots"]:
        for f in slot["variants"]:
            fid = "%s-%s" % (slot["id"], f["id"])
            if ids and fid not in ids:
                continue
            yield fid, "", base + "_page.html?only=%s&picks=%s:%s" % (slot["id"], slot["id"], f["id"]), f


def framed(base_root, url, w, h, check=False):
    return "%s_lab/frame.html?w=%d&h=%d%s&src=%s" % (base_root, w, h, "&check=1" if check else "", urllib.parse.quote(url, safe=""))


def cmd_check(a):
    d = resolve_lab(a.lab)
    info = ensure_server(False)
    root = info["url"]
    base = root.rstrip("/") + lab_path(d)
    data = collect(d)
    widths = [int(w) for w in (a.widths or "1440,390").split(",")]
    expected = data["lab"].get("parts", [])
    problems = 0
    checked = 0
    for vid, scr, src, meta in targets(d, data, a, base):
        if meta.get("external") and not src.startswith(root):
            print("%-34s skipped: lives outside the lab server, check it in the app" % vid)
            continue
        checked += 1
        whole = not src.startswith(base + "_page.html")
        # A baseline can't have parts the new work adds, and lab-meta may list a variant's own parts.
        want = [] if meta.get("baseline") else (meta.get("parts") if isinstance(meta.get("parts"), list) else expected)
        for w in widths:
            q = "labcheck=1" + ("&parts=" + ",".join(want) if want and whole else "")
            url = src + ("&" if "?" in src else "?") + q + ("#" + scr if scr else "")
            h = 844 if w < 700 else 900
            label = "%s%s @%d" % (vid, "#" + scr if scr else "", w)
            issues = None
            # Under load Chrome can cut off requests when its time budget ends, so a load failure gets one retry.
            for attempt in range(2):
                out = chrome(["--window-size=%d,%d" % (max(w, 500), h), "--virtual-time-budget=6000", "--dump-dom",
                              framed(root, url, w, h, check=True)]).stdout
                m = re.search(r'<script type="application/json" id="lab-check">(.*?)</script>', out, re.S)
                issues = json.loads(m.group(1)).get("issues", []) if m else None
                if issues is not None and not any(i.startswith(("failed to load", "image did not load")) for i in issues):
                    break
            if issues is None:
                print("%-34s no report: the page did not load or the lab runtime did not run" % label)
                problems += 1
                continue
            problems += len(issues)
            print("%-34s %s" % (label, "ok" if not issues else ""))
            for i in issues:
                print("    - " + i)
    if not checked:
        raise SystemExit("nothing to check: the lab has no variants or fragments yet")
    print("\n%d issue(s)" % problems)


def theme_args(theme):
    # Headless Chrome follows the Mac's appearance unless told otherwise. 0 is dark and 1 is light.
    return ["--blink-settings=preferredColorScheme=%d" % (0 if theme == "dark" else 1)] if theme in ("light", "dark") else []


def themed(url, theme):
    if theme not in ("light", "dark"):
        return url
    base, _, frag = url.partition("#")
    return withq(base, "labtheme=" + theme) + ("#" + frag if frag else "")


def withq(url, q):
    return url + ("&" if "?" in url else "?") + q


def measure(root, url, w):
    """Document height of url at width w, read through the runtime's check report."""
    out = chrome(["--window-size=%d,900" % max(w, 500), "--virtual-time-budget=6000", "--dump-dom",
                  framed(root, withq(url.partition("#")[0], "labcheck=1") + ("#" + url.partition("#")[2] if "#" in url else ""), w, 900, check=True)]).stdout
    m = re.search(r'<script type="application/json" id="lab-check">(.*?)</script>', out, re.S)
    try:
        return int(json.loads(m.group(1)).get("height") or 0) if m else 0
    except ValueError:
        return 0


def capture(root, url, out, w, h, wait_ms, scale=2, theme=None):
    """Screenshot url at exactly w x h CSS pixels. Narrow widths go through frame.html and a centred crop."""
    url = themed(url, theme)
    if w >= 500:
        chrome(theme_args(theme) + ["--window-size=%d,%d" % (w, h), "--virtual-time-budget=%d" % wait_ms,
                                    "--force-device-scale-factor=%s" % scale, "--screenshot=" + out, url])
    else:
        chrome(theme_args(theme) + ["--window-size=500,%d" % h, "--virtual-time-budget=%d" % wait_ms,
                                    "--force-device-scale-factor=%s" % scale, "--screenshot=" + out, framed(root, url, w, h)])
        if os.path.exists(out) and shutil.which("sips"):
            subprocess.run(["sips", "-c", str(int(h * scale)), str(int(w * scale)), out], capture_output=True)
    return os.path.exists(out)


def cmd_stills(a):
    """Freeze every visible design in every state, so the board can swap states instantly instead of running live frames."""
    d = resolve_lab(a.lab)
    info = ensure_server(False)
    root = info["url"]
    base = root.rstrip("/") + lab_path(d)
    data = collect(d)
    lab = data["lab"]
    skip = set((a.skip or "").split(","))
    screens = [s["id"] for s in lab.get("screens", []) if s["id"] not in skip]
    if not screens:
        raise SystemExit("stills needs screens in lab.json")
    w = a.width or (lab.get("widths") or [1440])[0]
    h = a.height or round(w * 9 / 16)
    out_dir = os.path.join(d, "shots", "stills")
    os.makedirs(out_dir, exist_ok=True)
    wanted = set(a.ids.split(",")) if a.ids else None
    jobs = []
    for v in data["variants"]:
        if (wanted and v["id"] not in wanted) or (not wanted and v.get("old")):
            continue
        src = v.get("url") or (base + v["file"])
        for scr in screens:
            if scr not in v.get("noScreens", []):
                jobs.append((v["id"], scr, src))
    ext = "jpg" if shutil.which("sips") else "png"

    def wait_for(vid, scr):
        # A design that loops needs catching before it restarts: lab.json "stillWait" per state, lab-meta "stillWait" per design.
        meta = next(v for v in data["variants"] if v["id"] == vid)
        return (meta.get("stillWait") or {}).get(scr) or (lab.get("stillWait") or {}).get(scr) or a.wait

    def one(job):
        vid, scr, src = job
        png = os.path.join(out_dir, "%s-%s.tmp.png" % (vid, scr))
        for _ in range(2):
            if capture(root, src + "#" + scr, png, w, h, wait_for(vid, scr), scale=1):
                break
        if not os.path.exists(png):
            return job, False
        final = os.path.join(out_dir, "%s-%s.%s" % (vid, scr, ext))
        if ext == "jpg":
            subprocess.run(["sips", "-Z", str(a.size), "-s", "format", "jpeg", "-s", "formatOptions", "84", png, "--out", final], capture_output=True)
            os.remove(png)
        else:
            os.replace(png, final)
        return job, True

    from concurrent.futures import ThreadPoolExecutor
    have = dict((lab.get("stills") or {}).get("have", {})) if wanted else {}
    for vid in {j[0] for j in jobs}:
        have[vid] = []
    with ThreadPoolExecutor(a.jobs) as pool:
        for (vid, scr, _), ok in pool.map(one, jobs):
            if ok:
                have[vid].append(scr)
            else:
                print("failed: %s %s" % (vid, scr))
    path = os.path.join(d, "lab.json")
    fresh = read_json(path, {})
    fresh["stills"] = {"dir": "shots/stills", "ext": ext, "screens": screens, "have": have, "stamp": datetime.datetime.now().strftime("%H%M%S")}
    write_json(path, fresh)
    print("%d stills in %s" % (sum(len(x) for x in have.values()), out_dir))


def cmd_shoot(a):
    d = resolve_lab(a.lab)
    info = ensure_server(False)
    root = info["url"]
    base = root.rstrip("/") + lab_path(d)
    data = collect(d)
    os.makedirs(os.path.join(d, "shots"), exist_ok=True)
    made = []
    stamp = datetime.datetime.now().strftime("%H%M%S")
    themes = ["light", "dark"] if a.theme == "both" else [a.theme]
    full = a.full or (a.height is None and data["lab"].get("scope") in ("component", "page"))
    for theme in themes:
        tag = "-" + theme if a.theme == "both" else ""
        if a.board:
            out = os.path.join(d, "shots", "board-r%s-%s%s.png" % (a.round or data["lab"].get("round", 1), stamp, tag))
            q = "?shot=1&cols=%d" % (a.cols or 3) + ("&round=%s" % a.round if a.round else "") + ("&view=%s" % a.view if a.view else "")
            q += "&theme=%s" % theme if theme in ("light", "dark") else ""
            if capture(root, base + q, out, a.width or 1800, a.height or 2400, 15000, scale=1.5, theme=theme):
                made.append(out)
            continue
        w = a.width or 1440
        for vid, scr, src, meta in targets(d, data, a, base):
            url = src + ("#" + scr if scr else "")
            h = a.height or (844 if w < 700 else 900)
            if full:
                h = min(max(h, measure(root, url, w)), 16000)
            out = os.path.join(d, "shots", "%s%s-%d%s.png" % (vid, "-" + scr.replace("/", "_") if scr else "", w, tag))
            if capture(root, url, out, w, h, 8000, theme=theme):
                made.append(out)
    for m in made:
        print(m)
    if not made:
        raise SystemExit("no screenshots taken")


def cmd_export(a):
    d = resolve_lab(a.lab)
    out = os.path.abspath(a.outdir)
    if os.path.exists(out) and os.listdir(out):
        raise SystemExit("%s is not empty" % out)
    shutil.copytree(d, out, dirs_exist_ok=True, ignore=shutil.ignore_patterns(
        ".lab", "state.json", "feedback", "FEEDBACK.md", "DECISIONS.md", "BRIEF*.md", "shots", ".tmp-*"))
    lab_copy = read_json(os.path.join(out, "lab.json"), {})
    lab_copy.pop("source", None)
    write_json(os.path.join(out, "lab.json"), lab_copy)
    shutil.copytree(BOARD_DIR, os.path.join(out, "_lab"))
    shutil.copy(os.path.join(BOARD_DIR, "index.html"), os.path.join(out, "index.html"))
    shutil.copy(os.path.join(BOARD_DIR, "page.html"), os.path.join(out, "_page.html"))
    data = collect(d)
    data.pop("dir", None)
    data["lab"].pop("source", None)
    data["state"] = {}
    data["static"] = True
    write_json(os.path.join(out, "lab-data.json"), data)
    for path in glob.glob(os.path.join(out, "variants", "*.html")):
        depth = os.path.relpath(path, out).count(os.sep)
        tag = RUNTIME_TAG.replace('"/_lab/', '"' + "../" * depth + "_lab/")
        with open(path, errors="replace") as f:
            text = f.read()
        if "data-lab-runtime" not in text:
            i = text.lower().rfind("</body>")
            text = text[:i] + tag + text[i:] if i >= 0 else text + tag
            with open(path, "w") as f:
                f.write(text)
    for name in ("index.html", "_page.html"):
        p = os.path.join(out, name)
        with open(p) as f:
            text = f.read()
        with open(p, "w") as f:
            f.write(text.replace('"/_lab/', '"_lab/'))
    print(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("init")
    p.add_argument("lab")
    p.add_argument("--title")
    p.add_argument("--scope", default="concept", choices=["concept", "flow", "component", "page", "system"])
    p.add_argument("--fidelity", default="native", choices=["native", "explore"])
    p.add_argument("--screens", help="id:Label,... hash routes or states every variant implements")
    p.add_argument("--parts", help="data-part names every variant marks")
    p.add_argument("--slots", help="id:Label,... page sections built as swappable fragments")
    p.set_defaults(fn=cmd_init)
    p = sub.add_parser("serve")
    p.add_argument("--port", type=int)
    p.add_argument("--tailnet", action="store_true", help="also listen on this Mac's tailnet address")
    p.add_argument("--foreground", action="store_true")
    p.set_defaults(fn=cmd_serve)
    p = sub.add_parser("url")
    p.add_argument("lab")
    p.add_argument("--tailnet", action="store_true")
    p.set_defaults(fn=cmd_url)
    p = sub.add_parser("stop")
    p.set_defaults(fn=cmd_stop)
    p = sub.add_parser("labs")
    p.set_defaults(fn=cmd_labs)
    p = sub.add_parser("list")
    p.add_argument("lab")
    p.set_defaults(fn=cmd_list)
    p = sub.add_parser("check")
    p.add_argument("lab")
    p.add_argument("--widths")
    p.add_argument("--ids")
    p.add_argument("--screens")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("stills")
    p.add_argument("lab")
    p.add_argument("--ids")
    p.add_argument("--skip", help="comma-separated screens to leave out, such as a live run-through")
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--size", type=int, default=1600, help="longest side of the saved image")
    p.add_argument("--wait", type=int, default=16000, help="virtual ms to let each state settle")
    p.add_argument("--jobs", type=int, default=6)
    p.set_defaults(fn=cmd_stills)
    p = sub.add_parser("shoot")
    p.add_argument("lab")
    p.add_argument("--ids")
    p.add_argument("--round")
    p.add_argument("--screens")
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--cols", type=int)
    p.add_argument("--view", help="board view for --board: grid, parts, flow or mix")
    p.add_argument("--theme", default="light", choices=["light", "dark", "both", "auto"],
                   help="colour scheme for the shots. auto follows this Mac's appearance")
    p.add_argument("--full", action="store_true", help="capture each variant's whole height. Default for component and page labs")
    p.add_argument("--board", action="store_true", help="one contact sheet of the whole board")
    p.set_defaults(fn=cmd_shoot)
    p = sub.add_parser("export")
    p.add_argument("lab")
    p.add_argument("outdir")
    p.set_defaults(fn=cmd_export)
    p = sub.add_parser("project")
    p.set_defaults(fn=lambda a: print(slugify(project_name())))
    a = ap.parse_args()
    if not getattr(a, "fn", None):
        ap.print_help()
        return
    a.fn(a)


if __name__ == "__main__":
    main()
