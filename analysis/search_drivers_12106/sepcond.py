import json
import glob
import os
from fractions import Fraction as Fr
from collections import Counter

scan = json.load(open(r'C:\tmp\toe_round\stype\z6scan_3.json'))
ok = {s[0]: s[2] != 'LOAD FAILED' for s in scan}
v = [Fr(0), Fr(1, 6), Fr(1, 3), Fr(-1, 2)]
v2 = sum(x * x for x in v)


def parse(fn):
    L = open(fn).read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    rows = [[Fr(x) for x in l.split()] for l in L]
    return rows


def dot(a, b, part=None):
    if part == 1:
        return sum(x * y for x, y in zip(a[:8], b[:8]))
    if part == 2:
        return sum(x * y for x, y in zip(a[8:], b[8:]))
    return sum(x * y for x, y in zip(a, b))


tab = Counter()
for lab, good in ok.items():
    rows = parse(r'C:\tmp\toe_round\stype\z6models\%s.txt' % lab)
    V, W5, W6 = rows[0], rows[6], rows[7]
    feats = (
        ('6(V2-v2) mod 2', (6 * (dot(V, V) - v2)) % 2),
        ('W5^2 mod 1', dot(W5, W5) % 1), ('W6^2 mod 1', dot(W6, W6) % 1),
        ('2VW5 mod1', (2 * dot(V, W5)) % 1), ('2VW6 mod1', (2 * dot(V, W6)) % 1), ('2W5W6 mod1', (2 * dot(W5, W6)) % 1),
        ('6VW5 mod 1', (6 * dot(V, W5)) % 1),
        ('V.W5 mod 1/2', dot(V, W5) % Fr(1, 2)), ('V.W6 mod 1/2', dot(V, W6) % Fr(1, 2)),
        ('W5^2 mod 2', dot(W5, W5) % 2), ('W6^2 mod 2', dot(W6, W6) % 2),
        ('3(V+W5)^2-..', (6 * (dot([a + b for a, b in zip(V, W5)], [a + b for a, b in zip(V, W5)]) - v2)) % 2),
    )
    for name, val in feats:
        tab[(name, str(val), good)] += 1
names = sorted({k[0] for k in tab})
for nm in names:
    rows = {(k[1], k[2]): c for k, c in tab.items() if k[0] == nm}
    print(nm, dict(sorted(rows.items())))
print('--- local conditions N_loc (V_loc^2 - v_loc^2) mod 2 for elements (theta^k, n5 e5 + n6 e6)')
import math
loc = Counter()
for lab, good in ok.items():
    rows = parse(r'C:\tmp\toe_round\stype\z6models\%s.txt' % lab)
    V, W5, W6 = rows[0], rows[6], rows[7]
    fails = []
    for k in range(6):
        for n5 in (0, 1):
            for n6 in (0, 1):
                if k == 0 and n5 == 0 and n6 == 0:
                    continue
                Vl = [k * a + n5 * b + n6 * c for a, b, c in zip(V, W5, W6)]
                vl = [k * x for x in v]
                N = 6 // math.gcd(k, 6) if k else 1
                if n5 or n6:
                    N = N * 2 // math.gcd(N, 2)
                val = (N * (dot(Vl, Vl) - sum(x * x for x in vl))) % 2
                if val != 0:
                    fails.append((k, n5, n6))
    loc[(good, len(fails) == 0)] += 1
print(dict(loc))
