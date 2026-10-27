"""12298: independent, pre-registered test of the bicharacter WITH fixed-point labels (the 12296 correction).  Fresh SUSY Z4_1_1 models
(seed 12298; standard embedding + random order-2 lines), and the shifted line is now W1 = W2 (on a torus that theta^2 rotates), not W5.
theta = diag(R90, R90, -1) on the unit lattice (Geometry_Z4_1_1).  For every consistent torsion class of W1 shifts, B is evaluated
exactly on all commuting pairs (labels in {0,1}^6, powers of theta) and the prediction 'changed iff B != 0 somewhere' is written to
predictions.json BEFORE any engine run."""
import json, sys, random, itertools, collections
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, '../search_drivers_12274'); sys.path.insert(0, '../search_drivers_12267'); sys.path.insert(0, '../search_drivers_12276')
import torsion_B
from mirage import e8_short, fmt
from brothers_z6 import R12
R90 = np.array([[0, -1], [1, 0]]); th = np.zeros((6, 6), dtype=np.int64)
th[0:2, 0:2] = R90; th[2:4, 2:4] = R90; th[4:6, 4:6] = -np.eye(2, dtype=np.int64)
def twists(geo):
    M = np.eye(6, dtype=np.int64); out = []
    for k in range(4):
        out.append(((k,), M.copy())); M = th @ M
    return out, 2
torsion_B.twists = twists
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
even = lambda x: x.denominator == 1 and x % 2 == 0
R8 = [list(r) for r in e8_short(2) if sum(x * x for x in r) == 2]
Z8 = [F(0)] * 8
ROOTS = [r + Z8 for r in R8] + [Z8 + r for r in R8]
V = [F(1, 4), F(1, 4), F(-1, 2)] + [F(0)] * 13
Z = [F(0)] * 16
rng = random.Random(12298)
def ok(W):
    if any(not even(2 * dot(a, V)) or not even(2 * dot(a, a)) for a in W):
        return False
    return all(even(2 * dot(W[i], W[j])) for i in range(len(W)) for j in range(i + 1, len(W)))
def randW():
    v = [F(0)] * 16
    for _ in range(rng.choice((1, 2, 3))):
        v = [x + y for x, y in zip(v, rng.choice(ROOTS))]
    return [x / 2 for x in v]
def write(path, lab, W1, W3, W5, W6):
    rows = [V, Z, W1, W1, W3, W3, W5, W6]
    open(path, 'w', newline='\n').write(f'begin model\nLabel:{lab}\nSpaceGroup:Geometry/Geometry_Z4_1_1.txt\nLattice:E8xE8\n'
                                        'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in r) for r in rows) + '\nend model\n')
pred, lst, m = [], [], 0
while m < 12:
    W1, W3, W5, W6 = [randW() if rng.random() < p else list(Z) for p in (1.0, 0.4, 0.8, 0.6)]
    if not any(W1) or not ok([W1, W3, W5, W6]):
        continue
    X = np.array([[int(12 * x) for x in r] for r in (V, W1, W3, W5, W6)], dtype=np.int64)
    G = (R12 @ X.T) % 288
    rep = {(0,) * 5: np.zeros(16, dtype=np.int64)}; fr = [(0,) * 5]
    while fr:
        new = []
        for g in fr:
            for i in range(len(R12)):
                h = tuple((np.array(g) + G[i]) % 288)
                if h not in rep:
                    rep[h] = rep[g] + R12[i]; new.append(h)
        fr = new
    for j, (c, l12) in enumerate(sorted(rep.items())):
        lam = [F(int(x), 12) for x in l12]
        W1b = [x + y for x, y in zip(W1, lam)]
        if not ok([W1b, W3, W5, W6]):
            continue
        p = f'z4/m{m:02d}_c{j:03d}.txt'
        write(p, f'Z4b_{m:02d}_{j:03d}', W1b, W3, W5, W6)
        rows9 = [Z, V, Z, W1, W1, W3, W3, W5, W6]          # torsion_B layout: Witten row (empty), shift rows, six lines
        nz, vals = (0, {}) if not any(lam) else torsion_B.nonzero_B(rows9, 'Z4', [0, 1], lam)
        pred.append(dict(model=m, j=j, trivial=not any(lam), file=p, nonzeroB=int(nz), prediction=('control' if not any(lam) else ('changed' if nz else 'identical'))))
        lst.append('/mnt/c/tmp/toe_wt/analysis/search_drivers_12298/' + p)
    m += 1
json.dump(pred, open('predictions.json', 'w'), indent=1)
open('list.txt', 'w', newline='\n').write('\n'.join(lst) + '\n')
print(len(pred), 'files;', collections.Counter(p['prediction'] for p in pred))
