#!/bin/sh
# Claude-Code-Hook SessionEnd: Endzeit + Dauer eintragen, dauer_min summieren, committen und pushen.
# ponytail: Sessions über Mitternacht werden dem Starttag zugerechnet und negative Dauer auf 0 gesetzt.
root="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
day="$(date +%Y-%m-%d)"; now="${FAKE_NOW:-$(date +%H:%M)}"
log="$root/vault/Log/$day.md"
[ -f "$log" ] || sh "$root/tools/session-start.sh"
start="$(grep -E '^- start [0-9]{2}:[0-9]{2}$' "$log" | tail -1 | awk '{print $3}')"
mins() { echo "$1" | awk -F: '{print $1*60+$2}'; }
dur=$(( $(mins "$now") - $(mins "$start") )); [ "$dur" -lt 0 ] && dur=0
printf -- '- ende %s (%s min)\n' "$now" "$dur" >> "$log"
total="$(grep -oE '\([0-9]+ min\)' "$log" | tr -dc '0-9\n' | awk '{s+=$1} END{print s+0}')"
sed -i '' "s/^dauer_min: .*/dauer_min: $total/" "$log"
[ -n "$NO_GIT" ] && exit 0
cd "$root" || exit 0
git add -A
sh tools/check-secrets.sh || { echo "session-end: Secrets gefunden, kein Commit" >> "$log"; exit 0; }
summary="$(awk '/^## Was ist passiert/{f=1;next} /^## /{f=0} f && /^- ./{sub(/^- /,""); print; exit}' "$log")"
git commit -q -m "Session $day $now: ${summary:-Arbeitsstand}" || exit 0
git push -q origin HEAD 2>>"$root/vault/Log/push-fehler.log" || true
exit 0
