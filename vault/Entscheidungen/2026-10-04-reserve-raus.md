---
datum: 2026-10-04
typ: entscheidung
---
# Reserve raus — Platinen ohne „vielleicht später“

**Kontext:** Teile und Fader sind noch nicht da, JLCPCB ist noch nicht bestellt. Leon: „so einfach wie möglich, nichts überkompliziert, aber funktional“. Die 18 Grilling-Entscheidungen bleiben; gestrichen wird nur, was nie bestückt würde und trotzdem Platz, Lötjumper und Fallen kostet.

**Optionen:** (a) streichen und alle drei Platinen neu generieren; (b) nur Spec/BOM ändern, Platinen in der GUI anpassen; (c) nichts streichen, nur unbestückt lassen. **Wahl: (a)** — der Generator bleibt die eine Quelle, `tools/test-kicad.sh` prüft das Ergebnis. Die GUI-Änderung am Mainboard vom 28.08. war nur eine Verschiebung um 54 mm, kein Design; Frontpanel und Augen-Adapter wurden nie in der GUI angefasst.

| Was | Entscheidung | Grund |
|---|---|---|
| Stepper-Sockel U7, Header J10, Elko C8, JP6–JP8 | raus | Grilling #2: kein Körper-Stepper |
| C3-Footprint U6, JP2/JP3 | raus | Grilling #4: C3 gestrichen; IO43/44 bleiben Debug-UART |
| GPIO45 → Backlight-PWM (JP1 Mainboard, JP11 Frontpanel) | raus, GPIO45 tabu | Dimmen ist Roadmap; einziger Grund für Falle 13 und den zweistufigen Schalter |
| nSLEEP-Jumper JP5 (ab Werk gebrückt) | raus, nSLEEP fest an 3V3 | wird nie geöffnet, es gibt keinen GPIO dafür |
| Backlight-Schalter | einstufig: MCP23017 GPB6 → 1 kΩ → Basis BC327 (high-side an 3V3), 10 kΩ Basis–Emitter; GPB6 low = Licht an | ohne GPIO45 ist der Pull-up erlaubt; 10 kΩ hält das Licht aus, bis die Firmware den MCP konfiguriert |
| INT-Jumper JP9/JP10 | raus, INTA direkt an IO_INT, INTB unbeschaltet | Firmware setzt MIRROR=1 |
| Augen-Reset | RC-Glied raus; DISP_RST vom MCP23017 (GPB5) über IDC-Pin 29 und Pin 10 des Augen-Kabels (bisher dritter GND), 10 kΩ Pull-up auf dem Frontpanel | ein Reset-Pfad für drei Panels; bisher floatete der Bauch-Reset bis zur MCP-Konfiguration (latenter Fehler), die Augen hatten nur den Software-Reset |
| VM-Boost-Jumper + MT3608-Header U5 | **bleibt**, Jumper heißt jetzt JP1 | einziger echter Einstellknopf: ob der X32-Fader bei 5 V schnell genug ist, zeigt erst die Messung |
| Zweiter DRV8833-Sockel, Fader 3/4 | bleibt | Grilling #8: 2 bestückt, 4 vorgesehen |

**Ergebnis:** Mainboard 8 → 1 Lötjumper, −2 Sockel, −1 Header, −1 Elko. Frontpanel 3 → 0 Lötjumper, −1 Transistor, −2 Widerstände, +1 Pull-up. Augen-Adapter nur noch Stecker + 2× 100 nF. Falle 13 ist gegenstandslos; `tools/test-pins.sh` blockt GPIO45 wie die anderen Strapping-Pins.

Nachgezogen: Spec §1, §2.1–2.4, §7, §8 · `hardware/bom.md` · `hardware/kicad/gen/boards.py` · `pins.h` · READMEs · [[Module-Masse]] · [[Pin-Map]].
