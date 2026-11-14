"""Pass 12667: is the attractor flow of a mixed state's charge a path through PHYSICAL states?
Endpoint (Pass 12665): X* = N^(1/3) (4 Pi - I), so I + X* has eigenvalues 1 + 3 N^(1/3) (x2) and 1 - N^(1/3) (x6), both >= 0 for
0 < N <= 1: the endpoint is the pseudo-pure state rho* = N^(1/3) Pi/2 + (1 - N^(1/3)) I/8, with the same cubic invariant N.
Here, for random mixed states with N > 0: (a) check rho* formula against the computed attractor; (b) along the geodesic
Q(t) = exp(t A*) Q, t in [0, 1], with A* the minimiser reached from the origin, record the smallest eigenvalue of I + X(Q(t))
(>= 0 means the charge is that of a physical state); (c) purity of rho_J(t) along the path, Tr(rho_J^2) = (Tr X^2 + 8)/64;
(d) |Q(t)|^2 is monotone along the path? (geodesic convexity of V predicts it).
usage: py -3 analysis/w33_attractor_path_physicality.py"""
import json, os
import numpy as np
from scipy.linalg import expm, expm_frechet
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_attractor_of_mixed_states.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_attractor_of_mixed_states.py")}
exec(src[: src.index("rng = np.random.default_rng(7); rows = []")], g)
Xof, Nof, PQ, P, rhoJ = g["Xof"], g["Nof"], g["PQ"], g["P"], g["rhoJ"]
Pst = np.array(P)
def solve(Q):
    def fg(a):
        A = np.einsum("i,ijk->jk", a, Pst); y = expm(A) @ Q
        return float(y @ y), np.array([2 * y @ (expm_frechet(A, Pi, compute_expm=False) @ Q) for Pi in Pst])
    r = minimize(fg, np.zeros(42), jac=True, method="BFGS", options=dict(gtol=1e-12, maxiter=5000))
    return np.einsum("i,ijk->jk", r.x, Pst)
rng = np.random.default_rng(21); rows = []
while len(rows) < 8:
    k = int(rng.integers(2, 6)); V = rng.standard_normal((8, k)) + 1j * rng.standard_normal((8, k)); w = rng.dirichlet(np.ones(k) * 0.5)
    rho = sum(wi * np.outer(V[:, i], V[:, i].conj()) / np.linalg.norm(V[:, i]) ** 2 for i, wi in enumerate(w))
    Q = np.einsum("ij,kji->k", rho, PQ).real; N = Nof(Q)
    if N <= 0.02: continue
    A = solve(Q); c = np.cbrt(N)
    RJ = rhoJ(rho); ev, U = np.linalg.eigh(RJ); Pi = U[:, -2:] @ U[:, -2:].conj().T
    rho_star = c * Pi / 2 + (1 - c) * np.eye(8) / 8
    Qend = expm(A) @ Q
    end_err = float(np.abs(np.einsum("ij,kji->k", rho_star, PQ).real - Qend).max())
    ts = np.linspace(0, 1, 41); mins = []; pur = []; V_ = []
    for t in ts:
        Qt = expm(t * A) @ Q; Xt = Xof(Qt)
        mins.append(float(np.linalg.eigvalsh(np.eye(8) + Xt).min())); pur.append(float((np.trace(Xt @ Xt).real + 8) / 64)); V_.append(float(Qt @ Qt))
    rows.append(dict(N=N, endpoint_matches_pseudo_pure=end_err, min_eig_I_plus_X_along_path=min(mins), min_at_t=float(ts[int(np.argmin(mins))]),
                     purity_start=pur[0], purity_end=pur[-1], purity_monotone=bool(all(b <= a + 1e-12 for a, b in zip(pur, pur[1:])) or all(b >= a - 1e-12 for a, b in zip(pur, pur[1:]))),
                     V_monotone_decreasing=bool(all(b <= a + 1e-10 for a, b in zip(V_, V_[1:]))), endpoint_min_eig=mins[-1], predicted_endpoint_min_eig=1 - c))
    print(rows[-1], flush=True)
res = dict(rows=rows, all_paths_physical=all(r["min_eig_I_plus_X_along_path"] >= -1e-9 for r in rows),
           all_endpoints_pseudo_pure=all(r["endpoint_matches_pseudo_pure"] < 1e-6 for r in rows))
print({k: v for k, v in res.items() if k != "rows"})
json.dump(res, open(os.path.join(ROOT, "data", "w33_attractor_path_physicality.json"), "w"), indent=1)
