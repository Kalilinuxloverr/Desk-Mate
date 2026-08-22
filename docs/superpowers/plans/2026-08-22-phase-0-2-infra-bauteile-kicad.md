# Desk-Mate — Plan Phase 0–2: Infrastruktur · Bauteilwahl · KiCad bis JLCPCB-Bestellung

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repo mit automatischer Doku/Zeiterfassung/Push steht, die Stückliste ist gegen Leons Bestand abgeglichen und bestellt, und drei KiCad-Designs (Mainboard, Frontpanel, Augen-Adapter) sind ERC/DRC-sauber als eine JLCPCB-Bestellung abgeschickt.

**Architecture:** Drei Through-Hole-Platinen um einen gesteckten ESP32-S3-DevKitC-1; alle Intelligenz im S3, Tasten/Touch über I²C-Expander auf dem Frontpanel, Motortreiber als Breakouts auf dem Mainboard. Doku lebt im Repo (`vault/` = Obsidian), Arbeitszeit und Push laufen über Claude-Code-Session-Hooks.

**Tech Stack:** git + gh (Kalilinuxloverr/Desk-Mate) · KiCad 10 (`/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` für ERC/DRC/Export) · arduino-cli (ab Phase 3) · sh-Skripte ohne Abhängigkeiten · Obsidian.

**Spec:** `docs/superpowers/specs/2026-08-22-desk-mate-design.md`

## Global Constraints

- Eine JLCPCB-Bestellung, kein Re-Spin: jede Platine wird vor Gerber-Export gegen Spec §2.2–2.5 geprüft.
- Kein Hand-SMD: nur THT-Bauteile oder gesteckte Breakouts/Module.
- Ein ESP32-S3 DevKitC-1 N16R8, gesteckt; Pin-Map exakt nach Spec §2.3 (Schleifer nur ADC1 GPIO 1–10; 0/3/45/46 nie als Funktion außer 45 per Lötjumper; 19/20 USB; 26–37 tabu; 43/44 frei lassen).
- Sprache: Doku/Commits/Kommentare Deutsch, Bezeichner/Netznamen/JSON Englisch. Commits: Satzform, ergebnisorientiert, kein Präfix.
- Secrets nie im Repo: `secrets.h`, `.env`, `*.local.xcconfig` in `.gitignore`; `tools/check-secrets.sh` muss vor jedem Commit grün sein.
- Jede Session: Tagesblatt `vault/Log/YYYY-MM-DD.md` → Abschnitt „Was ist passiert“ ergänzen (Pflicht laut CLAUDE.md).
- Jede Task endet mit Commit. Pfade relativ zu `/Users/leonfrohlich/Claude/Projects/Desk-Mate`.

---

## Phase 0 — Infrastruktur (2026-08-22, Nacht)

### Task 1: Repo-Grundgerüst (git, .gitignore, LICENSE, README, CLAUDE.md)

**Files:**
- Create: `.gitignore`, `LICENSE`, `README.md`, `CLAUDE.md`
- Existing: `docs/relic/2026-08-22-original-prompt.md`, `docs/superpowers/specs/2026-08-22-desk-mate-design.md`, dieser Plan

**Interfaces:**
- Produces: Repo-Root als `$CLAUDE_PROJECT_DIR`; `CLAUDE.md` definiert Session-Pflichten, auf die Task 3 und 4 verweisen.

- [ ] **Step 1: git init mit Branch `main`**

```bash
cd /Users/leonfrohlich/Claude/Projects/Desk-Mate && git init -b main
```
Erwartung: `Initialized empty Git repository`.

- [ ] **Step 2: `.gitignore` schreiben**

```gitignore
# Secrets — nie committen (Kühler-Lektion: Passwörter im Initial-Commit)
secrets.h
**/secrets.h
.env
.env.*
*.local.xcconfig
Signing.local.xcconfig

# Obsidian: nur Konfiguration versionieren, nicht Arbeitszustand
vault/.obsidian/workspace*
vault/.obsidian/cache
vault/.trash/

# KiCad
*-backups/
*.kicad_prl
*.kicad_sch-bak
*.kicad_pcb-bak
_autosave-*
fp-info-cache
*.lck

# Build / Tools
build/
.build/
DerivedData/
*.xcodeproj
*.xcworkspace
.history/
__pycache__/
*.pyc
node_modules/
.vercel/

# macOS
.DS_Store
```

- [ ] **Step 3: LICENSE (MIT, Jahr 2026, Leon Fröhlich)** — Hardware-Lizenz (CERN-OHL-P) ist Leons Entscheidung, offener Punkt im Spec §8.

- [ ] **Step 4: README.md nach Leons Template** (H1 → Was → ASCII-Architektur → Pfadtabelle → Bauen). Inhalt: Kurzbeschreibung aus Spec-Einleitung, ASCII aus Spec §2.1, Pfadtabelle aus Spec §6, „Bauen“ vorerst nur `git config core.hooksPath tools/githooks` und `sh tools/test-check-secrets.sh` (weitere Build-Befehle kommen mit den Phasen dazu).

- [ ] **Step 5: CLAUDE.md** mit Abschnitten: Projekt (1 Absatz + Links Spec/Plan/Relikt) · Architektur (Kurzform Spec §2–5) · Build & Test (aktuell: Secret-Check-Test; Platzhalterfrei: nur Befehle, die existieren) · **Bekannte Fallen (teuer erkauft — nicht wieder reintappen!)** (Startbestand aus dem Kühler-Log, soweit auf S3/Desk-Mate übertragbar: ADC2+WiFi, `WiFi.setSleep(false)`, NimBLE, `.ino`-Prototyp-Fallen, Struct-Änderung = Protokollversion, Secrets im Initial-Commit, UART-Baud/Puffer-Lektion aus VVVF) · Konventionen (Sprache, Commits, Dateinamen, Pin-Map ist im Spec die einzige Wahrheit bis `firmware/.../pins.h` existiert) · **Session-Pflichten** (Tagesblatt pflegen, Entscheidungen in `vault/Entscheidungen/`, Bestellungen in `vault/Bestellungen/`, Relikt nie anfassen, vor „fertig“ Tests laufen lassen, Memory ist kein Ersatz für den Vault).

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "Projektstart Desk-Mate: Spec, Plan, Relikt, README, CLAUDE.md"
```

### Task 2: Secret-Check als Pre-Commit-Hook (mit Test)

**Files:**
- Create: `tools/check-secrets.sh`, `tools/githooks/pre-commit`, `tools/test-check-secrets.sh`

**Interfaces:**
- Produces: `tools/check-secrets.sh` — Exit 0 = sauber, Exit 1 = Fund (Ausgabe: Datei:Zeile). Prüft nur gestagte Dateien. Wird von Task 3 (`session-end.sh`) aufgerufen.

- [ ] **Step 1: Test schreiben** (`tools/test-check-secrets.sh`)

```sh
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
```

- [ ] **Step 2: Test laufen lassen → muss fehlschlagen** (`sh tools/test-check-secrets.sh` → „check-secrets.sh: No such file“).

- [ ] **Step 3: `tools/check-secrets.sh`**

```sh
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
```

- [ ] **Step 4: Pre-Commit-Hook** (`tools/githooks/pre-commit`)

```sh
#!/bin/sh
exec sh "$(git rev-parse --show-toplevel)/tools/check-secrets.sh"
```

- [ ] **Step 5: ausführbar machen, Hook-Pfad setzen, Test grün**

```bash
chmod +x tools/*.sh tools/githooks/pre-commit
git config core.hooksPath tools/githooks
sh tools/test-check-secrets.sh
```
Erwartung: `OK: check-secrets`.

- [ ] **Step 6: Commit** — `git add tools && git commit -m "Secret-Check als Pre-Commit-Hook, mit Test"`

### Task 3: Zeiterfassung + Auto-Push über Claude-Code-Session-Hooks

**Files:**
- Create: `tools/session-start.sh`, `tools/session-end.sh`, `.claude/settings.json`, `tools/test-session-hooks.sh`

**Interfaces:**
- Consumes: `tools/check-secrets.sh` (Task 2).
- Produces: Tagesblatt-Format `vault/Log/YYYY-MM-DD.md`:
  ```
  ---
  datum: 2026-08-23
  dauer_min: 0
  ---
  # 2026-08-23

  ## Was ist passiert
  - 

  ## Sessions
  - start 09:12
  - ende 10:40 (88 min)
  ```
  Claude schreibt Bullet-Punkte unter „Was ist passiert“; der erste nicht-leere wird Commit-Betreff.

- [ ] **Step 1: Test** (`tools/test-session-hooks.sh`)

```sh
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
echo "OK: session-hooks"
```

- [ ] **Step 2: Test laufen lassen → fehlschlägt** (Skripte fehlen).

- [ ] **Step 3: `tools/session-start.sh`**

```sh
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
```

- [ ] **Step 4: `tools/session-end.sh`**

```sh
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
```

- [ ] **Step 5: `.claude/settings.json`**

```json
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup|resume|clear",
        "hooks": [ { "type": "command", "command": "sh \"$CLAUDE_PROJECT_DIR/tools/session-start.sh\"", "timeout": 10 } ] }
    ],
    "SessionEnd": [
      { "hooks": [ { "type": "command", "command": "sh \"$CLAUDE_PROJECT_DIR/tools/session-end.sh\"", "timeout": 120 } ] }
    ]
  }
}
```

- [ ] **Step 6: Test grün** — `chmod +x tools/*.sh && sh tools/test-session-hooks.sh` → `OK: session-hooks`.

- [ ] **Step 7: Commit** — `git add tools .claude && git commit -m "Zeiterfassung und Auto-Push ueber Session-Hooks, mit Test"`

### Task 4: Obsidian-Vault anlegen und heutige Session dokumentieren

**Files:**
- Create: `vault/Index.md`, `vault/Log/2026-08-22.md`, `vault/Entscheidungen/2026-08-22-Grilling.md`, `vault/Hardware/Pin-Map.md`, `vault/Apps/Claude-Hooks.md`, `vault/Bestellungen/README.md`, `vault/.obsidian/app.json`

- [ ] **Step 1: Struktur + Index** — `Index.md` mit Wikilinks auf alle Bereiche und auf Spec/Plan/Relikt (relative Markdown-Links, da außerhalb des Vaults).
- [ ] **Step 2: Tagesblatt 2026-08-22 von Hand** (Start 21:29 — Hook existierte noch nicht): „Was ist passiert“ = Grilling 18 Fragen, Spec, Plan, Infrastruktur; Sessions `- start 21:29` / `- ende HH:MM (N min)` mit echter Uhrzeit, `dauer_min` passend.
- [ ] **Step 3: Entscheidungsnotiz** — die 18 Fragen mit Optionen, Antwort, Begründung (aus dem Chat), je Abschnitt `[[…]]`-Links auf Hardware/Firmware/Apps-Notizen.
- [ ] **Step 4: `Hardware/Pin-Map.md`** — verweist auf Spec §2.3 als einzige Wahrheit bis Task 7 die verifizierte Version hier ablegt.
- [ ] **Step 5: `Apps/Claude-Hooks.md`** — verifizierte Hook-Fakten (Ereignisliste, `PermissionRequest`-Antwort-JSON, Notification-Typen, offene Punkte Timeout/AskUserQuestion), Quelle + Datum.
- [ ] **Step 6: `Bestellungen/README.md`** — Vorlage je Bestellung (Datum, Lieferant, Positionen, Kosten, Lieferzeit, Tracking, Fotos, Sponsoring-Hinweis).
- [ ] **Step 7: Commit** — `git add vault && git commit -m "Obsidian-Vault mit Tagesblatt, Entscheidungen und Hook-Fakten"`

### Task 5: Logo

**Files:**
- Create: `docs/logo/deskmate.svg`, `docs/logo/README.md`

- [ ] **Step 1: SVG** — 256×256, abgerundetes Quadrat (Körper) in Anthrazit, zwei runde Augen (weiß, Pupille türkis #2EC4B6), darunter ein Ampel-Punkt (grün #3DDC84). Nur Pfade/Kreise, keine Schrift, keine externen Fonts. Wortmarke „Desk-Mate“ separat als Text-SVG `deskmate-wordmark.svg` (Systemfont, da Logo-Fonts Lizenzfragen bringen).
- [ ] **Step 2: Sichtprüfung** — `qlmanage -p docs/logo/deskmate.svg` oder im Browser öffnen; README im Vault verlinkt das SVG.
- [ ] **Step 3: Commit** — `git add docs/logo && git commit -m "Logo als SVG"`

### Task 6: GitHub-Repo anlegen und pushen

- [ ] **Step 1:** `gh repo create Kalilinuxloverr/Desk-Mate --public --source=. --remote=origin --description "Wall-E-artiger Schreibtisch-Begleiter: Ampel fuer Claude Code & Downloads, Motorfader, Augen-Displays. ESP32-S3, Swift, KiCad, 3D-Druck." --push`
- [ ] **Step 2:** `git remote -v` zeigt `https://github.com/Kalilinuxloverr/Desk-Mate.git`; `gh repo view --web` optional.
- [ ] **Step 3:** Tagesblatt-Eintrag „Repo öffentlich, erster Push“ — Commit über `tools/session-end.sh` ist ab der nächsten Session automatisch.

---

## Phase 1 — Bauteilwahl (ab 2026-08-23)

### Task 7: Pin-Map verifizieren und als `pins.h` festschreiben

**Files:**
- Create: `firmware/arduino/deskmate/pins.h`, `vault/Hardware/Pin-Map.md` (ersetzt Verweis), `tools/test-pins.sh`

**Interfaces:**
- Produces: `pins.h` mit `constexpr int PIN_<NAME> = <gpio>;` für alle Einträge aus Spec §2.3 (Namen exakt wie dort: `PIN_FADER1_WIPER`, `PIN_FADER1_PWM`, `PIN_FADER1_DIR`, …, `PIN_SERVO_PAN`, `PIN_SERVO_TILT`, `PIN_SPI_MOSI`, `PIN_SPI_SCK`, `PIN_SPI_DC`, `PIN_CS_BELLY`, `PIN_CS_EYE_L`, `PIN_CS_EYE_R`, `PIN_I2C_SDA`, `PIN_I2C_SCL`, `PIN_IO_INT`, `PIN_WS2812_DATA`, `PIN_PSU_SENSE`, `PIN_BELLY_BL_PWM`). Alle Phase-3-Module greifen nur hierüber auf GPIOs zu.

- [ ] **Step 1: Quellen lesen** — ESP32-S3-Datenblatt (Strapping-Tabelle, ADC-Kanäle, GPIO 45/46/48-Verhalten) und ESP32-S3-DevKitC-1-Schaltplan (Espressif-Doku; Onboard-RGB-LED-Pin je Revision, welche Pins am Header liegen, USB-Pfad). Über WebFetch/Context7, Fundstellen mit URL in `vault/Hardware/Pin-Map.md` notieren.
- [ ] **Step 2: Abgleich** — jede Zeile aus Spec §2.3 gegen die Quellen: Pin am Header? Strapping? ADC1? Konflikt mit PSRAM (N16R8 = Octal → 35/36/37 belegt)? Ergebnis-Tabelle mit Spalte „verifiziert ✓/✗ + Quelle“. Abweichungen → Spec §2.3 anpassen (Spec bleibt Wahrheit) und Grund ins Tagesblatt.
- [ ] **Step 3: Test** (`tools/test-pins.sh`): prüft per `grep`/`awk`, dass in `pins.h` keine GPIO-Nummer doppelt ist, keine aus {0,3,19,20,26–37,43,44,46} vorkommt, `PIN_FADER*_WIPER` ∈ 1–10, und `PIN_BELLY_BL_PWM` nur mit Kommentar `// Loetjumper` erscheint. Vorher laufen lassen → fehlschlägt (Datei fehlt).
- [ ] **Step 4: `pins.h` schreiben** (ein `constexpr` pro Zeile, Kommentar mit Ziel/Hinweis aus der Tabelle).
- [ ] **Step 5: Test grün**, Commit: `Pin-Map gegen Datenblatt und DevKitC-1-Schaltplan verifiziert, pins.h`

### Task 8: Bestandsaufnahme Arduino-Box → `hardware/inventar.md`

- [ ] **Step 1:** Leon fotografiert/listet die Box (nach dem Urlaub). Claude legt `hardware/inventar.md` an: Tabelle `Bauteil | Anzahl | Zustand | Verwendbar für`.
- [ ] **Step 2:** Bekannt vorhanden eintragen: BME680-Breakout, WS2812-Breakout, C3 SuperMini (×?), CYD.
- [ ] **Step 3:** Commit.

### Task 9: Stückliste `hardware/bom.md` (Leons Format) mit Quellen, Preisen, Bestand

**Files:**
- Create: `hardware/bom.md`, `vault/Bestellungen/2026-08-xx-teile.md`

**Interfaces:**
- Produces: BOM-Tabelle `Ref | Bauteil | Gehäuse | Hinweis | Stück | Quelle | Preis | Bestand` — Referenzen (J1, U1, …) werden in Task 11–14 1:1 als KiCad-Referenzen verwendet.

- [ ] **Step 1: Kandidaten je Position mit Begründung** (Skill `bom` laden; Preise/Verfügbarkeit per WebFetch bei Reichelt/Mouser/AliExpress/Amazon.de, Stand mit Datum):
  - ESP32-S3-DevKitC-1-N16R8 (Espressif-Original bevorzugen, Revision notieren)
  - 2× Behringer MF60T (5er-Pack), 2× DRV8833-Breakout (Pololu-kompatibel, 2 Kanäle)
  - 2× GC9A01 1,28" (7-Pin-Modul), 1× ILI9341 2,8" SPI 14-Pin ohne Touch
  - 2× MG90S, Pan-Tilt-Halter (Druckteil oder Kit)
  - MCP23017 DIP-28 (+ Sockel), MPR121-Breakout, BME680 (vorhanden)
  - 10× MX-Schalter (Outemu/Gateron), 10× Hot-Swap-Sockel (Kailh, falls Footprint THT-tauglich — sonst direkt löten), 10× Blank-Keycaps DSA
  - EC11 mit Taster + Knopf
  - 2× USB-C-Buchse 16-Pin THT-Befestigung (z. B. GCT USB4085-GF-A oder kompatibel), 2× 5,1 kΩ
  - Versorgung: 2× P-FET TO-220 (z. B. IRF9540N-Alternative mit niedrigem Rds(on); oder 1× Dual-Schottky SB540-Paar) — Entscheidung hier treffen und im Spec §8 Punkt 3 schließen
  - LD1117V33 TO-220, Polyfuse 3 A (RUEF300), Elkos 1000 µF ×2, 470 µF, 100 µF ×2, 100 nF ×10, 10 µF ×4
  - IDC 2×15 Stift + Buchse + Flachband 30-polig (30 cm), JST-XH 3-Pin ×3 + Kabel
  - WS2812-Ring 12 (vorhanden prüfen), Buchsenleisten 1×22 ×2, 1×8 ×4, Stiftleisten
  - USB-C-Kabel, 5 V/3 A USB-C-Netzteil
- [ ] **Step 2: Gegen `inventar.md` abgleichen**, Spalte Bestand füllen; Gesamtkosten summieren.
- [ ] **Step 3: Bestellliste** je Lieferant als `vault/Bestellungen/<datum>-<lieferant>.md` (Vorlage aus Task 4). Leon bestellt; Claude trägt Bestelldatum/Tracking nach.
- [ ] **Step 4: Commit** — `Stueckliste mit Quellen und Preisen, Bestand abgeglichen`

### Task 10: Offene Spec-Punkte schließen (USB-Datenpfad, HiveMQ-Limit, Lizenz)

- [ ] **Step 1: USB-Datenpfad** — Schaltplan des DevKitC-1 lesen: liegen D+/D− (GPIO 19/20) am Header? Entscheidung: *Variante A* J_DATA → D+/D− direkt auf Header-Pins 19/20 mit ESD-Schutz (USBLC6-2 ist SMD → THT-Alternative: 2× 5,1 V-Zener BZX79 + 22 Ω Serie) oder *Variante B* internes USB-C-Kabel von der DevKit-USB-Buchse zur Gehäuserückwand (Panel-Mount-USB-C-Verlängerung, kein Layout nötig). **Empfehlung B** (kein Hochgeschwindigkeits-Layout auf dem Mainboard, keine ESD-Frage, DevKit bleibt frei flashbar); dann trägt J_DATA auf dem Mainboard nur 5 V. Ergebnis in Spec §2.2 + §8 eintragen.
- [ ] **Step 2: HiveMQ-Cloud-Free-Tier** — maximale Nachrichtengröße per WebFetch prüfen (HiveMQ-Doku); wenn < 256 KB → Screenshot-Breite 640 px, JPEG-Qualität 60; Wert in Spec §4 eintragen.
- [ ] **Step 3: Lizenz** — Leon fragen (MIT für Code + CERN-OHL-P-2.0 für `hardware/`?), Ergebnis in LICENSE/README.
- [ ] **Step 4: Commit** — `Offene Spec-Punkte USB-Pfad, HiveMQ-Limit, Lizenz geschlossen`

---

## Phase 2 — KiCad (drei Designs) bis JLCPCB-Bestellung

Werkzeug: KiCad 10 GUI für Schaltplan/Layout, `KICAD=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` für Prüfungen und Export. Skill `kicad` laden, bevor Task 11 beginnt; jede Review-Runde mit dem Skill gegen Spec §2 fahren.

### Task 11: KiCad-Projekte und Bibliothek anlegen

**Files:**
- Create: `hardware/kicad/mainboard/mainboard.kicad_pro` (+ `.kicad_sch`, `.kicad_pcb`), `hardware/kicad/frontpanel/…`, `hardware/kicad/eye-adapter/…`, `hardware/kicad/lib/deskmate.kicad_sym`, `hardware/kicad/lib/deskmate.pretty/`, `hardware/kicad/README.md`

- [ ] **Step 1: Drei Projekte** in KiCad 10 anlegen (2 Lagen, 1,6 mm, Default-Regeln JLCPCB: min. Leiterbahn 0,2 mm, Abstand 0,2 mm, Via 0,3/0,6 mm — als `.kicad_dru`).
- [ ] **Step 2: Projektbibliothek** — Symbole + Footprints, die KiCad nicht mitbringt oder die als Modul gesteckt werden: `ESP32-S3-DevKitC-1` (2× 1×22, 2,54 mm, Pinnamen = GPIO-Nummern), `DRV8833_Breakout` (2× 1×8-Reihen, Pololu-Raster), `MPR121_Breakout`, `BME680_Breakout`, `GC9A01_Module_7pin`, `ILI9341_2.8_14pin`, `MF60T` (Footprint aus FaderBuddy `electronics/` übernehmen, Maße gegen Datenblatt prüfen), `MX_Switch_THT_Hotswap`, `USB_C_16pin_THT`, `StepperDriver_Socket_A4988` (2× 1×8), `ESP32-C3_SuperMini` (2× 1×8).
- [ ] **Step 3: Prüfung** — für jeden Footprint: 3D-Modell oder zumindest Courtyard; Bohrdurchmesser THT ≥ 0,9 mm bei 2,54-mm-Stiften, ≥ 1,0 mm bei USB-C-Befestigung. `$KICAD fp export svg`-Stichprobe ansehen.
- [ ] **Step 4: Commit** — `KiCad-Projekte und Bibliothek fuer Mainboard, Frontpanel, Augen-Adapter`

### Task 12: Mainboard-Schaltplan (ERC sauber)

- [ ] **Step 1: Blätter** — Versorgung (J_DATA 5 V, J_PWR 5 V + CC-Widerstände, ODER-Stufe, Polyfuse, Bulk, LD1117V33 + 10 µF/100 nF, Testpunkte 5V/3V3/GND), MCU (DevKit-Sockel, alle Pins beschriftet nach `pins.h`, PSU_SENSE-Teiler 10 k/10 k, RESET/BOOT-Stecker), Motor (2× DRV8833-Sockel, IN1 = PWM, IN2 = DIR, 100 µF je VM, nSLEEP auf 3V3 über Jumper), Peripherie (2× Servo-JST + 470 µF + optional 10 Ω, WS2812-JST + 330 Ω + 1000 µF, BME680-Sockel, I²C-Pull-ups 4,7 kΩ), IDC 2×15 exakt nach Spec §2.4, Reserve (Stepper-Sockel mit Lötjumpern, C3-Footprint mit Lötjumpern).
- [ ] **Step 2: Netznamen** englisch und identisch zu `pins.h`-Namen ohne `PIN_` (z. B. `FADER1_PWM`, `SPI_MOSI`).
- [ ] **Step 3: ERC** — `$KICAD sch erc --severity-all --exit-code-violations hardware/kicad/mainboard/mainboard.kicad_sch` → Exit 0. Jede Ausnahme (z. B. unbenutzte Sockelpins) mit „No connect“-Flag, nicht per Regel unterdrücken.
- [ ] **Step 4: Review mit Skill `kicad`** gegen Spec §2.2/2.3/2.5 (Power-Tree, Pin-Map, Strompfad); Findings beheben oder begründet ins Tagesblatt.
- [ ] **Step 5: Commit** — `Mainboard-Schaltplan, ERC sauber`

### Task 13: Frontpanel-Schaltplan (ERC sauber)

- [ ] **Step 1:** 4× MF60T (Motor auf IDC MOT1–4, Schleifer über RC 1 kΩ/100 nF auf WIPER1–4, Touch-Pad auf MPR121 ELE0–3; Fader 3/4 als DNP markiert), 10× MX direkt auf MCP23017 GPA0–GPB1 mit internem Pull-up (Schalter nach GND), EC11 A/B/SW auf GPB2–4 + 10 nF Entprellung, MCP23017 (A0–A2 = GND → 0x20, RESET auf 3V3, INTA+INTB per Jumper auf IO_INT mit 10 kΩ Pull-up, INT als Open-Drain konfigurierbar), MPR121-Sockel (ADDR = GND → 0x5A, IRQ auf IO_INT), ILI9341-Steckleiste (VCC 3V3, GND, CS_BELLY, RESET ← MCP GPB5, DC, MOSI, SCK, LED ← Jumper: MCP GPB6 über Transistor BC337 oder BELLY_BL_PWM vom IDC), IDC 2×15 spiegelbildlich zu Task 12.
- [ ] **Step 2: ERC** wie Task 12, Exit 0.
- [ ] **Step 3: Review** mit Skill `kicad`; besonders: Backlight-Strom (ILI9341-LED-Pin zieht bis 150 mA → nie direkt aus MCP23017, immer Transistor).
- [ ] **Step 4: Commit** — `Frontpanel-Schaltplan, ERC sauber`

### Task 14: Augen-Adapter-Schaltplan + Layout

- [ ] **Step 1:** 10-Pin-Eingang (JST-XH 2,5 mm oder 2,54-Stift) → 2× 7-Pin-Buchse für GC9A01 (VCC, GND, SCL=SCK, SDA=MOSI, RES=DISP_RST, DC, CS_L/CS_R; BL-Pin falls Modul 8-polig). 100 nF je Modul.
- [ ] **Step 2:** ERC Exit 0, Layout 30 × 20 mm, DRC Exit 0 (`$KICAD pcb drc --severity-all --exit-code-violations …`).
- [ ] **Step 3: Commit** — `Augen-Adapter fertig (ERC/DRC sauber)`

### Task 15: Mainboard-Layout (DRC sauber)

- [ ] **Step 1: Platzierung** — DevKit am Rand mit Antenne über Platinenkante; USB-C-Buchsen an der Rückkante; DRV8833 nahe IDC; Bulk-Elko nahe ODER-Stufe; Montagelöcher 3,2 mm in den Ecken (Gehäuse-Referenz); Reserve-Sockel dort, wo sie keine Leiterbahnen der Hauptfunktion verlängern.
- [ ] **Step 2: Routing** — 5-V-Pfad ≥ 1,5 mm Leiterbahn (3 A), Motor-Leitungen ≥ 0,8 mm, Massefläche beidseitig, Schleifer-Leitungen weg von Motor-Leitungen, I²C kurz.
- [ ] **Step 3: DRC** Exit 0; 3D-Ansicht: DevKit-Antenne frei, USB-C-Stecker passen durch die spätere Rückwand (Abstand zur Kante notieren für `hardware/3d/`).
- [ ] **Step 4: Review** mit Skill `kicad` (DFM: Annular Rings, Bohrklassen, Silk-Lesbarkeit, Referenzen sichtbar). Beheben, Tagesblatt.
- [ ] **Step 5: Commit** — `Mainboard-Layout, DRC sauber`

### Task 16: Frontpanel-Layout (DRC sauber)

- [ ] **Step 1: Anordnung mit Leon abstimmen** (Skizze nachreichen!): Display oben mittig, 6 Soft-Keys darunter im 19,05-mm-Raster, je 2 Fader links/rechts (Fader 3/4 außen als DNP), 4 Makro-Keys + Encoder zwischen den Fadern. Maß der Frontblende daraus ableiten (→ `hardware/3d/`).
- [ ] **Step 2: Routing** wie Task 15; Touch-Leitungen zu den Fader-Kappen kurz und ohne Massefläche darunter (MPR121-Hinweis); Schleifer-RC nahe am Fader.
- [ ] **Step 3: DRC** Exit 0; 3D-Ansicht; Bohrungen für Display-Abstandshalter.
- [ ] **Step 4: Review** mit Skill `kicad`; Commit — `Frontpanel-Layout, DRC sauber`

### Task 17: Export, JLCPCB-Bestellung, Dokumentation

- [ ] **Step 1: Export je Projekt** — `$KICAD pcb export gerbers` + `drill`, Zip je Board in `hardware/kicad/<board>/fab/`; zusätzlich `$KICAD pcb export step` und ein PNG-Render für README/Vault.
- [ ] **Step 2: Gerber-Sichtprüfung** im JLCPCB-Viewer (Lagen, Umriss, Bohrungen) — Screenshot in `vault/Bestellungen/`.
- [ ] **Step 3: Bestellung** — drei Designs, je 5 Stück, 1,6 mm, HASL oder ENIG (Leon), Farbe (Leon). Leon bestellt über den Sponsoring-Account; `vault/Bestellungen/2026-xx-xx-jlcpcb.md` mit Positionen, Kosten, Lieferzeit, Bestellnummer. Leon informiert seinen JLCPCB-Kontakt (Erinnerung im Tagesblatt).
- [ ] **Step 4: README** — Abschnitt „Hardware“ mit Render + Link auf `hardware/kicad/`; `docs/anleitung/01-platinen.md` begonnen (Was bestellen, welche Dateien).
- [ ] **Step 5: Commit** — `Gerber/STEP exportiert, JLCPCB-Bestellung dokumentiert`; Tag `v0.1-pcb-bestellt`.

---

## Danach (eigene Pläne)

- **Phase 3 Firmware** (`docs/superpowers/plans/…-firmware.md`): Module aus Spec §3, beginnend mit `link` + `state` (host-testbar), dann HID, Display, Motion, Net. Braucht: DevKit + Displays + ein DRV8833 + ein Fader (Breadboard), noch keine Platine.
- **Phase 4 Agent + iOS-App** (Spec §4–5), parallel zur Platinen-Lieferzeit möglich.
- **Phase 5 Server** (Vercel-Function + APNs; Skill `vercel:marketplace` für Supabase-Anbindung).
- **Phase 6 Aufbau + Gehäuse + Anleitung + Fotos + Website-Eintrag P12.**

## Self-Review (erledigt 2026-08-22)

- Spec-Abdeckung Phase 0–2: §1 ✓ (Task 4 Entscheidungen), §2.2 ✓ (Task 11–16), §2.3 ✓ (Task 7), §2.4 ✓ (Task 12/13 IDC), §2.5 ✓ (Task 12 Versorgung, Task 15 Leiterbahnbreiten), §2.6 nur Maßableitung (Task 15/16) — Gehäuse selbst ist Phase 6, §2.7 ✓ (Task 8/9), §6 ✓ (Task 1–6), §8 ✓ (Task 7, 10). §3–5, §7: spätere Pläne.
- Platzhalter: keine „TBD/TODO“; Bestelldaten `2026-08-xx` sind bewusst offen, bis Leon bestellt.
- Namen: `pins.h`-Konstanten (Task 7) = Netznamen (Task 12/13) ohne `PIN_`; Tagesblatt-Format (Task 3) = Format in Task 4; `tools/check-secrets.sh` in Task 2 und 3 identisch benannt.
