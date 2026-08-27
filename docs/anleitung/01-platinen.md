# 01 · Platinen bestellen

Desk-Mate besteht aus drei Platinen, die in **einer** JLCPCB-Bestellung kommen. Alle Fertigungsdaten liegen fertig im Repo — du musst KiCad nicht öffnen.

| Platine | Datei für JLCPCB | Maß | Stück |
|---|---|---|---|
| Mainboard (Base) | `hardware/kicad/mainboard/fab/mainboard-gerber.zip` | 100 × 100 mm | 5 (Mindestmenge) |
| Frontpanel (Deck) | `hardware/kicad/frontpanel/fab/frontpanel-gerber.zip` | 120 × 136 mm | 5 |
| Augen-Adapter (Kopf) | `hardware/kicad/eye-adapter/fab/eye-adapter-gerber.zip` | 42 × 30 mm | 5 |

## Bestellparameter (JLCPCB „Standard PCB“)

- 2 Lagen, FR-4, **1,6 mm**, 1 oz Kupfer
- Oberfläche: HASL (bleifrei) reicht — alles Through-Hole; ENIG nur, wenn's schöner sein soll
- Farbe: frei (Referenz-Build: weiß, passend zum Gehäuse)
- Kein SMD-Assembly nötig (alles THT, Module gesteckt)

Alle drei Zips einzeln als eigenes Produkt hochladen (drei Designs = drei Positionen im Warenkorb). Im JLCPCB-Viewer kurz prüfen: Umriss geschlossen, Bohrungen da, Silkscreen lesbar.

## Was auf die Platinen kommt

Die Stückliste mit Bezugsquellen und Preisen steht in `hardware/bom.md`; welche Maße der gesteckten Module der Entwurf annimmt (und wie sicher das ist), in `vault/Hardware/Module-Masse.md`. **Vor dem Löten der Sockel** die Kandidaten mit „mittel“-Konfidenz am echten Modul nachmessen: ESP32-C3 SuperMini, MPR121-Breakout, DRV8833-Module aus der Box (Pololu-Raster 10,16 mm?), BME680-Pinreihenfolge.

## Schaltpläne und 3D

Je Platine liegt in `fab/` außerdem der Schaltplan als PDF, ein STEP-Modell (für das Gehäuse in `hardware/3d/`) und Renderings von Ober- und Unterseite. Quelle sind die KiCad-10-Projekte im jeweiligen Ordner — Änderungen bitte dort, nicht in den Exporten.
