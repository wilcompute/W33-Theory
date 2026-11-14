"""Pass 12665: where does the attractor flow send the charge of a MIXED three-qubit state?
For a density matrix rho, its charge is Q_v = Tr(rho P_v) over the 27 quadric Paulis; X(Q) = 8 rho_J - I with rho_J = (rho + J rho J^-1)/2
(Pass 12656).  rho_J has quaternionic eigenvalues p_1 >= p_2 >= p_3 >= p_4 (each doubly degenerate, sum 2 p_i = 1).
N(Q) = sum (8 p_i - 1)^3 / 24.  If N > 0 the attractor flow (w33_attractor_pure_states.py) ends at N^(1/3) times a pure-state charge,
with projector Pi*.  Hypothesis A: Pi* = projector onto the top quaternionic eigenspace of rho_J (spectral truncation).
Hypothesis B: the attractor projector is fixed by the USp(8)-covariant flow, so Pi* commutes with rho_J (weaker).
Also recorded: the state-body boundary.  For physical charges N <= 1 with equality iff the state is pure (from sum p_i = 1/2,
p_i >= 0); so the black-hole entropy S ~ pi sqrt(N) of a quantum state's charge is maximal exactly for pure states.
usage: py -3 analysis/w33_attractor_of_mixed_states.py"""
import json, os, time
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_attractor_pure_states.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_attractor_pure_states.py")}
exec(src[: src.index("rows = []")], g)
Xof, Nof, PQ, P, Ps, flow = g["Xof"], g["Nof"], g["PQ"], g["P"], g["Ps"], g["flow"]
a0 = 1 | 8
J = Ps[a0]  # P_a; the antiunitary is J psi = P_a conj(psi)
def rhoJ(rho): return (rho + J @ rho.conj() @ J.conj().T) / 2
rng = np.random.default_rng(7); rows = []
for trial in range(10):
    k = int(rng.integers(2, 5)); V = rng.standard_normal((8, k)) + 1j * rng.standard_normal((8, k))
    w = rng.dirichlet(np.ones(k) * 0.4); rho = sum(wi * np.outer(V[:, i], V[:, i].conj()) / np.linalg.norm(V[:, i]) ** 2 for i, wi in enumerate(w))
    Q = np.einsum("ij,kji->k", rho, PQ).real
    RJ = rhoJ(rho); X_direct = 8 * RJ - np.eye(8)
    assert np.allclose(Xof(Q), X_direct, atol=1e-10)
    ev, U = np.linalg.eigh(RJ); p = ev[::2][::-1] if False else np.sort(ev)[::-1][::2]
    N = Nof(Q)
    rec = dict(quaternionic_spectrum=[round(float(x), 5) for x in p], N=N, N_formula=float(sum((8 * x - 1) ** 3 for x in p) / 24))
    if N > 1e-6:
        Qs, Vmin = flow(Q, starts=3); c = np.cbrt(N)
        Pi_star = (Xof(Qs) / c + np.eye(8)) / 4
        top = U[:, -2:]; Pi_top = top @ top.conj().T
        rec.update(V_min=Vmin, three_N23=3 * N ** (2 / 3), hypA_top_eigenspace=float(np.abs(Pi_star - Pi_top).max()),
                   hypB_commutes=float(np.abs(Pi_star @ RJ - RJ @ Pi_star).max()), overlap_with_top=float(np.trace(Pi_star @ Pi_top).real / 2))
    rows.append(rec); print(rec, flush=True)
res = dict(rows=rows, n_positive=sum(1 for r in rows if r["N"] > 1e-6),
           hypA_holds=all(r.get("hypA_top_eigenspace", 0) < 1e-4 for r in rows), hypB_holds=all(r.get("hypB_commutes", 0) < 1e-4 for r in rows))
print({k: v for k, v in res.items() if k != "rows"})
json.dump(res, open(os.path.join(ROOT, "data", "w33_attractor_of_mixed_states.json"), "w"), indent=1)
