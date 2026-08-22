# Firmware-Module

Siehe Spec §3: `hid` · `link` · `net` · `face` · `motion` · `io` · `state` · `config`. Ein Sketch, je Modul `.cpp/.h`, kein Framework. Host-Tests für `link` und `state`.

Pflichtregeln: NimBLE, `WiFi.setSleep(false)`, Panels direkt zeichnen, Watchdog, keine Structs in `.ino`-Signaturen, Protokollversion bei jeder Änderung.
