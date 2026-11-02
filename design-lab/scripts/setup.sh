#!/bin/sh
# Gets this machine ready to host what design-lab shows: share links and video. Safe to run again.
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"
SHARE_LINKS="$HOME/.claude/skills/share-links"

if ! command -v share >/dev/null 2>&1; then
  if [ "$(uname)" != "Darwin" ]; then
    echo "share-links only installs on a Mac. Host files some other way on this machine."
  else
    if [ ! -f "$SHARE_LINKS/scripts/install.py" ]; then
      echo "Fetching share-links from Willayam/skills"
      tmp=$(mktemp -d)
      git clone --quiet --depth 1 https://github.com/Willayam/skills "$tmp/skills" || { echo "Could not fetch share-links."; rm -rf "$tmp"; exit 1; }
      skills="$HOME/.agents/skills"
      [ -d "$skills" ] || skills="$HOME/.claude/skills"
      mkdir -p "$skills"
      cp -R "$tmp/skills/share-links" "$skills/share-links"
      rm -rf "$tmp"
      for dir in "$HOME/.claude/skills" "$HOME/.codex/skills"; do
        if [ -d "$dir" ] && [ ! -e "$dir/share-links" ]; then ln -s "$skills/share-links" "$dir/share-links"; fi
      done
    fi
    /usr/bin/python3 "$SHARE_LINKS/scripts/install.py" --share-only
  fi
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then
    brew install ffmpeg
  else
    echo "ffmpeg is missing and Homebrew isn't installed. Install ffmpeg to ~/.local/bin to record video."
  fi
fi

for tool in share ffmpeg node; do
  printf '%-7s %s\n' "$tool" "$(command -v "$tool" || echo missing)"
done
