# Stückliste (Stand 2026-08-23, Preise inkl. MwSt., „~“ = ungefähr/unbestätigt)

Referenzen werden in KiCad 1:1 übernommen. Spalte **Bestand** wird nach Leons Arduino-Box-Inventur gefüllt (`hardware/inventar.md`). Bestellvorschlag je Lieferant: `vault/Bestellungen/2026-08-23-bestellvorschlag.md`.

## Mainboard

| Ref | Bauteil | Gehäuse | Stück | Quelle | Preis € | Bestand | Hinweis |
|---|---|---|---|---|---|---|---|
| U1 | ESP32-S3-DevKitC-1-**N16R8** (Espressif) | Sockel 2× 1×22 | 1 | [Mouser](https://www.mouser.at/ProductDetail/Espressif-Systems/ESP32-S3-DevKitC-1-N16R8) | ~14 | ? | BerryBase/Reichelt nur N8R8. Revision (v1.0/v1.1) nach Kauf prüfen → LED-Pin 48/38. Clone YD-ESP32-S3 ginge (~8 €), LED auf 48 + 5V-Dioden-Eigenheit |
| U2 | LD1117V33 | TO-220 | 1 | [Reichelt](https://www.reichelt.com/de/en/ldo-voltage-regulator-15-vin-3-3-vout-950-ma-to-220-ld1117v33-p216683.html) | 0,25 | ? | 3,3 V für Peripherie |
| U3, U4 | DRV8833-Breakout (Pololu 2130) | Sockel 2× 1×8 | 2 | [Eckstein](https://eckstein-shop.de/PololuDRV8833DualMotorDriverCarrierforTwoDCMotors12AperChannelEN) | 26,06 | ? | AliExpress-Variante ~2 €/St.: **nSLEEP muss hochgezogen sein**, Footprint erst nach Kauf final |
| U5 | MT3608-Boost (VM-Rail 9 V, optional) | Sockel | 1 | AliExpress/Amazon | ~2 | ? | AZ-Delivery ausverkauft. Vor Einbau auf 9 V trimmen. Unbestückt lassen, bis MF60T bei 5 V charakterisiert ist |
| U6 | C3-SuperMini-Reserve | Footprint, unbestückt | 0 | — | 0 | ✔ (vorhanden) | Lötjumper |
| U7 | Stepper-Treiber-Reserve (A4988-Raster) | Footprint, unbestückt | 0 | — | 0 | — | Lötjumper |
| D1 | SB540 Schottky | DO-201 | 1 | Reichelt | ~0,30 | ? | J_PWR → Rail; DevKit-Diode ist der zweite Zweig |
| F1 | Polyfuse 3 A (RXEF300) | radial | 1 | [Farnell](https://de.farnell.com/littelfuse/rxef300/polyswitch-sicherung-ptc-radial/dp/1345966) | ~0,50 | ? | |
| J1 | USB-C-Buchse 16-Pin, THT-Shell (GCT USB4085-GF-A) | THT | 1 | [TME](https://www.tme.eu/en/details/usb4085-gf-a/usb-ieee1394-connectors/gct/) | ~1 | ? | Nur 5 V; 2× 5,1 kΩ an CC1/CC2 |
| J2 | Wannenstecker IDC 2×15 + Buchse + Flachband 30-adrig 30 cm | DIN 41651 | 1 Set | Reichelt | ~5 | ? | |
| J3, J4 | Servo-Stecker JST-XH 3-Pin | THT | 2 | [eBay-Set](https://www.ebay.de/itm/335345792316) | ~2 | ? | |
| J5 | ARGB-Stecker JST-XH 3-Pin (5V/GND/Data) | THT | 1 | dito | ~1 | ✔ Streifen (Drohne) | generisch für jeden 5-V-WS2812-Streifen |
| J6 | BME680-Breakout-Sockel | 1×4 Buchse | 1 | — | 0 | ✔ BME680 | |
| J7 | Augen-Kabel-Stecker 10-Pin | 2,54 | 1 | Leistenware | ~0,50 | ? | |
| J8 | Reset/Boot nach außen | 2×2 | 1 | Leistenware | ~0,20 | ? | |
| C1 | 1000 µF/10 V (Rail) | radial | 1 | Reichelt | ~0,40 | ? | |
| C2, C3 | 100 µF (je DRV8833-VM) | radial | 2 | Reichelt | ~0,40 | ? | |
| C4 | 470 µF (Servo-Pfad) | radial | 1 | Reichelt | ~0,30 | ? | |
| C5 | 1000 µF (ARGB) | radial | 1 | Reichelt | ~0,40 | ? | |
| C6–C10 | 100 nF | RM 5 | 5 | Sortiment | ~0,50 | ? | |
| R1, R2 | 5,1 kΩ (CC) · R3/R4 10 kΩ (PSU_SENSE) · R5 330 Ω (ARGB) · R6/R7 4,7 kΩ (I²C) | axial | 7 | Sortiment | ~0,50 | ? | Sortiment ~10 € falls Box leer |

## Frontpanel

| Ref | Bauteil | Gehäuse | Stück | Quelle | Preis € | Bestand | Hinweis |
|---|---|---|---|---|---|---|---|
| FD1, FD2 | Behringer MF60T Motorfader (5er-Pack) | THT | 1 Pack | [Sweetwater US](https://www.sweetwater.com/store/detail/MOTORFADER--behringer-mf60t-motorized-faders-set-of-5-for-motor-controllers) | ~36 + Versand/Zoll | ? | **Kein EU-Händler gefunden (Thomann: nicht gelistet). Größtes Beschaffungsrisiko — eBay.de beobachten oder US-Import.** 10 kΩ linear, Motor 6–10 V |
| FD3, FD4 | MF60T | Footprint, DNP | 0 | (im 5er-Pack) | 0 | — | Reserve |
| SW1–SW10 | MX-Schalter linear (Gateron/Outemu) | THT | 10 | Keycapsss | ~4 | ? | |
| — | Kailh-Hot-Swap-Sockel MX | THT | 10 | [Keycapsss](https://keycapsss.com/Kailh-Hotswap-PCB-Sockets-10-pcs/KC10019-MX) | 1,80 | ? | **MX**, nicht Choc. Footprint-THT-Tauglichkeit in Task 11 prüfen, sonst direkt löten |
| — | DSA-Blank-Keycaps | — | 10 | [Keycapsss](https://keycapsss.com/keyboard-parts/keycaps/132/dsa-blank-pbt-1u-keycaps-for-mx-switches) / [eBay](https://www.ebay.de/itm/387005285864) | ~6 | ? | |
| ENC1 | EC11-Encoder mit Taster + Aluknopf | THT | 1 | AliExpress (~2) oder [Pimoroni PIM770](https://www.berrybase.de/en/pimoroni-picade-max-encoder-drehgeber-mit-druckfunktion-aluminium-drehknopf-ec11-encoder) (8,90) | 2–9 | ? | |
| U8 | MCP23017-E/SP + DIP-28-Sockel | DIP-28 | 1 | [Reichelt](https://www.reichelt.com/de/en/i-o-extension-16bit-1-8-5v-serial-i2c-dip-28-mcp-23017-e-sp-p140074.html) | 1,90 | ? | |
| U9 | MPR121-Breakout | Sockel | 1 | [BerryBase (Adafruit)](https://www.berrybase.de/en/adafruit-12-key-capacitive-touch-sensor-breakout-mpr121) | 8,75 | ? | Clone ~2 € geht; ADDR=GND |
| Q1 | BC337 (Backlight-Schalter) | TO-92 | 1 | Reichelt | ~0,10 | ? | |
| DSP1 | ILI9341 2,8" SPI 320×240 | Steckleiste 14-Pin | 1 | [Eckstein](https://eckstein-shop.de/28inch-TFT-Touchscreen-Display-Modul-ILI9341-240x320-mit-SPI-Schnittstelle-EN) | 10,00 | ? | EU-Ware meist MIT Touch — egal, Touch-Pins bleiben offen |
| — | RC-Filter: 4× 1 kΩ + 4× 100 nF · Encoder 2× 10 nF · Pull-up 10 kΩ | axial/RM5 | — | Sortiment | ~0,50 | ? | |
| J9/J10 | Steckleisten + IDC-Gegenstück | 2,54 | — | Leistenware | ~1 | ? | |

## Augen-Adapter + Kopf

| Ref | Bauteil | Gehäuse | Stück | Quelle | Preis € | Bestand | Hinweis |
|---|---|---|---|---|---|---|---|
| DSP2, DSP3 | GC9A01 1,28" rund, SPI, 7-Pin | Buchse | 2 | [makeroo](https://makeroo.de/products/1-28-zoll-rundes-tft-lcd-display-mit-spi-gc9a01-fur-arduino) ~6/St. · AliExpress ~3,50/St. | 7–12 | ? | |
| M1, M2 | MG90S Metallgetriebe | — | 2 | [roboter-bausatz.de](https://www.roboter-bausatz.de/p/mg90s-micro-servo-motor) | 7,90 | ? | Amazon/Ali voller Fakes |
| — | Pan-Tilt-Halter für MG90S | 3D-Druck | 1 | Printables/Thingiverse („SG90 pan tilt“) | 0 | — | Schrauben liegen Servos bei; alternativ Kit ~3 € AliExpress |
| J11–J13 | Stecker Augen-Adapter (10-Pin ein, 2× 7-Pin aus) | 2,54 | 3 | Leistenware | ~1 | ? | |

## Sonstiges

| Bauteil | Stück | Quelle | Preis € | Bestand | Hinweis |
|---|---|---|---|---|---|
| Panel-Mount-USB-C-Verlängerung (Buchse→Stecker, ~30 cm) | 1 | Amazon/AliExpress | ~5 | ? | Daten-Port Gehäuserückwand → DevKit-Buchse |
| Netzteil 5,1 V/3 A USB-C (Raspberry Pi 15 W) | 1 | [BerryBase/eBay](https://www.ebay.de/itm/177181865648) | ~10 | ? | No-Name „3 A“ liefert oft weniger |
| Buchsenleisten 1×40 zum Schneiden (für 1×22, 1×8) | 4 | Reichelt/AliExpress | ~3 | ? | 22er gibt es nicht fertig |
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
