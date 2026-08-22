#!/bin/sh
# Blockt Commits mit echten Zugangsdaten. Prüft nur gestagte Dateien.
# ponytail: grep statt gitleaks; gitleaks nachrüsten, wenn das hier mal durchrutscht.
cd "$(git rev-parse --show-toplevel)" || exit 1
files=$(git diff --cached --name-only --diff-filter=ACM | grep -v -E '\.example\.|^tools/(check-secrets|test-check-secrets)\.sh$|^docs/relic/' || true)
[ -z "$files" ] && exit 0
pattern='(ssid|password|passwd|token|api[_-]?key|secret)[[:space:]]*[=:][[:space:]]*["'"'"']?[A-Za-z0-9_./@!$%+-]{8,}'
hits=$(printf '%s\n' "$files" | xargs grep -n -i -E "$pattern" 2>/dev/null \
  | grep -v -i -E 'changeme|example|platzhalter|your[_-]|<[^>]+>|\$\{|\$[A-Z_]+|process\.env|getenv|xxxx' || true)
if [ -n "$hits" ]; then
  echo "check-secrets: mögliche Zugangsdaten — Commit abgebrochen:"
  echo "$hits"
  exit 1
fi
exit 0
