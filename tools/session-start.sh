#!/bin/sh
# Claude-Code-Hook SessionStart: Tagesblatt anlegen (falls neu) und Startzeit eintragen.
root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
day="$(date +%Y-%m-%d)"; now="${FAKE_NOW:-$(date +%H:%M)}"
log="$root/vault/Log/$day.md"
mkdir -p "$(dirname "$log")"
if [ ! -f "$log" ]; then
  printf -- '---\ndatum: %s\ndauer_min: 0\n---\n# %s\n\n## Was ist passiert\n- \n\n## Sessions\n' "$day" "$day" > "$log"
fi
printf -- '- start %s\n' "$now" >> "$log"
exit 0
