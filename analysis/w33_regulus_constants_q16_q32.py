"""Pass 12659: the 'certainty constants' c_q = d * min F of the F_q regulus MUB sets (q + 1 bases in dimension d = q^2), extended
to q = 16 (8 qubits, 17 bases, d = 256) and q = 32 (10 qubits, 33 bases, d = 1024), by analytic-gradient minimisation in the CZ model
(w33_regulus_minF_gradient.py; controls q = 2, 4 -> 1, q = 8 -> 2.498508646688).  Maximality of the q = 16, 32 sets is Kantor's theorem
(arXiv:1601.04194, Thm 5.2), not re-verified here.  Also the collision-entropy certainty relation implied by convexity:
sum_t H_2(B_t) <= m log2 d - m log2(1 + c_q / m), m = q + 1.   usage: py -3 analysis/w33_regulus_constants_q16_q32.py [starts16] [starts32]"""
import json, math, os, sys, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
POLY = {1: 0b11, 2: 0b111, 3: 0b1011, 4: 0b10011, 5: 0b100101}
def field(k):
    q = 1 << k; poly = POLY[k]
    def mul(a, b):
        r = 0
        while b:
            if b & 1: r ^= a
            b >>= 1; a <<= 1
            if a >> k & 1: a ^= poly
        return r
    def trace(a):
        s = 0; y = a
        for _ in range(k): s ^= y; y = mul(y, y)
        assert s in (0, 1); return s
    return q, mul, trace
def model(k):
    q, mul, trace = field(k)
    M = np.array([[mul(a, b) for b in range(q)] for a in range(q)]); tr = np.array([trace(a) for a in range(q)])
    Xi = 1.0 - 2 * tr[M]
    Phi = np.array([1.0 - 2 * tr[np.array([[mul(t, M[a, b]) for b in range(q)] for a in range(q)])] for t in range(q)])
    def fg(w):
        A = (w[: q * q] + 1j * w[q * q:]).reshape(q, q); nrm = np.linalg.norm(A); A = A / nrm
        s = (np.abs(A) ** 4).sum(); G = 2 * np.abs(A) ** 2 * A
        K = np.einsum("ka,tab,bl->tkl", Xi, A[None] * Phi, Xi) / q
        s += (np.abs(K) ** 4).sum()
        G += 2 * (Phi * np.einsum("ka,tab,bl->tkl", Xi, np.abs(K) ** 2 * K, Xi)).sum(0) / q
        G = (G - np.real(np.vdot(A, G)) * A) / nrm
        return float(s - (q + 1) / q ** 2), 2 * np.concatenate([G.real.ravel(), G.imag.ravel()])
    return q, fg
rng = np.random.default_rng(0); res = {}; t0 = time.time()
plan = ((1, 20), (2, 60), (3, 80), (4, int(sys.argv[1]) if len(sys.argv) > 1 else 60), (5, int(sys.argv[2]) if len(sys.argv) > 2 else 16))
for k, starts in plan:
    q, fg = model(k); d = q * q
    vals = sorted(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(maxiter=20000, gtol=1e-11, ftol=1e-15)).fun for _ in range(starts))
    c = vals[0] * d; m = q + 1
    res[f"q{q}"] = dict(qubits=2 * k, bases=m, d=d, starts=starts, c=c, lowest_c=[v * d for v in vals[:6]], n_at_min=sum(1 for v in vals if (v - vals[0]) * d < 1e-6),
                        H2_deficit_bits=m * math.log2(1 + c / m))
    print(q, res[f"q{q}"], round(time.time() - t0), "s", flush=True)
    json.dump(res, open(os.path.join(ROOT, "data", "w33_regulus_constants_q16_q32.json"), "w"), indent=1)
