"""Schritt 3: Fertigungsdaten je Board nach <board>/fab/ (Gerber+Drill-Zip fuer JLCPCB, STEP, Render, SVG-Schaltplan).

    python3 export_fab.py mainboard   (System-Python; ruft kicad-cli)
"""
import os
import shutil
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
K = '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'


def run(*args):
    r = subprocess.run([K] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-800:], r.stderr[-800:])
        raise SystemExit(f'kicad-cli fehlgeschlagen: {args[:3]}')


def export(name):
    d = f'{ROOT}/{name}'
    pcb = f'{d}/{name}.kicad_pcb'
    fab = f'{d}/fab'
    tmp = f'{fab}/gerber'
    os.makedirs(fab, exist_ok=True)
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    # JLCPCB-Vorgaben: Protel-Endungen, keine X2, Umriss auf Edge.Cuts, Bohrdaten Excellon mit Map
    run('pcb', 'export', 'gerbers', '--layers', 'F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts',
        '--no-x2', '--use-drill-file-origin', '--subtract-soldermask', '-o', tmp + '/', pcb)
    run('pcb', 'export', 'drill', '--format', 'excellon', '--drill-origin', 'absolute', '--excellon-separate-th',
        '--generate-map', '--map-format', 'gerberx2', '-o', tmp + '/', pcb)
    zpath = f'{fab}/{name}-gerber.zip'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(tmp)):
            z.write(f'{tmp}/{f}', f)
    shutil.rmtree(tmp)
    run('pcb', 'export', 'step', '--subst-models', '--no-dnp', '-o', f'{fab}/{name}.step', pcb)
    run('pcb', 'render', '--side', 'top', '-w', '1600', '-h', '1600', '--quality', 'high', '-o', f'{fab}/{name}-top.png', pcb)
    run('pcb', 'render', '--side', 'bottom', '-w', '1600', '-h', '1600', '-o', f'{fab}/{name}-bottom.png', pcb)
    run('sch', 'export', 'pdf', '-o', f'{fab}/{name}-schaltplan.pdf', f'{d}/{name}.kicad_sch')
    print(f'{name}: {os.path.getsize(zpath) // 1024} KB Gerber-Zip, STEP, Render, Schaltplan-PDF -> {fab}/')


if __name__ == '__main__':
    export(sys.argv[1])
