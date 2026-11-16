"""Pass 12680: logical stabiliser fidelity of all 512 torus Clifford eigenstates (64 lifts x 8 eigenvectors) on the T code space,
tabulated by the eigenvalue index r (measured from the absent ninth root; Pass 12672-12673: c = (47 - 32cos(4 pi r/9))/9 for
r = +-1, +-2, +-4, 37/3 for r = +-3).  Logical stabiliser states: joint eigenvectors (inside the code space) of the lifts of the 135
Lagrangians of T^perp/T (1080 states).   usage: py -3 analysis/w33_f8_torus_eigenstate_magic.py"""
import collections, contextlib, io, itertools, json, math, os
import numpy as np
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_clifford_eigenstates.py")}
src = open(os.path.join(HERE, "w33_f8_clifford_eigenstates.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("import math\nclosed")], G)
sols, B, basisE, apply, coord, keys, pauli, F64 = (G[k] for k in ("sols", "B", "basisE", "apply", "coord", "keys", "pauli", "F64"))
E = G["E"]; effP = G["effP"]; form = G["form"]
# Lagrangians of the effective space (coords 1..63 with symplectic form `form`)
pts = list(range(1, 64))
lags = set()
for a, b, c in itertools.combinations(pts, 3):
    if form(a, b) or form(a, c) or form(b, c): continue
    span = {0}
    for g in (a, b, c): span |= {s ^ g for s in span}
    if len(span) == 8: lags.add(frozenset(span))
assert len(lags) == 135
stabs = []
for Lg in lags:
    gens = []; span = {0}
    for p in sorted(Lg):
        if p not in span: gens.append(p); span |= {s ^ p for s in span}
    Mx = np.zeros((8, 8), complex)
    for i, g in enumerate(gens):
        P = effP(g); P = P if np.allclose(P, P.conj().T) else 1j * P
        Mx += (0.37 + 0.11 * i) * P
    _, Ub = np.linalg.eigh((Mx + Mx.conj().T) / 2); stabs.extend(Ub[:, i] for i in range(8))
S = np.array(stabs); assert len(stabs) == 1080
table = collections.defaultdict(collections.Counter)
for V in sols:
    M = np.linalg.matrix_power(V, 9); V9 = V / M[0, 0] ** (1 / 9)
    ev, U_ = np.linalg.eig(V9)
    js = [int(round(np.angle(e) / (2 * np.pi / 9))) % 9 for e in ev]; missing = [j for j in range(9) if j not in js][0]
    for i in range(8):
        r = (js[i] - missing) % 9; t = U_[:, i] / np.linalg.norm(U_[:, i])
        f = float(np.max(np.abs(S.conj() @ t) ** 2)); table[r][round(f, 9)] += 1
mp.mp.dps = 20; gam = 2 * mp.cos(2 * mp.pi / 9); s3 = mp.sqrt(3)
rows = {}
for r in sorted(table):
    rows[str(r)] = [dict(fidelity=k, count=v, pslq=str(mp.pslq([mp.mpf(k), 1, gam, gam * gam, s3, s3 * gam, s3 * gam * gam], maxcoeff=500, tol=mp.mpf(10) ** -8))) for k, v in sorted(table[r].items())]
    print("r =", r, rows[str(r)], flush=True)
json.dump(rows, open(os.path.join(ROOT, "data", "w33_f8_torus_eigenstate_magic.json"), "w"), indent=1)
# ---- (Pass 12681) full-precision values and identification in Q(cos 2pi/9, sqrt3)
vals = collections.defaultdict(list)
for V in sols:
    M = np.linalg.matrix_power(V, 9); V9 = V / M[0, 0] ** (1 / 9)
    ev, U_ = np.linalg.eig(V9)
    js = [int(round(np.angle(e) / (2 * np.pi / 9))) % 9 for e in ev]; missing = [j for j in range(9) if j not in js][0]
    for i in range(8):
        r = (js[i] - missing) % 9; t = U_[:, i] / np.linalg.norm(U_[:, i])
        vals[r].append(float(np.max(np.abs(S.conj() @ t) ** 2)))
ident = {}
for r in (3, 4):
    v = mp.mpf(float(np.median(vals[r]))); spread = max(vals[r]) - min(vals[r])
    rel = mp.pslq([v, 1, gam, gam * gam, s3, s3 * gam, s3 * gam * gam], maxcoeff=2000, maxsteps=10 ** 6, tol=mp.mpf(10) ** -13)
    ident[str(r)] = dict(value=mp.nstr(v, 16), spread=spread, pslq=str(rel))
    print("r =", r, ident[str(r)], flush=True)
out = json.load(open(os.path.join(ROOT, "data", "w33_f8_torus_eigenstate_magic.json")))
out["identification"] = ident
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_torus_eigenstate_magic.json"), "w"), indent=1)
