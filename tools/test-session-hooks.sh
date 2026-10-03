#!/bin/sh
# Start legt Tagesblatt an, Ende rechnet Minuten und summiert dauer_min. Kein git im Test (NO_GIT=1).
set -e
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
export CLAUDE_PROJECT_DIR="$tmp" NO_GIT=1 FAKE_NOW="09:00"
sh "$here/session-start.sh"
log="$tmp/vault/Log/$(date +%Y-%m-%d).md"
grep -q '^- start 09:00$' "$log" || { echo "FAIL: start fehlt"; exit 1; }
FAKE_NOW="10:30" sh "$here/session-end.sh"
grep -q '^- ende 10:30 (90 min)$' "$log" || { echo "FAIL: ende/minuten"; cat "$log"; exit 1; }
grep -q '^dauer_min: 90$' "$log" || { echo "FAIL: dauer_min"; cat "$log"; exit 1; }
FAKE_NOW="11:00" sh "$here/session-start.sh"; FAKE_NOW="11:10" sh "$here/session-end.sh"
grep -q '^dauer_min: 100$' "$log" || { echo "FAIL: Summe"; cat "$log"; exit 1; }
# Über Mitternacht: Start 23:50 im Blatt vom Vortag, heute noch kein Blatt -> Ende landet beim Starttag.
mkdir -p "$tmp/mn/vault/Log"; old="$tmp/mn/vault/Log/2000-01-01.md"
printf -- '---\ndatum: 2000-01-01\ndauer_min: 0\n---\n## Sessions\n- start 23:50\n' > "$old"
CLAUDE_PROJECT_DIR="$tmp/mn" FAKE_NOW="00:20" sh "$here/session-end.sh"
grep -q '^- ende 00:20 (30 min)$' "$old" || { echo "FAIL: Mitternacht"; cat "$old"; exit 1; }
[ ! -f "$tmp/mn/vault/Log/$(date +%Y-%m-%d).md" ] || { echo "FAIL: leeres Blatt fuer heute angelegt"; exit 1; }
echo "OK: session-hooks"
