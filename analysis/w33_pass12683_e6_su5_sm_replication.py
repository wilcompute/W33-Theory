"""Pass 12683: independent float replication of the other track's E6 -> SU5 -> SM cubic-stabilizer chain (6a4a37517, toe_20261116_E6_full_cubic_SM_stabilizer.py) with its own I3 code (random-point sampling + SVD ranks, no exact elimination), plus two F-term facts: E6 has no cubic Casimir (Tr X^3 = 0 on the 27) and Y annihilates both singlet VEVs.   usage: py -3 analysis/w33_pass12683_e6_su5_sm_replication.py"""
import numpy as np
rng = np.random.default_rng(7)
def I3grad(x):
    A, B, C = x[:9].reshape(3, 3), x[9:18].reshape(3, 3), x[18:].reshape(3, 3)
    cof = lambda M: np.linalg.det(M) * np.linalg.inv(M).T      # d det / dM
    gA = cof(A) - (B @ C).T; gB = cof(B) - (C @ A).T; gC = cof(C) - (A @ B).T
    return np.concatenate([gA.ravel(), gB.ravel(), gC.ravel()])
rows = []
for _ in range(1600):
    x = rng.standard_normal(27); g = I3grad(x)
    rows.append(np.outer(g, x).ravel())            # coefficient of T_ij in g . (T x)
R = np.array(rows)
def rank(M): s = np.linalg.svd(M, compute_uv=False); return int((s > 1e-9 * s[0]).sum())
r0 = rank(R); print("derivations of I3:", 729 - r0, "(rank", r0, ")")
def unit_rows(cols=(), rws=()):
    out = []
    for c in cols:
        for i in range(27): e = np.zeros((27, 27)); e[i, c] = 1; out.append(e.ravel())   # T e_c = 0
    for r in rws:
        for j in range(27): e = np.zeros((27, 27)); e[r, j] = 1; out.append(e.ravel())   # e_r^T T = 0
    return np.array(out)
V = unit_rows(cols=(7, 8), rws=(7, 8))
r1 = rank(np.vstack([R, V])); print("stabilizer of 2x(27 + 27bar) singlet VEVs:", 729 - r1)
# Y on A (L,R), B (R,C), C (C,L): dA = YL A - A YR, dB = YR B - B YC, dC = YC C - C YL
YL, YR, YC = np.diag([1, 1, -2.]), np.diag([4, -2, -2.]), np.zeros((3, 3))
def Yact(x):
    A, B, C = x[:9].reshape(3, 3), x[9:18].reshape(3, 3), x[18:].reshape(3, 3)
    return np.concatenate([(YL @ A - A @ YR).ravel(), (YR @ B - B @ YC).ravel(), (YC @ C - C @ YL).ravel()])
Ym = np.array([Yact(e) for e in np.eye(27)]).T
assert np.allclose(Ym[:, [7, 8]], 0), "Y does not fix the VEVs"
x = rng.standard_normal(27); assert abs(I3grad(x) @ (Ym @ x)) < 1e-9, "Y not a derivation"
Ccomm = np.array([(np.kron(Ym, np.eye(27)) - np.kron(np.eye(27), Ym.T))[k] for k in range(729)])   # vec_row([Y,T]) coefficients
r2 = rank(np.vstack([R, V, Ccomm])); print("adding adjoint VEV along Y ([T,Y]=0):", 729 - r2)
print("Y eigenvalues on the 27 (hypercharge multiplicities):", dict(zip(*np.unique(np.round(np.diag(Ym), 6), return_counts=True))))
# E6 Lie algebra basis on the 27 = null space of R
_, s, vh = np.linalg.svd(R); Tb = [vh[k].reshape(27, 27) for k in range(r0, 729)]
X = sum(rng.standard_normal() * T for T in Tb)
print("Tr X^2 =", round(np.trace(X @ X), 6), "| Tr X^3 / |X|^3 =", np.trace(X @ X @ X) / np.linalg.norm(X) ** 3, "(E6: no cubic Casimir -> 0)")
# both VEVs are annihilated by Y, so the coupling Hbar Phi_Y H and Phi_Y H vanish at the vacuum
v1 = np.zeros(27); v1[8] = 1; v2 = np.zeros(27); v2[7] = 1
print("Y v1, Y v2 norms:", np.linalg.norm(Ym @ v1), np.linalg.norm(Ym @ v2), "| <v_i|Y|v_j>:", [float(a @ Ym @ b) for a in (v1, v2) for b in (v1, v2)])
import json, os
json.dump(dict(source_commit="6a4a37517", derivations=729 - r0, stabilizer_two_singlet_pairs=729 - r1, stabilizer_with_adjoint_Y=729 - r2,
               Y_spectrum={str(k): int(v) for k, v in zip(*np.unique(np.round(np.diag(Ym), 6), return_counts=True))},
               trace_X3_normalised=float(np.trace(X @ X @ X) / np.linalg.norm(X) ** 3), Y_annihilates_vevs=bool(np.linalg.norm(Ym @ v1) + np.linalg.norm(Ym @ v2) == 0)),
          open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "w33_pass12683_e6_su5_sm_replication.json"), "w"), indent=1)
