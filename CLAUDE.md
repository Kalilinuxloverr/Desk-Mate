# Desk-Mate — Arbeitsanweisungen für Claude

Desk-Mate ist ein Wall-E-artiger Schreibtisch-Begleiter: Ampel für Claude Code und Downloads, Motorfader-Deck, Augen-Displays, Mac-Agent, iOS-App, MQTT-Anbindung ans Haus. Drei Through-Hole-Platinen um einen gesteckten ESP32-S3-DevKitC-1.

- **Spec (einzige Wahrheit):** `docs/superpowers/specs/2026-08-22-desk-mate-design.md`
- **Aktueller Plan:** `docs/superpowers/plans/2026-08-22-phase-0-2-infra-bauteile-kicad.md`
- **Relikt:** `docs/relic/2026-08-22-original-prompt.md` — nie ändern
- **Vault:** `vault/Index.md`

## Architektur (Kurzform)

- **Gerät:** ESP32-S3 (Hirn) · Mainboard (Base: USB-C ×2, Versorgung, DRV8833-Sockel, BME680) · Frontpanel (2(4)× MF60T, 10× MX, EC11, MCP23017, MPR121, 2,8" ILI9341) · Augen-Adapter (2× GC9A01). IDC 2×15 dazwischen. Pin-Map: Spec §2.3.
- **Verbindungen:** USB (Composite-HID + CDC-JSON zum Agent), BLE-HID + BLE-Config, WiFi (MQTT HiveMQ `deskmate/#`, NTP, OTA).
- **Agent:** Swift-Menüleisten-App (macOS), lokaler HTTP-Endpunkt `127.0.0.1:4821` für Claude-Hooks und Skripte, Watcher für `~/Downloads` und Steam-ACF, Screenshot → MQTT. iOS-App im selben Xcode-Projekt (`DeskMateCore` geteilt). Windows-Tray in Python (Phase 2).
- **Claude-Integration:** Hooks in `~/.claude/settings.json`: `UserPromptSubmit`→gelb, `PermissionRequest`→rot + Taste→`allow`/`deny`/`escalate`, `Notification`→rot blinkend, `Stop`→grün. Fakten: `vault/Apps/Claude-Hooks.md`.

## Build & Test — immer vor „fertig“ ausführen

```bash
sh tools/test-check-secrets.sh     # Secret-Check
sh tools/test-session-hooks.sh     # Zeiterfassung
sh tools/test-pins.sh              # Pin-Map-Regeln (pins.h)
sh tools/test-kicad.sh             # ERC + DRC + Netzlisten-Abgleich der drei KiCad-Projekte
```

Kommt mit den Phasen dazu: `arduino-cli compile` (Phase 3), `xcodebuild` (Phase 4). Neue Befehle hier eintragen, sobald sie existieren.

## Bekannte Fallen (teuer erkauft — nicht wieder reintappen!)

Startbestand aus ESP32-Kühler und VVVF; Desk-Mate-eigene Fallen werden hier nummeriert angehängt.

1. **ADC2 ist tot, sobald WiFi läuft.** Fader-Schleifer nur auf ADC1 (S3: GPIO 1–10).
2. **`WiFi.setSleep(false)`** sofort nach `WiFi.begin()`, sonst Paketverluste bei BLE-Koexistenz.
3. **NimBLE statt Bluedroid** — Bluedroid + WiFi + TLS sprengt den RAM.
4. **`.ino`-Prototyp-Fallen:** keine eigenen Structs oder Default-Argumente in Funktionssignaturen im `.ino`; die Wörter `extern "C"` brechen ctags. Alle Logik in `.cpp/.h`.
5. **Protokoll geändert = Versionsnummer hoch** und beide Seiten (Firmware + Agent + App) im selben Commit; Parser-Test mitziehen.
6. **Secrets im Initial-Commit** (Kühler `8958b76`): `secrets.h`/`.env` sind gitignored, `tools/check-secrets.sh` blockt. Trotzdem vor dem ersten Push nochmal `git log -p | grep -i passw`.
7. **UART zwischen zwei ESPs** (VVVF): Baud-Mismatch + Pufferüberlauf = „verbinden sich nie“. Desk-Mate hat deshalb nur einen ESP; der C3-Footprint ist Reserve mit Lötjumpern.
8. **Strapping-Pins S3:** 0, 3, 45, 46 nie als Funktion. 45 nur über Lötjumper (Backlight-PWM), Default ist Backlight über MCP23017 + Transistor.
9. **Onboard-RGB-LED des DevKitC-1** liegt je nach Revision auf GPIO 38 (v1.1) oder 48 (v1.0). WS2812-Daten auf 38 ist gewollt (spiegelt Pixel 0); 48 ist PSU_SENSE-Eingang — bei v1.0 leuchtet die LED dann mit, unkritisch.
10. **Motoren/Servos am Rechner-USB** = Brownout und „Gerät nicht erkannt“. Deshalb zwei USB-C-Buchsen; ohne Netzteil (`PSU_SENSE` low) nur gedrosselt fahren.
11. **ILI9341-Backlight** zieht bis 150 mA — nie direkt aus einem MCP23017-Pin, immer Transistor.
12. **Kapazitives Touch über Flachband** ist unzuverlässig — deshalb MPR121 auf dem Frontpanel, nicht die S3-Touch-Pins.
13. **GPIO45 darf keinen externen Pull-up sehen** (VDD_SPI-Strapping → 1,8 V → Flash tot). Deshalb Backlight-Steuerung zweistufig (BC337 low-side → BC327 high-side): die Steuerleitung sieht nur Basiswiderstand + Pull-down, nie einen Pull-up. Gilt für alles, was je über JP1 an GPIO45 hängt.
14. **DevKitC-1: Pin 1 beider Header liegt am Antennen-Ende**, nicht am USB-Ende (Espressif zeichnet mit Antenne oben). Footprint `ESP32-S3-DevKitC-1_Socket` ist so gebaut; beim Nachmessen nicht erschrecken.
15. **Modul-Lochraster vor dem Footprint prüfen** — MT3608-Module (6,45–6,8 mm Paarabstand) und viele Breakouts sind nicht 2,54-kompatibel. Regel: nur Module mit belegter Maßzeichnung bekommen einen Sockel, der Rest bekommt eine Stiftleiste + Drähte.
16. **Freerouting headless nur mit `-Djava.awt.headless=true`** — sonst hängt der Java-Prozess nach „Optimization was completed“ ewig in einem unsichtbaren Dialog (0 % CPU, keine .ses). `build_pcb.py` setzt das Flag.
17. **`pcbnew` (KiCad-Python) `board.Save()` schreibt die `.kicad_pro` mit Default-Netzklassen zurück** (0,2/0,2) — Projektregeln danach restaurieren (macht `build_pcb.py`) und eine Platine nur unter ihrem Projektnamen laden, sonst fehlen die Netzklassen beim DSN-Export. Außerdem: Anführungszeichen in Bauteilwerten (`2.8"`) zerstören die DSN-Datei.

## Konventionen

- Deutsch für Menschen (Doku, Commits, Kommentare, UI), Englisch für Bezeichner, Netznamen, JSON-Keys, MQTT-Topics.
- Commits: Satzform, ergebnisorientiert, kein Präfix, Umlaute dürfen ASCII-gefaltet sein (`Ueberlauf`).
- Dateien: Specs/Pläne `YYYY-MM-DD-<thema>.md`; CAD-Teile deutsch (`Kopf_Schale_vorne.stl`), je Teil STEP + STL; Sketch-Ordner snake_case.
- KiCad: Erstversion aus `hardware/kicad/gen/` generiert (Bauteil→Pin→Netz→Position in `boards.py`). Sobald in der GUI editiert wurde, sind `.kicad_sch`/`.kicad_pcb` die Wahrheit — Generator nicht mehr blind laufen lassen (`build_pcb.py` braucht `--force`). Sockel-Maße mit Quellen: `vault/Hardware/Module-Masse.md`.
- Pin-Map: `firmware/arduino/deskmate/pins.h` ist die Wahrheit (verifiziert, Test `tools/test-pins.sh`); Spec §2.3 und `vault/Hardware/Pin-Map.md` werden bei Änderungen nachgezogen.
- Through-Hole oder gesteckte Breakouts. Kein SMD auf unseren Platinen.
- `// ponytail:`-Kommentare markieren bewusste Vereinfachungen und nennen den Ausbaupfad.
- Jede nicht-triviale Logik hinterlässt genau einen lauffähigen Check (`tools/test-*.sh`, `assert`-Test), kein Test-Framework.

## Session-Pflichten (gelten in jeder Session, ohne Aufforderung)

1. **Tagesblatt** `vault/Log/YYYY-MM-DD.md`: Start/Ende schreiben die Hooks (`tools/session-start.sh`, `tools/session-end.sh`). Claude ergänzt unter „Was ist passiert“ stichpunktartig, was gemacht, entschieden und gelernt wurde. Erster Punkt = Commit-Betreff des Auto-Push.
2. **Entscheidungen** mit Optionen, Wahl und Begründung nach `vault/Entscheidungen/YYYY-MM-DD-<thema>.md`; Spec anpassen, wenn sich etwas ändert.
3. **Bestellungen** (Teile, JLCPCB) nach `vault/Bestellungen/YYYY-MM-DD-<lieferant>.md` mit Positionen, Kosten, Lieferzeit, Fotos (≤ 1 MB). JLCPCB ist Sponsor: Leon daran erinnern, den Kontakt zu informieren.
4. **Neue Falle gefunden?** Oben nummeriert eintragen, im selben Commit wie der Fix.
5. **Push** passiert beim SessionEnd-Hook automatisch; wenn `vault/Log/push-fehler.log` wächst, zuerst das lösen.
6. **Relikt nie anfassen.** Memory-Dateien ersetzen den Vault nicht — was fürs Projekt zählt, steht im Repo.
7. Vor „fertig“: Tests aus „Build & Test“ laufen lassen und Ergebnis nennen.
