"""Pass 12662: c_q from STABILISER starting points (q = 8 control, q = 32).  The random-start optimiser returned 15.16 at q = 32
although a stabiliser state with d F = 11 exists (Pass 12661), so it had not found the minimum.  Here the stabiliser state of the best
annealed Lagrangian M (data/w33_regulus_odd_k_structure.json) is built in the CZ model (X^a psi(x) = psi(x + a),
Z^b psi(x) = chi(b.x) psi(x); generators made Hermitian by a factor i when X^a Z^b squares to -1; successive projections (1 + H)/2),
its d F is checked to equal |M cap C|, and L-BFGS is started from it with perturbations of several sizes.
Control: at q = 8 the perturbed stabiliser starts must reach 2.498508646688 (< 3).   usage: py -3 analysis/w33_regulus_c32_from_stabiliser.py"""
import json, os, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("rng = np.random.default_rng(0); res")], g)
data = json.load(open(os.path.join(ROOT, "data", "w33_regulus_odd_k_structure.json")))
out = {}; t0 = time.time()
for k in (3, 5):
    q, mul, trace = g["field"](k); _, fg = g["model"](k); d = q * q; msk = q - 1
    MUL = np.array([[mul(a, b) for b in range(q)] for a in range(q)]); TR = np.array([trace(a) for a in range(q)])
    basis = data[f"q{q}"]["basis"]; mstar = data[f"q{q}"]["best"]
    rng = np.random.default_rng(k)
    psi = rng.standard_normal((q, q)) + 1j * rng.standard_normal((q, q))
    xs = np.arange(q)
    for v in basis:
        a1, a2, b1, b2 = v & msk, (v >> k) & msk, (v >> 2 * k) & msk, (v >> 3 * k) & msk
        ph = 1 - 2 * TR[MUL[b1][:, None] ^ MUL[b2][None, :]]          # chi(b1 x1 + b2 x2)
        def W(p):  # X^a Z^b p : (Z^b p)(x) = ph p ; then shift by a
            zp = ph * p
            return zp[np.ix_(xs ^ a1, xs ^ a2)]
        fac = 1j if TR[MUL[a1, b1] ^ MUL[a2, b2]] else 1.0
        new = psi + fac * W(psi)
        if np.linalg.norm(new) < 1e-9: new = psi - fac * W(psi)
        psi = new
    psi /= np.linalg.norm(psi)
    w0 = np.concatenate([psi.real.ravel(), psi.imag.ravel()])
    f_stab = fg(w0)[0] * d
    rec = dict(q=q, stabiliser_weight=mstar, dF_of_stabiliser_state=f_stab, runs=[])
    assert abs(f_stab - mstar) < 1e-8, (f_stab, mstar)
    for eps in (0.0, 0.02, 0.05, 0.1, 0.2, 0.4):
        for rep in range(1 if eps == 0 else (6 if k == 3 else 2)):
            w = w0 + eps * rng.standard_normal(w0.shape) / np.sqrt(len(w0)) * np.linalg.norm(w0)
            r = minimize(fg, w, jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-11, ftol=1e-15))
            rec["runs"].append(dict(eps=eps, c=r.fun * d))
            print(q, eps, rep, r.fun * d, round(time.time() - t0), "s", flush=True)
    rec["best_c"] = min(x["c"] for x in rec["runs"]); rec["stabiliser_is_local_minimum"] = bool(abs(rec["runs"][0]["c"] - mstar) < 1e-6)
    out[f"q{q}"] = rec
    json.dump(out, open(os.path.join(ROOT, "data", "w33_regulus_c32_from_stabiliser.json"), "w"), indent=1)
print({a: (b["stabiliser_weight"], b["best_c"], b["stabiliser_is_local_minimum"]) for a, b in out.items()})
