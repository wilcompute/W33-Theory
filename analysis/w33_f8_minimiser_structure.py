"""Pass 12660: structure of the minimiser of F for the F_8 regulus (c = 2.498508646688).  In the CZ model the Pauli group is
{X^a Z^b : a, b in F_8^2}, X^a |x> = |x + a>, Z^b |x> = chi(b.x)|x>.  Compute m(a, b) = |<psi| X^a Z^b |psi>|^2 for all 4096 (a, b):
 - the stabiliser S = {m = 1} (if |S| = 8 the minimiser lies in an 8-dimensional stabiliser code);
 - the level structure of m on covered points (Q(a,b) = a1 b1 + a2 b2 = 0) and uncovered points;
 - F recomputed from the Pauli side: d F = sum_{Q = 0, (a,b) != 0} m(a, b)  (cross-check of the model against the Pauli definition).
usage: py -3 analysis/w33_f8_minimiser_structure.py"""
import itertools, json, os
from collections import Counter
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("rng = np.random.default_rng(0); res")], g)
k = 3; q, mul, trace = g["field"](k); _, fg = g["model"](k); d = 64
rng = np.random.default_rng(3); best = None
for _ in range(120):
    r = minimize(fg, rng.standard_normal(128), jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-13, ftol=1e-16))
    if best is None or r.fun < best.fun: best = r
A = (best.x[:64] + 1j * best.x[64:]).reshape(8, 8); A /= np.linalg.norm(A)
chi = lambda y: 1 - 2 * trace(y)
m = {}
for a1, a2, b1, b2 in itertools.product(range(8), repeat=4):
    ph = np.array([[chi(mul(b1, x1) ^ mul(b2, x2)) for x2 in range(8)] for x1 in range(8)])
    Ash = np.array([[A[x1 ^ a1, x2 ^ a2] for x2 in range(8)] for x1 in range(8)])  # (X^a psi)(x) = psi(x + a)
    m[(a1, a2, b1, b2)] = abs(np.vdot(Ash, ph * A)) ** 2
Qf = lambda v: mul(v[0], v[2]) ^ mul(v[1], v[3])
zero = (0, 0, 0, 0)
S = [v for v, val in m.items() if val > 1 - 1e-8]
cov = [v for v in m if v != zero and Qf(v) == 0]; unc = [v for v in m if Qf(v) != 0]
res = dict(c=best.fun * 64, stabiliser_size=len(S), stabiliser=S[:16], n_covered=len(cov), dF_from_paulis=float(sum(m[v] for v in cov)),
           purity_check=float(sum(m.values()) / d),
           covered_levels=sorted(Counter(np.round([m[v] for v in cov], 6)).items()), uncovered_levels=sorted(Counter(np.round([m[v] for v in unc], 6)).items()),
           stabiliser_all_uncovered_or_identity=bool(all(v == zero or Qf(v) != 0 for v in S)),
           stabiliser_TrQ=sorted(Counter(trace(Qf(v)) for v in S).items()))
print({kk: (v if kk not in ("covered_levels", "uncovered_levels") else v[:12]) for kk, v in res.items()})
np.save(os.path.join(ROOT, "data", "w33_f8_minimiser.npy"), A)
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_minimiser_structure.json"), "w"), indent=1, default=float)
