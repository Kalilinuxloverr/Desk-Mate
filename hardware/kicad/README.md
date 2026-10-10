# KiCad — drei Platinen, eine JLCPCB-Bestellung

| Ordner | Platine | Maß | Inhalt |
|---|---|---|---|
| `mainboard/` | Base | 100 × 100 mm | S3-DevKit-Sockel, Schraubklemme für das USB-C-Breakout (5 V/3 A), Polyfuse + SB540, LD1117V33, 2× DRV8833-Sockel, Servo/ARGB/I²C-Stiftleisten, Augen-Kabel IDC 2×5, IDC 2×15, MT3608-Header (VM-Boost, optional) |
| `frontpanel/` | Deck | 120 × 136 mm | 10× MX, EC11, MCP23017, MPR121-Stiftleiste (Modul per Kabel), ILI9341-Sockel + 4 Abstandshalter, 4× Fader-Header, Backlight-Schalter, IDC 2×15 |
| `eye-adapter/` | Kopf | 42 × 30 mm | IDC 2×5 ein, 2× 1×7-Stiftleiste für die GC9A01 (per Dupont-Kabel) |
| `lib/` | — | — | Projektbibliothek `deskmate.kicad_sym` + `deskmate.pretty` (Modul-Sockel, Polyfuse) |
| `gen/` | — | — | Generator (siehe unten) |
| `<board>/fab/` | — | — | Gerber/Drill-Zip, STEP, Render — das geht zu JLCPCB |

Regeln (JLCPCB 2-Lagen): Leiterbahn ≥ 0,2 mm, Abstand ≥ 0,127 mm, Via 0,8/0,4 mm, Rand 0,3 mm. Netzklassen (Breite / Abstand 0,13): Default 0,25, Power 1,0 (Mainboard) bzw. 0,8 (Frontpanel), Motor 0,6, Power3V3 0,6 — Werte stehen in `gen/boards.py` und `gen/build_sch.py`. Massefläche beidseitig, Sperrzone unter der DevKit-Antenne.

## Generator statt Handarbeit (Erstversion)

Die Erstversion aller Dateien wurde aus `gen/boards.py` erzeugt — eine Tabelle „Bauteil → Pin → Netz → Position“. So sind Schaltplan, Layout und `netlist.json` per Konstruktion identisch, und `tools/test-kicad.sh` prüft das gegen KiCads eigene Netzliste.

```bash
cd hardware/kicad/gen
python3 build_sch.py                       # Bibliothek, Schaltpläne, Projekte, netlist.json
KIPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
$KIPY build_pcb.py mainboard --force       # Layout platzieren, Freerouting, Zonen füllen
$KIPY export_fab.py mainboard              # Gerber/Drill/STEP/Render nach mainboard/fab/
sh ../../../tools/test-kicad.sh            # ERC + DRC + Netzlisten-Abgleich
```

`build_pcb.py` routet bis zu 6-mal mit wechselnder Strategie und behält den ersten Lauf mit 0 offenen Verbindungen; GND-Pads sind vollflächig an die Massefläche angebunden (beim Löten heißer/länger). Freerouting: `~/Applications/freerouting-2.3.0.jar` (Java 17+; `curl -L -o ~/Applications/freerouting-2.3.0.jar https://github.com/freerouting/freerouting/releases/download/v2.3.0/freerouting-2.3.0.jar`).

**Wichtig:** Sobald in der KiCad-GUI etwas geändert wurde, sind die `.kicad_sch`/`.kicad_pcb` die Wahrheit — `build_*.py` nicht mehr blind laufen lassen (`build_pcb.py` weigert sich ohne `--force`). Der Generator ist ein Bootstrap, kein Roundtrip.

Der Schaltplan ist „Label-Stil“: jedes Pin trägt ein globales Label, keine Leitungen. Elektrisch vollständig, optisch schlicht — in der GUI beliebig umsortierbar.

## Was vor der Bestellung am echten Teil zu prüfen ist

Siehe `vault/Hardware/Module-Masse.md` (Quellen + Konfidenz). Kurz: DevKit-Reihenabstand 22,86 (hoch), Pololu-Raster 10,16 (hoch), MPR121-Clone 17,78 (mittel — nachmessen), ILI9341 MSP2807-Löcher (hoch), X32-Fader-Pins (unbekannt — Drähte an Stiftleiste).
