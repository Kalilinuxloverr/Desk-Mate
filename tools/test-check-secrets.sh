#!/bin/sh
# Einziger Test für check-secrets.sh: ein echtes Secret muss blocken, ein Platzhalter nicht.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
cd "$tmp" && git init -q -b main && git config user.email t@t && git config user.name t
cp "$here/check-secrets.sh" .

printf 'password = "hunter2hunter2"\n' > leak.txt && git add leak.txt
if sh check-secrets.sh >/dev/null 2>&1; then echo "FAIL: Secret nicht erkannt"; exit 1; fi
git rm -q --cached leak.txt

printf 'password = "CHANGEME"\nmqtt_token: ${MQTT_TOKEN}\n' > ok.example.h && git add ok.example.h
printf 'Gerätetokens liegen in Supabase. Kein Token hier.\n' > doku.md && git add doku.md
sh check-secrets.sh || { echo "FAIL: Platzhalter/Doku fälschlich geblockt"; exit 1; }
echo "OK: check-secrets"
