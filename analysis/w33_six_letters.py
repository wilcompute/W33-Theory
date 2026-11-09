"""Item 1: the six letters of the doily S6 inside each 5D sector of Sym^2(C^9).
In (5,1) the point stabiliser S5 of letter 6 fixes a line: f6 = the common +1 eigenvector (in the sector s = 0) of the transpositions
(k l) = t_k t_l t_k, k, l <= 5; then f_k = t_k f6.  Checks: the f's are permuted (up to sign) by every t, sum to 0 (standard rep), have equal
norms and pairwise overlap -1/5 (simplex).  Identification: reshape each f_k (a symmetric 9x9 matrix) - its rank and spectrum; if rank 1,
f_k = psi_k (x) psi_k and the letters are six states of C^9 (then test: stabiliser states? which context / which double-six?).
usage: py -3 analysis/w33_six_letters.py"""
import itertools, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
si = {"__name__": "x", "__file__": os.path.join(HERE, "w33_sentinel_identity.py")}
src = open(os.path.join(HERE, "w33_sentinel_identity.py"), encoding="utf-8").read().split("# --- Jucys-Murphy test")[0]
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    exec(src.replace('json.dump(res, open(os.path.join(ROOT, "data", "w33_sentinel_identity.json"), "w"), indent=1, default=str)', 'pass'), si)
Ss = si["Ss"]
lab = [(a, b) for a in range(3) for b in range(3)]
V = []
for i in range(9):
    for j in range(i, 9):
        if ((lab[i][0] + lab[j][0]) % 3, (lab[i][1] + lab[j][1]) % 3) == (0, 0):
            v = np.zeros(81, complex)
            if i == j: v[i * 9 + i] = 1
            else: v[i * 9 + j] = v[j * 9 + i] = 1 / np.sqrt(2)
            V.append(v)
V = np.array(V).T  # 81 x 5
t = [V.conj().T @ S @ V for S in Ss]
trans = [t[k] @ t[l] @ t[k] for k, l in itertools.combinations(range(5), 2)]
A = sum(trans) - len(trans) * np.eye(5)
w_, U_ = np.linalg.eigh((A + A.conj().T) / 2)
f6 = U_[:, np.argmin(np.abs(w_))]
assert all(np.allclose(T @ f6, f6, atol=1e-8) for T in trans)
F = [t[k] @ f6 for k in range(5)] + [f6]
G = np.array([[np.vdot(a, b) for b in F] for a in F])
perm_ok = all(any(np.allclose(T @ F[i], s * F[j], atol=1e-8) for j in range(6) for s in (1, -1)) for T in t for i in range(6))
res = dict(sum_zero=bool(np.allclose(sum(F), 0, atol=1e-8)), gram_diag=float(G[0, 0].real), gram_off=sorted(set(np.round(G[np.triu_indices(6, 1)].real, 6))), permuted=perm_ok)
mats = [(V @ f).reshape(9, 9) for f in F]
res["ranks"] = [int(np.sum(np.linalg.svd(Mx, compute_uv=False) > 1e-8)) for Mx in mats]
res["svals_first"] = [float(x) for x in np.round(np.linalg.svd(mats[0], compute_uv=False)[:9], 6)]
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_six_letters.json"), "w"), indent=1, default=str)

# --- each letter's distinguished 2-plane: top-2 singular subspace of its 9x9 matrix; does it lie in the parity -1 sector (dim 4)?
Par = np.zeros((9, 9))
for j1 in range(3):
    for j2 in range(3):
        Par[3 * ((-j1) % 3) + ((-j2) % 3), 3 * j1 + j2] = 1
Podd = (np.eye(9) - Par) / 2
planes = []
for Mx in mats:
    U, s, Vh = np.linalg.svd(Mx)
    Wk = U[:, :2]
    planes.append(Wk)
in_odd = [bool(np.allclose(Podd @ Wk, Wk, atol=1e-8)) for Wk in planes]
# pairwise relation of the 2-planes: principal angles
angs = sorted(set(np.round(np.linalg.svd(planes[0].conj().T @ planes[k], compute_uv=False), 6).tolist().__str__() for k in range(1, 6)))
# the matrix itself: is M_k = a*Par_sym + b*Q_k with Q_k projector onto the plane?
res.update(top2_in_parity_odd=in_odd, principal_cosines_vs_letter6=angs)
print("letter 2-planes inside the parity -1 sector:", in_odd, "| principal cosines with the other planes:", angs)
json.dump(res, open(os.path.join(ROOT, "data", "w33_six_letters.json"), "w"), indent=1, default=str)
