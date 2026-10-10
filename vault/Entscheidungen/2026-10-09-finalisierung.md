---
datum: 2026-10-09
typ: entscheidung
---
# Finalisierung der Platinen — Reichelt, Kabel statt Sockel, Silkscreen

**Kontext:** Leon: „finalisieren … so einfach wie möglich, so wenig SMD wie's geht, keine komplizierten Teile, alles muss ich auf Reichelt bekommen, coole Silkscreen“. Im Grilling präzisiert: **gelötete Teile von Reichelt, Module dürfen von Amazon kommen.** Grundlage: Reichelt-Recherche vom selben Tag (zwei Agenten + eigene Abfrage der Produktseiten, Art.-Nr. in `hardware/bom.md`).

## Was Reichelt nicht hat → Lösung

| Teil | Problem | Optionen | Wahl | Grund |
|---|---|---|---|---|
| USB-C-Platinenbuchse (GCT USB4085) | Reichelt führt keine THT-USB-C-Buchse | Breakout + Schraubklemme · Hohlbuchse · Buchse von TME | **USB-C-Breakout in der Rückwand → 4-pol. Schraubklemme MKDS 1,5/4-5,08** (VBUS GND CC1 CC2), 5,1 kΩ bleiben auf dem Mainboard | bleibt bei 2× USB-C (Grilling #11); die 0,85-mm-Buchse samt Handrouting entfällt; Breakout von Amazon oder Reichelt (Soldered 333011) |
| DRV8833-Breakout | Reichelt hat keinen | SN754410 DIP-16 · L298N-Modul · Amazon | **Pololu #2130 bleibt** (Amazon/Bestand) | Leon: „Amazon generell ist auch ok“; Sockel und Pin-Map unverändert |
| 2,8"-ILI9341-Modul | Reichelt hat nur Arduino-Shields (Parallelbus) und Industrie-Displays mit FPC | Amazon-MSP2807 · Reichelt 1,3" ST7789 | **2,8" von Amazon** | großes Bauch-Display (Grilling #9), Frontpanel bleibt |
| Keycaps | Reichelt hat keine | Amazon · 3D-Druck | Amazon oder Druck | — |
| Flachband 30-adrig | nur 40-adrig | — | 40-adrig, abreißen | Standard |

## Vereinfachungen, die dabei fielen

| Was | Vorher | Jetzt | Grund |
|---|---|---|---|
| Servo/ARGB | JST-XH | 1×3-Stiftleiste | Servostecker passt direkt, eine Teilefamilie weniger |
| BME680 | 1×6-Sockel (CJMCU-Reihenfolge ungeprüft) | 1×4-I²C-Stiftleiste, Sensor per Kabel | Pinfolge egal, Sensor weg von der ESP-Wärme |
| MPR121 | Sockel im SparkFun-Raster (Clone unbelegt) | 1×9-Stiftleiste J18, Modul per Kabel | Falle 15: ohne Maßzeichnung kein Sockel |
| Augen-Kabel | 1×10-Stiftleiste | IDC 2×5 (WSL 10G/PFL 10), GND zwischen SCK und MOSI | verpolsicher, gleiches Flachband |
| Augen-Adapter | 2× 7-Pin-Buchse 20 mm auseinander | 2× 1×7-Stiftleiste, Displays per Dupont | die 38-mm-Module hätten sich überlappt — Fehler im alten Entwurf |
| R17 (DISP_RST-Pull-up) | rechts neben dem MCP23017 | unter dem MCP23017 | blockierte die Leitung KEY9 beim Routen |
| 5-V-Schiene Servos/ARGB | Freerouting | feste Leiterbahn (pre_tracks) bei x = 92,5 | Freerouting fand sie mit 1 mm Breite an R5 vorbei nicht |

**Silkscreen:** vorne Desk-Mate-Kopf (Visier gefüllt, Augen und Lächeln als Aussparung), Platinenname, „Rev 1 · 2026-10“ und Pin-Namen an jedem Stecker; hinten großer Kopf, GitHub-Link, „Leon Fröhlich · 2026“, Feld `JLCJLCJLCJLC` (Bestellnummer, Option „Specify Position“). Referenzen ausgeblendet, wo Titel + Pin-Namen sie ersetzen. Daten: `'silk'` in `boards.py`, gezeichnet von `add_silk()` in `build_pcb.py`.

**Weiter offen (nicht platinenrelevant):** Lizenz → MIT für alles (Leon hat nicht widersprochen). Frontpanel-Anordnung → freigegeben. Fader-Charakterisierung → nach Lieferung, hängt an Drähten.

**Verifikation:** alle drei Boards 0 offene Verbindungen, 0 DRC-Fehler, ERC sauber, Netzlisten-Abgleich ok, `tools/test-*.sh` grün; Netzklassen-Zuordnung 15/12/2 intakt (Falle 18). Siehe [[2026-10-04-reserve-raus]], [[Module-Masse]].
