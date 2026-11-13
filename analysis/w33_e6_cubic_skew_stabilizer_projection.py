"""Pass 12653 (cross-track, executes the parallel assistant's PROPOSED-but-unexecuted calculation, 2026-11-13):
for the repository's signed E6 cubic N(x) = sum over the 45 canonical triads s_ijk x_i x_j x_k (E6-id coordinates; signs from
extracted_v13/.../canonical_su3_gauge_and_cubic.json, as in analysis/toe_20261113_chiral_e6_cubic_compatibility.py), compute
  g_N = {X in M_27(R) : L_X N = 0}  (L_X N(x) = 3 T(Xx, x, x), a linear system in X),
  k_N = g_N cap so(27),
and project the chiral clock generator D (analysis/toe_20261113_chiral_null_order3_gate.py; real skew, spectrum 0, +-3 sqrt3 i),
transported to E6 coordinates by the SAME fixed address table (D_E = Pi D Pi^T, both input and output relabelled), onto k_N:
X* = argmin ||X - D_E||_F over k_N.
Expectation (structure theory): a nondegenerate cubic on R^27 with E6-type stabiliser has dim g_N = 78 (a real form of e6), and
k_N is its maximal compact subalgebra: f4 (dim 52) for E6(-26), sp(4) = c4 (dim 36) for E6(6), su(6)+su(2) (dim 38) for E6(2), ...
Controls: (i) dim g_N computed for the UNSIGNED cubic (all s = +1) as a comparison; (ii) every basis element of k_N is verified to
satisfy N(e^{sX}x) = N(x) numerically at random x; (iii) D_E itself must FAIL (the parallel track's counterexample) with
||L_D N|| > 0.  Scope: ONE fixed noncanonical identification, as in the source; no statement about other identifications.
usage: py -3 analysis/w33_e6_cubic_skew_stabilizer_projection.py"""
import json, os, sys, itertools
import numpy as np
from scipy.linalg import expm, null_space

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import toe_20261113_chiral_null_order3_gate as G

canon = json.load(open(os.path.join(ROOT, "extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json"), encoding="utf-8"))
bridge = json.load(open(os.path.join(ROOT, "data/w33_e6id_current_h27_gauge_bridge.json"), encoding="utf-8"))
signs = {}
for row in canon["solution"]["d_triples"]:
    signs[tuple(sorted(map(int, row["triple"])))] = 1 if int(row["sign"]) % 3 == 1 else -1
assert len(signs) == 45


def tensor(sg):
    T = np.zeros((27, 27, 27))
    for (i, j, k), s in sg.items():
        for p in set(itertools.permutations((i, j, k))):
            T[p] = s / 6.0  # N(x) = T(x,x,x) = sum s x_i x_j x_k (distinct i<j<k)
    return T


def stabilizer(T):
    """basis of {X : sum_l (X_li T_ljk + X_lj T_ilk + X_lk T_ijl) = 0}, X flattened row-major (X[l, i] -> index 27*l + i)."""
    n = 27; rows = []
    # equation for each sorted (i<=j<=k): symmetrised derivative; build as linear map X -> S_ijk
    A = np.zeros((n, n, n, n, n))  # A[i,j,k,l,m] coefficient of X[l,m]
    for l in range(n):
        A[:, :, :, l, :] += np.einsum("jk,i...->ijk", np.zeros((n, n)), np.zeros(1)) if False else 0
    # direct construction: (X.T)(i,j,k) = sum_l X[l,i] T[l,j,k] + X[l,j] T[i,l,k] + X[l,k] T[i,j,l]
    idx = [(i, j, k) for i in range(n) for j in range(i, n) for k in range(j, n)]
    M = np.zeros((len(idx), n * n))
    for r, (i, j, k) in enumerate(idx):
        for l in range(n):
            M[r, l * n + i] += T[l, j, k]
            M[r, l * n + j] += T[i, l, k]
            M[r, l * n + k] += T[i, j, l]
    M = M[np.abs(M).sum(1) > 0]
    return null_space(M, rcond=1e-10)  # columns = basis vectors of g_N


def cubic(T, x): return np.einsum("ijk,i,j,k->", T, x, x, x)


T = tensor(signs)
gN = stabilizer(T)
T_unsigned = tensor({k: 1 for k in signs})
gN_unsigned = stabilizer(T_unsigned)
print("dim g_N (signed)", gN.shape[1], " dim g_N (unsigned control)", gN_unsigned.shape[1], flush=True)
# k_N = g_N cap so(27): solve for coefficients c with X(c) skew
n = 27
skew_res = np.array([(gN[:, a].reshape(n, n) + gN[:, a].reshape(n, n).T).reshape(-1) for a in range(gN.shape[1])]).T
cs = null_space(skew_res, rcond=1e-10)
K = gN @ cs  # columns: basis of k_N (flattened)
K, _ = np.linalg.qr(K)  # orthonormal (Frobenius)
dimK = K.shape[1]
print("dim k_N = g_N cap so(27):", dimK, flush=True)
rng = np.random.default_rng(0)
worst = 0.0
for a in range(dimK):
    X = K[:, a].reshape(n, n)
    for _ in range(3):
        x = rng.standard_normal(n); s = 0.37
        worst = max(worst, abs(cubic(T, expm(s * X) @ x) - cubic(T, x)))
print("control: max |N(e^{sX}x) - N(x)| over k_N basis", worst, flush=True)
# transport D to E6 coordinates (both sides)
_, _, D = G.build(); D = np.array(D, dtype=float)
e_to_h = {int(k): tuple(map(int, v)) for k, v in bridge["maps"]["e6id_to_current_H27_address"].items()}
Pi = np.zeros((n, n))
for i in range(n): Pi[i, G.VID[e_to_h[i]]] = 1
DE = Pi @ D @ Pi.T
LD = np.einsum("li,ljk->ijk", DE, T); LD = LD + LD.transpose(1, 0, 2) + LD.transpose(1, 2, 0)
print("control: ||L_D N|| (must be > 0):", float(np.abs(LD).max()), flush=True)
Xstar = (K @ (K.T @ DE.reshape(-1))).reshape(n, n)
ratio = float(np.linalg.norm(Xstar) / np.linalg.norm(DE))
ev = np.linalg.eigvals(Xstar)
res = dict(dim_g_N_signed=int(gN.shape[1]), dim_g_N_unsigned=int(gN_unsigned.shape[1]), dim_k_N=int(dimK),
           k_N_invariance_check=float(worst), L_D_N_max=float(np.abs(LD).max()),
           projection_norm_ratio=ratio, residual_norm_ratio=float(np.linalg.norm(DE - Xstar) / np.linalg.norm(DE)),
           Xstar_spectrum_imag_sorted=sorted(np.round(ev.imag, 6).tolist()),
           Xstar_nonzero_entries=int((np.abs(Xstar) > 1e-9).sum()), D_nonzero_entries=int((np.abs(DE) > 1e-9).sum()),
           scope="one fixed noncanonical address identification (as in the source); no statement about other identifications")
print({k: v for k, v in res.items() if k != "Xstar_spectrum_imag_sorted"}, flush=True)
print("X* spectrum (imag parts, distinct):", sorted(set(np.round(ev.imag, 4).tolist())), flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_e6_cubic_skew_stabilizer_projection.json"), "w"), indent=1)
