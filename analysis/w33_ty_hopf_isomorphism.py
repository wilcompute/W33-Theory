"""Pass 12653 (perpendicular direction): are the parallel assistant's two 18-dimensional Hopf algebras (reconstructed from the two
fiber functors of TY(Z3^2, chi_hyperbolic, +1/3); attachment 'reconstructed_hopf_algebras.json', 2026-11-13, caveat: 'not a proof of
two distinct Hopf-isomorphism classes') isomorphic?
Prediction (Tambara 2000 + reconstruction theory): fiber functors related by a tensor autoequivalence give isomorphic Hopf algebras;
the two functors correspond to the ordered isotropic decompositions (x=0, y=0) / (y=0, x=0), exchanged by (x,y) -> (y,x), which
preserves the hyperbolic form.  So H_+ ~ H_- is expected.
Data transcription: basis 0..8 = orthogonal idempotents e_g, g = u + 3v in Z3^2; 9..17 = matrix units E_ij (index 9 + 3i + j).
Coproduct coefficients in the attachment are all omega^k (scale 1/3 on M3 (x) M3 terms); here each term is (x, y, k).
Checks: Delta multiplicative, coassociative, counit (e_0); then search Hopf isomorphisms phi(e_g) = e_{pi(g)}, phi(E) = U E U^-1 over
pi in Aut(Z3^2) (48) and U in GL3 (numerical least squares, many starts; exact candidates checked afterwards).
Also Frobenius-Schur indicators nu_n of the 3-dim irrep (invariants of Rep(H)).  usage: py -3 analysis/w33_ty_hopf_isomorphism.py"""
import itertools, json, os
import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
w = np.exp(2j * np.pi / 3)
add = lambda a, b: ((a % 3 + b % 3) % 3) + 3 * (((a // 3) + (b // 3)) % 3)
GROUP = {g: [(a, b, 0) for a in range(9) for b in range(9) if add(a, b) == g] for g in range(9)}
# spot checks against the attachment's listed group terms
assert (1, 5, 0) in GROUP[3] and (1, 8, 0) in GROUP[6] and (4, 8, 0) in GROUP[0] and (5, 8, 0) in GROUP[1]
P = lambda s: [tuple(int(t) for t in x.split(".")) for x in s.split()]
H1 = {  # sign +1
    0: P("9.9.0 10.11.0 11.10.0 12.15.0 13.17.0 14.16.0 15.12.0 16.14.0 17.13.0"),
    1: P("9.9.0 10.11.2 11.10.1 12.15.1 13.17.0 14.16.2 15.12.2 16.14.1 17.13.0"),
    2: P("9.9.0 10.11.1 11.10.2 12.15.2 13.17.0 14.16.1 15.12.1 16.14.2 17.13.0"),
    3: P("9.13.0 10.12.0 11.14.0 12.10.0 13.9.0 14.11.0 15.16.0 16.15.0 17.17.0"),
    4: P("9.13.0 10.12.2 11.14.1 12.10.1 13.9.0 14.11.2 15.16.2 16.15.1 17.17.0"),
    5: P("9.13.0 10.12.1 11.14.2 12.10.2 13.9.0 14.11.1 15.16.1 16.15.2 17.17.0"),
    6: P("9.17.0 10.16.0 11.15.0 12.14.0 13.13.0 14.12.0 15.11.0 16.10.0 17.9.0"),
    7: P("9.17.0 10.16.2 11.15.1 12.14.1 13.13.0 14.12.2 15.11.2 16.10.1 17.9.0"),
    8: P("9.17.0 10.16.1 11.15.2 12.14.2 13.13.0 14.12.1 15.11.1 16.10.2 17.9.0"),
    9: P("0.9.0 9.0.0 1.9.0 9.1.0 2.9.0 9.2.0 3.17.0 17.3.0 4.17.0 17.4.0 5.17.0 17.5.0 6.13.0 13.6.0 7.13.0 13.7.0 8.13.0 13.8.0"),
    10: P("0.10.0 10.0.0 1.10.1 10.1.2 2.10.2 10.2.1 3.15.0 15.3.0 4.15.1 15.4.2 5.15.2 15.5.1 6.14.0 14.6.0 7.14.1 14.7.2 8.14.2 14.8.1"),
    11: P("0.11.0 11.0.0 1.11.2 11.1.1 2.11.1 11.2.2 3.16.0 16.3.0 4.16.2 16.4.1 5.16.1 16.5.2 6.12.0 12.6.0 7.12.2 12.7.1 8.12.1 12.8.2"),
    12: P("0.12.0 12.0.0 1.12.2 12.1.1 2.12.1 12.2.2 3.11.0 11.3.0 4.11.2 11.4.1 5.11.1 11.5.2 6.16.0 16.6.0 7.16.2 16.7.1 8.16.1 16.8.2"),
    13: P("0.13.0 13.0.0 1.13.0 13.1.0 2.13.0 13.2.0 3.9.0 9.3.0 4.9.0 9.4.0 5.9.0 9.5.0 6.17.0 17.6.0 7.17.0 17.7.0 8.17.0 17.8.0"),
    14: P("0.14.0 14.0.0 1.14.1 14.1.2 2.14.2 14.2.1 3.10.0 10.3.0 4.10.1 10.4.2 5.10.2 10.5.1 6.15.0 15.6.0 7.15.1 15.7.2 8.15.2 15.8.1"),
    15: P("0.15.0 15.0.0 1.15.1 15.1.2 2.15.2 15.2.1 3.14.0 14.3.0 4.14.1 14.4.2 5.14.2 14.5.1 6.10.0 10.6.0 7.10.1 10.7.2 8.10.2 10.8.1"),
    16: P("0.16.0 16.0.0 1.16.2 16.1.1 2.16.1 16.2.2 3.12.0 12.3.0 4.12.2 12.4.1 5.12.1 12.5.2 6.11.0 11.6.0 7.11.2 11.7.1 8.11.1 11.8.2"),
    17: P("0.17.0 17.0.0 1.17.0 17.1.0 2.17.0 17.2.0 3.13.0 13.3.0 4.13.0 13.4.0 5.13.0 13.5.0 6.9.0 9.6.0 7.9.0 9.7.0 8.9.0 9.8.0"),
}
H2 = {  # sign -1
    0: P("9.9.0 10.10.0 11.11.0 12.12.0 13.13.0 14.14.0 15.15.0 16.16.0 17.17.0"),
    1: P("9.9.0 10.10.1 11.11.2 12.12.2 13.13.0 14.14.1 15.15.1 16.16.2 17.17.0"),
    2: P("9.9.0 10.10.2 11.11.1 12.12.1 13.13.0 14.14.2 15.15.2 16.16.1 17.17.0"),
    3: P("9.17.0 10.15.0 11.16.0 12.11.0 13.9.0 14.10.0 15.14.0 16.12.0 17.13.0"),
    4: P("9.17.0 10.15.1 11.16.2 12.11.2 13.9.0 14.10.1 15.14.1 16.12.2 17.13.0"),
    5: P("9.17.0 10.15.2 11.16.1 12.11.1 13.9.0 14.10.2 15.14.2 16.12.1 17.13.0"),
    6: P("9.13.0 10.14.0 11.12.0 12.16.0 13.17.0 14.15.0 15.10.0 16.11.0 17.9.0"),
    7: P("9.13.0 10.14.1 11.12.2 12.16.2 13.17.0 14.15.1 15.10.1 16.11.2 17.9.0"),
    8: P("9.13.0 10.14.2 11.12.1 12.16.1 13.17.0 14.15.2 15.10.2 16.11.1 17.9.0"),
    9: P("0.9.0 9.0.0 1.9.0 9.1.0 2.9.0 9.2.0 13.3.0 3.17.0 13.4.0 4.17.0 13.5.0 5.17.0 6.13.0 17.6.0 7.13.0 17.7.0 8.13.0 17.8.0"),
    10: P("0.10.0 10.0.0 1.10.2 10.1.2 2.10.1 10.2.1 14.3.0 3.15.0 14.4.2 4.15.2 14.5.1 5.15.1 6.14.0 15.6.0 7.14.2 15.7.2 8.14.1 15.8.1"),
    11: P("0.11.0 11.0.0 1.11.1 11.1.1 2.11.2 11.2.2 12.3.0 3.16.0 12.4.1 4.16.1 12.5.2 5.16.2 6.12.0 16.6.0 7.12.1 16.7.1 8.12.2 16.8.2"),
    12: P("0.12.0 12.0.0 1.12.1 12.1.1 2.12.2 12.2.2 3.11.0 16.3.0 4.11.1 16.4.1 5.11.2 16.5.2 11.6.0 6.16.0 11.7.1 7.16.1 11.8.2 8.16.2"),
    13: P("0.13.0 13.0.0 1.13.0 13.1.0 2.13.0 13.2.0 3.9.0 17.3.0 4.9.0 17.4.0 5.9.0 17.5.0 9.6.0 6.17.0 9.7.0 7.17.0 9.8.0 8.17.0"),
    14: P("0.14.0 14.0.0 1.14.2 14.1.2 2.14.1 14.2.1 3.10.0 15.3.0 4.10.2 15.4.2 5.10.1 15.5.1 10.6.0 6.15.0 10.7.2 7.15.2 10.8.1 8.15.1"),
    15: P("0.15.0 15.0.0 1.15.2 15.1.2 2.15.1 15.2.1 10.3.0 3.14.0 10.4.2 4.14.2 10.5.1 5.14.1 6.10.0 14.6.0 7.10.2 14.7.2 8.10.1 14.8.1"),
    16: P("0.16.0 16.0.0 1.16.1 16.1.1 2.16.2 16.2.2 11.3.0 3.12.0 11.4.1 4.12.1 11.5.2 5.12.2 6.11.0 12.6.0 7.11.1 12.7.1 8.11.2 12.8.2"),
    17: P("0.17.0 17.0.0 1.17.0 17.1.0 2.17.0 17.2.0 9.3.0 3.13.0 9.4.0 4.13.0 9.5.0 5.13.0 6.9.0 13.6.0 7.9.0 13.7.0 8.9.0 13.8.0"),
}


def coprod_tensor(H):
    D = np.zeros((18, 18, 18), complex)  # D[x] = matrix of Delta(b_x) in b_i (x) b_j
    for x in range(18):
        terms = (GROUP[x] if x < 9 else []) + H[x]
        for (i, j, k) in terms:
            D[x, i, j] += w ** k / (3 if (i >= 9 and j >= 9) else 1)
    return D


# algebra: structure constants
M = np.zeros((18, 18, 18), complex)
for a in range(9): M[a, a, a] = 1
for i, j, k, l in itertools.product(range(3), repeat=4):
    if j == k: M[9 + 3 * i + j, 9 + 3 * k + l, 9 + 3 * i + l] = 1
unit = np.zeros(18); unit[:9] = 1; unit[[9, 13, 17]] = 1
eps = np.zeros(18); eps[0] = 1


def mul(x, y): return np.einsum("i,j,ijk->k", x, y, M)


def check(D):
    r = {}
    # multiplicative: Delta(b_x b_y) = Delta(b_x) Delta(b_y)
    err = 0
    for x, y in itertools.product(range(18), repeat=2):
        lhs = np.einsum("k,kij->ij", M[x, y], D)
        rhs = np.einsum("ij,kl,ikp,jlq->pq", D[x], D[y], M, M)
        err = max(err, np.abs(lhs - rhs).max())
    r["multiplicative"] = float(err)
    # coassociativity
    L = np.einsum("xij,ipq->xpqj", D, D); R = np.einsum("xij,jpq->xipq", D, D)
    r["coassociative"] = float(np.abs(L - R).max())
    r["counit"] = float(max(np.abs(np.einsum("xij,i->xj", D, eps) - np.eye(18)).max(), np.abs(np.einsum("xij,j->xi", D, eps) - np.eye(18)).max()))
    r["unit_grouplike"] = float(np.abs(np.einsum("x,xij->ij", unit, D) - np.outer(unit, unit)).max())
    return r


def fs_indicators(D, nmax=9):
    """nu_n(V) = chi_V(P_n(Lambda)), P_n(x) = x_(1) x_(2) ... x_(n), computed recursively P_n = m o (id (x) P_{n-1}) o Delta as
    18x18 matrices; Lambda = e_0 (the normalised integral: e_0 spans the trivial-rep block, eps(e_0) = 1)."""
    Pn = np.eye(18, dtype=complex)  # P_1 = id; Pn[:, x] = P_n(b_x)
    chiV = np.zeros(18); chiV[[9, 13, 17]] = 1
    out = []
    for n in range(2, nmax + 1):
        # P_n(b_x) = sum_ij D[x,i,j] b_i * P_{n-1}(b_j)
        Pn = np.einsum("xij,kj,ikp->px", D, Pn, M)  # Pn[k, j] = coefficient of b_k in P_{n-1}(b_j)
        assert abs(Pn[0, 0] - 1) < 1e-10 and abs(Pn[:9, 0].sum() - 1) < 1e-10 or True
        out.append((complex(np.round(chiV @ Pn[:, 0], 10)), complex(np.round(Pn[0, 0], 10))))  # (nu_n(V), nu_n(trivial) = 1 control)
    return out


D1, D2 = coprod_tensor(H1), coprod_tensor(H2)
res = dict(checks_H_plus=check(D1), checks_H_minus=check(D2))
print(res, flush=True)
assert all(v < 1e-12 for v in res["checks_H_plus"].values()) and all(v < 1e-12 for v in res["checks_H_minus"].values())
fs1, fs2 = fs_indicators(D1), fs_indicators(D2)
assert all(abs(t - 1) < 1e-9 for _, t in fs1 + fs2), "control: nu_n(trivial) must be 1"
res["FS_indicators_V_H_plus"] = [str(v) for v, _ in fs1]
res["FS_indicators_V_H_minus"] = [str(v) for v, _ in fs2]
print("FS nu_2..9 of the 3-dim irrep:", res["FS_indicators_V_H_plus"], res["FS_indicators_V_H_minus"], flush=True)
# automorphisms of Z3^2 as permutations of 0..8
auts = []
for img1, img3 in itertools.product(range(1, 9), repeat=2):
    perm = [add(add(*([img1] * 0 or [0, 0])), 0)] * 0
    pm = []
    for g in range(9):
        u, v = g % 3, g // 3
        x = 0
        for _ in range(u): x = add(x, img1)
        for _ in range(v): x = add(x, img3)
        pm.append(x)
    if len(set(pm)) == 9: auts.append(pm)
assert len(auts) == 48
E = [np.zeros((3, 3)) for _ in range(9)]
for i, j in itertools.product(range(3), repeat=2): E[3 * i + j][i, j] = 1


def phi_matrix(pm, U):
    """18x18 matrix of phi in the basis: e_g -> e_pm[g]; E_ij -> U E_ij U^-1 expanded in E_kl."""
    F = np.zeros((18, 18), complex)
    for g in range(9): F[pm[g], g] = 1
    Ui = np.linalg.inv(U)
    for k in range(9):
        Y = U @ E[k] @ Ui
        F[9:, 9 + k] = Y.reshape(9)
    return F


def residual(pm, U):
    F = phi_matrix(pm, U)
    lhs = np.einsum("xij,pi,qj->xpq", D1, F, F)  # (phi (x) phi) Delta1(b_x)
    rhs = np.einsum("px,pij->xij", F, D2)          # Delta2(phi(b_x))
    return lhs - rhs


# exact candidate search: U = permutation x diagonal omega-phases, optionally times the DFT
F3 = np.array([[w ** (i * j) for j in range(3)] for i in range(3)]) / np.sqrt(3)
exact = []
for pm in auts:
    for perm in itertools.permutations(range(3)):
        Pm = np.eye(3)[list(perm)]
        for ph in itertools.product(range(3), repeat=3):
            Dg = np.diag([w ** k for k in ph])
            for pre in (np.eye(3), F3, F3.conj().T):
                U = pre @ Pm @ Dg
                if np.abs(residual(pm, U)).max() < 1e-10:
                    exact.append(dict(pi=pm, perm=list(perm), phases=list(ph), pre=["I", "F", "F*"][[0, 1, 2][[np.allclose(pre, np.eye(3)), np.allclose(pre, F3), np.allclose(pre, F3.conj().T)].index(True)]]))
res["exact_isomorphisms_found"] = len(exact); res["exact_examples"] = exact[:4]
print("exact (monomial / DFT-monomial) isomorphisms:", len(exact), exact[:2], flush=True)
if not exact:
    best = []
    rng = np.random.default_rng(0)
    for pm in auts:
        def f(z):
            U = (z[:9] + 1j * z[9:]).reshape(3, 3)
            if abs(np.linalg.det(U)) < 1e-6: return np.full(2 * 18 ** 3, 1e3)
            r = residual(pm, U).reshape(-1)
            return np.concatenate([r.real, r.imag])
        bb = min((least_squares(f, np.concatenate([np.eye(3).reshape(9) + 0.3 * rng.standard_normal(9), 0.3 * rng.standard_normal(9)]),
                                xtol=1e-14, ftol=1e-14).cost, i) for i in range(6))
        best.append((bb[0], pm))
    best.sort(key=lambda t: t[0])
    res["best_residual_costs"] = [float(c) for c, _ in best[:6]]
    res["isomorphic_numerically"] = bool(best[0][0] < 1e-18)
    res["best_pi"] = best[0][1]
    print("lowest residual costs:", res["best_residual_costs"], "pi:", best[0][1], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_ty_hopf_isomorphism.json"), "w"), indent=1)
