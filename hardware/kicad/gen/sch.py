"""Schaltplan-Writer: erzeugt .kicad_sch (KiCad 10) aus einer Bauteil-/Netzliste.

Verdrahtung ausschließlich über globale Labels an den Pin-Enden — das ist
bewusst schlicht (ponytail: keine Leitungen, keine Blätter); in der GUI kann
Leon jederzeit umsortieren, die Netze bleiben erhalten.
"""
import copy
import json
import os

from kicad_sexp import Str, parse_file, find_all, find_first, dump
import uuid as _uuid

_NS = _uuid.UUID('6f1b1d2e-7c3a-4f7e-9d2b-desk0mate001'.replace('desk0mate001', '0a5c1e2d3b4f'))
_counter = [0]


def uuid4(key=None):
    """Deterministische UUIDs: gleicher Schluessel -> gleiche UUID, damit Neugenerieren die
    Schaltplan<->Layout-Verknuepfung (Footprint-Pfad) nicht bricht."""
    if key is None:
        _counter[0] += 1
        key = f'anon/{_counter[0]}'
    return str(_uuid.uuid5(_NS, key))

KICAD = '/Applications/KiCad/KiCad.app/Contents/SharedSupport'
SYMDIR = KICAD + '/symbols'
FPDIR = KICAD + '/footprints'
SCH_VERSION = 20260306
SYMLIB_VERSION = 20251024
PCB_VERSION = 20260206

_libcache = {}


def _lib(libname):
    if libname not in _libcache:
        doc = parse_file(f'{SYMDIR}/{libname}.kicad_sym')
        _libcache[libname] = {s[1]: s for s in find_all(doc[0], 'symbol')}
    return _libcache[libname]


def _rename_subunits(sym, old, new):
    for sub in find_all(sym, 'symbol'):
        if sub[1].startswith(old + '_'):
            sub[1] = Str(new + sub[1][len(old):])


def flat_symbol(libname, name, custom=None):
    """Liefert das Symbol als flache Kopie (extends aufgelöst), umbenannt in 'lib:name'."""
    syms = custom if custom is not None else _lib(libname)
    src = syms[name]
    ext = find_first(src, 'extends')
    if ext:
        parent = copy.deepcopy(syms[ext[1]])
        # Eigenschaften des abgeleiteten Symbols übernehmen, Rest vom Elternteil
        parent[:] = [c for c in parent if not (isinstance(c, list) and c and c[0] == 'property')]
        props = find_all(src, 'property')
        for kw in ('pin_names', 'pin_numbers', 'exclude_from_sim', 'in_bom', 'on_board', 'power'):
            o = find_first(src, kw)
            if o is not None:
                parent[:] = [c for c in parent if not (isinstance(c, list) and c and c[0] == kw)]
                parent.insert(2, copy.deepcopy(o))
        insert_at = 2
        for i, c in enumerate(parent):
            if isinstance(c, list) and c[0] in ('pin_names', 'pin_numbers', 'exclude_from_sim', 'in_bom', 'on_board'):
                insert_at = i + 1
        for p in reversed(props):
            parent.insert(insert_at, copy.deepcopy(p))
        _rename_subunits(parent, ext[1], name)
        sym = parent
    else:
        sym = copy.deepcopy(src)
    sym[1] = Str(f'{libname}:{name}')
    return sym


def symbol_pins(sym):
    """[(number, name, type, x, y, angle)] aller Pins (Unit 0/1)."""
    out = []
    for sub in find_all(sym, 'symbol'):
        for p in find_all(sub, 'pin'):
            at = find_first(p, 'at')
            out.append((str(find_first(p, 'number')[1]), str(find_first(p, 'name')[1]), p[1],
                        float(at[1]), float(at[2]), float(at[3]) if len(at) > 3 else 0.0))
    return out


def _effects(size=1.27, hide=False, justify=None):
    e = ['effects', ['font', ['size', size, size]]]
    if justify:
        e.append(['justify'] + justify)
    return e


def _prop(name, value, x, y, hide=False, rot=0):
    p = ['property', Str(name), Str(value), ['at', x, y, rot], ['show_name', 'no'], ['do_not_autoplace', 'no']]
    if hide:
        p.append(['hide', 'yes'])
    p.append(_effects())
    return p


def make_custom_symbol(name, pins, width=20.32, ref_prefix='U', desc='', height=None):
    """Rechteck-Symbol. pins: [(number, name, side 'L'/'R'/'T'/'B', slot, type)], slot in 2,54-mm-Schritten.

    Pinlänge 2,54 mm; Pin-Anschlusspunkt liegt außerhalb des Rechtecks.
    """
    lefts = [p for p in pins if p[2] == 'L']
    rights = [p for p in pins if p[2] == 'R']
    rows = max([p[3] for p in lefts + rights] + [0]) + 1
    h = height or rows * 2.54 + 2.54
    w = width
    top = h / 2
    body = ['symbol', Str(name), ['pin_names', ['offset', 1.016]], ['exclude_from_sim', 'no'], ['in_bom', 'yes'],
            ['on_board', 'yes'],
            _prop('Reference', ref_prefix, 0, top + 2.54),
            _prop('Value', name, 0, -top - 2.54),
            _prop('Footprint', '', 0, -top - 5.08, hide=True),
            _prop('Datasheet', '', 0, 0, hide=True),
            _prop('Description', desc, 0, 0, hide=True)]
    gfx = ['symbol', Str(name + '_0_1'),
           ['rectangle', ['start', -w / 2, top], ['end', w / 2, -top], ['stroke', ['width', 0.254], ['type', 'default']],
            ['fill', ['type', 'background']]]]
    pinunit = ['symbol', Str(name + '_1_1')]
    for num, pname, side, slot, ptype in pins:
        y = top - 2.54 - slot * 2.54
        if side == 'L':
            at = [-w / 2 - 2.54, y, 0]
        elif side == 'R':
            at = [w / 2 + 2.54, y, 180]
        elif side == 'T':
            at = [-w / 2 + 2.54 + slot * 2.54, top + 2.54, 270]
        else:
            at = [-w / 2 + 2.54 + slot * 2.54, -top - 2.54, 90]
        pinunit.append(['pin', ptype, 'line', ['at'] + at, ['length', 2.54],
                        ['name', Str(pname), _effects()], ['number', Str(num), _effects()]])
    body += [gfx, pinunit, ['embedded_fonts', 'no']]
    return body


class Schematic:
    def __init__(self, project, title, rev='1', company='Leon Fröhlich', paper='A3'):
        self.project = project
        self.title = title
        self.rev = rev
        self.company = company
        self.paper = paper
        self.uuid = uuid4(f'sheet/{project}')
        self.lib_symbols = {}
        self.items = []
        self.parts = []          # für Netzliste / PCB
        self.custom_syms = {}    # name -> symbol sexp (deskmate-Bibliothek)
        self.used_nets = set()

    def add_custom_symbol(self, sym):
        self.custom_syms[str(sym[1])] = sym

    def _symbol(self, lib, name):
        key = f'{lib}:{name}'
        if key not in self.lib_symbols:
            if lib == 'deskmate':
                sym = copy.deepcopy(self.custom_syms[name])
                sym[1] = Str(key)
            else:
                sym = flat_symbol(lib, name)
            self.lib_symbols[key] = sym
        return self.lib_symbols[key]

    def label(self, net, x, y, rot):
        self.used_nets.add(net)
        self.items.append(['global_label', Str(net), ['shape', 'passive'], ['at', x, y, rot], ['fields_autoplaced', 'yes'],
                           _effects(justify=['left'] if rot in (0, 90) else ['right']),
                           ['uuid', Str(uuid4())],
                           ['property', Str('Intersheetrefs'), Str('${INTERSHEET_REFS}'), ['at', x, y, 0],
                            ['show_name', 'no'], ['do_not_autoplace', 'no'], ['hide', 'yes'], _effects()]])

    def text(self, s, x, y, size=2.0):
        self.items.append(['text', Str(s), ['exclude_from_sim', 'no'], ['at', x, y, 0],
                           _effects(size=size, justify=['left', 'bottom']), ['uuid', Str(uuid4())]])

    def add(self, ref, lib, name, value, footprint, x, y, nets, dnp=False, pcb=None, props=None, in_bom=True):
        """Symbol platzieren. nets: {pin_number: netname | None (No-Connect)}. Jeder Pin muss vorkommen."""
        sym = self._symbol(lib, name)
        pins = symbol_pins(sym)
        numbers = [p[0] for p in pins]
        missing = [n for n in numbers if n not in nets]
        extra = [n for n in nets if n not in numbers]
        if missing or extra:
            raise ValueError(f'{ref} ({lib}:{name}): fehlende Pins {missing}, unbekannte Pins {extra}; Pins = {numbers}')
        u = uuid4(f'{self.project}/{ref}')
        inst = ['symbol', ['lib_id', Str(f'{lib}:{name}')], ['at', x, y, 0], ['unit', 1], ['body_style', 1],
                ['exclude_from_sim', 'no'], ['in_bom', 'yes' if in_bom else 'no'], ['on_board', 'yes'],
                ['in_pos_files', 'yes'], ['dnp', 'yes' if dnp else 'no'], ['fields_autoplaced', 'yes'],
                ['uuid', Str(u)],
                _prop('Reference', ref, x, y - 1.27 - self._top(pins)),
                _prop('Value', value, x, y + 1.27 + self._top(pins)),
                _prop('Footprint', footprint, x, y, hide=True),
                _prop('Datasheet', '', x, y, hide=True),
                _prop('Description', '', x, y, hide=True)]
        for k, v in (props or {}).items():
            inst.append(_prop(k, v, x, y, hide=True))
        seen = set()
        for num, pname, ptype, px, py, ang in pins:
            inst.append(['pin', Str(num), ['uuid', Str(uuid4(f'{self.project}/{ref}/pin/{num}/{len(inst)}'))]])
            gx, gy = round(x + px, 4), round(y - py, 4)
            net = nets[num]
            if num in seen:          # gleiche Pinnummer mehrfach (z. B. USB VBUS) - nur einmal beschriften
                continue
            seen.add(num)
            if net is None:
                self.items.append(['no_connect', ['at', gx, gy], ['uuid', Str(uuid4())]])
            else:
                self.label(net, gx, gy, (ang + 180) % 360)
        inst.append(['instances', ['project', Str(self.project),
                                   ['path', Str('/' + self.uuid), ['reference', Str(ref)], ['unit', 1]]]])
        self.items.append(inst)
        padnets = {}
        for num, *_ in pins:
            if nets[num] is not None:
                padnets[num] = nets[num]
        self.parts.append({'ref': ref, 'value': value, 'footprint': footprint, 'uuid': u, 'dnp': dnp,
                           'pads': padnets, 'pcb': pcb or {}})
        return u

    @staticmethod
    def _top(pins):
        return max([abs(p[4]) for p in pins] + [2.54])

    def pwr_flag(self, net, x, y):
        x, y = round(x / 1.27) * 1.27, round(y / 1.27) * 1.27
        self._symbol('power', 'PWR_FLAG')
        ref = f'#FLG{len([i for i in self.items if i[0] == "symbol" and "PWR_FLAG" in str(i[1])]) + 1:02d}'
        u = uuid4(f'{self.project}/{ref}')
        self.items.append(['symbol', ['lib_id', Str('power:PWR_FLAG')], ['at', x, y, 0], ['unit', 1], ['body_style', 1],
                           ['exclude_from_sim', 'no'], ['in_bom', 'yes'], ['on_board', 'yes'], ['in_pos_files', 'yes'],
                           ['dnp', 'no'], ['fields_autoplaced', 'yes'], ['uuid', Str(u)],
                           _prop('Reference', ref, x, y - 3.81, hide=True),
                           _prop('Value', 'PWR_FLAG', x, y - 3.81),
                           _prop('Footprint', '', x, y, hide=True), _prop('Datasheet', '', x, y, hide=True),
                           _prop('Description', '', x, y, hide=True),
                           ['pin', Str('1'), ['uuid', Str(uuid4())]],
                           ['instances', ['project', Str(self.project),
                                          ['path', Str('/' + self.uuid), ['reference', Str(ref)], ['unit', 1]]]]])
        self.label(net, x, y, 270)

    def dump(self):
        doc = ['kicad_sch', ['version', SCH_VERSION], ['generator', Str('eeschema')], ['generator_version', Str('10.0')],
               ['uuid', Str(self.uuid)], ['paper', Str(self.paper)],
               ['title_block', ['title', Str(self.title)], ['date', Str(__import__('datetime').date.today().isoformat())],
                ['rev', Str(self.rev)], ['company', Str(self.company)],
                ['comment', 1, Str('Desk-Mate — generiert aus hardware/kicad/gen (GUI-Änderungen danach sind die Wahrheit)')]],
               ['lib_symbols'] + [self.lib_symbols[k] for k in sorted(self.lib_symbols)]]
        doc += self.items
        doc += [['sheet_instances', ['path', Str('/'), ['page', Str('1')]]], ['embedded_fonts', 'no']]
        return dump(doc) + '\n'

    def nets(self):
        """{net: [(ref, pad)]} aus den platzierten Teilen."""
        n = {}
        for p in self.parts:
            for pad, net in p['pads'].items():
                n.setdefault(net, []).append((p['ref'], pad))
        return n


def write_custom_lib(path, symbols):
    doc = ['kicad_symbol_lib', ['version', SYMLIB_VERSION], ['generator', Str('deskmate_gen')], ['generator_version', Str('10.0')]]
    doc += [copy.deepcopy(s) for s in symbols.values()]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dump(doc) + '\n')


def write_project(dirpath, name, rules, netclasses, sch_uuid, board_w, board_h):
    """.kicad_pro mit JLCPCB-Regeln + Lib-Tabellen auf die Projektbibliothek."""
    pro = {
        "board": {"design_settings": {
            "defaults": {"board_outline_line_width": 0.05, "copper_line_width": 0.2, "copper_text_size_h": 1.5,
                         "copper_text_size_v": 1.5, "copper_text_thickness": 0.3, "courtyard_line_width": 0.05,
                         "fab_line_width": 0.1, "fab_text_size_h": 1.0, "fab_text_size_v": 1.0, "fab_text_thickness": 0.15,
                         "other_line_width": 0.1, "silk_line_width": 0.12, "silk_text_size_h": 1.0,
                         "silk_text_size_v": 1.0, "silk_text_thickness": 0.15},
            "diff_pair_dimensions": [], "drc_exclusions": [],
            "rules": rules,
            "track_widths": [0.0, 0.3, 0.5, 0.8, 1.5, 2.0],
            "via_dimensions": [{"diameter": 0.0, "drill": 0.0}, {"diameter": 0.8, "drill": 0.4}, {"diameter": 1.2, "drill": 0.6}]},
            "ipc2581": {"dist": "", "distpn": "", "internal_id": "", "mfg": "", "mpn": ""},
            "layer_presets": [], "viewports": []},
        "boards": [],
        "cvpcb": {"equivalence_files": []},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": f"{name}.kicad_pro", "version": 3},
        "net_settings": {"classes": netclasses, "meta": {"version": 4}, "net_colors": None, "netclass_assignments": None,
                         "netclass_patterns": []},
        "pcbnew": {"last_paths": {"gencad": "", "idf": "", "netlist": "", "plot": "", "pos_files": "", "specctra_dsn": "",
                                  "step": "", "svg": "", "vrml": ""}, "page_layout_descr_file": ""},
        "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
        "sheets": [[sch_uuid, "Root"]],
        "text_variables": {"BOARD_W": str(board_w), "BOARD_H": str(board_h)},
    }
    with open(f'{dirpath}/{name}.kicad_pro', 'w', encoding='utf-8') as f:
        json.dump(pro, f, indent=2, ensure_ascii=False)
        f.write('\n')
    with open(f'{dirpath}/sym-lib-table', 'w') as f:
        f.write('(sym_lib_table\n  (version 7)\n  (lib (name "deskmate")(type "KiCad")(uri "${KIPRJMOD}/../lib/deskmate.kicad_sym")(options "")(descr "Desk-Mate Projektbibliothek"))\n)\n')
    with open(f'{dirpath}/fp-lib-table', 'w') as f:
        f.write('(fp_lib_table\n  (version 7)\n  (lib (name "deskmate")(type "KiCad")(uri "${KIPRJMOD}/../lib/deskmate.pretty")(options "")(descr "Desk-Mate Projektbibliothek"))\n)\n')
