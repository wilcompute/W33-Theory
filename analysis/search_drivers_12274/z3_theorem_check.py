"""12275: T6/Z3 -- for random consistent models and random lattice vectors lam (both lines of one torus shifted), B vanishes on all
commuting pairs whenever the shifted model satisfies (7d)-(7f), and is nonzero when (7f) is violated (control: the theorem's
hypothesis is needed)."""
import random, json, sys, collections
from fractions import Fraction as F
sys.path.insert(0, '.'); sys.path.insert(0, '../search_drivers_12267'); sys.path.insert(0, '../search_drivers_12268')
from torsion_B import nonzero_B
from mirage import read, e8_short
from ploger_gate import check
R8 = [list(r) for r in e8_short(2) if sum(x * x for x in r) == 2]
Z8 = [F(0)] * 8
ROOTS = [r + Z8 for r in R8] + [Z8 + r for r in R8]
rng = random.Random(2027)
eng = [l.split() for l in open('../search_drivers_12265/z3_engine_out.txt')]
ok = [p[0].split('search_drivers_12265/')[1] for p in eng if len(p) == 3 and p[2] == '1']
tab = collections.Counter()
for t in range(400):
    name = rng.choice(ok)
    _, rows = read('../search_drivers_12265/' + name)
    tori = [tt for tt in range(3) if any(rows[3 + 2 * tt])]
    if not tori:
        continue
    tt = rng.choice(tori)
    lam = [F(0)] * 16
    for _ in range(rng.choice((1, 2, 3))):
        lam = [x + y for x, y in zip(lam, rng.choice(ROOTS))]
    new = [r[:] for r in rows]
    S = [2 * tt, 2 * tt + 1]
    for b in S:
        new[3 + b] = [x + y for x, y in zip(new[3 + b], lam)]
    consistent = not check(new)
    n, _ = nonzero_B(rows, 'Z3', S, lam)
    tab[('shift consistent' if consistent else 'shift violates Ploger', 'B=0' if n == 0 else 'B!=0')] += 1
for k, v in sorted(tab.items()):
    print(k, v)
json.dump({str(k): v for k, v in tab.items()}, open('z3_theorem_check.json', 'w'), indent=1)
