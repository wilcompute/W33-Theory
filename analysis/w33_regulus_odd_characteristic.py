"""Pass 12659: why regulus MUB sets are strongly unextendible only in characteristic 2.
For odd prime p the same construction (computational basis and CZ_t (F (x) F), t in F_p, on C^p (x) C^p; Lagrangians z = t (x2, x1))
gives p + 1 MUBs.  Claim: there is an explicit vector unbiased to all of them, so min F = 0:  A(x1, x2) = w^{a x1^2 + b x2^2} / p with
suitable a, b (w = exp(2 pi i / p)): a quadratic phase restricted to any affine line is a non-degenerate quadratic phase (when the
binary form  a s1^2 + t s1 s2 + b s2^2-type discriminant condition holds for every slope), hence has a flat Fourier transform.
In characteristic 2, squaring is additive, every quadratic form on F_q^2 has a singular direction, and this mechanism is unavailable.
Checks: p = 3, 5, 7: numerical min F (expect 0), and F at the explicit quadratic-phase states for all (a, b).
usage: py -3 analysis/w33_regulus_odd_characteristic.py"""
import itertools, json, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def model(p):
    w = np.exp(2j * np.pi / p); xs = np.arange(p)
    Xi = w ** np.outer(xs, xs); Phi = [w ** (t * np.outer(xs, xs)) for t in range(p)]
    def F(A):
        A = A / np.linalg.norm(A); s = (np.abs(A) ** 4).sum()
        for t in range(p):
            K = Xi.conj() @ (A * Phi[t]) @ Xi.conj() / p; s += (np.abs(K) ** 4).sum()
        return float(s - (p + 1) / p ** 2)
    return w, xs, F
rng = np.random.default_rng(0); res = {}
for p in (3, 5, 7):
    w, xs, F = model(p)
    num = min(minimize(lambda v: F((v[: p * p] + 1j * v[p * p:]).reshape(p, p)), rng.standard_normal(2 * p * p), method="L-BFGS-B").fun for _ in range(12))
    quad = {}
    for a, b in itertools.product(range(p), repeat=2):
        A = w ** (a * xs[:, None] ** 2 + b * xs[None, :] ** 2) / p
        quad[(a, b)] = F(A)
    zeros = sorted(k for k, v in quad.items() if abs(v) < 1e-12)
    res[p] = dict(numerical_min_F=num, n_quadratic_phase_zeros=len(zeros), zeros=[list(z) for z in zeros], min_quadratic_F=min(quad.values()))
    print(p, {k: v for k, v in res[p].items() if k != "zeros"}, "zeros (a,b):", zeros[:8], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_regulus_odd_characteristic.json"), "w"), indent=1)
