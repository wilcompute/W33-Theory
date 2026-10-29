"""12357-12360 shared engine: SM_2913_v6 fields (exact U(1) charges = complement of the non-abelian roots on the first weight, 12353) and
the minimal singlet degree of a gauge- and space-group-allowed coupling of a fixed set of fields (each with conjugation sign +-1) times
SM-singlet scalars s or s* (point group sum n = 0 mod 6, Witten sum = 0 mod 2, translation sum in sum_k (1 - theta^k) Lambda over the
sectors present -- the 12353 MILP, objective = total singlet degree).  'allowed' restricts the singlets (vacuum sets, 12360).
Not imposed: the non-SUSY vertex (H-momentum) rule; SU(3)/SU(2) contraction is ensured by the caller's choice of field types (Y and the
U(1)s are conserved exactly)."""
import re, json, os
import numpy as np
import sympy as sp
from scipy.optimize import milp, LinearConstraint, Bounds
HERE = os.path.dirname(os.path.abspath(__file__))
M_ = os.environ.get('MONO_MODEL', 'Z6II_23_SM_20260917_2913_v6')
yv = json.load(open(os.path.join(HERE, '../search_drivers_12351/yvec.json'))); ch = json.load(open(os.path.join(HERE, '../search_drivers_12351/chiral.json')))
Yv = [sp.Rational(x) for x in (json.loads(os.environ['MONO_Y']) if os.environ.get('MONO_Y') else yv[re.search(r'(SM_20260917_\d+)', M_).group(1)]['Yvec'])]
I3, I2 = (int(os.environ['MONO_I3']), int(os.environ['MONO_I2'])) if os.environ.get('MONO_I3') else (ch[M_]['SU3'], ch[M_]['SU2'])
th = np.zeros((6, 6), dtype=np.int64)
th[0:2, 0:2] = [[1, -1], [1, 0]]; th[2:4, 2:4] = [[0, -1], [1, -1]]; th[4:6, 4:6] = -np.eye(2, dtype=np.int64)
D6 = {k: np.eye(6, dtype=np.int64) - np.linalg.matrix_power(th, k) for k in range(1, 6)}
def load(p=None):
    p = p or os.environ.get('MONO_PATH') or next(q for q in (os.path.join(HERE, f'../search_drivers_12302/bro/{M_}__ctrl.nsoq'), os.path.join(HERE, f'../search_drivers_12281/bro/{M_}__ctrl.nsoq')) if os.path.exists(q))
    roots = []
    for l in open(p, errors='ignore'):
        if l.startswith('FACTOR'):
            for r in l.split('|')[1:]:
                roots.append([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()])
    Ub = sp.Matrix(roots).nullspace()
    out = []; cur = None
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            mm = re.match(r'FIELD (\d+) m=(\S+) k=\S+ mm=(\S+) n=(\S+) lat=(\S+) dim=(\S*) q=', l)
            cur = dict(id=int(mm.group(1)), m=int(mm.group(2)), w=int(mm.group(3)), n=int(mm.group(4)),
                       lat=[int(sp.Rational(x)) for x in mm.group(5).split(',')],
                       d=tuple(int(re.match(r'-?\d+', x).group(0)) for x in mm.group(6).split(',')) if mm.group(6) else (), P=None)
            out.append(cur)
        elif l.startswith('W ') and cur is not None and cur['P'] is None:
            cur['P'] = sp.Matrix([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')])
    for f in out:
        f['y'] = sum(a * b for a, b in zip(Yv, f['P'])) if f['P'] is not None else sp.Integer(0)
        f['q'] = [(u.T * f['P'])[0] for u in Ub] if f['P'] is not None else [sp.Integer(0)] * len(Ub)
    return out, Ub
FS, UB = load()
def smsing(f):
    return all(abs(f['d'][j]) == 1 for j in range(len(f['d'])) if j not in (I3, I2))
S = [f for f in FS if f['m'] == 15 and all(abs(x) == 1 for x in f['d']) and f['y'] == 0]     # one listing per complex scalar
NQ = len(UB); NS = len(S)
DENS = [int(sp.ilcm(*[f['q'][j].q for f in FS])) for j in range(NQ)]
QS = np.array([[int(f['q'][j] * DENS[j]) for j in range(NQ)] for f in S], dtype=np.int64)
def min_degree(fixed, allowed=None, xmax=6, cap=12):
    """fixed = [(field, sign)], sign +1 field / -1 conjugate.  Returns the minimal number of singlet insertions or None."""
    nv = 2 * NS + 30 + 5 + 2; A, lo, hi = [], [], []
    tq = [int(sum(s * f['q'][j] for f, s in fixed) * DENS[j]) for j in range(NQ)]
    for j in range(NQ):
        A.append(list(QS[:, j]) + list(-QS[:, j]) + [0] * 37); lo.append(-tq[j]); hi.append(-tq[j])
    v = -sum(s * f['n'] for f, s in fixed)
    A.append([f['n'] for f in S] + [-f['n'] for f in S] + [0] * 35 + [-6, 0]); lo.append(v); hi.append(v)
    v = -sum(s * f['w'] for f, s in fixed)
    A.append([f['w'] for f in S] + [-f['w'] for f in S] + [0] * 35 + [0, -2]); lo.append(v); hi.append(v)
    for i in range(6):
        yrow = []
        for k in range(1, 6): yrow += list(-D6[k][i, :])
        v = -sum(s * f['lat'][i] for f, s in fixed)
        A.append([f['lat'][i] for f in S] + [-f['lat'][i] for f in S] + yrow + [0] * 7); lo.append(v); hi.append(v)
    Mb = 50
    for kk, k in enumerate(range(1, 6)):
        for i in range(6):
            for sgn in (1, -1):
                r = [0] * nv; r[2 * NS + kk * 6 + i] = sgn; r[2 * NS + 30 + kk] = -Mb; A.append(r); lo.append(-np.inf); hi.append(0)
        present = 1 if any(f['n'] % 6 in (k, 6 - k) for f, s in fixed) else 0
        r = [0] * nv
        for si, f in enumerate(S):
            if f['n'] % 6 in (k, 6 - k): r[si] = -1; r[NS + si] = -1
        r[2 * NS + 30 + kk] = 1; A.append(r); lo.append(-np.inf); hi.append(present)
    A.append([1] * (2 * NS) + [0] * 37); lo.append(0); hi.append(cap)
    ub = [xmax] * (2 * NS)
    if allowed is not None:
        ub = [xmax if allowed[i % NS] else 0 for i in range(2 * NS)]
    res = milp(np.array([1] * (2 * NS) + [0] * 37, dtype=float), constraints=LinearConstraint(np.array(A, dtype=float), lo, hi),
               integrality=np.ones(nv), bounds=Bounds([0] * (2 * NS) + [-Mb] * 30 + [0] * 5 + [-100, -100], ub + [Mb] * 30 + [1] * 5 + [100, 100]))
    if not res.success:
        return None
    x = np.round(res.x[:2 * NS]).astype(int)
    return int(x.sum()), [(i, int(x[i]) - int(x[NS + i])) for i in range(NS) if x[i] or x[NS + i]]
def typ(f):
    """SM type in the fitted-vector orientation (quark doublets at Y = -1/6): returns (name, conj) with conj = True when the field is
    the conjugate of the named SM-like representation."""
    a, b, y = f['d'][I3], abs(f['d'][I2]), f['y']
    T = {(3, 2, sp.Rational(-1, 6)): 'Q', (-3, 1, sp.Rational(2, 3)): 'U', (-3, 1, sp.Rational(-1, 3)): 'D', (1, 2, sp.Rational(1, 2)): 'L',
         (1, 1, sp.Integer(-1)): 'E', (3, 1, sp.Rational(-1, 6)): 'X', (1, 2, sp.Integer(0)): 'Z', (1, 1, sp.Rational(1, 2)): 'F'}
    ca = -a if abs(a) == 3 else a
    if (a, b, y) in T and not (T[(a, b, y)] in 'ZF' and y < 0): return T[(a, b, y)], False
    if (ca, b, -y) in T: return T[(ca, b, -y)], True
    return None, None
if __name__ == '__main__':
    import collections
    F19 = [f for f in FS if f['m'] == 19 and smsing(f)]
    print('singlets', NS, 'U(1)s', NQ, collections.Counter(typ(f) for f in F19))
    # control: the top-type coupling known at degree 0 in 12354 must come out with degree 0
