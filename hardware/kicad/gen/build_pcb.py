"""Schritt 2: Layout aus netlist.json bauen, mit Freerouting routen, Zonen füllen.

    KIPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
    $KIPY build_pcb.py mainboard [--force] [--no-route]

Überschreibt <board>.kicad_pcb nur mit --force (GUI-Änderungen von Leon sind sonst die Wahrheit).
"""
import json
import os
import shutil
import subprocess
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KI_FP = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints'
JAR = os.path.expanduser('~/Applications/freerouting-2.3.0.jar')

SKELETON = '''(kicad_pcb (version 20260206) (generator "pcbnew") (generator_version "10.0")
\t(general (thickness 1.6) (legacy_teardrops no))
\t(paper "A4")
\t(layers (0 "F.Cu" signal) (2 "B.Cu" signal) (9 "F.Adhes" user "F.Adhesive") (11 "B.Adhes" user "B.Adhesive") (13 "F.Paste" user) (15 "B.Paste" user) (5 "F.SilkS" user "F.Silkscreen") (7 "B.SilkS" user "B.Silkscreen") (1 "F.Mask" user) (3 "B.Mask" user) (17 "Dwgs.User" user "User.Drawings") (19 "Cmts.User" user "User.Comments") (21 "Eco1.User" user "User.Eco1") (23 "Eco2.User" user "User.Eco2") (25 "Edge.Cuts" user) (27 "Margin" user) (31 "F.CrtYd" user "F.Courtyard") (29 "B.CrtYd" user "B.Courtyard") (35 "F.Fab" user) (33 "B.Fab" user))
\t(embedded_fonts no)
)
'''


def mm(v):
    return pcbnew.FromMM(v)


def V(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


def load_fp(fpid):
    lib, name = fpid.split(':')
    path = f'{ROOT}/lib/deskmate.pretty' if lib == 'deskmate' else f'{KI_FP}/{lib}.pretty'
    fp = pcbnew.FootprintLoad(path, name)
    if fp is None:
        raise SystemExit(f'Footprint nicht gefunden: {fpid}')
    return fp


def add_line(board, x1, y1, x2, y2, layer=pcbnew.Edge_Cuts, width=0.1):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(V(x1, y1))
    s.SetEnd(V(x2, y2))
    s.SetLayer(layer)
    s.SetWidth(mm(width))
    board.Add(s)


def add_text(board, text, x, y, layer=pcbnew.F_SilkS, size=1.5, rot=0):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetPosition(V(x, y))
    t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    t.SetTextThickness(mm(size * 0.15))
    t.SetTextAngleDegrees(rot)
    if layer == pcbnew.B_SilkS:
        t.SetMirrored(True)
    board.Add(t)


def add_zone(board, net, layer, x1, y1, x2, y2, rule_area=False):
    z = pcbnew.ZONE(board)
    if rule_area:
        z.SetIsRuleArea(True)
        (getattr(z, 'SetDoNotAllowZoneFills', None) or z.SetDoNotAllowCopperPour)(True)
        z.SetDoNotAllowTracks(False)
        z.SetDoNotAllowVias(False)
        ls = pcbnew.LSET()
        ls.addLayer(pcbnew.F_Cu)
        ls.addLayer(pcbnew.B_Cu)
        z.SetLayerSet(ls)
    else:
        z.SetLayer(layer)
        z.SetNet(net)
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(mm(0.5))
        z.SetThermalReliefSpokeWidth(mm(0.6))
        z.SetMinThickness(mm(0.25))
        z.SetLocalClearance(mm(0.3))
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    o = z.Outline()
    o.NewOutline()
    for x, y in ((x1, y1), (x2, y1), (x2, y2), (x1, y2)):
        o.Append(mm(x), mm(y))
    board.Add(z)
    return z


def build(name, force=False, route=True, attempts=6):
    d = f'{ROOT}/{name}'
    nl = json.load(open(f'{d}/netlist.json'))
    pcb_path = f'{d}/{name}.kicad_pcb'
    if os.path.exists(pcb_path) and not force:
        raise SystemExit(f'{pcb_path} existiert - mit --force ueberschreiben')
    with open(pcb_path, 'w') as f:
        f.write(SKELETON)
    board = pcbnew.LoadBoard(pcb_path)
    W, H = nl['w'], nl['h']

    nets = {}
    for netname in sorted(nl['nets']):
        ni = pcbnew.NETINFO_ITEM(board, netname)
        board.Add(ni)
        nets[netname] = ni

    for p in nl['parts']:
        fp = load_fp(p['footprint'])
        fp.SetReference(p['ref'])
        fp.SetValue(p['value'])
        fp.SetPath(pcbnew.KIID_PATH('/' + nl['sheet_uuid'] + '/' + p['uuid']))
        if p['dnp']:
            fp.SetDNP(True)
        board.Add(fp)
        pc = p['pcb']
        fp.SetOrientationDegrees(pc.get('rot', 0))
        fp.SetPosition(V(0, 0))
        bb = fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
        if bb.GetWidth() == 0:
            bb = fp.GetBoundingBox(False)
        c = bb.GetCenter()
        fp.SetPosition(pcbnew.VECTOR2I(mm(pc['x']) - c.x, mm(pc['y']) - c.y))
        for pad in fp.Pads():
            net = p['pads'].get(pad.GetNumber())
            if net:
                pad.SetNet(nets[net])
        # Wert-Text auf Fab lassen, Referenz lesbar
        fp.Reference().SetTextSize(pcbnew.VECTOR2I(mm(0.9), mm(0.9)))
        fp.Reference().SetTextThickness(mm(0.15))

    # Überlappungs-/Randcheck vor dem Routen (der eigentliche Fehlerfinder)
    boxes = []
    for fp in board.GetFootprints():
        bb = fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
        if bb.GetWidth() == 0:
            continue
        b = (pcbnew.ToMM(bb.GetLeft()), pcbnew.ToMM(bb.GetTop()), pcbnew.ToMM(bb.GetRight()), pcbnew.ToMM(bb.GetBottom()))
        if b[0] < -0.01 or b[1] < -0.01 or b[2] > W + 0.01 or b[3] > H + 0.01:
            print(f'  !! {fp.GetReference()} ragt ueber den Rand: {tuple(round(v, 1) for v in b)}')
        boxes.append((fp.GetReference(), b))
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                print(f'  !! Ueberlappung {boxes[i][0]} {tuple(round(v, 1) for v in a)} <-> {boxes[j][0]} {tuple(round(v, 1) for v in b)}')

    # Umriss mit 2 mm Eckenradius -> hier einfach Rechteck (ponytail: Radius macht Leon im GUI, falls gewünscht)
    add_line(board, 0, 0, W, 0)
    add_line(board, W, 0, W, H)
    add_line(board, W, H, 0, H)
    add_line(board, 0, H, 0, 0)
    add_text(board, f'Desk-Mate {name} v1 2026-08', W / 2, H - 1.2, size=0.8)
    add_text(board, 'github.com/Kalilinuxloverr/Desk-Mate', W / 2, H - 1.2, layer=pcbnew.B_SilkS, size=0.8)

    def pad_xy(ref, num):
        for fp in board.GetFootprints():
            if fp.GetReference() == ref:
                for pad in fp.Pads():
                    if pad.GetNumber() == num:
                        return (pcbnew.ToMM(pad.GetPosition().x), pcbnew.ToMM(pad.GetPosition().y))
        raise SystemExit(f'Pad {ref}.{num} nicht gefunden')

    for netname, width, layer, pts in nl.get('pre_tracks', []):
        pts = [pad_xy(*q) if isinstance(q[0], str) else tuple(q) for q in pts]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(V(x1, y1))
            t.SetEnd(V(x2, y2))
            t.SetWidth(mm(width))
            t.SetLayer(pcbnew.F_Cu if layer == 'F.Cu' else pcbnew.B_Cu)
            t.SetNet(nets[netname])
            board.Add(t)

    board.Save(pcb_path)
    print(f'{name}: {len(nl["parts"])} Footprints platziert, {len(nets)} Netze')
    pristine = open(pcb_path).read()
    pro_path = f'{d}/{name}.kicad_pro'
    pro_text = open(pro_path).read()      # pcbnew.Save schreibt das Projekt mit Defaults zurueck -> nachher restaurieren

    best = None
    for attempt in range(attempts if route else 1):
        with open(pcb_path, 'w') as f:
            f.write(pristine)
        board = pcbnew.LoadBoard(pcb_path)   # gleicher Dateiname -> Projektregeln/Netzklassen werden geladen
        nets = {n.GetNetname(): n for n in board.GetNetInfo().NetsByName().values()}
        if route:
            dsn = f'{d}/{name}.dsn'
            ses = f'{d}/{name}.ses'
            pcbnew.ExportSpecctraDSN(board, dsn)
            mt = str(1 + attempt % 4)
            us = ['Greedy', 'Global', 'Hybrid'][attempt % 3]
            cmd = ['java', '-Djava.awt.headless=true', '-jar', JAR, '-de', dsn, '-do', ses, '-mp', '150', '-l', 'en',
                   '-mt', mt, '-us', us]
            log = f'{d}/freerouting.log'
            with open(log, 'w') as lf:
                subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, text=True, timeout=3600)
            if not os.path.exists(ses):
                raise SystemExit('Freerouting hat keine .ses erzeugt - siehe ' + log)
            pcbnew.ImportSpecctraSES(board, ses)
            os.remove(dsn)
            os.remove(ses)
            os.remove(log)
        # Sperrzone (nur Kupferflaeche) und Masseflaechen erst jetzt: der Router soll dort Leiterbahnen legen duerfen
        for x1, y1, x2, y2 in nl.get('keepout', []):
            add_zone(board, None, None, x1, y1, x2, y2, rule_area=True)
        gnd = nets.get('GND')
        if gnd:
            add_zone(board, gnd, pcbnew.F_Cu, 0.5, 0.5, W - 0.5, H - 0.5)
            add_zone(board, gnd, pcbnew.B_Cu, 0.5, 0.5, W - 0.5, H - 0.5)
            for fp in board.GetFootprints():
                for pad in fp.Pads():
                    if pad.GetNetname() == 'GND':
                        pad.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
        pcbnew.ZONE_FILLER(board).Fill(board.Zones())
        board.BuildConnectivity()
        open_count = board.GetConnectivity().GetUnconnectedCount(True)
        print(f'{name}: Versuch {attempt + 1} (mt={mt if route else "-"}, {us if route else "-"}): {open_count} offen')
        if best is None or open_count < best[0]:
            best = (open_count, attempt)
            board.Save(pcb_path)
        if open_count == 0:
            break
    with open(pro_path, 'w') as f:
        f.write(pro_text)
    print(f'{name}: gespeichert -> {pcb_path} ({best[0]} offene Verbindungen, Versuch {best[1] + 1})')


if __name__ == '__main__':
    args = sys.argv[1:]
    build(args[0], force='--force' in args, route='--no-route' not in args)
