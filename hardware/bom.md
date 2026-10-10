# Stückliste — final (Stand 2026-10-09, Preise inkl. MwSt.)

**Regel:** Alles, was auf die drei Platinen gelötet wird, kommt von **Reichelt** (Art.-Nr. am 2026-10-09 auf reichelt.de geprüft, alle „2–3 Werktage“). Gesteckte oder verkabelte Module kommen von **Amazon** oder aus dem Bestand. Kein SMD. Referenzen = KiCad.

## A · Reichelt — alles für die Platinen

| Ref | Bauteil | Reichelt Art.-Nr. | Stück | Preis € | Hinweis |
|---|---|---|---|---|---|
| U1, U3, U4, DSP1 | Buchsenleiste 1×40, 2,54 (schneiden: 2× 22 DevKit, 4× 8 DRV8833, 1× 14 Display) | BKL 10120978 | 3 | 9,54 | beim Schneiden geht je Schnitt ein Pin verloren |
| J3–J6, U5, J12–J18 | Stiftleiste 1×40, 2,54 (schneiden) | SL 1X40G 2,54 | 2 | 0,60 | 72 Pins gebraucht |
| J8 | Stiftleiste 2×2 (RST/BOOT) | ECON SL4G2 | 1 | 0,13 | |
| J1 | Leiterplattenklemme 4-pol., RM 5,08 (VBUS GND CC1 CC2) | MKDS 1,5 4 5,08 | 1 | 1,61 | Phoenix, passt 1:1 zum KiCad-Footprint |
| J2, J9 | Wannenstecker 2×15 gerade | HAN 530 6324 | 2 | 4,24 | |
| — | Pfostenbuchse 30-pol. (Kabel Mainboard ↔ Frontpanel) | HAN 530 6803 | 2 | 3,70 | |
| J7, J11 | Wannenstecker 2×5 gerade | WSL 10G | 2 | 0,30 | Augen-Kabel, verpolsicher |
| — | Pfostenbuchse 10-pol. | PFL 10 | 2 | 0,20 | |
| — | Flachbandkabel 40-pol., 28 AWG, 3 m | AWG 28-40G 3M | 1 | 6,96 | auf 30 bzw. 10 Adern abreißen |
| U2 | LDO 3,3 V, TO-220 | LD1117V33 | 1 | 0,25 | |
| D1 | Schottky 40 V/5 A, DO-201 | SB 540 DIO | 1 | 0,30 | |
| F1 | PTC 3 A (Haltestrom), radial | LITT RXEF300 | 1 | 1,00 | Shop nennt den Auslösestrom 6 A |
| U8 | MCP23017-E/SP, DIP-28 | MCP 23017-E/SP | 1 | 1,76 | |
| — | IC-Sockel DIP-28 schmal | GS 28P-S | 1 | 0,45 | |
| Q1 | BC327-25, TO-92 | BC 327-25 | 1 | 0,06 | Backlight high-side |
| C1, C5 | Elko 1000 µF/16 V, RM 5 | RAD 105 1.000/16 | 2 | 0,42 | |
| C4 | Elko 470 µF/16 V, RM 3,5 | NHG-A 470U 16 | 1 | 0,23 | Servos |
| C2, C3 | Elko 100 µF/16 V, RM 2,5 | HD-A 100U 16 | 2 | 0,80 | DRV8833-VM |
| C11 | Elko 10 µF/63 V, RM 2 | JAM TKP100M1JD11 | 1 | 0,05 | LD1117-Ausgang |
| C6, C7, C12, C15–C18, C20, C21 | Kerko 100 nF, RM 5 | KERKO 100N | 9 | 0,36 | |
| C13, C14 | Kerko 10 nF | KERKO 10N | 2 | 0,16 | Encoder-Entprellung |
| R1, R2 | 5,1 kΩ 0207 | METALL 5,10K | 2 | 0,14 | CC1/CC2 |
| R3, R8, R10, R17 | 10 kΩ 0207 | METALL 10,0K | 4 | 0,28 | |
| R4 | 15 kΩ 0207 | METALL 15,0K | 1 | 0,07 | PSU_SENSE → 3,0 V |
| R5 | 330 Ω 0207 | METALL 330 | 1 | 0,07 | ARGB-Daten |
| R6, R7 | 4,7 kΩ 0207 | METALL 4,70K | 2 | 0,20 | I²C-Pull-ups |
| R11, R13–R16 | 1 kΩ 0207 | METALL 1,00K | 5 | 0,35 | Backlight-Basis, Schleifer-RC |
| SW1–SW10 | Cherry MX Black, Fixierzapfen (PCB-Montage) | CHERRY MX2A-11NW | 10 | 4,50 | |
| ENC1 | ALPS-Drehgeber mit Taster, vertikal (EC11-Footprint) | STEC11B03 | 1 | 4,69 | 15 Impulse / 30 Rastungen |
| — | Knopf für 6-mm-Achse | KNOPF 20-6 SW | 1 | 2,92 | |
| H9–H12 | Abstandsbolzen M3 × 11, Innen/Außen | ECON D3X11A5MT | 4 | 0,72 | Display; M3-Schrauben/Muttern aus dem Sortiment |
| | | | **Summe** | **≈ 47 €** | + Versand ab 6,95 € |

Lötjumper JP1 (VM: 1-2 = 5 V ab Werk, 2-3 = Boost) und die Testpunkte TP1–TP3 sind Kupfer, keine Bauteile.

## B · Module — Amazon oder Bestand (verkabelt oder gesteckt)

| Ref | Modul | Quelle | Preis € | Hinweis |
|---|---|---|---|---|
| U1 | ESP32-S3-DevKitC-1 **N16R8** (Espressif) | Amazon | 19,99 | N8R8 (Reichelt ESP32S3DK-C1N8R8, ~17,50) passt genauso: gleiche Pins, Octal-PSRAM. USB-Buchse am Board prüfen (USB-C oder Micro-USB) → passendes Einbaukabel |
| U3, (U4) | DRV8833-Breakout **Pololu #2130** | Bestand prüfen, sonst Amazon ~10 | 0–10 | nur das Pololu-Layout (Reihen 10,16 mm, 16 Pins) passt in den Sockel; U4 erst für Fader 3/4 |
| DSP1 | 2,8" ILI9341 SPI, **MSP2807-Typ** (rote Platine, 14-Pin-Leiste, 4 Löcher 76,08 × 44) | Amazon | 14,11 | Touch-Pins bleiben unbelegt |
| J12, J13 | 2× GC9A01 1,28" rund, 7-Pin (VCC GND SCL SDA RES DC CS) | Amazon (2er-Pack) | 10,07 | per 7-poligem Dupont-Kabel (Buchse–Buchse) an die Stiftleisten |
| J18 | MPR121-Breakout (beliebig) | Amazon | 6,04 | per Kabel an J18; ADDR am Modul auf GND |
| U5 | Boost-Modul ~9 V (MT3608 o. ä.) | Amazon (Pack) | 6,04 | per 4 Drähten an U5; vor Anschluss einstellen, JP1 dann auf 2-3 |
| J1 | USB-C-Buchse als Breakout mit CC1/CC2-Pins | Amazon oder Reichelt (Soldered 333011, 1,77) | ~2 | in die Rückwand; 4 Drähte an J1. Hat das Breakout schon 5,1 kΩ an CC: CC-Drähte weglassen |
| — | USB-C-Einbauverlängerung Buchse → Stecker (~30 cm) | Amazon | 8,05 | Daten-Port Rückwand → DevKit |
| J14–J17 | Behringer X32 Motorfader-Set (5× 100 mm) | Amazon | 39,32 | Drähte an die 8-Pin-Leisten; Reichelt-Alternative: ALPS RSA0N11M9 100 mm (18,70 je Stück, Motor 4–10 V) |
| J3, J4 | 2× MG90S | Amazon | 14,10 | Servostecker passt direkt auf die Stiftleiste |
| — | Keycaps blank, MX-Stem | Amazon oder 3D-Druck | 10,04 | Reichelt führt keine |
| | | **Summe** | **≈ 130 €** | + ggf. DRV8833 |

## C · Bestand

| Bauteil | Verwendung |
|---|---|
| BME680-Breakout | per 4-poligem Kabel an J6 (3V3 GND SCL SDA) — sitzt hinter den Lüftungsschlitzen, weg von der ESP-Wärme |
| ARGB/WS2812-Streifen (Drohne) | Mund/Ampel hinter dem Visier, an J5 (5V GND DIN) |
| Netzteil 5 V/3 A USB-C | Strom über J1 |
| USB-C-Kabel | 2 Stück |
| CYD ESP32-2432S028R | nicht verbaut — Testgerät für LovyanGFX |

## Summe

Reichelt ≈ 47 € + Versand, Module ≈ 130 € → **≈ 185 €** ohne Platinen. JLCPCB (Sponsor) separat: drei Designs, je 5 Stück.
