"""Minimaler S-Expression-Parser/-Writer für KiCad-Dateien.

Quoted Strings werden als `Str` (Unterklasse von str) gehalten, damit sie
beim Schreiben wieder in Anführungszeichen landen; nackte Atome bleiben str.
"""
import re


class Str(str):
    """Ein in Anführungszeichen stehender String."""


_TOK = re.compile(r'\s*(?:(\()|(\))|"((?:\\.|[^"\\])*)"|([^\s()"]+))', re.S)


def parse(text):
    pos, stack, root = 0, [], []
    cur = root
    while pos < len(text):
        m = _TOK.match(text, pos)
        if not m:
            break
        pos = m.end()
        if m.group(1):
            new = []
            cur.append(new)
            stack.append(cur)
            cur = new
        elif m.group(2):
            cur = stack.pop()
        elif m.group(3) is not None:
            cur.append(Str(m.group(3).replace('\\"', '"').replace('\\\\', '\\')))
        elif m.group(4) is not None:
            cur.append(m.group(4))
    return root


def parse_file(path):
    with open(path, encoding='utf-8') as f:
        return parse(f.read())


def find_all(node, kw):
    return [c for c in node if isinstance(c, list) and c and c[0] == kw]


def find_first(node, kw):
    for c in node:
        if isinstance(c, list) and c and c[0] == kw:
            return c
    return None


def _atom(a):
    if isinstance(a, Str):
        return '"' + a.replace('\\', '\\\\').replace('"', '\\"') + '"'
    if isinstance(a, float):
        s = f'{a:.6f}'.rstrip('0').rstrip('.')
        return s if s not in ('', '-0') else '0'
    return str(a)


def dump(node, indent=0):
    """Schreibt verschachtelte Listen als eingerücktes S-Expression."""
    if not isinstance(node, list):
        return _atom(node)
    if all(not isinstance(c, list) for c in node):
        return '(' + ' '.join(_atom(c) for c in node) + ')'
    out = ['(' + _atom(node[0])]
    i = 1
    while i < len(node) and not isinstance(node[i], list):
        out[0] += ' ' + _atom(node[i])
        i += 1
    for c in node[i:]:
        out.append('\t' * (indent + 1) + dump(c, indent + 1))
    out.append('\t' * indent + ')')
    return '\n'.join(out)


def uuid4():
    import uuid
    return str(uuid.uuid4())
