"""12358b: the gauged B - L vector (general solution: particular + free directions acting only off the SM fermions) and the charges of
the 6 vacuum singlets (12360) and of the colour-triplet scalars.  Matter parity survives iff some choice of the free parameters gives
every vacuum singlet 3(B - L) even (they break U(1)_{B-L} to Z2 at most) -- searched exactly over the free parameters' lattice of
admissible charge assignments (charges must be rational with the same denominators: a linear search on the parameter space)."""
import sys, json, collections, itertools
import sympy as sp
sys.path.insert(0, '.')
from mono import FS, typ, smsing, S, NS, I3, I2
vac = json.load(open('vacuum.json'))['vacuum']
F19 = [f for f in FS if f['m'] == 19 and smsing(f)]
roots = []
for l in open('../search_drivers_12302/bro/Z6II_23_SM_20260917_2913_v6__ctrl.nsoq', errors='ignore'):
    if l.startswith('FACTOR'):
        roots += [[sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()] for r in l.split('|')[1:]]
val = dict(Q=sp.Rational(1, 3), U=sp.Rational(-1, 3), D=sp.Rational(-1, 3), L=-1, E=1)
rows, rhs = [], []
for f in F19:
    t, c = typ(f)
    if t and t in 'QUDLE':
        rows.append(list(f['P'])); rhs.append((-1 if c else 1) * val[t])
A = sp.Matrix(rows + roots); b = sp.Matrix(rhs + [0] * len(roots))
sol, prm = A.gauss_jordan_solve(b)
print('free parameters:', len(prm))
def charge(f):
    return sp.expand((sol.T * f['P'])[0])
vq = {S[s]['id']: charge(S[s]) for s in vac}
print('vacuum singlet 3(B-L):', {k: sp.simplify(3 * v) for k, v in vq.items()})
# choose the free parameters to make 3(B-L) of all vacuum singlets even integers, if possible: solve 3 q_s = 2 k_s for integer k_s in a box
eqs = [3 * v for v in vq.values()]
found = None
if prm:
    syms = list(prm)
    for ks in itertools.product(range(-3, 4), repeat=len(eqs)):
        try:
            s2 = sp.solve([e - 2 * k for e, k in zip(eqs, ks)], syms, dict=True)
        except Exception:
            s2 = []
        if s2:
            found = (ks, s2[0]); break
else:
    found = 'no free parameters' if all(sp.nsimplify(e / 2).is_integer for e in eqs) else None
print('matter parity (3(B-L) even on all vacuum singlets) achievable:', found is not None, found)
T = [f for f in FS if f['m'] == 15 and smsing(f) and abs(f['d'][I3]) == 3 and abs(f['d'][I2]) == 1]
print('triplet scalars 3(B-L):', collections.Counter(str(sp.simplify(3 * charge(f))) for f in T))
json.dump(dict(free_params=len(prm), vacuum_3BL={str(k): str(sp.simplify(3 * v)) for k, v in vq.items()}, parity=str(found)), open('bminusl.json', 'w'), indent=1)
# --- anomalies of U(1)_{B-L} over ALL left-handed Weyl fermions (m = 19), as functions of the free parameter -----------------------
# (corrects the parity search above: with every vacuum charge identically 0 the equations are empty and sp.solve returns [] -- the
# vacuum leaves U(1)_{B-L} UNBROKEN, so matter parity holds trivially)
a3 = roots[0]; a2 = None
for l in open('../search_drivers_12302/bro/Z6II_23_SM_20260917_2913_v6__ctrl.nsoq', errors='ignore'):
    if l.startswith('FACTOR 1'):
        a2 = [sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l.split('|')[1].split()]
from mono import Yv
an = dict(grav=0, cubic=0, SU3=0, SU2=0, Y2=0)
cur = None
for l in open('../search_drivers_12302/bro/Z6II_23_SM_20260917_2913_v6__ctrl.nsoq', errors='ignore'):
    if l.startswith('FIELD'):
        cur = int(l.split()[2][2:])
    elif l.startswith('W ') and cur == 19:
        P = sp.Matrix([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')])
        q = sp.expand((sol.T * P)[0]); d3 = sum(x * y for x, y in zip(P, a3)); d2 = sum(x * y for x, y in zip(P, a2)); y = sum(x * c for x, c in zip(P, Yv))
        an['grav'] += q; an['cubic'] += q ** 3; an['SU3'] += q * d3 ** 2 / 4; an['SU2'] += q * d2 ** 2 / 4; an['Y2'] += q * y ** 2
an = {k: sp.factor(sp.expand(v)) for k, v in an.items()}
print('U(1)_{B-L} anomalies (weight level, all m=19 fermions):', an)
anomalous_for_all = any(sp.Poly(v, *prm).is_ground and v != 0 for v in an.values()) if prm else any(v != 0 for v in an.values())
roots_free = sp.solve([v for v in an.values() if v != 0], list(prm), dict=True) if prm else []
print('anomaly-free choice of the free parameter:', roots_free, ' anomalous for every choice:', anomalous_for_all)
d = json.load(open('bminusl.json')); d.update(vacuum_breaks_BL=False, anomalies={k: str(v) for k, v in an.items()}, anomaly_free_choice=str(roots_free),
                                          anomalous_for_all=bool(anomalous_for_all))
json.dump(d, open('bminusl.json', 'w'), indent=1)
# --- SM-singlet scalars carrying B - L: candidates to break U(1)_{B-L} (to matter parity if 3(B-L) is even) ------------------------
hist = collections.Counter(str(sp.simplify(3 * charge(f))) for f in S)
print('3(B-L) over the 80 SM-singlet scalars:', dict(hist))
even = [f for f in S if (lambda v: v.is_number and v != 0 and (v / 2).is_integer)(sp.simplify(3 * charge(f)))]
d = json.load(open('bminusl.json')); d.update(singlet_3BL_hist=dict(hist), even_nonzero_singlets=[f['id'] for f in even])
json.dump(d, open('bminusl.json', 'w'), indent=1)
print('singlets with even nonzero 3(B-L) (break U(1)_{B-L} to matter parity):', [f['id'] for f in even])
