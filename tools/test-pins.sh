#!/bin/sh
# Prüft pins.h: keine Dublette, keine Tabu-Pins, Schleifer auf ADC1, GPIO45 nur mit Loetjumper-Kommentar.
set -e
f="$(cd "$(dirname "$0")/.." && pwd)/firmware/arduino/deskmate/pins.h"
[ -f "$f" ] || { echo "FAIL: pins.h fehlt"; exit 1; }
nums="$(grep -E '^constexpr int PIN_' "$f" | sed -E 's/.*= ([0-9]+);.*/\1/')"
dup="$(printf '%s\n' "$nums" | sort -n | uniq -d)"
[ -z "$dup" ] || { echo "FAIL: doppelte GPIOs: $dup"; exit 1; }
for n in $nums; do
  case " 0 3 19 20 26 27 28 29 30 31 32 33 34 35 36 37 43 44 46 " in
    *" $n "*) echo "FAIL: Tabu-Pin $n belegt"; exit 1;;
  esac
done
for w in $(grep -E '^constexpr int PIN_FADER[0-9]_WIPER' "$f" | sed -E 's/.*= ([0-9]+);.*/\1/'); do
  [ "$w" -ge 1 ] && [ "$w" -le 10 ] || { echo "FAIL: Schleifer GPIO$w nicht auf ADC1"; exit 1; }
done
grep -E '^constexpr int PIN_BELLY_BL_PWM = 45; +// Loetjumper' "$f" >/dev/null || { echo "FAIL: GPIO45 ohne Loetjumper-Kommentar"; exit 1; }
echo "OK: pins"
