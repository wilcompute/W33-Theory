"""12217: THEOREM by exhaustion (same scope as the untwisted theorem 12170: the 7 e6+a2 bases x all 864 A4-type order-3 lambda).
A twisted massless state has |P|^2 = 4/3 (no oscillator; with one, 2/3 < 6/5), P = (P1, P2) in Gamma + V_f, and a 10 needs the
SU(5) projection of P1 to have norm 6/5; since |P2|^2 >= 0 it suffices to show no P1 in E8 + u with |P1|^2 <= 4/3 and
|proj_A4 P1|^2 = 6/5, for every first-E8 fixed-point class u = V1 + n1 Wf + n2 lambda (n1, n2 in Z3) and its Witten partner
u + V0.  u is reduced to its nearest E8 point (covering radius 1), so E8 vectors of norm <= 4 (2401) suffice.  Control: the
same machinery on the untwisted shell (u = 0, |P|^2 = 2) must find the 20 10-type roots of the generation 10s... in fact 40
(10 + 10bar, counted with the (10,5) multiplicity inside the first E8 only)."""
import itertools, json, sys
import numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
g = Gradings(); R = g.R
integ = lambda a: np.abs(a - np.round(a)) < 1e-9
SIMPLE = np.array([[0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
                   [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])
coefs = np.array(list(itertools.product(range(3), repeat=8)))
L3 = (coefs @ SIMPLE) / 3


def e8_upto(maxn):
    out = []
    for half in (0, 1):
        vals = [x + 0.5 * half for x in range(-3, 3)] if half else list(range(-2, 3))
        for v in itertools.product(vals, repeat=8):
            if sum(x * x for x in v) <= maxn + 1e-9 and round(sum(v)) % 2 == 0:
                out.append(v)
    return np.array(out, float)


E8S = e8_upto(4)


def nearest_d8(u):
    f = np.round(u)
    if round(f.sum()) % 2:
        i = np.argmax(np.abs(u - f)); f[i] += 1 if u[i] > f[i] else -1
    return f


def reduce(u):
    a = nearest_d8(u)
    b = nearest_d8(u - 0.5) + 0.5
    return u - (a if np.sum((u - a) ** 2) <= np.sum((u - b) ** 2) else b)


def hits(u, B, shell):
    P = E8S + reduce(u)
    n = (P * P).sum(1)
    P = P[n <= shell + 1e-9]
    pr = P @ B.T
    return int(np.sum(np.abs((pr * pr).sum(1) - 6 / 5) < 1e-9))


D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
BASES = ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']
assert len(E8S) == 2401
res = {}
for base in BASES:
    rows = open(D + '/' + base + '_9.txt').read().split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    v = [np.array([float(Fr(x)) for x in r.split()[:16]]) for r in rows]
    V0, V1, Wf = v[0][:8], v[1][:8], v[3][:8]
    d5 = next(c for c in g.comps(integ(R @ V0) & integ(R @ V1) & integ(R @ Wf)) if len(c) == 40)
    P = integ(R[d5] @ L3.T)
    nlam = tw = ctrl_bad = 0
    for j in range(len(coefs)):
        mk = np.zeros(240, bool); mk[np.array(d5)[P[:, j]]] = True
        if g.typ(mk) != ('A4',):
            continue
        nlam += 1
        a4 = np.nonzero(mk)[0]
        B = np.linalg.svd(R[a4])[2][:4]
        if hits(np.zeros(8), B, 2.0) == 0:
            ctrl_bad += 1
        for n1, n2 in itertools.product(range(3), repeat=2):
            u = V1 + n1 * Wf + n2 * L3[j]
            tw += hits(u, B, 4 / 3) + hits(u + V0, B, 4 / 3)
    res[base] = dict(lambdas=nlam, twisted_10_type_vectors=tw, control_failures=ctrl_bad)
    print(base, res[base], flush=True)
json.dump(res, open('exhaust10.json', 'w'), indent=1)
