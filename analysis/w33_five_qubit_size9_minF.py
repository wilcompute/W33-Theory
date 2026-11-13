"""Pass 12651 item 3: numerical min F for the five-qubit size-9 maximal partial spread (Pass 12650): covered Paulis = X-type, Z-type and
the 7 graphs {(x, Sx)}; F = (1/32) sum_{P in C} <P>^2 (twirl identity).  Many L-BFGS starts; compared with stabiliser values m/32.
usage: py -3 analysis/w33_five_qubit_size9_minF.py"""
import json, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
n = 5; d = 32; pos = [(i, j) for i in range(n) for j in range(i, n)]
ex = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]
def decode(code):
    S = np.zeros((n, n), int)
    for b, (i, j) in enumerate(pos):
        if code >> b & 1: S[i, j] = S[j, i] = 1
    return S
pts = set()
for x in range(1, 1 << n):
    xv = np.array([(x >> i) & 1 for i in range(n)])
    pts.add((tuple(xv), (0,) * n)); pts.add(((0,) * n, tuple(xv)))
    for c in ex:
        pts.add((tuple(xv), tuple(decode(c) @ xv % 2)))
assert len(pts) == 9 * 31
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(xv, zv):
    M = np.eye(1)
    for i in range(n):
        M = np.kron(M, (1j) ** (xv[i] * zv[i]) * np.linalg.matrix_power(X1, xv[i]) @ np.linalg.matrix_power(Z1, zv[i]))
    return M
Ps = np.array([pauli(a, b) for a, b in pts])
def fg(z):
    v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
    Pv = Ps @ v; f = np.einsum("i,ki->k", v.conj(), Pv).real
    gval = float(np.sum(f ** 2)) / d
    gr = (4 * np.einsum("ki,k->i", Pv, f) / d) / nv ** 2 - 4 * gval * v / nv ** 3
    return gval / nv ** 2, np.concatenate([gr.real, gr.imag])
rng = np.random.default_rng(9)
vals = sorted(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(gtol=1e-12, maxiter=20000)).fun for _ in range(150))
res = dict(n_covered=len(pts), min_F=float(vals[0]), min_F_times_32=float(vals[0] * 32), lowest_five=[float(v) for v in vals[:5]])
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_size9_minF.json"), "w"), indent=1)
