---
datum: 2026-08-27
typ: hardware
---
# Modul-Maße für die Sockel-Footprints (Recherche 27.08.2026)

Was der Generator (`hardware/kicad/gen/boards.py`) annimmt, woher es kommt, wie sicher es ist. **Alles mit „mittel/niedrig“ vor dem Löten am echten Teil nachmessen.**

| Modul | Maß im Footprint | Quelle | Konfidenz |
|---|---|---|---|
| ESP32-S3-DevKitC-1 v1.1 | Reihen 22,86 mm, 2×22, Pitch 2,54; PCB 62,74 × 25,40; letzter Pin 8,00 mm von der USB-Kante, erster Pin 1,40 mm von der Antennenkante; **Pin 1 beider Header am Antennenende** | Espressif DXF v1.1 (`dl.espressif.com/dl/schematics/esp_idf/DXF_ESP32-S3-DevKitC-1_V1.1_20220429.pdf`), Espressif KiCad-Footprint | hoch |
| DevKit Pinreihenfolge | J1: 3V3 3V3 RST 4 5 6 7 15 16 17 18 8 3 46 9 10 11 12 13 14 5V G · J3: G TX RX 1 2 42 41 40 39 38 37 36 35 0 45 48 47 21 20 19 G G | User Guide v1.1 (`…/user_guide_v1.1.html`, der „latest“-Link liefert 404) | hoch |
| Pololu DRV8833 #2130 | 12,7 × 20,3 mm, Reihen 10,16, Löcher Ø1,02; Draufsicht GND-Ende oben: links GND VMM BIN1 BIN2 AIN2 AIN1 nSLEEP nFAULT, rechts GND VIN BOUT1 BOUT2 AOUT2 AOUT1 AISEN BISEN | Pololu Maßzeichnung 0J1615, Pinout-Bild 0J3866 | hoch |
| Pololu A4988 (Reserve) | 15,2 × 20,3 mm, Reihen 12,70; A: ENABLE MS1 MS2 MS3 RESET SLEEP STEP DIR, B: VMOT GND 2B 2A 1A 1B VDD GND | Pololu Maßzeichnung 0J1082 | hoch |
| ESP32-C3 SuperMini (Reserve) | 22,5 × 18 mm, Reihen 15,24; links 5 6 7 8 9 10 20 21, rechts 5V GND 3V3 4 3 2 1 0 | ProtoSupplies, lastminuteengineers (Fotos, kein Datenblatt) | mittel |
| MPR121-Breakout (Clone) | 20,3 × 30,5 mm, Reihen 17,78; Elektroden ELE0–11 auf einer Längskante, Steuerpins 3.3V IRQ SCL SDA ADD GND gegenüber ELE8…ELE3 | SparkFun Eagle-Daten (Clone = 1:1) | hoch (SparkFun) / mittel (Clone) |
| ILI9341 2,8" MSP2807 | PCB 50 × 86 × 1,6 mm; 4 Löcher Ø3,2 im Raster 44 × 76,08, 3 mm von den Längskanten; Header 14-pol. an der kurzen Kante, Reihe 2,0 mm vom Rand, Pin 1 8,49 mm von der Ecke; Header ragt 11,17 mm unter das PCB → **M3×11-Abstandshalter** | LCDWIKI MSP2807_Size.pdf | hoch |
| GC9A01 1,28" 7-pol. | VCC GND SCL SDA RES DC CS, Pitch 2,54; Modul ~38 × 45 mm; **keine Montagelöcher dokumentiert** | ProtoSupplies, cb-electronics | mittel |
| MT3608-Modul | 36 × 17 mm, Löcher **nicht** 2,54-kompatibel (Paar 6,45–6,8 mm, Ende-zu-Ende 30,5–31) → deshalb 4-Pin-Stiftleiste + Drähte statt Sockel | components101, Community-Footprints | niedrig |
| Behringer X32-Fader 100 mm | Poti-Körper mit 8 Lötpins (Muster 2-1-1-2 / 4-3-3-4), Motor separat 2 Pins, **kein Touch-Kontakt**, kein Kabel/Stecker → Drähte an die 8-Pin-Stiftleiste J14–J17; Touch = Draht an Metallhebel/Kappe | Arduino-Forum, EEVblog (Community) | niedrig — **charakterisieren, sobald geliefert** |
| GCT USB4085-GF-A | 16-Kontakt-USB-2.0-Buchse, **komplett THT** (keine 6-Pin-Power-Only-THT bei GCT), 5 A, Right-Angle; KiCad `Connector_USB:USB_C_Receptacle_GCT_USB4085` | GCT-Zeichnung usb4085.pdf | hoch |

Nicht gefunden: GC9A01-Montagelöcher, MT3608-Herstellerzeichnung, X32-Pinout.
