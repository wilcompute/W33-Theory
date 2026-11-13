"""Pass 12651 item 1: an explicit model for kappa.  kappa = max over unit c in C^6 of ||sum_j c_j R_j||_op^2 (Pass 12650), R = {I} + a
pentagon of two-qubit Paulis.  Model: {II, XI, ZI, XZ, IX, ZY} (consecutive pentagon members anticommute, others commute).  Check the
anticommutation graph equals that of the data (Lemma B blocks), that the model's kappa equals the data's (3), and record the maximisers:
support of c and the block form M = I(x)B0 + X(x)B1 + Z(x)B2 with B0 in span{I,X}, B1 in span{I,Z}, B2 in span{I,Y}.
usage: py -3 analysis/w33_kappa_pentagon_model.py"""
import json, os, contextlib, io, itertools
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
I2 = np.eye(2); X = np.array([[0, 1], [1, 0]]); Z = np.diag([1, -1]); Y = np.array([[0, -1j], [1j, 0]])
model = [np.kron(I2, I2), np.kron(X, I2), np.kron(Z, I2), np.kron(X, Z), np.kron(I2, X), np.kron(Z, Y)]
def comm_graph(Rs): return [[int(np.allclose(A @ B, B @ A)) for B in Rs] for A in Rs]
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py")}
src = open(os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# kappa numerically")], g)
Mo = [M / g["nu"] for M in g["Ms"]]; data = [M @ Mo[0].conj().T for M in Mo]
deg = lambda G: sorted(sum(r) for r in G)
def kappa(Rs, starts=300, seed=0):
    rng = np.random.default_rng(seed)
    def neg(z):
        c = z[:6] + 1j * z[6:]; c = c / np.linalg.norm(c); M = sum(ci * R for ci, R in zip(c, Rs))
        return -np.linalg.norm(M, 2) ** 2
    rs = [minimize(neg, rng.standard_normal(12), method="Nelder-Mead", options=dict(maxiter=20000, xatol=1e-12, fatol=1e-14)) for _ in range(starts)]
    best = min(rs, key=lambda r: r.fun); c = best.x[:6] + 1j * best.x[6:]; c /= np.linalg.norm(c)
    return -best.fun, c
km, cm = kappa(model); kd, cd = kappa(data)
res = dict(model_degrees=deg(comm_graph(model)), data_degrees=deg(comm_graph(data)), kappa_model=float(km), kappa_data=float(kd),
           maximiser_abs_c_model=[round(float(abs(x)), 6) for x in cm], maximiser_abs_c_data=[round(float(abs(x)), 6) for x in cd])
print(json.dumps(res)); json.dump(res, open(os.path.join(ROOT, "data", "w33_kappa_pentagon_model.json"), "w"), indent=1)
