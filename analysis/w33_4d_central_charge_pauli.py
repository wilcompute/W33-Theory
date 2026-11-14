"""Pass 12666: the 4D N=8 central charge in three-qubit Pauli language.
The 28 three-qubit Paulis with an odd number of Y's are antisymmetric 8x8 matrices and span the antisymmetric matrices.  So a central
charge Z_AB (28 complex = 56 real numbers, the 56 of E7(7) at the origin of moduli space) can be written Z = sum_a z_a P_a, z in C^28.
Cartan-Cremmer-Julia quartic invariant (in the SU(8) basis, e.g. Ferrara-Kallosh hep-th/0603247 eq. 2.x):
    I4(Z) = Tr(Z Zb Z Zb) - (1/4) (Tr Z Zb)^2 + 4 (Pf Z + Pf Zb),       Zb = conj(Z)
(normalisation checked here on the normal form: skew-eigenvalues (rho, 0, 0, 0) must give I4 = rho^4, the 1/8-BPS attractor).
Tests:
 (1) span: the 28 antisymmetric Paulis are linearly independent antisymmetric matrices (rank 28);
 (2) two states phi, psi give Z = phi psi^T - psi phi^T: rank 2, skew-eigenvalues (r, 0, 0, 0) with r = |phi ^ psi|, I4 = r^4 > 0,
     Pf Z = 0 -- the 1/8-BPS attractor form (residual SU(2) x SU(6), the stabiliser of the two-plane: Gr(2,8));
     its Pauli coefficients are z_a = (1/8) Tr(P_a^dag Z) = -(phi^T P_a psi)/4 (P_a Hermitian, antisymmetric);
 (3) 5D -> 4D: the quaternionic line {psi, J psi} of Pass 12665 gives Z = psi (J psi)^T - (J psi) psi^T, again rank 2 with r = 1;
 (4) controls: a generic Z (random z) has I4 of either sign and rank 8; rank-4 Z built from two planes has I4 computed;
     I4 is SU(8)-invariant: I4(U Z U^T) = I4(Z) for random U in SU(8) (not U(8): Pf(U Z U^T) = det U Pf Z).
usage: py -3 analysis/w33_4d_central_charge_pauli.py"""
import itertools, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)
def P(v):
    M = np.eye(1)
    for i in range(3):
        xi, zi = v >> i & 1, v >> (3 + i) & 1
        M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
    return M
q0 = lambda v: bin((v & 7) & (v >> 3)).count("1") % 2
anti = [v for v in range(1, 64) if q0(v) == 1]
PA = np.array([P(v) for v in anti])
def pf(A):
    """Pfaffian by recursive expansion (8x8)"""
    n = len(A)
    if n == 0: return 1.0 + 0j
    s = 0j
    for j in range(1, n):
        if A[0, j] == 0: continue
        idx = [k for k in range(n) if k not in (0, j)]
        s += (-1) ** (j + 1) * A[0, j] * pf(A[np.ix_(idx, idx)])
    return s
def I4(Z):
    Zb = Z.conj(); M = Z @ Zb
    return complex(np.trace(M @ M) - 0.25 * np.trace(M) ** 2 + 4 * (pf(Z) + pf(Zb)))
def skew_eigs(Z):
    s = np.linalg.svd(Z, compute_uv=False); return np.round(s[::2], 8)  # singular values come in pairs
rng = np.random.default_rng(0); res = {}
# (1)
assert all(np.allclose(M, -M.T) for M in PA)
res["n_antisymmetric_paulis"] = len(anti); res["span_rank"] = int(np.linalg.matrix_rank(PA.reshape(28, -1)))
# normal form check: Z = rho (e1 e2^T - e2 e1^T)
rho = 1.7; Zn = np.zeros((8, 8), complex); Zn[0, 1] = rho; Zn[1, 0] = -rho
res["normal_form_I4_over_rho4"] = I4(Zn).real / rho ** 4
# four equal skew eigenvalues: Z = rho * sum_k (e_{2k} e_{2k+1}^T - ...)
Z4 = np.zeros((8, 8), complex)
for k in range(4): Z4[2 * k, 2 * k + 1] = 1; Z4[2 * k + 1, 2 * k] = -1
res["four_equal_eigs_I4"] = I4(Z4).real
# (2) two-state charges
rows = []
for _ in range(6):
    phi = rng.standard_normal(8) + 1j * rng.standard_normal(8); psi = rng.standard_normal(8) + 1j * rng.standard_normal(8)
    Z = np.outer(phi, psi) - np.outer(psi, phi)
    z = np.array([np.trace(M.conj().T @ Z) / 8 for M in PA]); Zrec = np.einsum("a,aij->ij", z, PA)
    r = np.sqrt(np.linalg.norm(phi) ** 2 * np.linalg.norm(psi) ** 2 - abs(np.vdot(phi, psi)) ** 2)
    rows.append(dict(reconstruct_err=float(np.abs(Zrec - Z).max()), rank=int(np.linalg.matrix_rank(Z, tol=1e-9)), skew=skew_eigs(Z).tolist(),
                     r_formula=float(r), I4=I4(Z).real, I4_over_r4=I4(Z).real / r ** 4, pf=abs(pf(Z)),
                     coeff_formula_err=float(np.abs(z + np.array([phi @ M @ psi for M in PA]) / 4).max())))
res["two_state"] = rows
# (3) 5D -> 4D
Pa = P(1 | 8); five = []
for _ in range(4):
    psi = rng.standard_normal(8) + 1j * rng.standard_normal(8); psi /= np.linalg.norm(psi); jpsi = Pa @ psi.conj()
    Z = np.outer(psi, jpsi) - np.outer(jpsi, psi)
    five.append(dict(rank=int(np.linalg.matrix_rank(Z, tol=1e-9)), skew=skew_eigs(Z).tolist(), I4=I4(Z).real))
res["five_to_four"] = five
# (4) controls
U, _ = np.linalg.qr(rng.standard_normal((8, 8)) + 1j * rng.standard_normal((8, 8))); U = U / np.linalg.det(U) ** (1 / 8)  # SU(8): Pf picks up det U
ctrl = []
for _ in range(6):
    z = rng.standard_normal(28) + 1j * rng.standard_normal(28); Z = np.einsum("a,aij->ij", z, PA)
    ctrl.append(dict(rank=int(np.linalg.matrix_rank(Z, tol=1e-9)), I4=I4(Z).real, I4_im=abs(I4(Z).imag), su8_invariance=abs(I4(U @ Z @ U.T) - I4(Z))))
res["generic"] = ctrl
res["generic_I4_signs"] = sorted({int(np.sign(c["I4"])) for c in ctrl})
print(json.dumps({k: v for k, v in res.items() if k not in ("two_state", "five_to_four", "generic")}, indent=0))
for k in ("two_state", "five_to_four", "generic"):
    for r_ in res[k]: print(k, r_)
json.dump(res, open(os.path.join(ROOT, "data", "w33_4d_central_charge_pauli.json"), "w"), indent=1, default=float)
