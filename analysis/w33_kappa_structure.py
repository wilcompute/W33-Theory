"""Pass 12649: structure behind kappa = 3 (Lemma B of the analytic 1/8 route).  R_j = a_j a_1 restricted to V_+ (two-qubit operators):
pairwise commutation pattern, which are proportional to Paulis, and the optimiser (x, y) of sum_j |<x|M_j|y>|^2: Schmidt-like data and
how many M_j contribute.  usage: py -3 analysis/w33_kappa_structure.py"""
import json, os, contextlib, io, itertools
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py")}
src = open(os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# kappa numerically")], g)
Ms, nu, reps, pauli, pts, Vp, Vm = g["Ms"], g["nu"], g["reps"], g["pauli"], g["pts"], g["Vp"], g["Vm"]
Mo = [M / nu for M in Ms]  # orthonormal-basis blocks (unitary 4x4)
R = [M @ Mo[0].conj().T for M in Mo]  # maps V_+ -> V_+ via a_j a_1
comm = [[int(np.allclose(R[i] @ R[j], R[j] @ R[i])) for j in range(6)] for i in range(6)]
unit = all(np.allclose(M @ M.conj().T, np.eye(4)) for M in Mo)
rng = np.random.default_rng(1)
def neg(z):
    x = z[:4] + 1j * z[4:8]; y = z[8:12] + 1j * z[12:]
    x /= np.linalg.norm(x); y /= np.linalg.norm(y)
    return -sum(abs(np.vdot(x, M @ y)) ** 2 for M in Mo)
best = min((minimize(neg, rng.standard_normal(16), method="BFGS") for _ in range(40)), key=lambda r: r.fun)
x = best.x[:4] + 1j * best.x[4:8]; y = best.x[8:12] + 1j * best.x[12:]; x /= np.linalg.norm(x); y /= np.linalg.norm(y)
contrib = sorted(float(abs(np.vdot(x, M @ y)) ** 2) for M in Mo)
res = dict(blocks_unitary=unit, commutation_matrix=comm, kappa=-float(best.fun), contributions=contrib)
print(json.dumps(res)); json.dump(res, open(os.path.join(ROOT, "data", "w33_kappa_structure.json"), "w"), indent=1)
