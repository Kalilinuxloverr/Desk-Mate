#!/bin/sh
# ERC + DRC + Netzlisten-Abgleich fuer die drei KiCad-Projekte (Plan Phase 2).
# Erwartet KiCad 10 unter /Applications/KiCad. Exit != 0 bei Verstoessen.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
K=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
T="$(mktemp -d "${TMPDIR:-/tmp}/deskmate-kicad-test.XXXXXX")"
fail=0
for b in mainboard frontpanel eye-adapter; do
  d="$ROOT/hardware/kicad/$b"
  bf=0
  if ! "$K" sch erc --severity-error --exit-code-violations -o "$T/erc_$b.rpt" "$d/$b.kicad_sch" >/dev/null 2>&1; then
    echo "FAIL ERC $b"; grep -c "error" "$T/erc_$b.rpt"; bf=1
  fi
  if ! "$K" pcb drc --severity-error --exit-code-violations -o "$T/drc_$b.rpt" "$d/$b.kicad_pcb" >/dev/null 2>&1; then
    echo "FAIL DRC $b"; grep -E "^\[|Found" "$T/drc_$b.rpt" | head -5; bf=1
  fi
  "$K" sch export netlist --format kicadxml -o "$T/net_$b.xml" "$d/$b.kicad_sch" >/dev/null 2>&1
  if ! python3 - "$d/netlist.json" "$T/net_$b.xml" <<'PY'
import json, sys, xml.etree.ElementTree as ET
mine = {k: sorted(map(tuple, v)) for k, v in json.load(open(sys.argv[1]))['nets'].items()}
theirs = {n.get('name'): sorted((x.get('ref'), x.get('pin')) for x in n.findall('node'))
          for n in ET.parse(sys.argv[2]).getroot().iter('net')}
bad = [k for k in mine if theirs.get(k) != mine[k]]
if bad:
    print('  Netz-Abweichung Schaltplan vs. netlist.json:', bad[:5]); sys.exit(1)
PY
  then echo "FAIL Netzliste $b"; bf=1; fi
  [ $bf -eq 0 ] && echo "ok   $b (ERC, DRC, Netzliste)"
  fail=$((fail | bf))
done
rm -r "$T"
exit $fail
