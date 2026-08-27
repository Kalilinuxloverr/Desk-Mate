"""Schritt 1: Bibliothek + Schaltpläne + Projekte + netlist.json je Board.

    python3 build_sch.py            (System-Python reicht; kein pcbnew nötig)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

from sch import Schematic, symbol_pins, write_custom_lib, write_project
import fp as FP
import boards as B

JLC_RULES = {"min_clearance": 0.127, "min_connection": 0.0, "min_copper_edge_clearance": 0.3, "min_hole_clearance": 0.25,
             "min_hole_to_hole": 0.25, "min_microvia_diameter": 0.2, "min_microvia_drill": 0.1, "min_resolved_spokes": 0,
             "min_silk_clearance": 0.0, "min_text_height": 0.8, "min_text_thickness": 0.08,
             "min_through_hole_diameter": 0.3, "min_track_width": 0.2, "min_via_annular_width": 0.13,
             "min_via_diameter": 0.5, "solder_mask_to_copper_clearance": 0.0, "use_height_for_length_calcs": True}


def netclass(name, width, clearance=0.13):
    return {"bus_width": 12, "clearance": clearance, "diff_pair_gap": 0.25, "diff_pair_via_gap": 0.25,
            "diff_pair_width": 0.2, "line_style": 0, "microvia_diameter": 0.3, "microvia_drill": 0.1, "name": name,
            "pcb_color": "rgba(0, 0, 0, 0.000)", "priority": 2147483647 if name == 'Default' else 0,
            "schematic_color": "rgba(0, 0, 0, 0.000)", "track_width": width, "via_diameter": 0.8 if width < 1 else 1.2,
            "via_drill": 0.4 if width < 1 else 0.6, "wire_width": 6}


def footprints():
    dy = B.DEVKIT_OUTLINE_DY
    ant = [FP._rect(-9, -B.DEVKIT_L / 2 + dy - 5.9, 9, -B.DEVKIT_L / 2 + dy, 'F.Fab', 0.1),
           FP._rect(-9, -B.DEVKIT_L / 2 + dy - 5.9, 9, -B.DEVKIT_L / 2 + dy, 'F.SilkS', 0.12),
           FP._text('user', 'Antenne', 0, -B.DEVKIT_L / 2 + dy - 2.9, 'F.SilkS', 0.8),
           FP._text('user', 'USB', 0, B.DEVKIT_L / 2 + dy - 2.5, 'F.SilkS', 0.8)]
    fps = [
        FP.module_socket('ESP32-S3-DevKitC-1_Socket', (-B.DEVKIT_ROW_SPACING / 2, B.DEVKIT_ROW_SPACING / 2), 22,
                         B.DEVKIT_W, B.DEVKIT_L,
                         'Sockel 2x 1x22 fuer ESP32-S3-DevKitC-1 v1.1 (Pin 1 = Antennenende; J1 = Pads 1-22 links, J3 = 23-44 rechts, Antenne oben)',
                         y_offset=dy, extra=ant),
        FP.module_socket('DRV8833_Socket', (-B.DRV8833_ROW_SPACING / 2, B.DRV8833_ROW_SPACING / 2), 8,
                         B.DRV8833_W, B.DRV8833_L, 'Sockel 2x 1x8 fuer Pololu DRV8833 #2130 (Pad 1 = GND, VMM-Seite links)'),
        FP.module_socket('A4988_Socket', (-B.A4988_ROW_SPACING / 2, B.A4988_ROW_SPACING / 2), 8,
                         B.A4988_W, B.A4988_L, 'Sockel 2x 1x8 fuer A4988/TMC2209-Raster (Reserve), Pad 1 = ENABLE, Pad 9 = VMOT'),
        FP.module_socket('ESP32-C3_SuperMini', (-B.C3_ROW_SPACING / 2, B.C3_ROW_SPACING / 2), 8,
                         B.C3_W, B.C3_L, 'Sockel 2x 1x8 fuer ESP32-C3 SuperMini (Reserve), Pad 1 = IO5, Pad 9 = 5V'),
        FP.module_socket('MPR121_Breakout', (-B.MPR121_ROW_SPACING / 2, B.MPR121_ROW_SPACING / 2), 12,
                         20.3, 30.5, 'Sockel fuer MPR121-Breakout (SparkFun-Layout): rechts 1x12 Elektroden ELE0-11 (Pads 7-18), links 1x6 Steuerpins (1-6: 3V3 IRQ SCL SDA ADD GND, gegenueber ELE8..ELE3)',
                         pads=[(1, -B.MPR121_ROW_SPACING / 2, 8), (2, -B.MPR121_ROW_SPACING / 2, 7),
                               (3, -B.MPR121_ROW_SPACING / 2, 6), (4, -B.MPR121_ROW_SPACING / 2, 5),
                               (5, -B.MPR121_ROW_SPACING / 2, 4), (6, -B.MPR121_ROW_SPACING / 2, 3)] +
                              [(7 + i, B.MPR121_ROW_SPACING / 2, i) for i in range(12)]),
        FP.two_pad_radial('Polyfuse_Radial_P5.08mm', 5.08, 12.0, 4.0, 'Polyfuse radial, RM 5,08 (RXEF300)'),
    ]
    return fps


def layout_board(board):
    """Schaltplan mit Abschnitten; Symbole fließend auf A2 (594 x 420) platziert."""
    sch = Schematic(board['name'], board['title'], paper='A2')
    for s in B.CUSTOM_SYMBOLS.values():
        sch.add_custom_symbol(s)
    x, y, rowh = 20.0, 30.0, 0.0
    for title, parts in board['sections']:
        x, y = 20.0, y + rowh + 12
        rowh = 0
        sch.text(title, x, y - 4, size=2.5)
        for part in parts:
            ref, lib, sym, value, footprint, nets, pcb = part[:7]
            dnp = part[7] if len(part) > 7 else False
            pins = symbol_pins(sch._symbol(lib, sym))
            xs = [p[3] for p in pins] or [0]
            ys = [p[4] for p in pins] or [0]
            w = (max(xs) - min(xs)) + 30    # Platz für Labels links/rechts
            h = (max(ys) - min(ys)) + 12
            if x + w > 580:
                x, y = 20.0, y + rowh + 6
                rowh = 0
            cx = round((x - min(xs) + 15) / 1.27) * 1.27
            cy = round((y + max(ys) + 6) / 1.27) * 1.27
            sch.add(ref, lib, sym, value, footprint, cx, cy, nets, dnp=dnp, pcb=pcb)
            x += w
            rowh = max(rowh, h)
    y += rowh + 16
    x = 20.0
    sch.text('PWR_FLAGs', x, y - 4, size=2.5)
    for net in board['pwr_flags']:
        sch.pwr_flag(net, x + 5, y + 5)
        x += 25
    return sch


def main():
    libdir = f'{ROOT}/lib'
    os.makedirs(libdir, exist_ok=True)
    write_custom_lib(f'{libdir}/deskmate.kicad_sym', B.CUSTOM_SYMBOLS)
    FP.write_pretty(f'{libdir}/deskmate.pretty', footprints())
    for board in B.BOARDS:
        d = f'{ROOT}/{board["name"]}'
        os.makedirs(d, exist_ok=True)
        sch = layout_board(board)
        with open(f'{d}/{board["name"]}.kicad_sch', 'w', encoding='utf-8') as f:
            f.write(sch.dump())
        classes = [netclass('Default', 0.25)]
        assignments = {}
        for name, (nets, width) in board['netclasses'].items():
            classes.append(netclass(name, width))
            for n in nets:
                assignments[n] = name
        write_project(d, board['name'], JLC_RULES, classes, sch.uuid, board['w'], board['h'])
        # netclass_assignments nachtragen
        pro = json.load(open(f'{d}/{board["name"]}.kicad_pro'))
        pro['net_settings']['netclass_assignments'] = assignments
        json.dump(pro, open(f'{d}/{board["name"]}.kicad_pro', 'w'), indent=2, ensure_ascii=False)
        nl = {'board': board['name'], 'w': board['w'], 'h': board['h'], 'sheet_uuid': sch.uuid,
              'parts': sch.parts, 'nets': sch.nets(), 'netclasses': board['netclasses'], 'keepout': board['keepout'],
              'pre_tracks': board.get('pre_tracks', [])}
        json.dump(nl, open(f'{d}/netlist.json', 'w'), indent=1, ensure_ascii=False)
        print(f'{board["name"]}: {len(sch.parts)} Teile, {len(nl["nets"])} Netze')


if __name__ == '__main__':
    main()
