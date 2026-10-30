---
name: share-links
description: Give the user links that still work hours later, from any device. Use before putting a localhost, 127.0.0.1, LAN or tailnet link in a reply, to share a page, build, mockup or screenshot, and to set up or debug the share server, the design-lab server, the release of settled worktrees' processes or the link-check hook on a Mac.
---

# Share links

The user opens links hours later, often from their phone. By then a dev server is gone. T3 ends an
idle agent session after 30 minutes, or 4 hours if a background task is running, and the session's
background tasks end with it. Agents stop their own servers when they finish checking. T3 deletes
the worktree once the thread settles, and nothing restarts a server after a reboot.

So never link a dev server port. Link one of these instead.

| What | How | Link |
|---|---|---|
| A built page, HTML file, mockup, image or video | `share <file-or-folder>` | The first line it prints |
| A design lab | `lab.py url <lab> --tailnet` | The tailnet line |
| A page that needs its backend | The project's preview deploy, if it has one | The preview URL |

`share` copies into `~/shared/<project>/<name>/` and prints an HTTPS tailnet URL that works on
every device. The copy outlives the session, the worktree and a reboot. Every share gets its own
URL, so an earlier link keeps showing what it showed. A taken name becomes `name-2`, then `name-3`.
The project comes from the repository and the name from the file or folder. A generic build folder
like `dist` takes the branch name. Pass `--name` to choose one, and `--replace` to overwrite a name
instead.

```bash
bun run build -- --base ./ && share dist            # a Vite app, built with relative asset paths
share variants/ --name accounts-options              # a folder of mockups
share /tmp/shot.png                                  # one file
```

A build served under `/<project>/<name>/` needs relative asset paths. For Vite, build with
`--base ./`. Client-side routes beyond the first page won't resolve, so link the entry page.

When a page only works against a live backend and the project has no preview deploy, say so in
the reply. Give the command that starts it and attach a screenshot. Don't post the bare address.

Files and folders whose names start with a dot are never served, and neither are symlinks that
point outside `~/shared`. `share` skips `.git` and `node_modules`.

## The link check

`scripts/check_links.py` is a Stop hook for Claude Code and Codex. When a final reply links this
Mac, the LAN or the tailnet on a port that doesn't stay up, the hook sends the reply back once with
instructions. The second attempt always goes through, so a link kept on purpose survives. Code
blocks and inline code don't count. A loopback link like 127.0.0.1 always goes back, because it
won't open on the phone. The installer fills `durable_ports` in `~/.config/share-links/config.json`
from the share server, the design-lab server and whatever `tailscale serve` exposes. Add your own
under `extra_ports`, which reinstalling keeps.

## Settled worktrees free their ports

`scripts/release.py` runs every five minutes. It stops processes left running in T3 worktrees
whose threads are all settled, archived or deleted, and in worktrees whose folder is gone. It only
stops orphans, meaning processes no app, terminal multiplexer, ssh session, launchd job or agent
runtime owns. A dev server started with `nohup` or `( ... &)` is an orphan. A live session's own
processes are left for T3 to end with the session. Run it without `--apply` to see what it would
stop. Kills are logged in `~/Library/Logs/share-links/release.log`.

Once those processes are gone, the scheduled `t3-worktree-cleanup` run can remove the worktree.

## Set up on a Mac

```bash
python3 ~/.claude/skills/share-links/scripts/install.py
```

The installer is safe to run again. It sets up:
- a LaunchAgent serving `~/shared` on 127.0.0.1:4860
- `tailscale serve` on HTTPS 8446
- a LaunchAgent keeping the design-lab server on port 4870, when that skill is installed
- the release LaunchAgent
- `share` in `~/.local/bin`
- the Stop hook in `~/.claude/settings.json` and `~/.codex/hooks.json`

Codex runs a new hook only after you trust it once in its `/hooks` screen. Run the installer again
after moving this folder. `install.py --uninstall` removes everything except `~/shared`.
