"""Pass 12649 item 1: an analytic proof route to min F = 1/8 for the three-qubit size-5 sets.
F = (7 - Sigma_U)/8 with Sigma_U = sum_{P in U} <P>^2.  Let P0 be the distinguished uncovered Pauli (coherent-closure singleton,
Pass 12643), psi = c psi_+ + s psi_- (P0-eigenspaces V_+-, c, s >= 0, t = <P0> = c^2 - s^2), A = uncovered Paulis anticommuting with
P0 (12), B = uncovered Paulis commuting with P0 (15).
 Lemma A: if B maps bijectively onto the 15 points of p0^perp/<p0> (= W(3,2)), then on each V_+- the B-operators are, up to sign, the
   15 non-identity two-qubit Paulis, so sum_B <P>_{+-}^2 <= 3 (two-qubit purity), and by convexity sum_B <P>^2 <= c^2 3 + s^2 3 = 3.
 Lemma B: <Q> = 2cs Re<psi_+|Q|psi_->.  A = 6 pairs {a, a+p0}; the Hermitian Pauli of a+p0 is +-i a P0, so its matrix
   element is -+i times that of a: the pair contributes 4c^2 s^2 (Re z^2 + Im z^2) = (1-t^2)|z|^2 EXACTLY (z = <psi_+|a|psi_->).
   Hence sum_A <Q>^2 = (1-t^2) sum_{j=1}^6 |<psi_+|a_j|psi_->|^2 <= (1-t^2) kappa, kappa := max over unit x in V_+, y in V_- of
   sum_j |<x|M_j|y>|^2.  Need kappa <= 3.
 Then Sigma_U <= t^2 + 3(1-t^2) + 3 = 6 - 2t^2 <= 6, i.e. F >= 1/8 (equality structure: t = 0).
This script verifies the combinatorial hypotheses exactly, computes kappa numerically (product-vector optimisation), and tries an exact
decomposable certificate 3 I - sum vec(M_j)vec(M_j)^H = P + Q^Gamma, P, Q >= 0 (Gaussian rationals, exact LDL^T).
usage: py -3 analysis/w33_threequbit_analytic_one_eighth.py"""
import json, os, contextlib, io, itertools
from fractions import Fraction as Fr
import numpy as np, cvxpy as cp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
pr_ = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_conditioning_profile.py")}
src = open(os.path.join(HERE, "w33_threequbit_conditioning_profile.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("def parts(")], pr_)
pts, w, C, U, p0, A, Bc, pauli, idx = (pr_[k] for k in ("pts", "w", "C", "U", "p0", "A", "Bc", "pauli", "idx"))
add = lambda a, b: idx[tuple((x + y) % 2 for x, y in zip(pts[a], pts[b]))]
res = {}
# Lemma A hypothesis: each pair {b, b+p0} (b in p0^perp, b != p0) has exactly one uncovered member, and B hits every pair once
perp = [b for b in range(63) if b != p0 and w(pts[b], pts[p0]) == 0]
pairs = {frozenset((b, add(b, p0))) for b in perp}
lemmaA = len(pairs) == 15 and all(sum(1 for x in pr if x not in C) == 1 for pr in pairs) and len(Bc) == 15
# Lemma B hypothesis: A closed under +p0
lemmaB_pairs = len(A) == 12 and all(add(a, p0) in A for a in A)
res.update(n_A=len(A), n_B=len(Bc), lemmaA_bijection=lemmaA, lemmaB_six_pairs=lemmaB_pairs)
print(res, flush=True)
# equal-norm Gaussian-integer eigenbases of P0: joint eigenbasis of a Lagrangian through p0 (stabiliser states)
P0 = pauli(pts[p0])
lag_through = next(L for L in pr_["lag"] if p0 in L)
gens = [pauli(pts[q]) for q in sorted(lag_through)]
Hm = sum((k + 1) * 0.731 ** k * G for k, G in enumerate(gens))
_, V = np.linalg.eigh((Hm + Hm.conj().T) / 2)
cols = []
for v in V.T:
    k = np.flatnonzero(np.abs(v) > 1e-9); u = v * np.sqrt(len(k)); u = u / (u[k[0]] / abs(u[k[0]]))
    R = np.round(u.real) + 1j * np.round(u.imag); assert np.abs(u - R).max() < 1e-9; cols.append(R)
norms = {int(round(np.vdot(c, c).real)) for c in cols}; assert len(norms) == 1; nu = norms.pop()
Vp = np.array([c for c in cols if np.allclose(P0 @ c, c)]).T; Vm = np.array([c for c in cols if np.allclose(P0 @ c, -c)]).T
assert Vp.shape == (8, 4) and Vm.shape == (8, 4)
reps = []; seen = set()
for a in A:
    if a in seen: continue
    seen |= {a, add(a, p0)}; reps.append(a)
Ms = [Vp.conj().T @ pauli(pts[a]) @ Vm for a in reps]  # = nu * (block in orthonormal basis)
# kappa numerically (orthonormal scaling: divide by nu)
def neg(z):
    x = z[:4] + 1j * z[4:8]; y = z[8:12] + 1j * z[12:]
    x = x / np.linalg.norm(x); y = y / np.linalg.norm(y)
    return -sum(abs(np.vdot(x, M @ y) / nu) ** 2 for M in Ms)
rng = np.random.default_rng(4)
kappa = -min(minimize(neg, rng.standard_normal(16), method="BFGS").fun for _ in range(60))
res.update(kappa_numeric=float(kappa)); print("kappa =", kappa, flush=True)
# decomposable certificate on C^4 (x) C^4:  x^H M y = <x (x) conj(y), m>, m = vec(M) row-major
m = [np.array([M[i, j] for i in range(4) for j in range(4)]) for M in Ms]   # coordinates (i, j) <-> x_i conj(y_j)
Mtot = sum(np.outer(v, v.conj()) for v in m)  # = nu^2 * (orthonormal version)
W = 3 * nu ** 2 * np.eye(16) - Mtot
def ptrans(X):  # partial transpose on the second factor (indices (i,j),(k,l) -> (i,l),(k,j))
    Y = X.reshape(4, 4, 4, 4).transpose(0, 3, 2, 1).reshape(16, 16); return Y
Qr = cp.Variable((16, 16), symmetric=True); Qi = cp.Variable((16, 16)); t = cp.Variable()
# P = W - Q^Gamma ; Q^Gamma is linear in Q: build via index permutation
perm = np.arange(256).reshape(4, 4, 4, 4).transpose(0, 3, 2, 1).reshape(-1)
QGr = cp.reshape(cp.vec(Qr, order="C")[perm], (16, 16), order="C"); QGi = cp.reshape(cp.vec(Qi, order="C")[perm], (16, 16), order="C")
Pr = W.real - QGr; Pi = W.imag - QGi
cons = [Qi == -Qi.T, cp.bmat([[Qr, -Qi], [Qi, Qr]]) >> t * np.eye(32), cp.bmat([[Pr, -Pi], [Pi, Pr]]) >> t * np.eye(32), t <= 1]
prob = cp.Problem(cp.Maximize(t), cons); prob.solve(solver=cp.SCS, eps=1e-10, max_iters=200000)
res.update(decomposable_margin=float(t.value) if t.value is not None else None, sdp_status=prob.status); print("decomposable margin", t.value, prob.status, flush=True)
# exact rounding: Q rounded to Gaussian rationals, P := W - Q^Gamma exactly; check P, Q >= 0 by exact LDL^T (realified)
def ldl_psd(M):
    M = [row[:] for row in M]; n_ = len(M)
    for i in range(n_):
        if M[i][i] <= 0:
            if M[i][i] < 0 or any(M[i][j] != 0 for j in range(i + 1, n_)): return False
            continue
        for j in range(i + 1, n_):
            if M[j][i] != 0:
                f = M[j][i] / M[i][i]
                for k in range(i, n_): M[j][k] -= f * M[i][k]
    return True
def realify(Re, Im):
    n_ = len(Re); return [[Re[i][j] for j in range(n_)] + [-Im[i][j] for j in range(n_)] for i in range(n_)] + [[Im[i][j] for j in range(n_)] + [Re[i][j] for j in range(n_)] for i in range(n_)]
Wr = [[Fr(int(round(W[i, j].real))) for j in range(16)] for i in range(16)]; Wi = [[Fr(int(round(W[i, j].imag))) for j in range(16)] for i in range(16)]
assert np.allclose(W, np.round(W.real) + 1j * np.round(W.imag))
res["exact_attempts"] = []
if t.value is not None:
    Qv = Qr.value + 1j * Qi.value
    for D in (2, 4, 8, 16, 64, 256, 1024, 4096):
        Qer = [[Fr(round(((Qv[i, j] + Qv[j, i].conjugate()) / 2).real * D), D) for j in range(16)] for i in range(16)]
        Qei = [[Fr(round(((Qv[i, j] - Qv[j, i].conjugate()) / 2).imag * D), D) if i != j else Fr(0) for j in range(16)] for i in range(16)]
        for i in range(16):
            for j in range(i):
                Qei[i][j] = -Qei[j][i]
        QGr_ = [[Qer[perm[i * 16 + j] // 16][perm[i * 16 + j] % 16] for j in range(16)] for i in range(16)]
        QGi_ = [[Qei[perm[i * 16 + j] // 16][perm[i * 16 + j] % 16] for j in range(16)] for i in range(16)]
        Per = [[Wr[i][j] - QGr_[i][j] for j in range(16)] for i in range(16)]; Pei = [[Wi[i][j] - QGi_[i][j] for j in range(16)] for i in range(16)]
        okQ = ldl_psd(realify(Qer, Qei)); okP = okQ and ldl_psd(realify(Per, Pei))
        res["exact_attempts"].append(dict(D=D, Q_psd=okQ, P_psd=okP)); print("D", D, okQ, okP, flush=True)
        if okP:
            res["kappa_le_3_exact"] = True; break
    else:
        res["kappa_le_3_exact"] = False
json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_analytic_one_eighth.json"), "w"), indent=1)
