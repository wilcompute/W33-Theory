"""12296: the refined torsion rule on SUSY T6/Z4 (Geometry_Z4_1_1: twist (1/4, 1/4, -1/2); order-2 lines, W1 = W2, W3 = W4, W5 and W6
independent on torus 3, which theta^2 fixes).  Refined prediction: a twist power theta^k that fixes the torus of an order-2 line gives
B = (k/2) V.lam with V.lam integral by consistency, so torsion needs k odd; on Z4 only k = 2 fixes torus 3 -> NO torsion, although
gcd(2, 2) = 2 (the naive coprime-order rule would allow it).  Models: standard-embedding shift V = (1/4, 1/4, -1/2, 0^5)(0^8) plus
random order-2 lines; every consistent torsion class of W5 shifts (c = 2 X.lam mod 4 for X = V, W1, W3, W5, W6) is a brother.
Consistency prefilter (prefactors gcd(4,2) = 2 and 2): 2 W.V, 2 W.W, 2 W.W' even for every pair; the engine decides at load."""
import random, json, sys
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, '../search_drivers_12267'); sys.path.insert(0, '../search_drivers_12276')
from mirage import e8_short, fmt
from brothers_z6 import R12
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
even = lambda x: x.denominator == 1 and x % 2 == 0
R8 = [list(r) for r in e8_short(2) if sum(x * x for x in r) == 2]
Z8 = [F(0)] * 8
ROOTS = [r + Z8 for r in R8] + [Z8 + r for r in R8]
V = [F(1, 4), F(1, 4), F(-1, 2)] + [F(0)] * 13
rng = random.Random(12296)
def ok(W):
    for a in W:
        if not even(2 * dot(a, V)) or not even(2 * dot(a, a)):
            return False
    for i in range(len(W)):
        for j in range(i + 1, len(W)):
            if not even(2 * dot(W[i], W[j])):
                return False
    return True
def randW():
    v = [F(0)] * 16
    for _ in range(rng.choice((1, 2, 3))):
        v = [x + y for x, y in zip(v, rng.choice(ROOTS))]
    return [x / 2 for x in v]
def write(path, lab, W1, W3, W5, W6):
    rows = [V, [F(0)] * 16, W1, W1, W3, W3, W5, W6]
    open(path, 'w', newline='\n').write(f'begin model\nLabel:{lab}\nSpaceGroup:Geometry/Geometry_Z4_1_1.txt\nLattice:E8xE8\n'
                                        'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in r) for r in rows) + '\nend model\n')
models, lst = [], []
tries = 0
while len(models) < 12 and tries < 200000:
    tries += 1
    W1, W3, W5, W6 = [randW() if rng.random() < p else [F(0)] * 16 for p in (0.4, 0.4, 1.0, 0.6)]
    if not any(W5) or not ok([W1, W3, W5, W6]):
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
    m = len(models); bro = []
    for j, (c, l12) in enumerate(sorted(rep.items())):
        lam = [F(int(x), 12) for x in l12]
        W5b = [x + y for x, y in zip(W5, lam)]
        if not ok([W1, W3, W5b, W6]):
            continue
        p = f'z4/m{m:02d}_c{j:03d}.txt'
        write(p, f'Z4_{m:02d}_{j:03d}', W1, W3, W5b, W6)
        bro.append(dict(j=j, cls=list(map(int, c)), trivial=not any(lam), file=p))
        lst.append('/mnt/c/tmp/toe_wt/analysis/search_drivers_12296/' + p)
    models.append(dict(model=m, classes=len(rep), brothers=bro))
json.dump(models, open('z4_index.json', 'w'), indent=1)
open('z4_list.txt', 'w', newline='\n').write('\n'.join(lst) + '\n')
print(len(models), 'models', [len(mm['brothers']) for mm in models], 'tries', tries)
