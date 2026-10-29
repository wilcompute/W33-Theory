"""12353/12354: for the seven three-generation models: massless Bose-Fermi balance (on-shell component counts as in 12280), Higgs scalars
((1,2) under the chosen SU(3) x SU(2) with |Y| = 1/2, Y from the SUSY parent's exact vector), and whether the fractional-charge
fermions (all chiral content is SM, so these are the (1,2)_0 doublets and any vector-like fractional states) can pair up: conjugate
SU(3) x SU(2) x hidden representations, opposite Y, and q_a + q_b in the INTEGER lattice of the SM-singlet scalars' U(1) charges plus
the point-group (sum of Z6 powers = 0 mod 6) and Witten (sum = 0 mod 2) rules; translation rule as in 12311 (SU(3) x SU(3) x SU(2)^2
lattice).  For the pseudo-real (1,2)_0 doublets a pair may also be two copies (a = b is excluded: needs two distinct fields)."""
import re, json, os, sys, math, itertools, collections
import numpy as np
import sympy as sp
import networkx as nx
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, '../search_drivers_12277')
from bf_count import count
yv = json.load(open('../search_drivers_12351/yvec.json')); ch = json.load(open('../search_drivers_12351/chiral.json'))
th = np.zeros((6, 6), dtype=np.int64)
th[0:2, 0:2] = [[1, -1], [1, 0]]; th[2:4, 2:4] = [[0, -1], [1, -1]]; th[4:6, 4:6] = -np.eye(2, dtype=np.int64)
D6 = {k: np.eye(6, dtype=np.int64) - np.linalg.matrix_power(th, k) for k in range(1, 6)}
def fields(p, Y):
    L = open(p, errors='ignore').read().split('\n'); out = []; cur = None
    for l in L:
        if l.startswith('FIELD'):
            m = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=(\S+) n=(\S+) lat=(\S+) dim=(\S*) q=(\S*)', l)
            cur = dict(m=int(m.group(1)), mm=int(m.group(2)), n=int(m.group(3)), lat=[int(sp.Rational(x)) for x in m.group(4).split(',')],
                       d=tuple(int(re.match(r'-?\d+', x).group(0)) for x in m.group(5).split(',')) if m.group(5) else (),
                       q=[sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in m.group(6).split(',') if x], y=None)
            out.append(cur)
        elif l.startswith('W ') and cur is not None and cur['y'] is None:
            P = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')]
            cur['y'] = sum(a * b for a, b in zip(Y, P))
    return out
def frac(d, i3, i2, y):
    for t in ([sp.Rational(1, 2), -sp.Rational(1, 2)] if abs(d[i2]) == 2 else [0]):
        if (3 * (t + y) if abs(d[i3]) == 3 else t + y).is_integer is False:
            return True
    return False
res = {}
for m in ('Z6II_06_SM_20260917_2618_v0', 'Z6II_06_SM_20260917_2618_v1', 'Z6II_06_SM_20260917_2618_v2', 'Z6II_06_SM_20260917_2618_v3',
          'Z6II_23_SM_20260917_2913_v6', 'Z6II_23_SM_20260917_2913_v7', 'Z6II_23_SM_20260917_2913_v8'):
    lab = re.search(r'(SM_20260917_\d+)', m).group(1); Y = [sp.Rational(x) for x in yv[lab]['Yvec']]
    D = '../search_drivers_12302/bro/' if os.path.exists(f'../search_drivers_12302/bro/{m}__ctrl.nsoq') else '../search_drivers_12281/bro/'
    p = D + f'{m}__ctrl.nsoq'
    c = count(p); bos = c['gauge'] + c['scalar'] + c['moduli'] + c['gravity']
    fs = fields(p, Y); i3, i2 = ch[m]['SU3'], ch[m]['SU2']
    # exact U(1) charges: the printed q can carry float noise with huge rational denominators (SM_2913 overflowed int64).
    # U(1) neutrality of a combination <=> its total weight lies in the span of the non-abelian roots, so use an exact rational
    # basis of the orthogonal complement of the roots (FACTOR lines) and q' = U . P on each field's first left-moving weight.
    roots = []
    for l in open(p, errors='ignore'):
        if l.startswith('FACTOR'):
            for r in l.split('|')[1:]:
                roots.append([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()])
    Ub = sp.Matrix(roots).nullspace() if roots else [sp.eye(16)[:, i] for i in range(16)]
    Wfirst = {}
    cur = None
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            cur = int(l.split()[1])
        elif l.startswith('W ') and cur is not None and cur not in Wfirst:
            Wfirst[cur] = sp.Matrix([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')])
    idx = 0
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            fid = int(l.split()[1]); f = fs[idx]; idx += 1
            f['q'] = [ (u.T * Wfirst[fid])[0] for u in Ub ] if fid in Wfirst else [0] * len(Ub)
    others = lambda d: [j for j in range(len(d)) if j not in (i3, i2)]
    higgs = sum(1 for f in fs if f['m'] in (15, 16) and abs(f['d'][i3]) == 1 and abs(f['d'][i2]) == 2 and abs(f['y']) == sp.Rational(1, 2)
                and all(abs(f['d'][j]) == 1 for j in others(f['d'])))
    Fr = [f for f in fs if f['m'] == 19 and frac(f['d'], i3, i2, f['y'])]
    S = [f for f in fs if f['m'] in (15, 16) and all(abs(x) == 1 for x in f['d']) and f['y'] == 0]
    nq = len(S[0]['q']); ns = len(S)
    # each U(1) row is its own equation: scale component j by its own denominator (a common one overflowed int64 for SM_2913)
    dens = [int(sp.ilcm(*[f['q'][j].q for f in S + Fr])) for j in range(nq)]
    Qs = np.array([[int(f['q'][j] * dens[j]) for j in range(nq)] for f in S], dtype=np.int64)
    def allowed(a, b, xmax=4, cap=8):
        nv = 2 * ns + 30 + 5 + 2; A, lo, hi = [], [], []
        tq = [int((a['q'][j] + b['q'][j]) * dens[j]) for j in range(nq)]
        for j in range(nq):
            A.append(list(Qs[:, j]) + list(-Qs[:, j]) + [0] * 37); lo.append(-tq[j]); hi.append(-tq[j])
        A.append([f['n'] for f in S] + [-f['n'] for f in S] + [0] * 35 + [-6, 0]); v = -(a['n'] + b['n']); lo.append(v); hi.append(v)
        A.append([f['mm'] for f in S] + [-f['mm'] for f in S] + [0] * 35 + [0, -2]); v = -(a['mm'] + b['mm']); lo.append(v); hi.append(v)
        for i in range(6):
            yrow = []
            for k in range(1, 6): yrow += list(-D6[k][i, :])
            A.append([f['lat'][i] for f in S] + [-f['lat'][i] for f in S] + yrow + [0] * 7); v = -(a['lat'][i] + b['lat'][i]); lo.append(v); hi.append(v)
        M = 50
        for kk, k in enumerate(range(1, 6)):
            for i in range(6):
                for sgn in (1, -1):
                    r = [0] * nv; r[2 * ns + kk * 6 + i] = sgn; r[2 * ns + 30 + kk] = -M; A.append(r); lo.append(-np.inf); hi.append(0)
            present = 1 if (a['n'] % 6 in (k, 6 - k) or b['n'] % 6 in (k, 6 - k)) else 0
            r = [0] * nv
            for si, f in enumerate(S):
                if f['n'] % 6 in (k, 6 - k): r[si] = -1; r[ns + si] = -1
            r[2 * ns + 30 + kk] = 1; A.append(r); lo.append(-np.inf); hi.append(present)
        A.append([1] * (2 * ns) + [0] * 37); lo.append(0); hi.append(cap)
        resm = milp(np.array([1] * (2 * ns) + [0] * 37, dtype=float), constraints=LinearConstraint(np.array(A, dtype=float), lo, hi),
                    integrality=np.ones(nv), bounds=Bounds([0] * (2 * ns) + [-M] * 30 + [0] * 5 + [-100, -100], [xmax] * (2 * ns) + [M] * 30 + [1] * 5 + [100, 100]))
        return resm.success
    conj = lambda d: tuple(-x if abs(x) > 2 else x for x in d)
    G = nx.Graph(); G.add_nodes_from(range(len(Fr)))
    for a, b in itertools.combinations(range(len(Fr)), 2):
        A_, B_ = Fr[a], Fr[b]
        if conj(A_['d']) == B_['d'] and A_['y'] + B_['y'] == 0 and allowed(A_, B_):
            G.add_edge(a, b)
    Mt = nx.max_weight_matching(G, maxcardinality=True)
    res[m] = dict(n_F=c['fermion'], n_B=bos, nF_minus_nB=c['fermion'] - bos, higgs_scalars=higgs, fractional_fermions=len(Fr),
                  pairable=G.number_of_edges(), liftable=2 * len(Mt), singlets=ns)
    print(m, res[m])
json.dump(res, open('vet.json', 'w'), indent=1)
