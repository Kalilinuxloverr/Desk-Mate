---
datum: 2026-08-27
typ: entscheidung
---
# KiCad-Erstversion per Generator statt GUI-Handarbeit — und die Schaltungsdetails, die dabei fielen

**Kontext:** Leon will die Platinen sofort, damit JLCPCB zusammen mit den Teilen bestellt wird. Claude hat keine GUI; drei Boards mit ~110 Bauteilen von Hand als S-Expression zu tippen wäre fehleranfällig.

## 1. Generator (`hardware/kicad/gen/`)
- **Optionen:** (a) Leon zeichnet alles in der GUI nach Spec; (b) Claude schreibt die KiCad-Dateien von Hand; (c) Datenmodell „Bauteil → Pin → Netz → Position“ in Python, daraus Schaltplan (Label-Stil), Bibliothek und Layout (pcbnew-Python + Freerouting), Prüfung per `kicad-cli` ERC/DRC und Netzlisten-Abgleich.
- **Wahl:** (c). Schaltplan und Layout sind per Konstruktion identisch, jede Änderung ist ein Einzeiler, der Test ist eingebaut. Nachteil: Schaltplan ohne Leitungen (nur globale Labels) — in der GUI umsortierbar; der Generator ist Bootstrap, kein Roundtrip (GUI-Änderungen danach sind die Wahrheit).

## 2. Schaltungsdetails (Spec nachgezogen)
| Punkt | Optionen | Wahl | Grund |
|---|---|---|---|
| PSU_SENSE-Teiler | 10k/10k (2,5 V) · 10k/15k (3,0 V) | **10k/15k** | 2,5 V liegt nur 25 mV über VIH (0,75·3,3); 3,0 V hat Reserve, bleibt unter 3,3 V auch bei 5,25 V |
| Backlight-Schalter ILI9341 (150 mA) | NPN low-side (geht nicht: LED-Pin ist Anode) · PNP high-side direkt vom MCP · **BC337 → BC327 zweistufig** | zweistufig | Der PNP-Basis-Pull-up (10 k an 3V3) würde über JP11/JP1 an GPIO45 hängen → Strapping VDD_SPI 1,8 V → Flash tot (Falle 13). Zweistufig sieht die Steuerleitung nur Basiswiderstand + 100 k Pull-down |
| Augen-Reset | DISP_RST vom MCP über 30-adriges IDC (kein Pin frei) · extra GPIO (keiner frei) · **RC 10k/1µ auf dem Adapter** | RC | Software-Reset (SWRESET) reicht im Betrieb; LovyanGFX `pin_rst=-1` |
| MT3608-Boost | Sockel · **4-Pin-Stiftleiste + Drähte** | Stiftleiste | Modul-Lochraster ist nicht 2,54 (6,45–6,8 mm), Sockel wäre Revisionsrisiko; Modul ist optional |
| Servo-Serienwiderstand 10 Ω | drin · **weg** | weg | 0,7 A Stall × 10 Ω = 7 V Abfall — Unsinn; Drosselung macht die Firmware (PSU_SENSE) |
| Pull-ups I²C/IO_INT | Frontpanel · **Mainboard** | Mainboard | IO_INT auch ohne Frontpanel definiert |
| Mainboard-Größe | 100×80 · 100×90 · **100×100** | 100×100 | Reserve-Sockel + IDC + Anschlusskante brauchen Platz; JLCPCB-Preisstufe bleibt ≤100×100 |
| Frontpanel-Anordnung | — | Vorschlag 120×136: Display oben quer (Header links), 6 Soft-Keys, 2×2 Makro, Encoder rechts, Fader **neben** dem PCB | Leons Skizze steht aus — Positionen sind Einzeiler in `boards.py` |
| Fader-Anschluss | Stecker-Footprint · **8-Pin-Stiftleiste je Fader** (MOT+ MOT− GND 3V3 WIPER GND TOUCH GND) | Stiftleiste | X32-Fader hat Lötpins, kein Kabel, kein Touch-Kontakt (Community) — Drähte, Touch am Metallhebel |
| MPR121-Sockel | nur Steuerpins + Drähte · **beide Reihen (SparkFun-Raster 17,78)** | beide Reihen | SparkFun-Eagle-Daten liegen vor; Clone ist 1:1. Wenn der Clone abweicht: Steuerreihe stecken, Elektroden per Draht |

Verifikation: ERC 0 Fehler (3 Boards), Netzlisten-Abgleich KiCad ↔ Modell identisch, DRC siehe Tagesblatt. Quellen der Maße: [[Module-Masse]].
