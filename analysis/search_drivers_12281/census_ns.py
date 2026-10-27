"""12281: torsion brothers of the non-SUSY Z6-II A8 models (~/orb/p1109x/ssz6ii, 1400 with an order-2 W5 on the SU(2)^2-type torus).
Prediction from the bicharacter (12274/12282): among consistent shifts of W5 only V0.lam mod 2 matters (Witten element x order-2
translation); all other parities (V1, W3, W5) are coprime-order and invisible.  For 300 random models: control, an 'even' brother
(V0.lam even, other parities nonzero), an 'odd' brother (V0.lam odd), and a lattice-valued W6 = lam with V0.lam odd (Scherk-Schwarz-type).
Consistency of every shifted model (prefactors gcd of the orders 2, 6, 3, 2): 2 W.V0, 2 W.V1, W.W3, 2 W.W, 2 W.W' even."""
import glob, random, json, sys, os, itertools
from fractions import Fraction as F
sys.path.insert(0, '../search_drivers_12267')
from mirage import read, fmt, e8_short
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
even = lambda x: x.denominator == 1 and x % 2 == 0
R8 = [list(r) for r in e8_short(2) if sum(x * x for x in r) == 2]
Z8 = [F(0)] * 8
ROOTS = [r + Z8 for r in R8] + [Z8 + r for r in R8]
rng = random.Random(12281)
CAND = ROOTS + [[x + y for x, y in zip(rng.choice(ROOTS), rng.choice(ROOTS))] for _ in range(3000)]


def ok(rows):
    V0, V1, W3, W5, W6 = rows[0], rows[1], rows[5], rows[7], rows[8]
    for W, other in ((W5, W6), (W6, W5)):
        if not any(W):
            continue
        if not (even(2 * dot(W, V0)) and even(2 * dot(W, V1)) and even(dot(W, W3)) and even(2 * dot(W, W)) and even(2 * dot(W, other))):
            return False
    return True


def find(rows, row, want_odd, need_other_nonzero=False):
    for lam in CAND:
        p = dot(lam, rows[0])
        if p.denominator != 1 or (p % 2 == 1) != want_odd:
            continue
        if need_other_nonzero and all((2 * dot(lam, rows[k])) % 4 == 0 for k in (1, 5, 7)):
            continue
        new = [r[:] for r in rows]
        new[row] = [x + y for x, y in zip(new[row], lam)]
        if ok(new):
            return new
    return None


files = sorted(f for f in glob.glob('models/*.txt'))
rng.shuffle(files)
lst, idx = [], []
for f in files:
    head, rows = read(f)
    if len(rows) != 9 or not any(rows[7]) or any(rows[8]) or not ok(rows):
        continue
    base = os.path.basename(f)[:-4]
    entry = dict(model=base, files={})
    for tag, row, odd, other in (('even', 7, False, True), ('odd', 7, True, False), ('w6odd', 8, True, False)):
        new = find(rows, row, odd, other)
        if new is None:
            continue
        p = f'bro/{base}__{tag}.txt'
        open(p, 'w', newline='\n').write(head + 'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in r) for r in new) + '\nend model\n')
        entry['files'][tag] = p
    p = f'bro/{base}__ctrl.txt'
    open(p, 'w', newline='\n').write(open(f).read())
    entry['files']['ctrl'] = p
    idx.append(entry)
    lst += ['/mnt/c/tmp/toe_wt/analysis/search_drivers_12281/' + q for q in entry['files'].values()]
    if len(idx) == 300:
        break
json.dump(idx, open('census_index.json', 'w'), indent=1)
open('census_list.txt', 'w', newline='\n').write('\n'.join(lst) + '\n')
import collections
print(len(idx), 'models', collections.Counter(tuple(sorted(e['files'])) for e in idx))
