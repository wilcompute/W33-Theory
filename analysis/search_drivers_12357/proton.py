"""12358: proton decay in SM_2913_v6.
(a) Is baryon number, or B - L, a gauged U(1)?  Solve t . P_f = B(f) exactly for a 16-vector t orthogonal to every non-abelian root, over
    every SM-type left-handed fermion (Q, U, D, L, E and their vector-like conjugates); exotics unconstrained.
(b) Four-fermion Delta B = Delta L = 1 operators QQQL, UUDE, QQ U* E*, QL U* D* (all field choices): minimal singlet degree with all 80
    singlets and with the 6-singlet set of 12360 (None = forbidden at every degree <= cap by the selection rules used).
(c) Massless colour-triplet scalars (3 or 3bar, 1) with renormalisable couplings to QQ / UD (diquark) and to QL / UE (leptoquark): a
    triplet with both mediates proton decay at its mass scale.
Not imposed: the non-SUSY vertex rule (so allowed = upper bound on what is allowed)."""
import sys, json, itertools, collections
import sympy as sp
sys.path.insert(0, '.')
from mono import FS, min_degree, typ, smsing, NS, UB, I3, I2
vac = json.load(open('vacuum.json'))['vacuum']; allowed6 = [s in vac for s in range(NS)]
F19 = [f for f in FS if f['m'] == 19 and smsing(f)]
G = collections.defaultdict(list)
for f in F19:
    t, c = typ(f)
    if t: G[(t, c)].append(f)
out = {}
# (a)
roots = []
for l in open('../search_drivers_12302/bro/Z6II_23_SM_20260917_2913_v6__ctrl.nsoq', errors='ignore'):
    if l.startswith('FACTOR'):
        roots += [[sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()] for r in l.split('|')[1:]]
for name, val in (('B', dict(Q=sp.Rational(1, 3), U=sp.Rational(-1, 3), D=sp.Rational(-1, 3), L=0, E=0)),
                  ('B-L', dict(Q=sp.Rational(1, 3), U=sp.Rational(-1, 3), D=sp.Rational(-1, 3), L=-1, E=1)),
                  ('Y (control: must be solvable)', None)):
    rows, rhs = [], []
    for (t, c), fl in G.items():
        if t not in 'QUDLE': continue
        for f in fl:
            rows.append(list(f['P'])); rhs.append((f['y'] if val is None else (-1 if c else 1) * val[t]))
    A = sp.Matrix(rows + roots); b = sp.Matrix(rhs + [0] * len(roots))
    try:
        sol, prm = A.gauss_jordan_solve(b); ok = True
    except ValueError:
        ok = False
    out[f'gauged_{name}'] = ok
    print('gauged', name, ok)
# (b)
OPS = dict(QQQL=[('Q', False, 1)] * 3 + [('L', False, 1)], UUDE=[('U', False, 1)] * 2 + [('D', False, 1), ('E', False, 1)],
           QQUcEc=[('Q', False, 1)] * 2 + [('U', False, -1), ('E', False, -1)], QLUcDc=[('Q', False, 1), ('L', False, 1), ('U', False, -1), ('D', False, -1)])
for op, spec in OPS.items():
    best = {}
    for tag, al in (('all', None), ('vac6', allowed6)):
        seen = set(); b = None
        pools = [G[(t, c)] for t, c, s in spec]
        for combo in itertools.product(*[range(len(p)) for p in pools]):
            key = tuple(sorted(zip([t for t, c, s in spec], combo)))
            if key in seen: continue
            seen.add(key)
            r = min_degree([(pools[k][i], spec[k][2]) for k, i in enumerate(combo)], al, cap=10)
            if r is not None and (b is None or r[0] < b): b = r[0]
            if b == 0: break
        best[tag] = b
    out[f'op_{op}'] = best; print(op, best, flush=True)
# (c)
T = [f for f in FS if f['m'] == 15 and smsing(f) and abs(f['d'][I3]) == 3 and abs(f['d'][I2]) == 1]
print('colour-triplet scalars:', len(T), collections.Counter(str(f['y'] * (1 if f['d'][I3] > 0 else -1)) for f in T))
dq_lq = []
pairs = dict(QQ=('Q', 'Q'), UD=('U', 'D'), QL=('Q', 'L'), UE=('U', 'E'))
for tf in T:
    rec = {}
    for nm, (a, b) in pairs.items():
        hit = None
        for x, y in itertools.combinations_with_replacement(range(max(len(G[(a, False)]), len(G[(b, False)]))), 2):
            for i, j in ((x, y), (y, x)):
                if i >= len(G[(a, False)]) or j >= len(G[(b, False)]): continue
                for sg in (1, -1):
                    r = min_degree([(G[(a, False)][i], 1), (G[(b, False)][j], 1), (tf, sg)], cap=0)
                    if r is not None: hit = True
        rec[nm] = bool(hit)
    dq_lq.append(dict(id=tf['id'], y=str(tf['y']), **rec))
both = [r for r in dq_lq if (r['QQ'] or r['UD']) and (r['QL'] or r['UE'])]
out['triplet_scalars'] = dq_lq; out['triplets_with_diquark_and_leptoquark_couplings'] = len(both)
print('triplets with both diquark and leptoquark renormalisable couplings:', len(both), 'of', len(T))
json.dump(out, open('proton.json', 'w'), indent=1, default=str)
