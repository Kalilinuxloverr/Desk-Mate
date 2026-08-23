# Pin-Map ESP32-S3 DevKitC-1 — verifiziert 2026-08-23

Code-Wahrheit: `firmware/arduino/deskmate/pins.h` (Test: `sh tools/test-pins.sh`). Spec §2.3 ist deckungsgleich.

## Quellen
- [DevKitC-1 v1.1 User Guide](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html) + [Schaltplan V1.1](https://dl.espressif.com/dl/schematics/SCH_ESP32-S3-DevKitC-1_V1.1_20221130.pdf)
- [ESP32-S3-WROOM-1 Datenblatt](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) · [ESP32-S3 Datenblatt](https://www.espressif.com/documentation/esp32-s3_datasheet_en.pdf)
- [ESP-IDF ADC-Doku](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/adc/adc_oneshot.html) · [LEDC-Doku](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/ledc.html)

## Verifiziert
- **Alle geplanten GPIOs liegen am Header** (J1 + J3), inkl. 19/20 (USB D−/D+) und 43/44 (UART0 → CP2102N-A02-GQFN28).
- **Onboard-RGB-LED:** v1.0 = GPIO 48, v1.1 = GPIO 38 (0-Ω-Widerstand R17). Keine offizielle äußere Erkennung — beim ersten Boot ausprobieren. v1.1: LED spiegelt unser Pixel 0 (gewollt). v1.0: LED hängt am PSU_SENSE-Knoten (GPIO 48) — Digital-Read bleibt gültig, Teiler 10k/10k ist niederohmig genug.
- **Octal-PSRAM (N16R8):** GPIO 35/36/37 intern belegt → am Sockel **unverbunden lassen** (liegen am Header!).
- **Strapping:** 0 (Pull-up, Boot), 3 (JTAG-Sel, per eFuse-Default ignoriert), 45 (VDD_SPI: **nie high beim Boot**, danach frei — deshalb Backlight nur per Lötjumper), 46 (Pull-down, danach frei). **48 ist kein Strapping-Pin.** Latch-Zeit ≥ 3 ms nach Reset.
- **ADC:** ADC1_CH0–9 = GPIO 1–10, ADC2 = 11–20 (mit WiFi unbrauchbar). Schleifer auf 1/2/4/5 ✓.
- **LEDC:** 8 Kanäle, 4 Timer, nur Low-Speed. Belegt: 4 Motor + 2 Servo + 1 BL = 7.
- **JTAG 39–42:** frei, solange USB-Serial-JTAG (eFuse-Default) genutzt wird.

## Flags für Bauteilwahl / Firmware
1. **MF60T-Motor:** Behringer nennt keine Motorspannung; Soundwell-60-mm-Referenz sagt **6–10 V** ([soundwell.hk](https://www.soundwell.hk/soundwell-60mm-motorized-slide-potentiometer.html), mittlere Konfidenz). FaderBuddy fährt ihn mit 5 V (funktioniert, langsamer). → Mainboard bekommt **VM-Lötjumper: 5 V (Default) oder unbestückter Boost-Sockel (MT3608-Breakout, 2×4-Pin) auf ~9 V**. Motor vor dem Layout am Netzteil charakterisieren (Anlauf, Stall bei 5 V).
2. **DRV8833-Breakout:** Pololu #2130 ist 16-polig (VIN/VMM getrennt, AISEN/BISEN nach GND, nSLEEP high). Bei Noname-Breakouts prüfen, ob nSLEEP hochgezogen ist. Footprint erst nach Kauf final.
3. **Fader-Track 10 kΩ linear** ✓ (Behringer-Produktseite) — RC 1 kΩ/100 nF passt.
4. **LED-Ausgang ist generisch:** 3-Pin-Buchse 5V/GND/Data für jeden WS2812/ARGB-Streifen (Leon hat einen aus einer Drohnen-Bestellung). Anzahl LEDs = NVS-Konfig, Strom-Cap in Firmware.
