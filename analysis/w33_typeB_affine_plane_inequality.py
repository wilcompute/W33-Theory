"""Pass 12657: type B (four-qubit lifted five-set = F_4 regulus set) min F = 1/16 is EQUIVALENT to an inequality on AG(2,4):
for A: F_4^2 -> C with sum |A_p|^2 = 1,
    (*)   sum_p |A_p|^4  +  (1/4) |sum_p A_p^2|^2  +  sum_{20 affine lines l} sum_{3 pairings ab|cd of l} |A_a A_b + A_c A_d|^2  >=  3/8,
and  F(A) - 1/16 = LHS(*) - 3/8  identically (F + 5/16 = LHS) (checked against the CZ-model F on random A).
Derivation in PASS12657 note (index-of-coincidence formula with q = 4; {x, x+s, x+ws, x+w^2 s} is the affine F_4-line).
Numerics: min of LHS over unit A (must be 3/8); the values on stabiliser-type minimisers.  usage: py -3 analysis/w33_typeB_affine_plane_inequality.py"""
import itertools, json, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_mub_sets.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_mub_sets.py")}
exec(src[: src.index("g = {")], g)
q, mul, trace = g["field"](2)
pts = list(itertools.product(range(4), repeat=2)); pid = {p: i for i, p in enumerate(pts)}
lines = set()
for p in pts:
    for s in pts:
        if s == (0, 0): continue
        lines.add(frozenset(pid[(p[0] ^ mul(l, s[0]), p[1] ^ mul(l, s[1]))] for l in range(4)))
lines = [sorted(l) for l in lines]; assert len(lines) == 20 and all(len(l) == 4 for l in lines)
pairings = lambda l: [((l[0], l[1]), (l[2], l[3])), ((l[0], l[2]), (l[1], l[3])), ((l[0], l[3]), (l[1], l[2]))]
def lhs(a):
    v = (np.abs(a) ** 4).sum() + abs((a ** 2).sum()) ** 2 / 4
    for l in lines:
        for (i, j), (k, m) in pairings(l): v += abs(a[i] * a[j] + a[k] * a[m]) ** 2
    return float(v)
# model F from the CZ construction (exec the helper functions)
exec(src[src.index("def ic_model"): src.index("form = {}")], g)
rng = np.random.default_rng(1); worst = 0
for _ in range(5):
    A = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4)); A /= np.linalg.norm(A)
    ic_inf, s, _, _ = g["ic_model"](2, A); F = ic_inf + s - 5 / 16
    a = np.array([A[p] for p in pts]); worst = max(worst, abs((F - 1 / 16) - (lhs(a) - 3 / 8)))
f = lambda w: lhs((w[:16] + 1j * w[16:]) / np.linalg.norm(w))
vals = sorted(minimize(f, rng.standard_normal(32), method="L-BFGS-B").fun for _ in range(60))
res = dict(n_lines=20, identity_residual=worst, min_LHS=vals[0], lowest5=vals[:5], target=3 / 8, basis_state_LHS=lhs(np.eye(16)[0].astype(complex)),
           uniform_real_LHS=lhs(np.ones(16, complex) / 4))
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_typeB_affine_plane_inequality.json"), "w"), indent=1)
