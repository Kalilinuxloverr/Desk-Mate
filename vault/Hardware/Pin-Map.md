# Pin-Map ESP32-S3 DevKitC-1

Bis Plan-Task 7 erledigt ist, gilt ausschließlich Spec §2.3:
[docs/superpowers/specs/2026-08-22-desk-mate-design.md](../../docs/superpowers/specs/2026-08-22-desk-mate-design.md)

Task 7 legt hier die gegen Datenblatt und DevKitC-1-Schaltplan verifizierte Tabelle ab (Spalte „verifiziert + Quelle“) und erzeugt `firmware/arduino/deskmate/pins.h`.

Zu prüfen: Onboard-RGB-LED-Pin je DevKit-Revision (38 vs. 48) · GPIO 45 als Backlight-PWM über Lötjumper · GPIO 48 als PSU_SENSE-Eingang · liegen D+/D− (19/20) am Header?
