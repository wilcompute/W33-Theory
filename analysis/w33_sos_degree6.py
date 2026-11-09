"""Item 2 + 3: (2) degree-6 Hermitian SOS: F(v)|v|^2 is a (3,3)-form = (v(x)v(x)v)^dag K (v(x)v(x)v), K = sum_e A_e (x) A_e (x) I; its
representative on Sym^3(C^d) is unique, so delta_6 = lambda_min(P3 K P3 | Sym^3) is the best bound F(v)|v|^2 >= delta_6 |v|^6.
Applied to the three-qubit size-5 sets (degree-4 failed: -5/8) and the two-qutrit pentads (degree-4: 1/9; sphere min 0.14711).
(3) exact-value patterns: the full degree-4 spectrum on Sym^2 (eigenvalues x d and multiplicities) for d4 size-3, d8 size-5, d9 size-5, d9 size-8.
usage: py -3 analysis/w33_sos_degree6.py"""
import itertools, json, os
from collections import Counter
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
exec(open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read().split("res = {}")[0], cs)
geometry, bases_for, maximal_partial_spreads = cs["geometry"], cs["bases_for"], cs["maximal_partial_spreads"]
def sym_basis(d, k):
    cols = []
    for combo in itertools.combinations_with_replacement(range(d), k):
        v = np.zeros(d ** k, complex)
        perms = set(itertools.permutations(combo))
        for p in perms:
            idx = 0
            for x in p: idx = idx * d + x
            v[idx] = 1
        cols.append(v / np.linalg.norm(v))
    return np.array(cols).T
def spectrum(E, d, k):
    S = sym_basis(d, k)
    As = [np.outer(e, e.conj()) - np.eye(d) / d for e in E]
    H = np.zeros((S.shape[1], S.shape[1]), complex)
    for A in As:
        if k == 2:
            K = np.kron(A, A)
        else:
            K = np.kron(np.kron(A, A), np.eye(d))
        H += S.conj().T @ K @ S
    H = (H + H.conj().T) / 2
    return np.linalg.eigvalsh(H)
out = {}
for (p, n, size, label) in ((2, 2, 3, "d4_size3"), (2, 3, 5, "d8_size5"), (3, 2, 5, "d9_size5"), (3, 2, 8, "d9_size8")):
    pts, lag, w = geometry(p, n); d = p ** n
    B = bases_for(p, n, pts, lag)
    mps, disj = maximal_partial_spreads(lag)
    S_ = sorted(next(S for S in mps if len(S) == size))
    E = [b for L in S_ for b in B[L].T]
    ev2 = spectrum(E, d, 2)
    spec2 = sorted(Counter(round(x * d, 6) for x in ev2).items())
    row = dict(d=d, degree4_spectrum_times_d=spec2)
    if label in ("d8_size5", "d9_size5"):
        ev3 = spectrum(E, d, 3)
        row["degree6_delta"] = float(ev3[0])
    out[label] = row
    print(label, "deg-4 spectrum (eigenvalue*d: mult):", spec2, ("| deg-6 delta = %.6f" % row["degree6_delta"]) if "degree6_delta" in row else "")
json.dump(out, open(os.path.join(ROOT, "data", "w33_sos_degree6.json"), "w"), indent=1)
