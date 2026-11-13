"""Pass 12653 item 2 (type B, Pass 12648 lifted four-qubit five-set): numerical shape of the coupled inequality of Pass 12652
addendum C.  With x = 14 - a(u), y = 14 - b(w) (three-qubit slacks) and e = 30 - c(u, w), min F = 1/16 <=> e - 2 >= -2 sqrt(x y) for
all unit u in V+, w in V- (at a lift point).  Test the cleaner, STRONGER candidate e - 2 >= -2 min(x, y): minimise
m1 = e - 2 + 2 sqrt(xy) (must be >= 0: the theorem, numerically) and m2 = e - 2 + 2 min(x, y) (candidate).  usage: py -3 analysis/w33_typeB_coupled_margin.py"""
import json, os, numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_four_qubit_typeB_lift_reduction.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_typeB_lift_reduction.py")}
exec(src[: src.index("t0 = time.time(); out = {}")], g)
t = g["census"]["types"][1]; S = t["example"]; lags = g["lags"]; NV = g["NV"]; P = g["P"]
C = frozenset().union(*[lags[i] for i in S]) - {0}
p = g["lift_points"](S, C | {0})[0]
U = [x for x in range(1, NV) if x not in C]; PU = np.array([P[x] for x in U])
ev, V = np.linalg.eigh(P[p]); Vm, Vp = V[:, ev < 0], V[:, ev > 0]
SU = lambda v: float((np.einsum("i,kij,j->k", v.conj(), PU, v).real ** 2).sum())
cv = lambda z: (z[:8] + 1j * z[8:16]) / np.linalg.norm(z[:8] + 1j * z[8:16])
def parts(z):
    u, w = cv(z[:16]), cv(z[16:]); a, b = SU(Vp @ u), SU(Vm @ w); c = SU(Vp @ u + Vm @ w) - a - b
    return 14 - a, 14 - b, 30 - c
rng = np.random.default_rng(0); out = {}
for name, f in (("m1_sqrt", lambda z: (lambda x, y, e: e - 2 + 2 * np.sqrt(max(x, 0) * max(y, 0)))(*parts(z))),
                ("m2_min", lambda z: (lambda x, y, e: e - 2 + 2 * min(x, y))(*parts(z)))):
    vals = sorted(minimize(f, rng.standard_normal(32), method="Nelder-Mead" if False else "L-BFGS-B").fun for _ in range(60))
    out[name] = dict(min=vals[0], lowest5=vals[:5]); print(name, vals[:5], flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_typeB_coupled_margin.json"), "w"), indent=1)
