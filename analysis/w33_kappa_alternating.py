"""Pass 12650: independent check that kappa = max sum_j |<x|M_j|y>|^2 equals 3 (orthonormal scaling), by alternating maximisation
(x <- top eigenvector of sum_j M_j y y^H M_j^H, then y likewise) from many random starts.  usage: py -3 analysis/w33_kappa_alternating.py"""
import json, os, contextlib, io
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py")}
src = open(os.path.join(HERE, "w33_threequbit_analytic_one_eighth.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("# kappa numerically")], g)
Mo = [M / g["nu"] for M in g["Ms"]]
rng = np.random.default_rng(12650); vals = []
for _ in range(2000):
    y = rng.standard_normal(4) + 1j * rng.standard_normal(4); y /= np.linalg.norm(y)
    for _ in range(200):
        A = sum(M @ np.outer(y, y.conj()) @ M.conj().T for M in Mo); w, V = np.linalg.eigh(A); x = V[:, -1]
        B = sum(M.conj().T @ np.outer(x, x.conj()) @ M for M in Mo); w2, V2 = np.linalg.eigh(B); y = V2[:, -1]
    vals.append(float(w2[-1]))
res = dict(starts=2000, max=max(vals), min_local=min(vals), histogram=dict((round(v, 6), vals.count(v)) for v in sorted(set(np.round(vals, 6)))[:10]))
print(res); json.dump({k: (str(v) if k == "histogram" else v) for k, v in res.items()}, open(os.path.join(ROOT, "data", "w33_kappa_alternating.json"), "w"), indent=1)
