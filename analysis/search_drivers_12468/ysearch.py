"""12364: exact hypercharge search.  Y = t . P with t orthogonal to every non-abelian root (all factors stay unbroken) and to the
anomalous U(1) direction (t_anom ~ sum over left-handed Weyl fermions of their U(1)-projected weights).  Each left-handed fermion's Y
is chosen from a finite set by binaries; the net chiral content (rep, Y) minus conjugates must be exactly three SM generations
(conjugated orientation fixed by the model's chiral (3bar,2)), every other (rep, Y) type vector-like.  MILP (scipy/HiGHS); solutions
rationalised and re-verified exactly with sympy; no-good cuts enumerate distinct Y vectors.  Model and SU(3)/SU(2) factor indices are
arguments."""
import sys, os, re, json, collections, itertools
import numpy as np
import sympy as sp
from scipy.optimize import milp, LinearConstraint, Bounds
M, I3, I2 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); NSOL = int(sys.argv[4]) if len(sys.argv) > 4 else 6
p = os.environ.get('YS_NSOQ') or f'../search_drivers_12281/bro/{M}__ctrl.nsoq'
if not os.path.exists(p): p = p.replace('12281', '12302')
roots = []; fields = []; cur = None
for l in open(p, errors='ignore'):
    if l.startswith('FACTOR'):
        roots += [[sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()] for r in l.split('|')[1:]]
    elif l.startswith('FIELD'):
        mm = re.match(r'FIELD (\d+) m=(\S+) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*)', l)
        cur = dict(id=int(mm.group(1)), m=int(mm.group(2)), d=tuple(int(re.match(r'-?\d+', x).group(0)) for x in mm.group(3).split(',')) if mm.group(3) else (), P=None)
        fields.append(cur)
    elif l.startswith('W ') and cur is not None and cur['P'] is None:
        cur['P'] = sp.Matrix([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')])
Ub = sp.Matrix(roots).nullspace(); nu = len(Ub)
F = [f for f in fields if f['m'] == 19]
for f in F: f['q'] = [(u.T * f['P'])[0] for u in Ub]
# anomalous direction in the U(1) basis: A_a = sum_f q_a(f) * dim(rest);  t . t_anom = 0 with the Gram matrix of Ub
G = sp.Matrix(nu, nu, lambda a, b: (Ub[a].T * Ub[b])[0])
def mult(f): return int(np.prod([abs(x) for x in f['d']]))
A_an = sp.Matrix([sum(f['q'][a] * mult(f) for f in F) for a in range(nu)])
anom = any(x != 0 for x in A_an)
# allowed Y values by (|SU3|, |SU2|, hidden-singlet?)
def hidden(f): return any(abs(f['d'][j]) > 1 for j in range(len(f['d'])) if j not in (I3, I2))
def allowed(f):
    a, b = abs(f['d'][I3]), abs(f['d'][I2])
    if os.environ.get('XWIDE') and not (a == 3 and b == 2): return [sp.Rational(v, 18) for v in range(-36, 37)]   # 12469: |Y| <= 2, step 1/18
    if os.environ.get('LOOSE') and not (a == 3 and b == 2): return [sp.Rational(v, 6) for v in range(-6, 7)]
    if hidden(f):
        if os.environ.get('WIDE'): return [sp.Rational(v, 6) for v in range(-6, 7)]
        return [sp.Integer(0), sp.Rational(1, 2), -sp.Rational(1, 2), sp.Integer(1), -sp.Integer(1)]
    if a == 3 and b == 2: return [sp.Rational(1, 6), -sp.Rational(1, 6)]
    if a == 3: return [sp.Rational(v, 6) for v in (4, -4, 2, -2, 1, -1)]
    if b == 2: return [sp.Rational(1, 2), -sp.Rational(1, 2), sp.Integer(0)]
    return [sp.Integer(0), sp.Integer(1), -sp.Integer(1), sp.Rational(1, 2), -sp.Rational(1, 2)]
def ctype(f, y):
    """canonical type key and sign: a field and its conjugate map to the same key with opposite sign"""
    d = list(f['d']); s = 1
    key = (tuple(d), y)
    cd = tuple(-x if abs(x) > 2 else x for x in d)
    ck = (cd, -y)
    return (key, 1) if str(key) <= str(ck) else (ck, -1)
# SM targets in the orientation of the model's chiral (3bar,2): orientation e = sign so that Q = (e*3, 2, -e/6)... determined below
nb = []; yvals = []
for i, f in enumerate(F):
    for v in allowed(f): nb.append((i, v))
nt = nu; nvar = nt + len(nb)
def dvec(f):
    return [float(x) for x in f['q']]
rowsA, lo, hi = [], [], []
# one value per field
for i in range(len(F)):
    r = [0.0] * nvar
    for k, (j, v) in enumerate(nb):
        if j == i: r[nt + k] = 1
    rowsA.append(r); lo.append(1); hi.append(1)
# t . q_f = y_f   (scaled by 6 * L to keep integrality friendly)
for i, f in enumerate(F):
    r = dvec(f) + [0.0] * len(nb)
    for k, (j, v) in enumerate(nb):
        if j == i: r[nt + k] = -float(v)
    rowsA.append(r); lo.append(0); hi.append(0)
if anom and not os.environ.get('NO_ANOM'):
    w = list(A_an)      # t . T = sum_a c_a (Ub_a . T) = c . A_an  (a first version used G * A_an -- wrong basis)
    rowsA.append([float(x) for x in w] + [0.0] * len(nb)); lo.append(0); hi.append(0)
# net chiral content per canonical type
types = collections.defaultdict(lambda: [0.0] * nvar)
for k, (i, v) in enumerate(nb):
    key, s = ctype(F[i], v)
    types[key][nt + k] += s * mult(F[i]) / max(1, abs(F[i]['d'][I3]) * abs(F[i]['d'][I2]))   # count in units of SM multiplets x hidden dims
# orientation from (3,2): which of (3,2)/(3bar,2) is chiral
n32 = sum(1 for f in F if f['d'][I3] == 3 and abs(f['d'][I2]) == 2); n3b2 = sum(1 for f in F if f['d'][I3] == -3 and abs(f['d'][I2]) == 2)
e = 1 if n32 > n3b2 else -1
def tk(d3, d2, y):
    d = [1] * len(F[0]['d']); d[I3] = d3; d[I2] = d2
    f = dict(d=tuple(d)); return ctype(f, y)
target = {}
for (d3, d2, y) in ((3, 2, sp.Rational(1, 6)), (-3, 1, -sp.Rational(2, 3)), (-3, 1, sp.Rational(1, 3)), (1, 2, -sp.Rational(1, 2)), (1, 1, sp.Integer(1))):
    key, s = tk(e * d3 if abs(d3) == 3 else d3, d2, e * y)
    target[key] = target.get(key, 0) + 3 * s
# hidden-charged types with y = 0 may be chiral (hidden sector); every other type: net = target or 0
for key, r in types.items():
    hid = any(abs(x) > 1 for j, x in enumerate(key[0]) if j not in (I3, I2))
    if hid and key[1] == 0: continue
    cd = tuple(-x if abs(x) > 2 else x for x in key[0])
    if os.environ.get('ONLY') and not eval(os.environ['ONLY']): continue
    if (cd, -key[1]) == key: continue          # self-conjugate types (neutral singlets, (1,2)_0): no chirality constraint
    rowsA.append(r); t = target.get(key, 0); lo.append(t); hi.append(t)
missing = [k for k in target if k not in types]
A = np.array(rowsA); integ = np.array([0] * nt + [1] * len(nb))
LB = [-20] * nt + [0] * len(nb); UB_ = [20] * nt + [1] * len(nb)
if os.environ.get('KCAP'):
    # 12469: necessary condition for k_Y = 2|t|^2 <= K in the 16-dim coordinates: sum_j |t_j| <= 4 sqrt(K/2).  Infeasible => no
    # hypercharge in this menu has k_Y <= K.  t = sum_a c_a Ub_a, so t_j = sum_a c_a Ub_a[j].
    K = float(sp.Rational(os.environ['KCAP'])); Bt = np.array([[float(Ub[a][j]) for a in range(nu)] for j in range(16)])
    A = np.hstack([A, np.zeros((A.shape[0], 16))]); extra = []
    for j in range(16):
        r = np.zeros(A.shape[1]); r[:nt] = -Bt[j]; r[nvar + j] = 1; extra.append((r, 0, np.inf))     # u_j >= t_j
        r = np.zeros(A.shape[1]); r[:nt] = Bt[j]; r[nvar + j] = 1; extra.append((r, 0, np.inf))      # u_j >= -t_j
    r = np.zeros(A.shape[1]); r[nvar:] = 1; extra.append((r, -np.inf, 4 * np.sqrt(K / 2)))
    A = np.vstack([A] + [e[0] for e in extra]); lo = list(lo) + [e[1] for e in extra]; hi = list(hi) + [e[2] for e in extra]
    integ = np.concatenate([integ, np.zeros(16)]); LB += [0] * 16; UB_ += [100] * 16; nvar = A.shape[1]
sols = []
for it in range(NSOL):
    res = milp(np.zeros(nvar), constraints=LinearConstraint(A, lo, hi), integrality=integ,
               bounds=Bounds(LB, UB_), options=dict(time_limit=float(os.environ.get('YS_TL', 600))))
    if not res.success:
        print('no (further) solution:', res.message); break
    c = [sp.nsimplify(round(x, 9), rational=True, tolerance=1e-7) for x in res.x[:nt]]
    t = sum((c[a] * Ub[a] for a in range(nu)), sp.zeros(16, 1))
    ys = [(t.T * f['P'])[0] for f in F]
    ok = all(y in allowed(f) for y, f in zip(ys, F))
    net = collections.Counter()
    for f, y in zip(F, ys):
        key, s = ctype(f, y); net[key] += s * mult(f) // max(1, abs(f['d'][I3]) * abs(f['d'][I2]))
    selfc = lambda k: (tuple(-x if abs(x) > 2 else x for x in k[0]), -k[1]) == k
    chiral = {str(k): v for k, v in net.items() if v and not selfc(k) and not (any(abs(x) > 1 for j, x in enumerate(k[0]) if j not in (I3, I2)) and k[1] == 0)}
    kY = 2 * (t.T * t)[0]
    sols.append(dict(t=[str(x) for x in t], kY=str(kY), exact_values_ok=ok, chiral=chiral, trY=str(sum(y * mult(f) for f, y in zip(F, ys)))))
    print(it, 'k_Y =', kY, 'exact ok', ok, 'chiral', chiral)
    sel = [k for k in range(len(nb)) if res.x[nt + k] > 0.5]
    r = [0.0] * A.shape[1]
    for k in sel: r[nt + k] = 1
    A = np.vstack([A, r]); lo.append(-np.inf); hi.append(len(sel) - 1)
json.dump(dict(model=M, SU3=I3, SU2=I2, n_u1=nu, anomalous=anom, solutions=sols, missing_targets=[str(k) for k in missing]), open(f'ysearch_{M}' + ('_noanom' if os.environ.get('NO_ANOM') else '') + ('_wide' if os.environ.get('WIDE') else '') + ('_loose' if os.environ.get('LOOSE') else '') + ('_xwide' if os.environ.get('XWIDE') else '') + (('_kcap' + os.environ['KCAP'].replace('/', 'o')) if os.environ.get('KCAP') else '') + ('_only' if os.environ.get('ONLY') else '') + '.json', 'w'), indent=1)
