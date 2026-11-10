"""Pass 12646: numerical min F for each census set (F = (1/16) sum_{P in C} <P>^2, L-BFGS, many starts) against the stabiliser value
m*/16 and the Lovasz bound (15 - theta)/16; flags sets whose optimum is non-stabiliser.
usage: py -3 analysis/w33_four_qubit_minF_census.py"""
import json, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags = ex["lags"]; n = 4; d = 16
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(v):
    M = np.eye(1)
    for i in range(n):
        x = (v >> i) & 1; z = (v >> (n + i)) & 1
        M = np.kron(M, (1j) ** (x * z) * np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z))
    return M
census = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_set_census.json")))
out = []
for k, r in enumerate(census):
    C = frozenset().union(*[lags[i] for i in r["lines"]]); Ps = np.array([pauli(v) for v in C])
    def fg(z):
        v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
        Pv = Ps @ v; f = np.einsum("i,ki->k", v.conj(), Pv).real
        g = float(np.sum(f ** 2)) / d
        gr = (4 * np.einsum("ki,k->i", Pv, f) / d) / nv ** 2 - 4 * g * v / nv ** 3
        return g / nv ** 2, np.concatenate([gr.real, gr.imag])
    rng = np.random.default_rng(k)
    fmin = min(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(gtol=1e-13, maxiter=10000)).fun for _ in range(150))
    row = dict(index=k, n_inside=r["n_inside"], n_partitions=r["n_partitions"], m_star=r["m_star"], theta=r["theta"], stabiliser_value=r["m_star"] / 16,
               lovasz_lower=(15 - r["theta"]) / 16, numeric_min_F=float(fmin), non_stabiliser_optimum=bool(fmin < r["m_star"] / 16 - 1e-7))
    out.append(row); print(row, flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_four_qubit_minF_census.json"), "w"), indent=1)
