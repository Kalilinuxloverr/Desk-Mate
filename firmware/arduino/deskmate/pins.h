// Desk-Mate — verifizierte Pin-Map (2026-08-23). Quellen: vault/Hardware/Pin-Map.md, Spec §2.3.
// Board: ESP32-S3-DevKitC-1 (WROOM-1-N16R8). Aenderungen nur mit Spec-Update.
#pragma once

// Fader (Schleifer zwingend ADC1 = GPIO1-10; ADC2 ist mit WiFi unbrauchbar)
constexpr int PIN_FADER1_WIPER = 1;   // ADC1_CH0, RC-Filter auf Frontpanel
constexpr int PIN_FADER2_WIPER = 2;   // ADC1_CH1
constexpr int PIN_FADER3_WIPER = 4;   // ADC1_CH3, Reserve (DNP)
constexpr int PIN_FADER4_WIPER = 5;   // ADC1_CH4, Reserve (DNP)
constexpr int PIN_FADER1_PWM = 6;     // LEDC 20 kHz -> DRV8833 A-IN1
constexpr int PIN_FADER1_DIR = 7;     // GPIO -> DRV8833 A-IN2
constexpr int PIN_FADER2_PWM = 8;     // LEDC -> DRV8833 B-IN1
constexpr int PIN_FADER2_DIR = 9;     // GPIO -> DRV8833 B-IN2
constexpr int PIN_FADER3_PWM = 10;    // Reserve
constexpr int PIN_FADER3_DIR = 11;    // Reserve
constexpr int PIN_FADER4_PWM = 12;    // Reserve
constexpr int PIN_FADER4_DIR = 13;    // Reserve

// Kopf
constexpr int PIN_SERVO_PAN = 14;     // LEDC 50 Hz
constexpr int PIN_SERVO_TILT = 15;    // LEDC 50 Hz
constexpr int PIN_WS2812_DATA = 38;   // RMT, Mund/Ampel; DevKit v1.1: Onboard-LED spiegelt Pixel 0 (gewollt)

// Displays (ein SPI-Bus, drei Panels)
constexpr int PIN_SPI_MOSI = 16;
constexpr int PIN_SPI_SCK = 39;       // JTAG-Default; frei, da USB-Serial-JTAG (eFuse-Default)
constexpr int PIN_SPI_DC = 40;
constexpr int PIN_CS_BELLY = 41;
constexpr int PIN_CS_EYE_L = 42;
constexpr int PIN_CS_EYE_R = 47;
constexpr int PIN_BELLY_BL_PWM = 45;  // Loetjumper! Strapping VDD_SPI: darf beim Boot nie high sein. Default: BL ueber MCP23017 GPB6 + Transistor.

// I2C (MCP23017 0x20, MPR121 0x5A, BME680 0x76/0x77)
constexpr int PIN_I2C_SDA = 17;
constexpr int PIN_I2C_SCL = 18;
constexpr int PIN_IO_INT = 21;        // MCP23017-INT + MPR121-IRQ, wired-OR (Open-Drain, Pull-up)

// Versorgung
constexpr int PIN_PSU_SENSE = 48;     // Teiler an J_PWR-5V; DevKit v1.0: Onboard-LED haengt hier (unkritisch)

// Tabu: 0, 3, 46 (Strapping), 19/20 (USB), 26-34 (Flash), 35-37 (Octal-PSRAM, unverbunden lassen), 43/44 (UART0/CP2102N)
