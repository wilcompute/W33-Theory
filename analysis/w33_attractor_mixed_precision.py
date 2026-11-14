"""Pass 12665: is the 1e-3 residual between the attractor projector and the top quaternionic eigenspace of rho_J (rank >= 3 cases of
w33_attractor_of_mixed_states.py) an optimiser artefact or real?  For fixed mixed states: minimise V(A) = |exp(A) Q|^2 over A in p
from several starts with an ANALYTIC gradient (d/dA_i V = 2 <exp(A)Q, d exp(A)[P_i] Q>, via the Frechet derivative) and tight
tolerances; compare the attractor projectors across starts and with the top eigenspace.  V is geodesically convex on E6(6)/USp(8),
but the stabiliser F4(4) of Q is non-compact, so the minima form a manifold (flat directions); the start at the origin and the
displacement norm |A| of each minimiser are recorded.
usage: py -3 analysis/w33_attractor_mixed_precision.py"""
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
def solve(Q, a0):
    def fg(a):
        A = np.einsum("i,ijk->jk", a, Pst); E = expm(A); y = E @ Q
        grad = np.array([2 * y @ (expm_frechet(A, Pi, compute_expm=False) @ Q) for Pi in Pst])
        return float(y @ y), grad
    r = minimize(fg, a0, jac=True, method="BFGS", options=dict(gtol=1e-13, maxiter=5000))
    A = np.einsum("i,ijk->jk", r.x, Pst); return expm(A) @ Q, r.fun, float(np.abs(r.jac).max()), float(np.linalg.norm(r.x))
rng = np.random.default_rng(11); out = []
for trial in range(4):
    k = 4; V = rng.standard_normal((8, k)) + 1j * rng.standard_normal((8, k)); w = np.array([0.7, 0.15, 0.1, 0.05])
    rho = sum(wi * np.outer(V[:, i], V[:, i].conj()) / np.linalg.norm(V[:, i]) ** 2 for i, wi in enumerate(w))
    Q = np.einsum("ij,kji->k", rho, PQ).real; N = Nof(Q); c = np.cbrt(N)
    RJ = rhoJ(rho); ev, U = np.linalg.eigh(RJ); Pi_top = U[:, -2:] @ U[:, -2:].conj().T
    Pis = []; recs = []
    for s in range(5):
        Qs, V_, gmax, anorm = solve(Q, 0.1 * rng.standard_normal(42) if s else np.zeros(42))
        Pi = (Xof(Qs) / c + np.eye(8)) / 4; Pis.append(Pi); recs.append(dict(V=V_, grad=gmax, anorm=anorm, dev=float(np.abs(Pi - Pi_top).max())))
    spread = max(float(np.abs(Pis[i] - Pis[j]).max()) for i in range(5) for j in range(i + 1, 5))
    dev = float(np.abs(Pis[0] - Pi_top).max())
    commut = float(np.abs(Pis[0] @ RJ - RJ @ Pis[0]).max())
    rec = dict(quaternionic_spectrum=[round(float(x), 5) for x in np.sort(ev)[::-1][::2]], N=N, V_vs_3N23=recs[0]["V"] - 3 * N ** (2 / 3),
               max_grad=max(r["grad"] for r in recs), spread_across_starts=spread,
               displacement_norms=[round(r["anorm"], 6) for r in recs], deviations_by_start=[float(r["dev"]) for r in recs], deviation_from_top=dev, commutator_with_rhoJ=commut)
    out.append(rec); print(rec, flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_attractor_mixed_precision.json"), "w"), indent=1)
