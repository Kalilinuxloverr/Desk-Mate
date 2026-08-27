"""Footprint-Writer für hardware/kicad/lib/deskmate.pretty (nur THT)."""
from kicad_sexp import Str, dump
from sch import PCB_VERSION


def _text(kind, value, x, y, layer, size=1.0):
    return ['property', Str(kind), Str(value), ['at', x, y, 0], ['layer', Str(layer)],
            ['effects', ['font', ['size', size, size], ['thickness', 0.15]]]] if kind in ('Reference', 'Value') else \
        ['fp_text', 'user', Str(value), ['at', x, y, 0], ['layer', Str(layer)],
         ['effects', ['font', ['size', size, size], ['thickness', 0.15]]]]


def _rect(x1, y1, x2, y2, layer, width):
    return ['fp_rect', ['start', x1, y1], ['end', x2, y2], ['stroke', ['width', width], ['type', 'default']],
            ['fill', 'no'], ['layer', Str(layer)]]


def _line(x1, y1, x2, y2, layer, width=0.12):
    return ['fp_line', ['start', x1, y1], ['end', x2, y2], ['stroke', ['width', width], ['type', 'default']],
            ['layer', Str(layer)]]


def _pad(num, x, y, drill=1.0, size=1.7, shape='circle'):
    return ['pad', Str(str(num)), 'thru_hole', shape, ['at', x, y], ['size', size, size], ['drill', drill],
            ['layers', Str('*.Cu'), Str('*.Mask')], ['remove_unused_layers', 'no']]


def footprint(name, desc, tags, items):
    fp = ['footprint', Str(name), ['version', PCB_VERSION], ['generator', Str('deskmate_gen')], ['layer', Str('F.Cu')],
          ['descr', Str(desc)], ['tags', Str(tags)], ['attr', 'through_hole']]
    fp += items
    fp.append(['embedded_fonts', 'no'])
    return fp


def module_socket(name, rows_x, n, module_w, module_h, desc, pin1='top', first_numbers=None, drill=1.0,
                  pad=1.7, extra=None, y_offset=0.0, pads=None):
    """Modul auf zwei (oder mehr) Buchsenreihen.

    rows_x: X-Positionen der Reihen (mm, relativ zur Modulmitte), Pins laufen in +Y (Pitch 2,54).
    n: Pins je Reihe. Nummerierung: Reihe 0 = 1..n von oben nach unten, Reihe 1 = n+1..2n von oben nach unten.
    module_w/h: Umriss des gesteckten Moduls (Fab + Courtyard), Ursprung = Modulmitte.
    """
    items = []
    y0 = -(n - 1) * 2.54 / 2
    if pads:                      # explizite Liste (num, x, slot)
        for num, px, slot in pads:
            items.append(_pad(num, px, y0 + slot * 2.54, drill, pad, 'rect' if num == 1 else 'circle'))
    else:
        for r, rx in enumerate(rows_x):
            for i in range(n):
                num = (first_numbers[r] if first_numbers else r * n + 1) + i
                items.append(_pad(num, rx, y0 + i * 2.54, drill, pad, 'rect' if i == 0 else 'circle'))
    hw, hh = module_w / 2, module_h / 2
    items.append(_rect(-hw, -hh + y_offset, hw, hh + y_offset, 'F.Fab', 0.1))
    items.append(_rect(-hw - 0.25, -hh - 0.25 + y_offset, hw + 0.25, hh + 0.25 + y_offset, 'F.CrtYd', 0.05))
    items.append(_rect(-hw, -hh + y_offset, hw, hh + y_offset, 'F.SilkS', 0.12))
    # Pin-1-Markierung
    items.append(_line(rows_x[0] - 1.6, y0 - 1.6 - (2.54 * pads[0][2] if pads else 0), rows_x[0] + 1.6,
                       y0 - 1.6 - (2.54 * pads[0][2] if pads else 0), 'F.SilkS', 0.2))
    items.insert(0, ['property', Str('Reference'), Str('REF**'), ['at', 0, -hh - 1.5 + y_offset, 0], ['layer', Str('F.SilkS')],
                     ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]]]])
    items.insert(1, ['property', Str('Value'), Str(name), ['at', 0, hh + 1.5 + y_offset, 0], ['layer', Str('F.Fab')],
                     ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]]]])
    items.insert(2, ['property', Str('Datasheet'), Str(''), ['at', 0, 0, 0], ['layer', Str('F.Fab')], ['hide', 'yes'],
                     ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]]]])
    items.insert(3, ['property', Str('Description'), Str(desc), ['at', 0, 0, 0], ['layer', Str('F.Fab')], ['hide', 'yes'],
                     ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]]]])
    if extra:
        items += extra
    return footprint(name, desc, 'module socket THT', items)


def two_pad_radial(name, pitch, body_w, body_h, desc, drill=1.0, pad=2.0):
    items = [
        ['property', Str('Reference'), Str('REF**'), ['at', 0, -body_h / 2 - 1.5, 0], ['layer', Str('F.SilkS')],
         ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]]]],
        ['property', Str('Value'), Str(name), ['at', 0, body_h / 2 + 1.5, 0], ['layer', Str('F.Fab')],
         ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]]]],
        ['property', Str('Datasheet'), Str(''), ['at', 0, 0, 0], ['layer', Str('F.Fab')], ['hide', 'yes'],
         ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]]]],
        ['property', Str('Description'), Str(desc), ['at', 0, 0, 0], ['layer', Str('F.Fab')], ['hide', 'yes'],
         ['effects', ['font', ['size', 1, 1], ['thickness', 0.15]]]],
        _pad(1, -pitch / 2, 0, drill, pad, 'rect'), _pad(2, pitch / 2, 0, drill, pad),
        _rect(-body_w / 2, -body_h / 2, body_w / 2, body_h / 2, 'F.Fab', 0.1),
        _rect(-body_w / 2, -body_h / 2, body_w / 2, body_h / 2, 'F.SilkS', 0.12),
        _rect(-body_w / 2 - 0.25, -body_h / 2 - 0.25, body_w / 2 + 0.25, body_h / 2 + 0.25, 'F.CrtYd', 0.05)]
    return footprint(name, desc, 'radial THT', items)


def write_pretty(dirpath, fps):
    import os
    os.makedirs(dirpath, exist_ok=True)
    for fp in fps:
        with open(f'{dirpath}/{fp[1]}.kicad_mod', 'w', encoding='utf-8') as f:
            f.write(dump(fp) + '\n')
