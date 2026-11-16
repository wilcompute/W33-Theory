"""Pass 12682: the F_8 certainty-purity boundary (the other track's open item, 8f8467de2 / a9ae33bd4).
C(rho) = sum over the 567 covered Paulis of Tr(rho P)^2 = 64 sum_t sum_k p_{t,k}^2 - 9 (nine MUBs).  They showed C = 0 is attainable for
every purity 1/64 <= p <= 1/2 (rank-five uncovered stabiliser code); pure states have C >= c8 > 0.  Stabiliser-code states cannot pass
1/2 (no Lagrangian is fully uncovered: every one has >= 3 covered points, Pass 12661).  Here: rank-2 states rho = l |a><a| + (1-l)|b><b|
(purity l^2 + (1-l)^2), minimising C over orthonormal (a, b) for a grid of l, to locate the largest l with min C = 0, and the minimum
of C as a function of purity above that threshold.   usage: py -3 analysis/w33_f8_certainty_purity_boundary.py"""
import json, math, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], g)
q, mul, trace = g["field"](3)
Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(8)] for a in range(8)], float)
Phi = np.array([[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(8)] for a in range(8)] for t in range(8)], float)
U = [np.eye(64)]
for t in range(8):
    Ut = np.zeros((64, 64))
    for x in range(64):
        e = np.zeros((8, 8)); e.flat[x] = 1; Ut[:, x] = (Xi @ (e * Phi[t]) @ Xi / 8).ravel()
    U.append(Ut)
Uall = np.vstack(U)                                   # 576 x 64 real
C8 = (47 - 32 * math.cos(2 * math.pi / 9)) / 9
rng = np.random.default_rng(126820)
def C_and_grad(v, l, mu=50.0):
    a = v[:64] + 1j * v[64:128]; b = v[128:192] + 1j * v[192:]
    ua = Uall @ a; ub = Uall @ b
    p = l * np.abs(ua) ** 2 + (1 - l) * np.abs(ub) ** 2
    C = 64 * np.sum(p * p) - 9
    ga = 64 * 2 * l * (Uall.T @ (p * ua)); gb = 64 * 2 * (1 - l) * (Uall.T @ (p * ub))   # dC/d conj(a), dC/d conj(b)
    ab = np.vdot(a, b); na = np.vdot(a, a).real - 1; nb = np.vdot(b, b).real - 1
    pen = mu * (abs(ab) ** 2 + na ** 2 + nb ** 2)
    ga = ga + mu * (b * np.conj(ab) + 2 * na * a)     # d/d conj(a) of mu(|<a,b>|^2 + na^2)
    gb = gb + mu * (a * ab + 2 * nb * b)
    grad = np.concatenate([2 * ga.real, 2 * ga.imag, 2 * gb.real, 2 * gb.imag])
    return C + pen, grad
from scipy.optimize import check_grad
_v = rng.standard_normal(256) / 8
_err = check_grad(lambda v: C_and_grad(v, 0.7)[0], lambda v: C_and_grad(v, 0.7)[1], _v)
print("gradient check error:", _err, flush=True); assert _err < 1e-4 * np.linalg.norm(C_and_grad(_v, 0.7)[1])
def min_C(l, starts=12):
    best = 1e9
    for _ in range(starts):
        r = minimize(C_and_grad, rng.standard_normal(256) / 8, args=(l,), jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-12, ftol=1e-16))
        a = r.x[:64] + 1j * r.x[64:128]; b = r.x[128:192] + 1j * r.x[192:]
        Q_, _ = np.linalg.qr(np.stack([a, b], 1)); a, b = Q_[:, 0], Q_[:, 1]      # exact orthonormalisation, re-evaluate
        p = l * np.abs(Uall @ a) ** 2 + (1 - l) * np.abs(Uall @ b) ** 2
        best = min(best, 64 * np.sum(p * p) - 9)
    return best
grid = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
rows = []
for l in grid:
    m = min_C(l); rows.append(dict(l=l, purity=l * l + (1 - l) ** 2, min_C=m)); print(rows[-1], flush=True)
# bisection for the threshold
lo = max(r["l"] for r in rows if r["min_C"] < 1e-7); hi = min(r["l"] for r in rows if r["l"] > lo)
for _ in range(10):
    mid = (lo + hi) / 2
    if min_C(mid, 16) < 1e-7: lo = mid
    else: hi = mid
res = dict(grid=rows, threshold_l=lo, threshold_purity=lo * lo + (1 - lo) ** 2, pure_limit=C8)
print("rank-2 threshold: l* ~", round(lo, 5), "purity ~", round(res["threshold_purity"], 5), "| pure-state value", C8, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_certainty_purity_boundary.json"), "w"), indent=1)
# ---- general rank: maximise purity subject to C = 0 (penalty), rho = A A^H / tr, A in C^{64 x r}
def neg_purity_pen(v, r_, mu):
    A = (v[: 64 * r_] + 1j * v[64 * r_:]).reshape(64, r_); rho = A @ A.conj().T; tr = np.trace(rho).real; rho = rho / tr
    p = np.real(np.einsum("ki,ij,kj->k", Uall, rho, Uall))
    C = 64 * np.sum(p * p) - 9
    return -np.real(np.trace(rho @ rho)) + mu * C
gen = []
for r_ in (2, 3, 4, 8):
    best = None
    for s in range(6):
        v = rng.standard_normal(2 * 64 * r_)
        for mu in (1.0, 10.0, 100.0, 1000.0):
            v = minimize(neg_purity_pen, v, args=(r_, mu), method="L-BFGS-B", options=dict(maxiter=3000)).x
        A = (v[: 64 * r_] + 1j * v[64 * r_:]).reshape(64, r_); rho = A @ A.conj().T; rho /= np.trace(rho).real
        p = np.real(np.einsum("ki,ij,kj->k", Uall, rho, Uall)); C = 64 * np.sum(p * p) - 9; pur = np.real(np.trace(rho @ rho))
        if C < 1e-6 and (best is None or pur > best[0]): best = (pur, C)
    gen.append(dict(rank=r_, max_purity_with_C0=None if best is None else best[0], C=None if best is None else best[1]))
    print(gen[-1], flush=True)
res = json.load(open(os.path.join(ROOT, "data", "w33_f8_certainty_purity_boundary.json")))
res["general_rank"] = gen
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_certainty_purity_boundary.json"), "w"), indent=1)
