"""Passes 11897-11898: the Kahler modulus carries the Siegel structure -- the Eisenstein duality group of two Z3 tori acts
on the nine twisted fixed points by the two-qutrit Weil representation, and the Siegel slice is the dual Burkhardt.

Setting. On T^4/Z3 = (C/Z[w])^2/Z3 the complex structure is frozen and the untwisted moduli are the Hermitian Kahler +
B-field matrix Z = B + iG (4 complex moduli, off-diagonal ones included: the Z3 orbifold keeps all T_{i jbar}). Their
space is the Hermitian half-space of degree 2 over O = Z[w], with duality group U(2,2;O). The nine fixed points are
(O/sqrt(-3))^2 = F3^2, and the twisted-sector instanton sums are built from the theta functions

    theta_mu(Z) = sum_{x in O^2 + mu/sqrt(-3)} e(x^* Z x),     mu in F3^2.

11897 (the finite modular flavour group):
  * theta(-Z^-1) = det(Z/i) F theta(Z) with F = (1/3) w^{mu.nu} (weight 1, both tori Fourier); Z -> Z + B multiplies by
    e(mu^* B mu / 3): diagonal B -> phase gates w^{c_i^2}, off-diagonal B = 1 (or w) -> the entangling gate w^{2 c1 c2},
    off-diagonal B in sqrt(-3) O -> trivial; Z -> A^* Z A (A in GL(2,O)) permutes mu -> A mu mod sqrt(-3).
  * The generated group has projective order 51840 and maps isomorphically (Pauli conjugation) onto Sp(4,3) = Aut W(3,3);
    linear order 103680. Diagonal moduli alone (one SL(2,Z) per torus) give only 576 = |T' x T'|: the W(3,3) structure is
    carried exactly by the off-diagonal Kahler moduli.
  * theta_mu = theta_{-mu}: the moduli-dependent couplings span the even Weil 5; the odd 4 vanish identically.
  * Together with the traditional (space-group) Heisenberg group 3^(1+4) of two Wilson-line-free tori (Pass 11105) this is
    the full two-qutrit Clifford group; W(3,3) = the commutation geometry of the 40 traditional flavour classes.
11898 (geometry and the three-torus extension):
  * the five even thetas map the Kahler moduli dominantly to P^4 (real Jacobian rank 8);
  * the unique PSp(4,3)-invariant quartic is the Burkhardt quartic; invariant dimensions in degrees 4..18 are
    1,1,1,2,3,2,4,5; on the Siegel slice (real symmetric Z) exactly one invariant vanishes, first in degree 18, and it
    its image is the DUAL Burkhardt: for every Siegel point y some polar preimage grad I4(b) = y lies on the quartic
    (defect 1e-16; generic Kahler points 1e-3) -- the Siegel slice maps into the dual Burkhardt (degree
    4*27 - 2*45 = 18) -- reproducing Freitag-Salvati Manni (A2(3)* = dual Burkhardt; Hermitian level sqrt(-3) <-> Burkhardt);
  * T6/Z3: theta(-Z^-1) = det(Z/i)^{...} F^{(x)3} theta(Z) on the 27 fixed points, the 27 twisted 9bars of the W(3,3)
    sector (Pass 11714) span 14 even functions, and the modular group reduces to Sp(6,3) (order 9170703360).
Physics: Kahler moduli are gauge singlets, so this two-qutrit/Siegel structure is Standard-Model neutral -- the field the
flagship tension (Pass 11896) asked for. It needs two Wilson-line-free tori (present in the Pass 11714 sector, absent in
the 104 three-generation spectra of Pass 11105, where Wilson lines reduce it to one torus).
"""

import itertools
import json
from collections import deque
from pathlib import Path

import numpy as np
from sympy.combinatorics import Permutation, PermutationGroup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11897_11898_kahler_moduli_two_qutrit_weil.json"
W = np.exp(2j * np.pi / 3)
S3 = 1j * np.sqrt(3)
MUS = list(itertools.product(range(3), repeat=2))
IDX = {m: i for i, m in enumerate(MUS)}


def lattice(N):
    r = np.arange(-N, N + 1)
    m, n = np.meshgrid(r, r, indexing="ij")
    return (m + n * W).ravel()


def theta2(Z, O):
    out = np.zeros(9, complex)
    for k, mu in enumerate(MUS):
        x1 = (O + mu[0] / S3)[:, None]
        x2 = (O + mu[1] / S3)[None, :]
        q = Z[0, 0] * abs(x1) ** 2 + Z[1, 1] * abs(x2) ** 2 + Z[0, 1] * np.conj(x1) * x2 + Z[1, 0] * np.conj(x2) * x1
        out[k] = np.exp(2j * np.pi * q).sum()
    return out


def theta3(Z, O):
    out = np.zeros(27, complex)
    for k, mu in enumerate(itertools.product(range(3), repeat=3)):
        x = [O + mu[i] / S3 for i in range(3)]
        X = np.stack(np.meshgrid(*x, indexing="ij"), -1).reshape(-1, 3)
        q = np.einsum("ni,ij,nj->n", X.conj(), Z, X)
        out[k] = np.exp(2j * np.pi * q).sum()
    return out


def rand_Z(rng, n=2, sym=False, ymin=0.8, yscale=3.0):
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    X = (A + A.conj().T) / 4
    B = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    Y = B @ B.conj().T / yscale + ymin * np.eye(n)
    if sym:
        X, Y = X.real, Y.real
    return X + 1j * Y


def fourier(n):
    ms = list(itertools.product(range(3), repeat=n))
    return np.array([[W ** (sum(a[i] * b[i] for i in range(n)) % 3) for b in ms] for a in ms]) / 3 ** (n / 2)


def diag2(f):
    return np.diag([W ** (f(*m) % 3) for m in MUS])


def perm2(A):
    P = np.zeros((9, 9))
    for m in MUS:
        im = tuple(int(x) % 3 for x in np.array(A) @ np.array(m))
        P[IDX[im], IDX[m]] = 1
    return P


GENS = {"S": fourier(2), "T1": diag2(lambda a, b: a * a), "T2": diag2(lambda a, b: b * b),
        "Toff": diag2(lambda a, b: 2 * a * b), "U": perm2([[1, 1], [0, 1]]), "Sw": perm2([[0, 1], [1, 0]]),
        "N": perm2([[2, 0], [0, 1]])}


def key(M, proj):
    if proj:
        v = M.ravel()
        k = np.flatnonzero(abs(v) > 1e-6)[0]
        M = M * abs(v[k]) / v[k]
    return (np.round(M, 4) + 0.0).tobytes()


def closure(G, proj, dim=9):
    I = np.eye(dim, dtype=complex)
    seen = {key(I, proj): I}
    q = deque([I])
    while q:
        x = q.popleft()
        for g in G:
            y = g @ x
            k = key(y, proj)
            if k not in seen:
                seen[k] = y
                q.append(y)
    return list(seen.values())


def pauli(a, b):
    X = perm2([[1, 0], [0, 1]]) * 0
    for m in MUS:
        X[IDX[((m[0] + a[0]) % 3, (m[1] + a[1]) % 3)], IDX[m]] = 1
    return X @ np.diag([W ** ((b[0] * m[0] + b[1] * m[1]) % 3) for m in MUS])


PAULIS = {(a, b): pauli(a, b) for a in MUS for b in MUS}


def symplectic_image(g):
    cols = []
    for e in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)):
        P = g @ PAULIS[(e[:2], e[2:])] @ g.conj().T
        for (a, b), Q in PAULIS.items():
            c = np.vdot(Q, P) / 9
            if abs(abs(c) - 1) < 1e-8:
                cols.append(a + b)
                break
    return np.array(cols, dtype=int).T % 3


def part_11897(rng):
    O = lattice(7)
    F = GENS["S"]
    inv_err, ratios = [], []
    for _ in range(3):
        Z = rand_Z(rng)
        t0, t1 = theta2(Z, O), theta2(-np.linalg.inv(Z), O)
        pred = np.linalg.det(Z / 1j) * (F @ t0)
        inv_err.append(float(np.max(abs(t1 - pred)) / np.max(abs(t1))))
    Z = rand_Z(rng)
    t0 = theta2(Z, O)
    tr = {}
    for name, B, expect in (("diag", np.array([[1, 0], [0, 0]]), GENS["T1"]),
                            ("offdiag_1", np.array([[0, 1], [1, 0]]), GENS["Toff"]),
                            ("offdiag_w", np.array([[0, W], [W ** 2, 0]]), GENS["Toff"]),
                            ("offdiag_sqrt-3", np.array([[0, S3], [np.conj(S3), 0]]), np.eye(9))):
        tr[name] = float(np.max(abs(theta2(Z + B, O) - expect @ t0)) / np.max(abs(t0)))
    A = np.array([[1, 1], [0, 1]])
    perm_err = float(np.max(abs(theta2(A.conj().T @ Z @ A, O) - GENS["U"].T @ t0)) / np.max(abs(t0)))
    even_err = float(max(abs(t0[IDX[m]] - t0[IDX[((-m[0]) % 3, (-m[1]) % 3)]]) for m in MUS) / np.max(abs(t0)))
    full = closure(list(GENS.values()), True)
    diag_only = closure([GENS["S"], GENS["T1"], GENS["T2"]], True)
    linear = closure(list(GENS.values()), False)
    # Pauli conjugation -> Sp(4,3)
    Om = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]])
    simg = [symplectic_image(g) for g in GENS.values()]
    preserves = all(((s.T @ Om @ s - Om) % 3 == 0).all() for s in simg)
    seen = {np.eye(4, dtype=int).tobytes()}
    q = deque([np.eye(4, dtype=int)])
    while q:
        x = q.popleft()
        for s in simg:
            y = (s @ x) % 3
            if y.tobytes() not in seen:
                seen.add(y.tobytes())
                q.append(y)
    # W(3,3) = commutation graph of the 40 projective Pauli classes
    pts = []
    for v in itertools.product(range(3), repeat=4):
        if any(v) and not any(tuple((2 * x) % 3 for x in v) == p for p in pts):
            pts.append(v)
    adj = np.array([[1 if i != j and (np.array(u) @ Om @ np.array(w)) % 3 == 0 else 0 for j, w in enumerate(pts)]
                    for i, u in enumerate(pts)])
    ev = sorted(set(np.round(np.linalg.eigvalsh(adj), 6)))
    return dict(inversion_rel_err=inv_err, translation_rel_err=tr, gl2_perm_rel_err=perm_err, even_rel_err=even_err,
                projective_order_full=len(full), projective_order_diagonal_moduli=len(diag_only),
                linear_order=len(linear), symplectic_image_order=len(seen), symplectic_preserves_form=preserves,
                w33_points=len(pts), w33_degree=int(adj.sum(1)[0]), w33_eigenvalues=[float(e) for e in ev])


def even_basis():
    pairs, seen = [], set()
    for m in MUS:
        if m in seen:
            continue
        mm = ((-m[0]) % 3, (-m[1]) % 3)
        seen |= {m, mm}
        pairs.append((m, mm))
    E = np.zeros((9, 5))
    for k, (a, b) in enumerate(pairs):
        E[IDX[a], k] += 0.5
        E[IDX[b], k] += 0.5
    return E


def part_11898(rng):
    O = lattice(8)
    E = even_basis()
    Ep = np.linalg.pinv(E)
    g5 = [Ep @ g @ E for g in GENS.values()]
    G5 = np.array(closure(g5, False, dim=5))

    def img(sym):
        x = Ep @ theta2(rand_Z(rng, sym=sym, ymin=0.45, yscale=4.0), O)
        return x / np.linalg.norm(x)
    # dominance: real Jacobian of Z -> P^4
    Z = rand_Z(rng)
    h = 1e-5
    x0 = Ep @ theta2(Z, O)
    x0 = x0 / x0[0]
    cols = []
    for (i, j) in ((0, 0), (1, 1), (0, 1), (1, 0)):
        for d in (1, 1j):
            dZ = np.zeros((2, 2), complex)
            dZ[i, j] = h * d
            x = Ep @ theta2(Z + dZ, O)
            dx = (x / x[0] - x0) / h
            cols.append(np.concatenate([dx.real, dx.imag]))
    jac_rank = int(np.linalg.matrix_rank(np.array(cols).T, 1e-4))
    # Burkhardt quartic
    mons = list(itertools.combinations_with_replacement(range(5), 4))

    def ev4(x):
        return np.array([np.prod(x[list(c)]) for c in mons])
    rows = []
    for g in g5:
        for _ in range(30):
            x = rng.normal(size=5) + 1j * rng.normal(size=5)
            rows.append(ev4(g @ x) - ev4(x))
    s, v = np.linalg.svd(np.array(rows))[1:]
    n_quartic = int(np.sum(s < 1e-9 * s[0])) + (70 - len(s))
    P4 = v[-1].conj()
    Sym = np.array([img(True) for _ in range(40)])
    Gen = np.array([img(False) for _ in range(40)])
    Arand = rng.normal(size=(12, 5)) + 1j * rng.normal(size=(12, 5))

    def inv_eval(X, d):
        GX = np.einsum("gij,nj->ngi", G5, X)
        return np.stack([((GX @ a) ** d).sum(1) / len(G5) for a in Arand], 1)
    dims, sym_ranks = {}, {}
    for d in (4, 6, 8, 10, 12, 14, 16, 18):
        sg = np.linalg.svd(inv_eval(Gen, d), compute_uv=False)
        ss = np.linalg.svd(inv_eval(Sym, d), compute_uv=False)
        dims[d] = int(np.sum(sg > 1e-8 * sg[0]))
        sym_ranks[d] = int(np.sum(ss[: dims[d]] > 1e-8 * ss[0]))
    # dual Burkhardt test: y is in the dual variety iff some solution of grad I4(b) = y lies on {I4 = 0}
    T4 = np.zeros((5,) * 4, complex)
    for cm, coef in zip(mons, P4):
        ps = set(itertools.permutations(cm))
        for pp in ps:
            T4[pp] += coef / len(ps)

    def grad(b):
        return 4 * np.einsum("ijkl,j,k,l->i", T4, b, b, b)

    def polar_defect(y, starts=300):
        y = y / np.linalg.norm(y)
        best = np.inf
        for _ in range(starts):
            b = rng.normal(size=5) + 1j * rng.normal(size=5)
            for _ in range(80):
                r = grad(b) - y
                if np.linalg.norm(r) < 1e-13:
                    break
                b = b - np.linalg.solve(12 * np.einsum("ijkl,k,l->ij", T4, b, b), r)
            if np.linalg.norm(grad(b) - y) < 1e-11:
                best = min(best, abs(np.einsum("ijkl,i,j,k,l", T4, b, b, b, b)) / (np.linalg.norm(b) * np.linalg.norm(y)))
        return float(best)
    D2 = np.diag(E.T @ E)  # contragredient of the (non-orthonormal) even basis
    siegel_defect = [polar_defect(np.conj(D2 * img(True))) for _ in range(4)]
    generic_defect = [polar_defect(np.conj(D2 * img(False))) for _ in range(4)]
    # genus 3 (T6/Z3)
    O3 = lattice(4)
    Z = rand_Z(rng, n=3, ymin=1.0, yscale=6.0)
    t0, t1 = theta3(Z, O3), theta3(-np.linalg.inv(Z), lattice(6))
    pred = np.linalg.det(Z / 1j) * (fourier(3) @ t0)
    g3_err = float(np.max(abs(t1 - pred)) / np.max(abs(t1)))
    ms3 = list(itertools.product(range(3), repeat=3))
    even3 = len({min(m, tuple((-x) % 3 for x in m)) for m in ms3})
    sp63 = sp6_order()
    return dict(group_on_even5_linear_order=len(G5), jacobian_real_rank=jac_rank, invariant_quartics=n_quartic,
                invariant_dims=dims, siegel_slice_ranks=sym_ranks, dual_burkhardt_defect_siegel=siegel_defect,
                dual_burkhardt_defect_generic=generic_defect, genus3_inversion_rel_err=g3_err,
                genus3_even_functions=even3, sp63_order=sp63)


def sp6_order():
    def T(Bs):
        M = np.eye(6, dtype=int)
        M[:3, 3:] = Bs
        return M % 3

    def L(A, Ai):
        M = np.zeros((6, 6), int)
        M[:3, :3], M[3:, 3:] = A, np.array(Ai).T
        return M % 3
    Jm = np.zeros((6, 6), int)
    Jm[:3, 3:], Jm[3:, :3] = np.eye(3, dtype=int), -np.eye(3, dtype=int)
    gens = [Jm % 3, T(np.diag([1, 0, 0])), T(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]])),
            L([[1, 1, 0], [0, 1, 0], [0, 0, 1]], [[1, 2, 0], [0, 1, 0], [0, 0, 1]]),
            L([[0, 1, 0], [0, 0, 1], [1, 0, 0]], [[0, 0, 1], [1, 0, 0], [0, 1, 0]]),
            L([[2, 0, 0], [0, 1, 0], [0, 0, 1]], [[2, 0, 0], [0, 1, 0], [0, 0, 1]])]
    for g in gens:
        assert ((g.T @ Jm @ g - Jm) % 3 == 0).all()
    vecs = [v for v in itertools.product(range(3), repeat=6) if any(v)]
    ix = {v: i for i, v in enumerate(vecs)}
    return int(PermutationGroup([Permutation([ix[tuple((M @ np.array(v)) % 3)] for v in vecs]) for M in gens]).order())


def main():
    rng = np.random.default_rng(11897)
    a = part_11897(rng)
    b = part_11898(rng)
    res = dict(pass_id=[11897, 11898], part_11897=a, part_11898={k: (v if not isinstance(v, dict) else
                                                                    {str(kk): vv for kk, vv in v.items()})
                                                                for k, v in b.items()})
    res["checks"] = {k: bool(v) for k, v in dict(
        inversion_weight_one_fourier=max(a["inversion_rel_err"]) < 1e-9,
        translations_phase_gates=max(a["translation_rel_err"].values()) < 1e-9,
        gl2_permutes_fixed_points=a["gl2_perm_rel_err"] < 1e-9,
        odd_part_vanishes=a["even_rel_err"] < 1e-12,
        projective_group_51840=a["projective_order_full"] == 51840,
        isomorphic_to_sp43=a["symplectic_image_order"] == 51840 and a["symplectic_preserves_form"],
        linear_order_103680=a["linear_order"] == 103680,
        diagonal_moduli_only_576=a["projective_order_diagonal_moduli"] == 576,
        w33_srg_40_12_2_4=a["w33_points"] == 40 and a["w33_degree"] == 12 and a["w33_eigenvalues"] == [-4.0, 2.0, 12.0],
        thetas_dominant_onto_P4=b["jacobian_real_rank"] == 8,
        unique_invariant_quartic=b["invariant_quartics"] == 1,
        invariant_dims=[b["invariant_dims"][d] for d in (4, 6, 8, 10, 12, 14, 16, 18)] == [1, 1, 1, 2, 3, 2, 4, 5],
        siegel_slice_first_relation_degree_18=all(b["siegel_slice_ranks"][d] == b["invariant_dims"][d]
                                                  for d in (4, 6, 8, 10, 12, 14, 16))
        and b["siegel_slice_ranks"][18] == 4,
        siegel_slice_in_dual_burkhardt=max(b["dual_burkhardt_defect_siegel"]) < 1e-12,
        generic_kahler_not_in_dual_burkhardt=min(b["dual_burkhardt_defect_generic"]) > 1e-5,
        genus3_inversion=b["genus3_inversion_rel_err"] < 1e-8,
        genus3_14_even=b["genus3_even_functions"] == 14,
        sp63_order=b["sp63_order"] == 9170703360,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
