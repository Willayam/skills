"""Paths, ports and config shared by the share-links scripts. Standard library only, Python 3.9+."""
import json
import os

HOME = os.path.expanduser("~")
SCRIPTS = os.path.dirname(os.path.realpath(__file__))
CONFIG = os.path.join(HOME, ".config/share-links/config.json")
LOGS = os.path.join(HOME, "Library/Logs/share-links")

DEFAULTS = {
    "root": os.path.join(HOME, "shared"),
    "port": 4860,
    "https_port": 8446,
    "origin": None,
    # Ports of servers launchd or tailscale serve keep running. A link to any other local port dies.
    "durable_ports": [4860, 8446, 4870],
}


def config():
    cfg = dict(DEFAULTS)
    try:
        with open(CONFIG) as f:
            cfg.update(json.load(f))
    except (OSError, ValueError):
        pass
    return cfg


def local_origin(cfg):
    return "http://127.0.0.1:%d" % cfg["port"]
