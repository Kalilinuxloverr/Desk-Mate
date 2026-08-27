# Desk-Mate — Design-Spec

**Datum:** 2026-08-22 · **Status:** von Leon im Chat abgenommen (Abschnitte 1–5), 18 Grill-Fragen beantwortet · **Relikt:** [`docs/relic/2026-08-22-original-prompt.md`](../../relic/2026-08-22-original-prompt.md)

Desk-Mate ist ein kleiner Wall-E-artiger Schreibtisch-Begleiter: eine Ampel für alles, was dich braucht (Claude Code, Downloads, Steam), ein Deck mit Motorfadern und Soft-Keys, ein Kopf mit zwei Augen-Displays — verbunden per USB, BLE und WiFi, steuerbar von Mac, Handy und Haus-MQTT.

Leitplanken aus dem Grilling: **eine PCB-Bestellung** (drei Designs, kein Re-Spin), **kein Hand-SMD** (Through-Hole + gesteckte Breakouts), **ein ESP32-S3**, **alles in v1**, **Dokumentation und Arbeitszeit ab Commit 1**.

---

## 1 · Entscheidungen (Kurzfassung)

| # | Frage | Entscheidung |
|---|---|---|
| 1 | v1-Umfang | Alles (A–E); Reihenfolge Plan → KiCad → Teile → JLCPCB → Rest |
| 2 | Mechanik | Base statisch, **kein Körper-Stepper**; Treiber-Sockel nur als Reserve |
| 3 | Hirn | **Ein ESP32-S3 DevKitC-1 N16R8**, gesteckt; C3 nur als unbestückter Footprint |
| 5 | Zentrale | Hybrid: USB → Desktop-Agent primär, BLE → Handy, Gerät auch standalone |
| 6 | Standalone | BLE-HID + Gesicht + **WiFi in v1** (MQTT, NTP, OTA, Wetter, Haus-Nodes) |
| 7 | Fader-Regelung | Eigene, einfache Regelung auf dem S3; DRV8833-Breakouts gesteckt. Fader: **Behringer X32-Ersatz, 100 mm, panel-mounted mit Kabel** (entschieden 2026-08-23) |
| 8 | Fader-Anzahl | 2 verbaut, 4 vorgesehen (5er-Set: +1 Ersatz) |
| 9 | Displays | 2× rund 1,28" GC9A01 (Augen) + 2,8" ILI9341 (Bauch), ein SPI-Bus |
| 10 | Tasten | 6 Soft-Keys + 4 Makro-Keys (MX, Hot-Swap) + EC11-Encoder; SmartKnob: Roadmap |
| 11 | Strom | 2× USB-C außen (Daten-Verlängerung / 5 V 3 A); Mainboard: Polyfuse + Schottky, DevKit-Diode als zweiter Zweig |
| 12 | Kopf | 2× MG90S Pan/Tilt, Easing, PWM-Aus im Ruhezustand |
| 13 | Claude | Claude-Code-**Hooks** (Status + Freigabe), Tastendruck nur als Fallback; generische Ereignisquellen |
| 14 | Agent | Swift-Menüleisten-App im Xcode-Projekt der iOS-App; Windows-Tray in Python (Phase 2); S3 = Composite-HID |
| 15 | Fernzugriff | MQTT (HiveMQ) + minimaler Server nur für APNs-Push (Vercel + Supabase) |
| 16 | Doku | Obsidian-Vault im Repo (`vault/`), Arbeitszeit per Session-Hooks |
| 17 | Git | SessionEnd-Hook commit + push, öffentlich ab Commit 1, Secret-Grep |
| 18 | Platinen | **Mainboard + Frontpanel + Augen-Adapter**, 2×15-IDC dazwischen |

Frage 4 (UART vs. ESP-NOW) entfiel mit dem C3. Jede Entscheidung hat eine Notiz in `vault/Entscheidungen/`.

---

## 2 · Hardware

### 2.1 Aufbau

```
 ┌─────────────────────┐
 │ KOPF  (pan/tilt)    │  Augen-Adapter-PCB → 2× GC9A01
 │                     │  WS2812-Ring (Ampel) · 2× MG90S im Hals
 ├─────────────────────┤
 │ BAUCH / DECK        │  FRONTPANEL-PCB
 │  [ 2,8" ILI9341 ]   │   6 Soft-Keys unter dem Display
 │  [k][k][k][k][k][k] │   4 Makro-Keys · EC11
 │  |F| [k][k] (o) |F| │   2(4)× MF60T · MCP23017 · MPR121
 │  |F|  [k][k]    |F| │
 ├─────────────────────┤
 │ BASE (statisch)     │  MAINBOARD-PCB
 │  USB-C(D) USB-C(P)  │   S3 DevKitC-1 · P-FET-ODER · LD1117V33
 │  BME680 hinter      │   2(4)× DRV8833 · Reserve: Stepper, C3
 │  Lüftungsschlitzen  │
 └─────────────────────┘
```

**Design-Richtung (Referenzbild `docs/design/2026-08-23-referenz-roboter.png`, Leon 2026-08-23):** weißes, rundes Gehäuse; der Kopf trägt **ein durchgehendes dunkles Visier**, hinter dem beide Augen-Displays leuchten (EVE-/Chatbot-Look, kein kantiger Wall-E); der **Mund ist die WS2812-Leiste hinter dem Visier** — im Ruhezustand türkises Lächeln, als Ampel grün/gelb/rot. Das Bedienpanel (Frontpanel) sitzt vorne **angewinkelt** (Arbeitsannahme 20°, wird am Druckteil geprüft). Stummelärmchen als feste Druckteile (keine Aktorik). Genaue Anordnung der Tasten/Fader wird beim Frontpanel-Layout mit Leon abgestimmt.

### 2.2 Platinen (drei Designs, eine JLCPCB-Bestellung)

**Mainboard (Base)** — 2 Lagen, **100 × 100 mm** (KiCad 2026-08-27; Rückwand = obere Kante: USB-C-Netzteilbuchse, BME680-Sockel, Testpunkte; DevKit links mit USB-Ende zur Rückwand, Antenne nach vorn über einer Kupfer-Sperrzone; IDC an der Vorderkante)
- Sockel für ESP32-S3-DevKitC-1 (2× 1×22 Buchsenleiste, 2,54 mm; Antennenseite über Platinenrand hinaus, nichts darüber)
- **Daten-Port** = Panel-Mount-USB-C-Verlängerung von der DevKit-USB-Buchse zur Gehäuserückwand (entschieden 2026-08-23: kein USB-Routing/ESD auf dem Mainboard, DevKit direkt flashbar). Auf dem Mainboard nur **J_PWR**: USB-C-Buchse 16-Pin THT, nur 5 V, CC1/CC2 mit 5,1 kΩ nach GND → 3 A vom Netzteil. Außen am Gehäuse bleiben zwei USB-C-Ports (Entscheidung 11)
- Versorgung (entschieden 2026-08-23, ersetzt P-FET-ODER): J_PWR → Polyfuse 3 A → **Schottky SB540** → 5-V-Rail; USB-Pfad speist die Rail über die **DevKit-eigene Diode** am 5V-Pin (Standard-Praxis, sperrt Rückspeisung zum Host). PSU_SENSE-Teiler **10 k/15 k** (→ 3,0 V bei 5 V; 10 k/10 k lägen mit 2,5 V zu nah an VIH) greift **vor** der SB540 ab → eindeutig „Netzteil da“. Rail liegt real bei ~4,6–4,7 V (Diodenabfall) — für Logik/Displays egal, für Fader-Motoren siehe VM-Boost-Sockel. Bulk 1000 µF/10 V an der Rail, LD1117V33 (TO-220) für 3,3-V-Peripherie (Displays, MCP23017, MPR121, BME680); DevKit-LDO versorgt nur den S3
- 2× Sockel für DRV8833-Breakout (Pololu #2130, 16-polig, Raster 10,16 mm) = 4 Motorkanäle; je 100 µF am VM-Pin; **VM-Rail per Lötjumper JP4: 5 V (Default) oder MT3608-Boost auf ~9 V** — das MT3608-Modul hat kein 2,54-Raster, deshalb 4-Pin-Stiftleiste U5 (VIN+ VIN− VOUT+ VOUT−) und Drähte statt Sockel (2026-08-27); nSLEEP beider Treiber über JP5 (gebrückt) an 3V3 — MF60T-Motor ist lt. Soundwell für 6–10 V spezifiziert, läuft bei 5 V nur langsamer (FaderBuddy-Praxis)
- 2× Servo-Stecker JST-XH 3-Pin (GND/5V/Signal), 470 µF direkt an den Steckern; der 10-Ω-Serienwiderstand ist gestrichen (2026-08-27: bei 0,7 A Stall fielen 7 V ab — Drosselung macht die Firmware über PSU_SENSE)
- WS2812/ARGB-Stecker 3-Pin (5 V, GND, Data über 330 Ω), 1000 µF lokal — generisch: beliebiger 5-V-ARGB-Streifen/Ring (Leons Drohnen-Streifen), LED-Anzahl per NVS, Strom-Cap in Firmware
- BME680-Breakout-Sockel 1×6 (VCC GND SCL SDA SDO CS, CJMCU-680-Reihenfolge — am Modul prüfen)
- I²C-Pull-ups 4,7 kΩ und IO_INT-Pull-up 10 kΩ sitzen auf dem Mainboard (2026-08-27: damit der Interrupt-Eingang auch ohne gestecktes Frontpanel definiert ist)
- Reserve C3-SuperMini: TX/RX über offene Lötjumper JP2/JP3 an UART0 (GPIO 43/44, geteilt mit dem CP2102); A4988-Sockel: STEP/DIR/EN über JP6–JP8 an FADER3_PWM/FADER3_DIR/FADER4_PWM (nur sinnvoll, wenn Fader 3/4 unbestückt bleiben)
- IDC 2×15 zum Frontpanel (Pinbelegung 2.4)
- Augen-/Servo-/WS2812-Kabel gehen vom Mainboard nach oben (Kopf ist am Bauch, Kabel durch Bauch-Rückwand)
- **Reserve, unbestückt:** Stepper-Treiber-Sockel (A4988/TMC2209-Standard-Footprint, 2× 1×8) mit STEP/DIR/EN auf Lötjumper; C3-SuperMini-Footprint (2× 1×8) mit 5 V, GND, UART-TX/RX auf Lötjumper
- Taster RESET und BOOT per Kabel/Pins nach außen führbar (DevKit-Taster liegen unter dem Gehäuse)

**Frontpanel (Deck)** — 2 Lagen, **120 × 136 mm** (KiCad 2026-08-27): ILI9341-Modul quer oben (x 17–103, y 6–56, Header links, 4× M3×11-Abstandshalter im MSP2807-Raster 76,08 × 44), darunter 6 Soft-Keys im 19,05-Raster, 4 Makro-Keys 2×2 mittig, Encoder rechts, MCP23017 links, MPR121-Sockel rechts, Fader-Header an den Seitenkanten, IDC an der Unterkante; die Fader sitzen links/rechts **neben** dem PCB im Panel. Anordnung ist ein Vorschlag — Leons Skizze entscheidet
- Fader: **Behringer X32-Ersatzfader, 100 mm, 5er-Set** (entschieden 2026-08-23, ersetzt MF60T 60 mm) — Metallrahmen wird ans Gehäuse-Panel geschraubt, Anschluss über die mitgelieferten Kabel auf 4× Header am PCB (Motor 2-polig, Poti/Touch mehradrig — Pinout bei Charakterisierung). Kein Fader-Footprint mehr → größtes Footprint-Risiko eliminiert. Deck wird durch den 100-mm-Fahrweg ~4–5 cm höher als mit 60ern
- 10× MX-kompatibler Schalter-Footprint (**THT, direkt gelötet** — Hot-Swap-Sockel gestrichen 2026-08-24: sind SMD), keine Dioden (kein Matrix-Scan, direkt am Expander)
- EC11-Encoder mit Taster
- MCP23017 (DIP-28) — Tasten 0–9, Encoder A/B/SW, Display-RST, Display-BL (on/off); INT_A/B → IDC
- MPR121-Breakout-Sockel (I²C) — Fader-Touch 0–3 (Kanal 4–11 frei, z. B. Touch am Kopf)
- Steckleiste für das 2,8"-ILI9341-Modul (14-Pin-Variante; SPI, ohne Touch-Pins), Display sitzt über den Soft-Keys. **Backlight-Schalter zweistufig:** Steuerleitung → 1 kΩ → BC337 (low-side) → 1 kΩ → BC327 (high-side an 3V3) → LED-Pin; 100 kΩ Pull-down an der Steuerleitung, 10 kΩ B-E am BC327. Grund: GPIO45 (Option über JP11/JP1) verträgt keinen Pull-up (Falle 13)
- MCP23017 RESET fest an 3V3, A0–A2 an GND (0x20), INTA über JP9 (gebrückt) und INTB über JP10 (offen) an IO_INT; Firmware setzt MIRROR=1, INT open-drain
- 4× Fader-Anschluss-Header (Motor + Schleifer + Touch), RC-Filter (1 kΩ / 100 nF) je Schleifer vor dem IDC
- IDC 2×15 zum Mainboard

**Augen-Adapter (Kopf)** — 2 Lagen, ca. 30 × 20 mm, nur Stecker
- 1× 10-Pin-Eingang (3V3, 3V3, GND, GND, MOSI, SCK, DC, CS_L, CS_R, GND — identisch zu J7 auf dem Mainboard)
- 2× 7-Pin-Buchse für GC9A01 (VCC GND SCL SDA RES DC CS), 100 nF je Modul
- **Reset per RC** (10 kΩ/1 µF an 3V3): es gibt keinen freien GPIO für DISP_RST zu den Augen; im Betrieb reicht der Software-Reset (LovyanGFX `pin_rst = -1`). Das Bauch-Display bekommt DISP_RST vom MCP23017
- 42 × 30 mm, nur Stecker + RC → kann keine Revision kosten

### 2.3 Pin-Map ESP32-S3 DevKitC-1 (N16R8)

Regeln: Schleifer nur auf **ADC1 (GPIO 1–10)** (ADC2 ist mit WiFi tot) · keine Strapping-Pins (0, 3, 45, 46) für Funktionen · 19/20 = USB · 26–37 = Flash/Octal-PSRAM (nicht nutzen) · 43/44 = UART0 zum CP2102 (Debug, frei lassen) · 38/48 = je nach DevKit-Revision die Onboard-RGB-LED.

Motoren laufen im **PWM + DIR**-Schema am DRV8833 (IN1 = PWM, IN2 = DIR; rückwärts mit invertiertem Duty = Drive/Brake). So braucht jeder Motor **einen** LEDC-Kanal; der S3 hat 8 LEDC-Kanäle → 4 Motoren + 2 Servos + 1 Backlight-Reserve = 7.

| GPIO | Funktion | Bus | Ziel | Hinweis |
|---|---|---|---|---|
| 1 | FADER1_WIPER | ADC1_CH0 | Frontpanel | RC-Filter |
| 2 | FADER2_WIPER | ADC1_CH1 | Frontpanel | |
| 4 | FADER3_WIPER | ADC1_CH3 | Frontpanel | Reserve |
| 5 | FADER4_WIPER | ADC1_CH4 | Frontpanel | Reserve |
| 6 | FADER1_PWM | LEDC | DRV8833 A-IN1 | 20 kHz (unhörbar) |
| 7 | FADER1_DIR | GPIO | DRV8833 A-IN2 | |
| 8 | FADER2_PWM | LEDC | DRV8833 B-IN1 | |
| 9 | FADER2_DIR | GPIO | DRV8833 B-IN2 | |
| 10 | FADER3_PWM | LEDC | DRV8833 #2 | Reserve |
| 11 | FADER3_DIR | GPIO | DRV8833 #2 | Reserve |
| 12 | FADER4_PWM | LEDC | DRV8833 #2 | Reserve |
| 13 | FADER4_DIR | GPIO | DRV8833 #2 | Reserve |
| 14 | SERVO_PAN | LEDC 50 Hz | Kopf | |
| 15 | SERVO_TILT | LEDC 50 Hz | Kopf | |
| 16 | SPI_MOSI | SPI2 | alle Displays | 40 MHz-fähig |
| 17 | I2C_SDA | I²C | MCP23017, MPR121, BME680 | 4,7 kΩ Pull-up auf 3V3 |
| 18 | I2C_SCL | I²C | dito | |
| 21 | IO_INT | GPIO in | MCP23017 INT (+ MPR121 IRQ, wired-OR) | Open-Drain, Pull-up |
| 38 | WS2812_DATA | RMT | Ampel-Ring | auf DevKit v1.1 spiegelt die Onboard-LED Pixel 0 — gewollt |
| 39 | SPI_SCK | SPI2 | alle Displays | JTAG-Default, frei wenn USB-JTAG |
| 40 | SPI_DC | GPIO | alle Displays | geteilt |
| 41 | CS_BELLY | GPIO | ILI9341 | |
| 42 | CS_EYE_L | GPIO | GC9A01 links | |
| 47 | CS_EYE_R | GPIO | GC9A01 rechts | |
| 45 | BELLY_BL_PWM | LEDC | ILI9341 LED-Pin | **Strapping (VDD_SPI):** nur über Lötjumper; Default = BL on/off am MCP23017. Kein externer Pull-up erlaubt |
| 48 | PSU_SENSE | GPIO in | Spannungsteiler an J_PWR-5V | „Netzteil da?“ (Onboard-LED auf DevKit v1.0 hängt hier — unkritisch) |
| 0, 3, 46 | — | | | Strapping, nicht belegen |
| 19, 20 | USB D−/D+ | USB | J_DATA | über DevKit-USB-Buchse oder direkt; Entscheidung bei Bauteilwahl |
| 43, 44 | UART0 | | CP2102 | Debug/Flash-Fallback |

Über den MCP23017 (Frontpanel): GPA0–GPA5 Soft-Keys 1–6 · GPA6–GPA7 + GPB0–GPB1 Makro-Keys 1–4 · GPB2 ENC_A · GPB3 ENC_B · GPB4 ENC_SW · GPB5 DISP_RST (alle Displays) · GPB6 BELLY_BL_EN · GPB7 frei. Encoder über INT-on-change ist für Handdrehung ausreichend (< 100 Flanken/s).

**Verifiziert 2026-08-23** gegen Datenblätter und DevKitC-1-Schaltplan — Details und Quellen: `vault/Hardware/Pin-Map.md`. GPIO 35–37 liegen am Header, bleiben aber unverbunden (Octal-PSRAM).

### 2.4 IDC 2×15 Mainboard ↔ Frontpanel

| Pin | Signal | Pin | Signal |
|---|---|---|---|
| 1 | 5V | 2 | 5V |
| 3 | GND | 4 | GND |
| 5 | 3V3 | 6 | 3V3 |
| 7 | MOT1+ | 8 | MOT1− |
| 9 | MOT2+ | 10 | MOT2− |
| 11 | MOT3+ | 12 | MOT3− |
| 13 | MOT4+ | 14 | MOT4− |
| 15 | GND | 16 | GND |
| 17 | WIPER1 | 18 | WIPER2 |
| 19 | WIPER3 | 20 | WIPER4 |
| 21 | GND | 22 | I2C_SDA |
| 23 | I2C_SCL | 24 | IO_INT |
| 25 | SPI_MOSI | 26 | SPI_SCK |
| 27 | SPI_DC | 28 | CS_BELLY |
| 29 | BELLY_BL_PWM | 30 | GND |

Motorleitungen liegen zwischen GND-Paaren (Störungen), Schleifer ebenfalls. DRV8833 bleiben auf dem Mainboard (kurzer Strompfad zum Bulk-Elko); 0,2–0,6 A pro Motor über 28-AWG-Flachband ist im Rahmen (≤ 1 A/Ader).

### 2.5 Strombudget (5 V)

| Verbraucher | typ. | Spitze | Anmerkung |
|---|---|---|---|
| ESP32-S3 DevKit (WiFi + BLE) | 0,25 A | 0,5 A | |
| 2× X32-100-mm-Fader-Motor | 0,3 A | 1,2 A | Annahme MF60T-Klasse; bei Charakterisierung messen |
| 2× MG90S | 0,3 A | 1,4 A | Stall 0,7 A je; PWM aus im Ruhezustand |
| ILI9341 2,8" (Backlight) | 0,15 A | 0,15 A | |
| 2× GC9A01 | 0,08 A | 0,08 A | |
| WS2812 × 12 | 0,2 A | 0,72 A | Firmware-Cap 50 % → 0,36 A |
| Rest (Expander, Sensoren) | 0,02 A | 0,02 A | |
| **Summe** | **~1,3 A** | **~3,7 A theor. / ~2,5 A real** | Motoren und Servos werden nicht gleichzeitig mit vollem Duty gefahren (Firmware-Regel) |

→ 5 V/3 A Netzteil, Polyfuse 3 A, Bulk 1000 µF + je 100 µF an Motortreibern + 470 µF an Servos. Bei 4 Fadern: Budget erneut rechnen; ggf. 5 V/4 A.
→ Ohne Netzteil (nur J_DATA am Rechner): `PSU_SENSE` low → Firmware fährt Motoren/Servos gedrosselt (Duty ≤ 40 %, nie gleichzeitig) oder gar nicht („Netzteil-Modus“ konfigurierbar).

### 2.6 Gehäuse (3D-Druck)

- Stil nach Referenzbild (§2.1): weiße Schalen, Kopf mit dunklem Visier (getönt gedrucktes/Acryl-Fenster) über beiden Augen und der WS2812-Mund-Leiste; Frontpanel um ~20° angewinkelt
- Drei Baugruppen: Base (Mainboard, USB-Buchsen hinten, Lüftungsschlitze für BME680, Gummifüße), Bauch (Frontpanel angewinkelt, Display-Fenster, Tastenausschnitte, Fader-Schlitze, Stummelärmchen fest), Kopf (Visier, Augen, Pan-Tilt-Halter für MG90S — Standard-Halter, STL frei verfügbar)
- Kabelführung: ein Strang Base → Bauch (IDC), ein Strang Bauch → Kopf (Augen 10 Adern + WS2812 3 Adern); Servos sitzen im Bauch/Hals, nicht im Kopf
- Alle Teile als STEP + STL, je Teil eine Datei, deutsche Dateinamen wie beim Kühler (`Kopf_Schale_vorne.stl`); Druckparameter in `hardware/3d/README.md`
- Fader-Kappen: X32-Kappen sind dabei; Touch über Draht/Federkontakt an die Metallachse (MPR121)
- Deck-Höhe: 100-mm-Fader (~13 cm Körper) bestimmen das Panel — Winkel ~20°, Fader längs im Panel

### 2.7 Bauteile, die Leon schon hat

BME680-Breakout, WS2812-Breakout, C3 SuperMinis, CYD, „Arduino-Box“ (Inventur nach dem Urlaub, Ende August 2026). Die Bauteilwahl (Plan-Task) gleicht die BOM gegen diese Inventur ab, bevor bestellt wird.

---

## 3 · Firmware (ESP32-S3, arduino-cli, ein Sketch)

`firmware/arduino/deskmate/` mit `project.json` (arduino-cli-Workflow, Core-Version gepinnt), FQBN `esp32:esp32:esp32s3` mit USB-Modus für natives USB (HID + CDC), `PartitionScheme` mit OTA + großem App-Slot, PSRAM `opi`.

**Module (je eine `.cpp/.h`, kein Framework):**

| Modul | Aufgabe | Bibliothek |
|---|---|---|
| `hid` | Composite-USB-HID: Tastatur + Consumer (Lautstärke/Media) + Gamepad (Fader = Achsen); dieselben Reports über BLE-HID | ESP32-Arduino `USBHIDKeyboard/USBHIDConsumerControl/USBHIDGamepad`, NimBLE-HID |
| `link` | Serielles JSON-Zeilenprotokoll zum Agent über USB-CDC (parallel zu HID), versioniert (`{"v":1,...}`), fester Puffer 512 B, Zeile zu lang → verwerfen + Fehlerzähler (VVVF-Lektion) | ArduinoJson |
| `net` | WiFi-STA, NTP, MQTT (HiveMQ TLS, `deskmate/#`), OTA (ArduinoOTA oder HTTP-Update), Wetter (Topic der Wetterstation + optional Open-Meteo) | WiFiClientSecure, PubSubClient |
| `face` | Augen (2× GC9A01): Blinzeln, Blickrichtung, Emotionen; Bauch: Seiten *Gesicht / Claude / Downloads / Wetter / Haus / Einstellungen*; Soft-Key-Labels; Encoder-Navigation | LovyanGFX (ein Bus, drei Panels) |
| `motion` | Fader-P-Regler mit Totband + Touch-Stopp + Rasten/Endanschlag-Haptik (FaderBuddy-Verhalten); Servo-Easing, PWM-Aus nach Stillstand | ESP32Servo oder LEDC direkt |
| `io` | MCP23017 (Tasten, Encoder, RST/BL), MPR121 (Touch), BME680 | Adafruit MCP23X17, Adafruit MPR121, Adafruit BME680 |
| `state` | Eine Ampel-Zustandsmaschine: `idle` (grün) / `busy` (gelb) / `needs_you` (rot) / `needs_you_urgent` (rot blinkend) mit Quelle und Text; Ereignisse aus `link`, `net`, lokalen Tasten | — |
| `config` | NVS: Tastenbelegung (HID-Keycodes/Makros), Fader-Layer, WiFi/MQTT-Credentials (nie im Code, `secrets.h` gitignored) | Preferences |

**Pflichtregeln (aus dem Kühler-Fallen-Log):** NimBLE statt Bluedroid · `WiFi.setSleep(false)` · kein großes Vollbild-Sprite, Panels direkt zeichnen (PSRAM erlaubt Sprites, aber erst messen) · Watchdog aktiv · keine Structs/Default-Args in `.ino`-Signaturen (alle Logik in `.cpp`) · jede Protokolländerung = Versionsnummer hoch + Parser-Test.

**Test:** `firmware/arduino/deskmate/test/` mit einem Host-kompilierbaren Test für das Zeilenprotokoll und die Zustandsmaschine (plain C++, `assert`, kein Framework). Build-Befehl steht in CLAUDE.md und ist vor jedem „fertig“ auszuführen.

---

## 4 · Agent und Apps (Swift, ein Xcode-Projekt via XcodeGen)

```
app/
  project.yml
  DeskMateCore/        Swift Package: Modelle, Protokoll (Serial-JSON, MQTT-Topics), Einstellungen, Ereignisse
  DeskMateMac/         Menüleisten-App (SwiftUI, AppKit-Statusitem)
  DeskMateiOS/         iPhone-App (SwiftUI); später Widgets/Live Activity, Watch
  Tests/
```

**macOS-Agent** (Menüleiste, läuft beim Login):
- `SerialLink`: findet Desk-Mate über USB-CDC (Vendor/Product-ID des S3, Gerätename), Reconnect
- `EventHub`: lokaler HTTP-Server auf `127.0.0.1:4821` — `POST /event {source, state, text, ttl}` (Claude-Hooks, Skripte), `POST /await-ack` (blockierend bis Taste, mit Timeout), `GET /state`
- `Watchers`: `~/Downloads` (FSEvents; `.crdownload/.download/.part` → läuft; verschwindet → fertig), Steam (`~/Library/Application Support/Steam/steamapps/appmanifest_*.acf`, Felder `BytesDownloaded`/`BytesToDownload`, Rate über 30 s → Restzeit)
- `Keystroke`: Fallback für Trust-Dialog/AskUserQuestion: Terminal-App (Terminal/iTerm/VS Code/Ghostty — konfigurierbar) aktivieren, `CGEvent` senden; braucht Accessibility-Recht, wird beim ersten Start erklärt
- `Screen`: Screenshot auf Anfrage (Screen-Recording-Recht), skaliert auf 800 px, JPEG → MQTT `deskmate/screen` (nicht retained, oder retained mit TTL per Leer-Publish nach 60 s)
- `MQTT`: publiziert `deskmate/state`, `deskmate/downloads`, abonniert `deskmate/cmd`
- Einstellungen: Tastenbelegung, Fader-Zuweisung (Lautstärke / Gamepad-Achse / App-spezifisch), Watcher an/aus, Terminal-App, MQTT-Zugang — werden ans Gerät geschrieben (`link`) und gespiegelt in `UserDefaults`

**iOS-App:** Ampel + Quelle + Text, Buttons *Weiter / Nein / Screenshot*, Downloads-Liste mit Restzeit, Gerätekonfiguration (BLE direkt, wenn am Tisch; sonst MQTT), Verbindungsstatus. Push: Vercel-Function `POST /api/push` (vom Agent aufgerufen, mit Shared-Secret) → APNs; Gerätetokens in Supabase-Tabelle `deskmate_devices`. Ohne Push bleibt alles funktionsfähig (MQTT bei offener App).

**Windows (Phase 2):** `agent-windows/deskmate_tray.py` — pyserial + watchdog + pystray + kleiner HTTP-Server; derselbe Ereignis-Endpunkt, dieselbe Serial-Protokollversion. Gamepad/Media-Keys brauchen keinen Agent.

---

## 5 · Claude-Code-Integration (Hooks) — verifiziert gegen die Doku am 2026-08-22

Quelle: https://code.claude.com/docs/en/hooks.md. Global in `~/.claude/settings.json` (gilt für alle Projekte), Skript `tools/deskmate-hook.sh` im Repo. Jeder Hook ruft nur `curl -s localhost:4821/...` auf und ist in < 50 ms fertig — außer dem Freigabe-Hook, der wartet. Hooks erhalten JSON auf stdin (`hook_event_name`, `session_id`, `cwd`, bei Notification `notification_type`), `$CLAUDE_PROJECT_DIR` ist gesetzt.

| Ereignis | Matcher | Aktion | Ampel |
|---|---|---|---|
| `UserPromptSubmit` | — | `POST /event {source:"claude", state:"busy", cwd}` | gelb |
| **`PermissionRequest`** | Tool-Name (z. B. `Bash`, `Write`, `Edit`, `*`) | `POST /await-ack` mit Timeout *T* (z. B. 45 s, `timeout` im Hook-Eintrag etwas höher). Taste **Weiter** → Hook antwortet `{"hookSpecificOutput":{"hookEventName":"PermissionRequest","permissionDecision":"allow","permissionDecisionReason":"Desk-Mate Taste"}}`; Taste **Nein** → `deny`; Timeout → `escalate` (normaler Prompt) | rot, bis Taste |
| `Notification` | `permission_prompt`, `idle_prompt`, `agent_needs_input` | `POST /event {state:"needs_you_urgent", text:<notification_type>}` | rot blinkend |
| `PreToolUse` | `AskUserQuestion` | `POST /event {state:"needs_you", text:<Frage aus tool_input>}` — ob `tool_input` die Frage trägt, ist **nicht dokumentiert** → beim Bau testen | rot |
| `Stop` | — | `POST /event {state:"idle", text:"fertig"}` | grün + Freude-Animation |
| `SessionStart` / `SessionEnd` | — | projektlokal (Zeiterfassung, commit/push), siehe 6 | — |

Nicht abfangbar (verifiziert): der Trust-Dialog beim Start feuert vor allen Hooks. Für ihn und für `AskUserQuestion`-Antworten bleibt der Tastendruck-Fallback des Agents. `permissionDecision` kennt `allow | deny | escalate` (nicht „ask“). Ein maximaler Hook-Timeout ist nicht dokumentiert → im Plan: mit 60 s testen, Ergebnis in `CLAUDE.md` → Bekannte Fallen.

Sicherheits-Regel: Der Freigabe-Hook gibt **nur** frei, was Claude Code ohnehin per Prompt gefragt hätte, und nur für den aktuellen Aufruf. Keine Pauschal-Freigaben; `deny` ist immer eine Taste entfernt.

---

## 6 · Projekt-Infrastruktur (ab Commit 1)

```
Desk-Mate/
  README.md                 Template (Was · Architektur-ASCII · Pfadtabelle · Bauen)
  CLAUDE.md                 Architektur · Build & Test · Bekannte Fallen · Konventionen · Session-Pflichten
  LICENSE                   MIT (Hardware-Teile CERN-OHL-P wäre Alternative — Entscheidung Leon)
  .gitignore                secrets.h, .env, *.local.xcconfig, .obsidian/workspace*, Build-Ordner, KiCad-Backups
  .claude/settings.json     SessionStart/SessionEnd-Hooks (Zeiterfassung, commit+push)
  tools/                    session-start.sh, session-end.sh, check-secrets.sh (pre-commit), deskmate-hook.sh
  docs/relic/               Ursprungs-Prompt (unveränderlich)
  docs/superpowers/specs/   dieser Spec
  docs/superpowers/plans/   Implementierungsplan
  docs/anleitung/           Bauanleitung (wächst mit den Tasks)
  docs/logo/                Logo SVG + PNG
  vault/                    Obsidian-Vault: Log/ Entscheidungen/ Hardware/ Firmware/ Apps/ Bestellungen/ Index.md
  hardware/kicad/{mainboard,frontpanel,eye-adapter}/
  hardware/3d/
  hardware/bom.md
  firmware/arduino/deskmate/
  app/
  agent-windows/
  server/                   Vercel-Function für APNs
```

**Arbeitszeit:** `SessionStart`-Hook schreibt `- start HH:MM` in `vault/Log/YYYY-MM-DD.md` (legt Datei mit Frontmatter an, wenn fehlt); `SessionEnd`-Hook schreibt `- ende HH:MM (N min)` und summiert `dauer_min` im Frontmatter. Claude ergänzt im selben Tagesblatt *Was ist passiert* (Pflicht laut CLAUDE.md).
**Push:** `SessionEnd`-Hook: `git add -A && git commit -m "Session YYYY-MM-DD HH:MM: <erste Zeile aus Was-ist-passiert>" && git push` — nur wenn `check-secrets.sh` sauber ist (Grep nach `ssid|password|passwd|token|apikey|secret` mit Wert ≠ Platzhalter in getrackten Dateien außer `*.example.*`). Hook-Timeout 120 s; Push-Fehler landen in `vault/Log/` statt die Session zu blockieren.
**Sponsoring:** jede Bestellung als `vault/Bestellungen/YYYY-MM-DD-<lieferant>.md` (Positionen, Kosten, Lieferzeit, Fotos skaliert ≤ 1 MB); daraus entsteht später die Case-Study. Leon benachrichtigt JLCPCB selbst — Claude erinnert im Tagesblatt.
**Website:** Eintrag P12 im Portfolio (Supabase `projects.items`), sobald das erste echte Foto existiert — Task am Ende von Phase „Hardware aufgebaut“.

---

## 7 · Roadmap (nicht v1)

SmartKnob als externes Gerät über MQTT/USB · watchOS-App (Ampel am Handgelenk) · Android-App · iPadOS · Home-Assistant-Discovery-Payloads · Körper-Stepper (Sockel ist da) · 4 Fader bestücken · Lern-Funktion (Arbeitsrhythmus → Pausen-Erinnerung; erst wenn Log-Daten da sind) · Backlight-Dimmen über GPIO 45 · Windows-Tray.

---

## 8 · Offene Punkte (werden im Plan als Tasks geführt)

1. ~~Pin-Map prüfen~~ erledigt 2026-08-23: alles verifiziert, siehe `vault/Hardware/Pin-Map.md` und `firmware/arduino/deskmate/pins.h`. Neu offen: **X32-Fader charakterisieren, sobald geliefert (Di 25.08.):** Kabel-Pinout, Motorspannung/-strom bei 5 V (Anlauf/Stall), Touch-Kontaktierung, Rahmen-Maße + Schraubpunkte für Panel/3D-Druck → erst danach Frontpanel-Layout und VM-Rail final.
2. ~~USB-Daten~~ erledigt 2026-08-23: Panel-Mount-USB-C-Verlängerung zur DevKit-Buchse (§2.2).
3. ~~ODER-Stufe~~ erledigt 2026-08-23: Polyfuse + SB540 + DevKit-Diode, kein P-FET (§2.2).
4. ~~HiveMQ-Free-Tier~~ erledigt 2026-08-23: max. Nachrichtengröße 5 MB (Quelle: community.hivemq.com/t/maximum-message-size/3087) → 800-px-Screenshots unkritisch.
5. `PreToolUse`/`AskUserQuestion`: trägt `tool_input` die Frage? Maximaler Hook-Timeout? → testen.
6. Lizenz (MIT vs. CERN-OHL für Hardware) — Leon.
7. Leons Skizze nachreichen → Frontpanel-Anordnung (KiCad-Vorschlag vom 2026-08-27 steht, siehe §2.2; Änderung = Positionen in `hardware/kicad/gen/boards.py`).
8. Vor der JLCPCB-Bestellung am echten Teil nachmessen (2026-08-27): C3-SuperMini-Reihenabstand 15,24, MPR121-Clone 17,78, DRV8833-Module aus der Box = Pololu-Raster 10,16?, BME680-Pinreihenfolge. DevKit-Sockel 22,86 ist per Espressif-DXF belegt. Details `vault/Hardware/Module-Masse.md`.
