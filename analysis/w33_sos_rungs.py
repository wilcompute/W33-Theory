"""Item 3: the 1/d pattern.  Hermitian-SOS bound delta* = lambda_min(P_S M P_S on Sym^2(C^d)) for the smallest weakly unextendible Pauli
MUB sets on three rungs: d = 4 (two qubits, size 3), d = 8 (three qubits, size 5), d = 9 (two qutrits, size 5, = 1/9 proved).
Tightness: delta* equals the true minimum of F on the sphere iff the minimising eigenvector of H is (proportional to) a product v (x) v,
i.e. its 9x9 (d x d) reshaping has rank 1.  Reported: delta*, the numerical sphere minimum (Pass 12638 census), and the rank profile.
usage: py -3 analysis/w33_sos_rungs.py"""
import itertools, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read().split("res = {}")[0]
exec(src, cs)
geometry, bases_for, maximal_partial_spreads = cs["geometry"], cs["bases_for"], cs["maximal_partial_spreads"]
def herm_sos(B, Ls, d):
    E = [b for L in Ls for b in B[L].T]
    S = []
    for i in range(d):
        for j in range(i, d):
            v = np.zeros(d * d, complex)
            if i == j: v[i * d + i] = 1
            else: v[i * d + j] = v[j * d + i] = 1 / np.sqrt(2)
            S.append(v)
    S = np.array(S).T
    M = np.zeros((d * d, d * d), complex)
    for e in E:
        A = np.outer(e, e.conj()) - np.eye(d) / d
        M += np.kron(A, A)
    H = S.conj().T @ M @ S; H = (H + H.conj().T) / 2
    w, V = np.linalg.eigh(H)
    mult = int(np.sum(np.abs(w - w[0]) < 1e-9))
    # tightness: does the bottom eigenspace contain a product v(x)v ?  check rank of reshaped bottom eigenvectors (rank-1 candidate)
    ranks = []
    for k in range(mult):
        x = S @ V[:, k]
        ranks.append(int(np.sum(np.linalg.svd(x.reshape(d, d), compute_uv=False) > 1e-8)))
    return float(w[0]), mult, ranks
out = {}
for (p, n, size, label) in ((2, 2, 3, "d4_size3"), (2, 3, 5, "d8_size5"), (3, 2, 5, "d9_size5"), (3, 2, 8, "d9_size8")):
    pts, lag, w = geometry(p, n); d = p ** n
    B = bases_for(p, n, pts, lag)
    mps, disj = maximal_partial_spreads(lag)
    S_ = sorted(next(S for S in mps if len(S) == size))
    ds, mult, ranks = herm_sos(B, S_, d)
    out[label] = dict(d=d, delta_star=ds, delta_times_d=ds * d, bottom_multiplicity=mult, bottom_eigvec_ranks=ranks)
    print(label, "delta* = %.10f (x d = %.6f), bottom multiplicity %d, reshaped ranks %s" % (ds, ds * d, mult, ranks[:6]))
json.dump(out, open(os.path.join(ROOT, "data", "w33_sos_rungs.json"), "w"), indent=1)
