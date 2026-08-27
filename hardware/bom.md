# Stückliste (Stand 2026-08-27 nach KiCad, Preise inkl. MwSt., „~“ = ungefähr/unbestätigt)

Referenzen werden in KiCad 1:1 übernommen. Spalte **Bestand** wird nach Leons Arduino-Box-Inventur gefüllt (`hardware/inventar.md`). Bestellvorschlag je Lieferant: `vault/Bestellungen/2026-08-23-bestellvorschlag.md`.

## Mainboard (100 × 100 mm)

| Ref | Bauteil | Gehäuse | Stück | Quelle | Preis € | Bestand | Hinweis |
|---|---|---|---|---|---|---|---|
| U1 | ESP32-S3-DevKitC-1-**N16R8** (Espressif Original) | Sockel 2× 1×22 | 1 | Amazon (Prime) | **19,99** | im Warenkorb 24.08. | Revision nach Lieferung prüfen (LED-Pin 38/48); Sockel wird am echten Board vermessen |
| U2 | LD1117V33 | TO-220 | 1 | [Reichelt](https://www.reichelt.com/de/en/ldo-voltage-regulator-15-vin-3-3-vout-950-ma-to-220-ld1117v33-p216683.html) | 0,25 | ? | 3,3 V für Peripherie |
| U3, U4 | DRV8833-Breakout | Sockel | 2 | **Bestand** (Arduino-Box) | 0 | ✔ | Amazon-Fallback 10,07 €. **nSLEEP prüfen**, Footprint nach den vorhandenen Modulen |
| U5 | MT3608-Boost (VM-Rail 9 V, optional) | **4-Pin-Stiftleiste + Drähte** (Modul-Raster ist nicht 2,54) | 1 | Amazon (Pack) | **6,04** | im Warenkorb 24.08. | Vor Einbau auf 9 V trimmen; erst nach Fader-Charakterisierung; JP4 auf 3 |
| U6 | C3-SuperMini-Reserve | Footprint, unbestückt | 0 | — | 0 | ✔ (vorhanden) | Lötjumper |
| U7 | Stepper-Treiber-Reserve (A4988-Raster) | Footprint, unbestückt | 0 | — | 0 | — | Lötjumper |
| D1 | SB540 Schottky | DO-201 | 1 | Reichelt | ~0,30 | ? | J_PWR → Rail; DevKit-Diode ist der zweite Zweig |
| F1 | Polyfuse 3 A (RXEF300) | radial | 1 | [Farnell](https://de.farnell.com/littelfuse/rxef300/polyswitch-sicherung-ptc-radial/dp/1345966) | ~0,50 | ? | |
| J1 | USB-C-Buchse 16-Pin, THT-Shell (GCT USB4085-GF-A) | THT | 1 | [TME](https://www.tme.eu/en/details/usb4085-gf-a/usb-ieee1394-connectors/gct/) | ~1 | ? | Nur 5 V; 2× 5,1 kΩ an CC1/CC2 |
| J2 | Wannenstecker IDC 2×15 + Buchse + Flachband 30-adrig 30 cm | DIN 41651 | 1 Set | Reichelt | ~5 | ? | |
| J3, J4 | Servo-Stecker JST-XH 3-Pin | THT | 2 | [eBay-Set](https://www.ebay.de/itm/335345792316) | ~2 | ? | |
| J5 | ARGB-Stecker JST-XH 3-Pin (5V/GND/Data) | THT | 1 | dito | ~1 | ✔ Streifen (Drohne) | generisch für jeden 5-V-WS2812-Streifen |
| J6 | BME680-Breakout-Sockel | 1×6 Buchse (VCC GND SCL SDA SDO CS) | 1 | — | 0 | ✔ BME680 | Pinreihenfolge am Modul prüfen |
| J7 | Augen-Kabel-Stecker 10-Pin | 2,54 | 1 | Leistenware | ~0,50 | ? | |
| J8 | Reset/Boot nach außen | 2×2 | 1 | Leistenware | ~0,20 | ? | |
| C1 | 1000 µF/10 V (Rail) | radial | 1 | Reichelt | ~0,40 | ? | |
| C2, C3 | 100 µF (je DRV8833-VM) | radial | 2 | Reichelt | ~0,40 | ? | |
| C4 | 470 µF (Servo-Pfad) | radial | 1 | Reichelt | ~0,30 | ? | |
| C5 | 1000 µF (ARGB) | radial | 1 | Reichelt | ~0,40 | ? | |
| C6, C7 | 100 nF | RM 5 | 2 | Sortiment | ~0,20 | ? | |
| C8 | 100 µF (A4988-Reserve) | radial | 0 | — | 0 | — | unbestückt |
| C11 | 10 µF | radial | 1 | Sortiment | ~0,10 | ? | LD1117-Ausgang |
| JP1–JP8 | Lötjumper (JP4 3-fach) | — | 8 | — | 0 | — | JP4 1-2 + JP5 ab Werk gebrückt; Rest offen |
| J10 | Stepper-Header 1×4 (Reserve) | 2,54 | 0 | — | 0 | — | unbestückt |
| TP1–TP3 | Testpunkte 5V/3V3/GND | Ø1,5 Pad | 3 | — | 0 | — | Lötpunkt |
| R1, R2 | 5,1 kΩ (CC) · R3 10 kΩ + R4 **15 kΩ** (PSU_SENSE → 3,0 V) · R5 330 Ω (ARGB) · R6/R7 4,7 kΩ (I²C) · R8 10 kΩ (IO_INT) | axial | 8 | Sortiment | ~0,50 | ? | Sortiment ~10 € falls Box leer |

## Frontpanel (120 × 136 mm)

| Ref | Bauteil | Gehäuse | Stück | Quelle | Preis € | Bestand | Hinweis |
|---|---|---|---|---|---|---|---|
| FD1, FD2 | Behringer X32 Motor-Fader 100 mm (5er-Set) | panel-mount + Kabel | 1 Set | Amazon.de („Behringer X32 MOTOR FADER Set“) | 39,32 | bestellt 23.08. | **Ersetzt MF60T:** Prime-Lieferung 25.08., 30 Tage Retour, kein PCB-Footprint nötig. Pinout/Motorspannung bei Charakterisierung |
| FD3, FD4 | X32-Fader (aus dem Set) | panel-mount, Reserve | 0 | (im Set, +1 Ersatz) | 0 | ✔ | Reserve |
| J14–J17 | Fader-Anschluss-Header 1×8 (MOT+ MOT− GND 3V3 WIPER GND TOUCH GND) | 2,54 Stift | 4 | Leistenware | ~1 | ? | X32-Fader hat Lötpins, kein Kabel → Drähte anlöten; Touch = Draht an Metallhebel |
| SW1–SW10 | MX-Schalter linear | THT | 10 | Amazon | **7,04** | im Warenkorb 24.08. |
| — | ~~Hot-Swap-Sockel~~ | — | 0 | gestrichen 24.08. | 0 | — | Sockel sind SMD → Switches direkt THT löten (Kein-Hand-SMD-Regel) |
| — | Blank-Keycaps | — | 10 | Amazon | **10,04** | im Warenkorb 24.08. |
| ENC1 | EC11-Encoder nackt (5er-Pack) | THT | 1 Pack | Amazon | **7,04** | im Warenkorb 24.08.; Aluknopf separat (offen) |
| U8 | MCP23017-E/SP + DIP-28-Sockel | DIP-28 | 1 | [Reichelt](https://www.reichelt.com/de/en/i-o-extension-16bit-1-8-5v-serial-i2c-dip-28-mcp-23017-e-sp-p140074.html) | 1,90 | ? | |
| U9 | MPR121-Breakout (Clone) | Sockel | 1 | Amazon | **6,04** | im Warenkorb 24.08.; ADDR=GND |
| Q1 | **BC327** (PNP, High-Side an 3V3) | TO-92 | 1 | Reichelt | ~0,10 | ? | Backlight 150 mA |
| Q2 | BC337 (NPN, Vorstufe) | TO-92 | 1 | Reichelt | ~0,10 | ? | zweistufig wegen GPIO45-Strapping (Falle 13) |
| DSP1 | ILI9341 2,8" SPI 320×240 | Steckleiste 14-Pin | 1 | Amazon | **14,11** | im Warenkorb 24.08. | EU-Ware meist MIT Touch — egal, Touch-Pins bleiben offen |
| R13–R16, C15–C18 | Schleifer-RC 4× 1 kΩ + 4× 100 nF | axial/RM5 | 8 | Sortiment | ~0,50 | ? | |
| R9, R11 1 kΩ · R10 10 kΩ · R12 100 kΩ | Backlight-Schalter | axial | 4 | Sortiment | ~0,20 | ? | |
| C12 100 nF · C13, C14 10 nF | MCP-Abblock, Encoder-Entprellung | RM 5 | 3 | Sortiment | ~0,20 | ? | |
| JP9–JP11 | Lötjumper (JP11 3-fach) | — | 3 | — | 0 | — | JP9 + JP11 1-2 ab Werk gebrückt |
| — | Abstandshalter M3 × 11 mm + Schrauben (Display) | — | 4 | Reichelt/Set | ~2 | ? | MSP2807: Header ragt 11,17 mm unter das Modul |
| J9/J10 | Steckleisten + IDC-Gegenstück | 2,54 | — | Leistenware | ~1 | ? | |

## Augen-Adapter (42 × 30 mm) + Kopf

| Ref | Bauteil | Gehäuse | Stück | Quelle | Preis € | Bestand | Hinweis |
|---|---|---|---|---|---|---|---|
| DSP2, DSP3 | GC9A01 1,28" rund, SPI, 7-Pin | Buchse | 2 | Amazon (2er-Pack) | **10,07** | im Warenkorb 24.08. | |
| M1, M2 | MG90S Metallgetriebe | — | 2 | Amazon | **14,10** | im Warenkorb 24.08. |
| — | Pan-Tilt-Halter für MG90S | 3D-Druck | 1 | Printables/Thingiverse („SG90 pan tilt“) | 0 | — | Schrauben liegen Servos bei; alternativ Kit ~3 € AliExpress |
| J11–J13 | Stecker Augen-Adapter (10-Pin Stift ein, 2× 7-Pin Buchse aus) | 2,54 | 3 | Leistenware | ~1 | ? | |
| R17 10 kΩ · C19 1 µF · C20, C21 100 nF | Reset-RC + Abblock | axial/RM5 | 4 | Sortiment | ~0,20 | ? | Reset nur per RC + Software |

## Sonstiges

| Bauteil | Stück | Quelle | Preis € | Bestand | Hinweis |
|---|---|---|---|---|---|
| Panel-Mount-USB-C-Verlängerung (Buchse→Stecker, ~30 cm) | 1 | Amazon | **8,05** | im Warenkorb 24.08. | Daten-Port Gehäuserückwand → DevKit-Buchse |
| Netzteil 5 V/3 A USB-C | 1 | **Bestand** | 0 | ✔ | Leon hat passendes (5V⎓3A geprüft) |
| Buchsenleisten 1×40 zum Schneiden (2× 1×22 DevKit, 4× 1×8 DRV8833, 1×6/1×12 MPR121, 1×14 Display, 2× 1×7 Augen, 1×6 BME680; Reserve 4× 1×8) | 6 | Reichelt/AliExpress | ~3 | ? | 22er gibt es nicht fertig |
| USB-C-Kabel | 2 | — | ~5 | vermutlich ✔ | |

## Bereits vorhanden (aus früheren Projekten / Drohnen-Bestellung)

| Bauteil | Verwendung |
|---|---|
| BME680-Breakout | Base, J6 |
| ARGB/WS2812-Streifen (Drohnen-Bestellung) | Mund/Ampel hinter dem Visier, J5 |
| ESP32-C3 SuperMini | Reserve-Footprint U6 (unbestückt) |
| CYD ESP32-2432S028R | nicht verbaut — Testgerät für LovyanGFX-Entwicklung |

## Summe (Schätzung 2026-08-23)

- Beste EU-Quellen inkl. MF60T-US-Import: **~160 €**
- Mit AliExpress-Alternativen (Displays, DRV8833, Encoder, Pan-Tilt): **~100–110 €**
- Vor der Bestellung: Inventur (`hardware/inventar.md`) gegen Spalte „Bestand“, dann Bestellvorschlag im Vault aktualisieren.
