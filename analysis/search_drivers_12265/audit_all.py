"""12265: corpus-wide Ploger audit.  Every orbifold model block (any geometry, SUSY or not) in the given files: Wilson lines = the rows
after the shift rows (shifts: rows before the six/seven Wilson-line rows), each with its order N_a = the least N with N A_a in E8 x E8;
conditions (Ploger et al. hep-th/0702176): (7e) N_a A_a^2 = 0 mod 2, (7d) N_a (A_a . V_i) = 0 mod 2 for every shift row, (7f)
gcd(N_a, N_b)(A_a . A_b) = 0 mod 2.  usage: py -3 audit_all.py LISTFILE OUTJSON  (LISTFILE: one model-file path per line)"""
import json, math, sys, os
from fractions import Fraction as F
from collections import Counter, defaultdict
from itertools import combinations
dot = lambda a, b: sum(x * y for x, y in zip(a, b))


def in_e8(v):
    return (all(x.denominator == 1 for x in v) or all(x.denominator == 2 for x in v)) and sum(v) % 2 == 0


def in_g(v):
    return in_e8(v[:8]) and in_e8(v[8:])


def order(v):
    for n in range(1, 25):
        if in_g([n * x for x in v]):
            return n
    return None


def even(x):
    return x.denominator == 1 and x % 2 == 0


def check_block(rows):
    nsh = len(rows) - 6
    shifts, wls = rows[:nsh], [r for r in rows[nsh:] if any(r)]
    fails = []
    ords = [order(w) for w in wls]
    if None in ords:
        return ['order?']
    for w, n in zip(wls, ords):
        if not even(n * dot(w, w)):
            fails.append('7e')
        for s in shifts:
            if any(s) and not even(n * dot(w, s)):
                fails.append('7d')
    for (a, na), (b, nb) in combinations(list(zip(wls, ords)), 2):
        if not even(math.gcd(na, nb) * dot(a, b)):
            fails.append('7f')
    return sorted(set(fails))


files = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
per_dir = defaultdict(Counter)
for f in files:
    try:
        t = open(f, encoding='utf-8', errors='ignore').read()
    except OSError:
        continue
    for blk in t.split('begin model')[1:]:
        if 'Shifts and Wilsonlines:' not in blk:
            continue
        try:
            rows = [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n') if r.strip()]
        except Exception:
            continue
        if not rows or any(len(r) != 16 for r in rows) or len(rows) < 7:
            continue
        geo = (blk.split('SpaceGroup:')[1].split()[0] if 'SpaceGroup:' in blk else '?').split('/')[-1]
        fl = check_block(rows)
        d = os.path.dirname(f)
        per_dir[(d, geo)]['models'] += 1
        per_dir[(d, geo)]['consistent'] += not fl
        for x in fl:
            per_dir[(d, geo)]['fail_' + x] += 1
out = {f'{d} | {g}': dict(c) for (d, g), c in sorted(per_dir.items())}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
tot = Counter()
for c in per_dir.values():
    tot.update(c)
print('TOTAL', dict(tot))
for k, v in out.items():
    if v['models'] != v['consistent']:
        print(k[-110:], v)
