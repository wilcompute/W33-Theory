"""Search Z6-II (G2 x SU3 x SU2^2) models realising the SO(10) clock grading + a three-family order-3 shift."""
import sys
import itertools
import random
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
from w33_pass12053_gate_sets_and_real_forms import setup

g = Gradings()
R, fib = g.R, g.fib
Adj, invs, tick, _ = setup()
ev = {h: frozenset(x for x in range(40) if not g.vecs[h][fib[x]].any()) for h in range(g.n)}
cpt = {h: next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == set(ev[h])) for h in range(g.n) if g.kinds[h] == 'clock'}
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])


def e8_norm(n2):
    out = []
    for half in (False, True):
        rng = [k / 2 for k in range(-5, 6, 2)] if half else list(range(-2, 3))
        for v in itertools.product(rng, repeat=8):
            if abs(sum(x * x for x in v) - n2) < 1e-9 and abs(sum(v) % 2) < 1e-9:
                out.append(np.array(v, float))
    return out


N2, N4 = e8_norm(2), e8_norm(4)
par = lambda a: (np.round(2 * (R @ a)).astype(int) % 2 == 1)  # noqa: E731
lift = {}
for v in N2 + N4:
    lift.setdefault(par(v / 2).tobytes(), []).append(v / 2)
p = 0
K = [h for h in cpt if cpt[h] == p]
sig = next(s for s in range(g.n) if g.kinds[s] == 'split' and g.typ(g.fixedmask(g.span_of(K[:2] + [s]))) == ('D5',))
V3 = g.span_of(K[:2] + [sig])
d5 = np.nonzero(g.fixedmask(V3))[0]
# three-family shifts keeping d5: net 16 = +-3, fixed dim 86
coefs = np.array(list(itertools.product(range(3), repeat=8)))
lams = coefs @ SIMPLE
PH = np.round(lams @ R.T).astype(int) % 3
Bd = np.linalg.svd(R[d5])[2][:5]
proj = np.array([np.sum((Bd @ R[a]) ** 2) for a in range(240)])
tfam = [lams[i] / 3 for i in range(len(PH)) if PH[i].any() and not np.any(PH[i][d5] != 0) and 8 + int(np.sum(PH[i] == 0)) == 86]
print('three-family-type shifts keeping d5:', len(tfam))
v2 = Fr(7, 18)
rnd = random.Random(1)
# second-E8 libraries
lib6 = [np.zeros(8)] + [lam / 6 for lam in (coefs[rnd.sample(range(len(coefs)), 400)] @ SIMPLE)] + [lam / 3 for lam in (coefs[rnd.sample(range(len(coefs)), 200)] @ SIMPLE)] + [v / 2 for v in N2[:60]]
half_roots = [v / 2 for v in N2]
half_n4 = [v / 2 for v in N4]
fr = lambda x: Fr(x).limit_denominator(36)  # noqa: E731
found = []
for t in tfam:
    for a1 in lift[g.vecs[K[0]].tobytes()][:8]:
        for a2 in lift[g.vecs[K[1]].tobytes()][:8]:
            for as_ in lift[g.vecs[sig].tobytes()][:8]:
                A = a1 + t
                for Vp in lib6:
                    VV = fr(A @ A) + fr(Vp @ Vp)
                    if (VV - v2) * 3 % 1 != 0 or ((VV - v2) * 6) % 2 != 0:
                        continue
                    for b2 in half_roots[:40]:
                        W5sq = fr(a2 @ a2) + fr(b2 @ b2)
                        if W5sq.denominator != 1:
                            continue
                        if (2 * (fr(A @ a2) + fr(Vp @ b2))).denominator != 1:
                            continue
                        for b3 in [np.zeros(8)] + half_n4[:60]:
                            W6sq = fr(as_ @ as_) + fr(b3 @ b3)
                            if W6sq.denominator != 1:
                                continue
                            if (2 * (fr(A @ as_) + fr(Vp @ b3))).denominator != 1:
                                continue
                            if (2 * (fr(a2 @ as_) + fr(b2 @ b3))).denominator != 1:
                                continue
                            found.append((A, Vp, a2, b2, as_, b3))
                            break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                break
        if found:
            break
    if found:
        break
print('found', len(found))
if found:
    A, Vp, a2, b2, as_, b3 = found[0]
    def row(x, y):
        return ' '.join(str(fr(v)) if fr(v).denominator != 1 else '%d/1' % int(fr(v)) for v in list(x) + list(y))
    zero = np.zeros(8)
    lines = [row(A, Vp)] + [row(zero, zero)] * 4 + [row(a2, b2), row(as_, b3)]
    txt = 'begin model\nLabel:W33SO10\nSpaceGroup:Geometry/Geometry_Z6-II_G2xSU3xSU2^2.txt\nLattice:E8xE8\nShifts and Wilsonlines:\n' + '\n'.join(lines) + '\nend model\n'
    open('model_so10.txt', 'w').write(txt)
    print(txt)
