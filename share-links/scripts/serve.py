#!/usr/bin/env python3
"""Serve the share root read-only on 127.0.0.1.

launchd keeps this running and `tailscale serve` puts it on the tailnet over HTTPS. Paths with a
segment that starts with a dot, and symlinks that lead out of the root, return 404. That keeps
`.env` files, `.git` folders and `share`'s staging folder private. Files answer byte-range requests,
since Safari on iOS won't play a video without them.
"""
import html
import http.server
import io
import os
import re
import sys
import urllib.parse

sys.dont_write_bytecode = True  # Keep __pycache__ out of the skill folder.
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common import config  # noqa: E402


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".json": "application/json",
        ".wasm": "application/wasm",
        ".svg": "image/svg+xml",
        ".webmanifest": "application/manifest+json",
    }
    remaining = None  # Bytes left to send for a range request, or None for the whole file.

    def send_head(self):
        url_path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        if any(part.startswith(".") for part in url_path.split("/") if part):
            self.send_error(404)
            return None
        root = os.path.realpath(self.directory)
        real = os.path.realpath(self.translate_path(self.path))
        # Where a symlink leads counts too: outside the root, or to a dot name inside it.
        if os.path.commonpath([root, real]) != root or any(
                part.startswith(".") for part in os.path.relpath(real, root).split(os.sep) if part != "."):
            self.send_error(404)
            return None
        self.remaining = None
        match = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers.get("Range", "").strip())
        if not match or not os.path.isfile(real) or match.groups() == ("", ""):
            return super().send_head()
        f = open(real, "rb")
        size = os.fstat(f.fileno()).st_size
        first, last = match.groups()
        if first:
            start, end = int(first), min(int(last), size - 1) if last else size - 1
        else:
            start, end = max(size - int(last), 0), size - 1  # "bytes=-500" is the last 500 bytes.
        if start > end or start >= size:
            f.close()
            self.send_response(416)
            self.send_header("Content-Range", "bytes */%d" % size)
            self.end_headers()
            return None
        f.seek(start)
        self.remaining = end - start + 1
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(real))
        self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.send_header("Content-Length", str(self.remaining))
        self.end_headers()
        return f

    def copyfile(self, source, outputfile):
        if self.remaining is None:
            return super().copyfile(source, outputfile)
        while self.remaining > 0:
            chunk = source.read(min(64 * 1024, self.remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            self.remaining -= len(chunk)

    def list_directory(self, path):
        names = sorted(n for n in os.listdir(path) if not n.startswith("."))
        rows = []
        for name in names:
            label = name + "/" if os.path.isdir(os.path.join(path, name)) else name
            rows.append('<li><a href="%s">%s</a></li>' % (urllib.parse.quote(label), html.escape(label)))
        title = html.escape(urllib.parse.unquote(self.path.split("?")[0]))
        body = (
            '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
            "<title>%s</title><h1>%s</h1><ul>%s</ul>" % (title, title, "".join(rows) or "<li>Nothing shared yet.</li>")
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return io.BytesIO(body)

    def end_headers(self):
        # A re-shared name replaces its files, so the browser must not keep the old ones.
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def log_message(self, format, *args):
        pass


class Server(http.server.ThreadingHTTPServer):
    request_queue_size = 128


def main():
    cfg = config()
    os.makedirs(cfg["root"], exist_ok=True)
    handler = lambda *a, **kw: Handler(*a, directory=cfg["root"], **kw)  # noqa: E731
    with Server(("127.0.0.1", cfg["port"]), handler) as server:
        print("serving %s on http://127.0.0.1:%d/" % (cfg["root"], cfg["port"]), flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
