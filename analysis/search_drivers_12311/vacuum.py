"""12311: the candidate's fractional-charge mass pairings under the FULL space-group rule.  Elements (theta^n w^mm, l) (l = the engine's
fixed-point translation 'lat', lattice basis of Geometry_Z6-II_1_1: SU(3) x SU(3) x SU(2)^2, theta = diag(th1, th2, -1),
th1 = [[1,-1],[1,0]] (60 deg), th2 = [[0,-1],[1,-1]] (120 deg)).  A coupling chi_a chi_b prod S^x (x integer; x < 0 = conjugate)
is allowed iff U(1) charges cancel, sum n = 0 mod 6, sum mm = 0 mod 2, and sum of translations lies in sum_k (1 - theta^k) Lambda over
the sectors k present (conjugates contribute -n, -l).  Exact MILP per pair (|x_s| <= 4, degree <= 8), then maximum matching."""
import re, sys, json, itertools
import numpy as np
import sympy as sp
import networkx as nx
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '../search_drivers_12286')
from lr_hypercharge import solve, fermions
P = '../search_drivers_12281/bro/Z6II_60_SM_20260917_810_v9__w6odd.nsoq'
T0 = sp.Rational(-1, 148)
fs = fermions(P); c, eqs, sol = solve(fs); s = sol[0]
free = sorted((set(c) - set(s)) | {x for v in s.values() for x in sp.sympify(v).free_symbols}, key=str)
cv = [sp.sympify(s.get(ci, ci)).subs(free[0], T0) for ci in c]
th = np.zeros((6, 6), dtype=np.int64)
th[0:2, 0:2] = [[1, -1], [1, 0]]; th[2:4, 2:4] = [[0, -1], [1, -1]]; th[4:6, 4:6] = -np.eye(2, dtype=np.int64)
assert (np.linalg.matrix_power(th, 6) == np.eye(6)).all()
I6 = np.eye(6, dtype=np.int64)
D = {k: I6 - np.linalg.matrix_power(th, k) for k in range(1, 6)}
def recs(kinds):
    out = []
    for l in open(P):
        m = re.match(r'FIELD (\d+) m=(\S+) k=\S+ mm=(\S+) n=(\S+) lat=(\S+) dim=(\S*) q=(\S*)', l)
        if m and int(m.group(2)) in kinds:
            d = [int(re.match(r'-?\d+', x).group(0)) for x in m.group(6).split(',')] if m.group(6) else []
            q = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in m.group(7).split(',') if x]
            lat = [int(sp.Rational(x)) for x in m.group(5).split(',')]
            out.append(dict(dims=d, q=q, mm=int(m.group(3)), n=int(m.group(4)), lat=lat, y=sum(a * b for a, b in zip(cv, q))))
    return out
def frac(d, y):
    tl = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[1]) == 2 else [0]
    tr = [sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[2]) == 2 else [0]
    return any((3 * (a + b + y) if abs(d[0]) == 3 else a + b + y).is_integer is False for a in tl for b in tr)
L = recs({19}); S = [r for r in recs({15, 16}) if all(abs(x) == 1 for x in r['dims']) and r['y'] == 0]
Fr = [r for r in L if frac(r['dims'], r['y'])]
den = int(sp.ilcm(*[x.q for r in S + Fr for x in r['q']]))
nq = len(S[0]['q']); ns = len(S)
Qs = np.array([[int(x * den) for x in r['q']] for r in S], dtype=np.int64)
def pair_allowed(a, b, cap=8, xmax=4):
    # variables: xp (ns), xm (ns), y_k (6 x 5), z_k (5 binary), t_n, t_mm (slacks)
    nv = 2 * ns + 30 + 5 + 2
    A, lo, hi = [], [], []
    tq = [int((a['q'][j] + b['q'][j]) * den) for j in range(nq)]
    for j in range(nq):
        A.append(list(Qs[:, j]) + list(-Qs[:, j]) + [0] * 37); lo.append(-tq[j]); hi.append(-tq[j])
    A.append([r['n'] for r in S] + [-r['n'] for r in S] + [0] * 35 + [-6, 0]); v = -(a['n'] + b['n']); lo.append(v); hi.append(v)
    A.append([r['mm'] for r in S] + [-r['mm'] for r in S] + [0] * 35 + [0, -2]); v = -(a['mm'] + b['mm']); lo.append(v); hi.append(v)
    for i in range(6):
        row = [r['lat'][i] for r in S] + [-r['lat'][i] for r in S]
        yrow = []
        for k in range(1, 6):
            yrow += list(-D[k][i, :])
        A.append(row + yrow + [0] * 5 + [0, 0]); v = -(a['lat'][i] + b['lat'][i]); lo.append(v); hi.append(v)
    M = 50
    for kk, k in enumerate(range(1, 6)):
        for i in range(6):
            base = [0] * (2 * ns) + [0] * 30 + [0] * 5 + [0, 0]
            r1 = list(base); r1[2 * ns + kk * 6 + i] = 1; r1[2 * ns + 30 + kk] = -M; A.append(r1); lo.append(-np.inf); hi.append(0)
            r2 = list(base); r2[2 * ns + kk * 6 + i] = -1; r2[2 * ns + 30 + kk] = -M; A.append(r2); lo.append(-np.inf); hi.append(0)
        present = 1 if (a['n'] % 6 in (k, 6 - k) or b['n'] % 6 in (k, 6 - k)) else 0
        row = [0] * (2 * ns + 30 + 5 + 2)
        for si, r in enumerate(S):
            if r['n'] % 6 in (k, 6 - k):
                row[si] = -1; row[ns + si] = -1
        row[2 * ns + 30 + kk] = 1
        A.append(row); lo.append(-np.inf); hi.append(present)
    A.append([1] * (2 * ns) + [0] * 37); lo.append(0); hi.append(cap)
    cobj = np.array([1] * (2 * ns) + [0] * 37, dtype=float)
    lb = [0] * (2 * ns) + [-M] * 30 + [0] * 5 + [-100, -100]; ub = [xmax] * (2 * ns) + [M] * 30 + [1] * 5 + [100, 100]
    res = milp(cobj, constraints=LinearConstraint(np.array(A, dtype=float), lo, hi), integrality=np.ones(nv), bounds=Bounds(lb, ub))
    return (int(round(res.fun)) if res.success else None)
conj = lambda d: [(-x if abs(x) in (3, 8, 28, 56) else x) for x in d]
G = nx.Graph(); G.add_nodes_from(range(len(Fr))); deg = {}
for i, j in itertools.combinations(range(len(Fr)), 2):
    A_, B_ = Fr[i], Fr[j]
    if conj(A_['dims']) != B_['dims'] or A_['y'] + B_['y'] != 0:
        continue
    d = pair_allowed(A_, B_)
    if d is not None:
        G.add_edge(i, j); deg[(i, j)] = d
Mt = nx.max_weight_matching(G, maxcardinality=True)
# control: the rule must reject something -- the same search with the translation rows dropped is 12300 (134 pairs)
out = dict(fractional=len(Fr), singlets=ns, allowed_pairs=G.number_of_edges(), liftable=2 * len(Mt),
           degrees=sorted(deg[tuple(sorted(e))] for e in Mt) if Mt else [])
print(out); json.dump(out, open('vacuum.json', 'w'), indent=1)
