"""Pass 12658: reliable numerical min F for the F_q regulus sets in the CZ model with ANALYTIC gradients (many starts), q = 4, 8,
and stabiliser values: F at the states e_x (x) ..., i.e. min over a sample of stabiliser states |M cap C| / d is not needed -- instead
the optimiser's best values are compared with multiples of 1/d.  Control: q = 2 must give 1/4 and q = 4 must give 1/16 (Pass 12657).
usage: py -3 analysis/w33_regulus_minF_gradient.py [starts_q8]"""
import json, os, sys, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_mub_sets.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_mub_sets.py")}
exec(src[: src.index("g = {")], g)
def model(k):
    q, mul, trace = g["field"](k)
    Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(q)] for a in range(q)], float)
    Phi = np.array([[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(q)] for a in range(q)] for t in range(q)], float)
    def fg(w):
        A = (w[: q * q] + 1j * w[q * q:]).reshape(q, q); nrm = np.linalg.norm(A); A = A / nrm
        s = (np.abs(A) ** 4).sum(); G = 2 * np.abs(A) ** 2 * A
        for t in range(q):
            K = Xi @ (A * Phi[t]) @ Xi / q; s += (np.abs(K) ** 4).sum()
            G += 2 * Phi[t] * (Xi @ (np.abs(K) ** 2 * K) @ Xi) / q
        # s is homogeneous of degree 4 in A; project gradient onto the sphere and undo normalisation
        G = (G - np.real(np.vdot(A, G)) * A) / nrm  # d s / d conj(A) restricted to tangent
        return float(s - (q + 1) / q ** 2), 2 * np.concatenate([G.real.ravel(), G.imag.ravel()])
    return q, fg
rng = np.random.default_rng(0); res = {}; t0 = time.time()
# gradient check
q, fg = model(2); w = rng.standard_normal(32); f0, g0 = fg(w); e = np.zeros(32); e[5] = 1e-6
res["gradient_check"] = abs((fg(w + e)[0] - fg(w - e)[0]) / 2e-6 - g0[5]); assert res["gradient_check"] < 1e-6
for k, starts in ((1, 30), (2, 200), (3, int(sys.argv[1]) if len(sys.argv) > 1 else 400)):
    q, fg = model(k); vals = sorted(minimize(fg, rng.standard_normal(2 * q * q), jac=True, method="L-BFGS-B", options=dict(maxiter=4000, gtol=1e-12, ftol=1e-15)).fun for _ in range(starts))
    d = q * q
    res[f"q{q}"] = dict(starts=starts, min_F=vals[0], min_F_times_d=vals[0] * d, lowest=vals[:6], distinct_levels_times_d=sorted({round(v * d, 3) for v in vals})[:10])
    print(q, res[f"q{q}"], round(time.time() - t0), "s", flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_regulus_minF_gradient.json"), "w"), indent=1)
