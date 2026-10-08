"""Pass 11681: E8 built from two qutrits -- sl(9) of two-qutrit operators plus three-fermion creation and annihilation;
the Pauli-singlet trivectors are a Cartan subalgebra; the roots, read there, are the Witting polytope with W(3,3) as
orthogonality graph.

CONSTRUCTION.  V = C^9 = two qutrits.  e8 = sl(V) + Lambda^3 V + Lambda^3 V* with
  [A, B] = AB - BA,  [A, x] = A.x,  [A, xi] = -A^T.xi,  [x, y] = *(x ^ y),  [xi, eta] = *(xi ^ eta),
  [x, xi] = gamma (x . xi)_traceless   (contraction over two indices).
The Jacobi identity fixes gamma = -1 and then holds on all 27 type-triples.  (Classical: Kac's Z3-grading of E8 with grade-0
part sl9; the Pauli grading of sl9 is Pass 2026-09-15.)
FOUND.
  * The Pauli group acts by automorphisms (conjugation on sl9, P(x)P(x)P on Lambda^3).  Its fixed subalgebra
    h = (Lambda^3 V)^Heis + (Lambda^3 V*)^Heis is spanned by the four trivectors T_u - T_(-u) of Pass 11680 (the four
    parallel classes of AG(2,3): Vinberg-Elashvili's Cartan subspace) and their duals; it is 8-dim and ABELIAN, and ad(h)
    for generic h has exactly 8 zero and 240 distinct nonzero eigenvalues: a Cartan subalgebra.
  * Every nonzero Pauli degree v in F3^4 carries exactly 3 roots (80 x 3 = 240); degree 0 is h.
  * Restricted to the 4-dim trivector half (the Pauli-singlet THREE-FERMION states) the 240 roots have norm sqrt3 and
    form exactly 40 rays x 6 Eisenstein phases with overlaps {0, 1/3}: the WITTING configuration.  Each ray is one
    projective Pauli point (a point of W(3,3)); two rays are orthogonal iff the Paulis commute.  The repository's 6:1
    fibration E8 roots -> W(3,3) (Pass 1021) is the reading of the two-qutrit E8 roots on its Pauli-singlet Cartan.
  * The Clifford gates act on the trivector Cartan with a linear image of order 103680 containing 4 scalars: projectively
    PSp(4,3), the projective Witting group, with no complex reflections (the order-3 reflections of G32 = mu6.PSp(4,3) are
    Weyl-group elements outside the Clifford image).
  * Codex's Hilbert-space Witting rays (odd parts of Pauli projectors, Pass 11663) form a Witting configuration with the
    same labels and orthogonality; the naive basis map T_u - T_(-u) -> |u> - |-u> matches only 14 of 40 rays, so the two are
    related by an antilinear intertwiner (the representations are conjugate), which is not constructed here.
  * TIME REVERSAL: the structure constants are real, so complex conjugation of the two-qutrit amplitudes is an antilinear
    automorphism (checked); its real form sl(9,R) + Lambda^3 R^9 + Lambda^3 R^9* has invariant form of signature
    (44 + 84, 36 + 84) = (128, 120): the split real form E8(8).
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
OUT = ROOT / "data" / "w33_pass11681_e8_from_two_qutrits.json"

TR = list(itertools.combinations(range(9), 3))
TI = {t: i for i, t in enumerate(TR)}
GAMMA = -1.0
W3 = np.exp(2j * np.pi / 3)
X1 = np.roll(np.eye(3), 1, axis=0)
Z1 = np.diag([1, W3, W3 * W3])
PTS = list(itertools.product(range(3), repeat=2))
IDX = {p: 3 * p[0] + p[1] for p in PTS}
DIRS = [(0, 1), (1, 0), (1, 1), (1, 2)]


def psign(seq):
    s = 1
    seq = list(seq)
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                s = -s
    return s


def full(c):
    T = np.zeros((9, 9, 9), complex)
    for (i, j, k), v in zip(TR, c):
        for p in itertools.permutations(range(3)):
            t = (i, j, k)
            T[tuple(t[p[m]] for m in range(3))] = psign(p) * v
    return T


def sorted_c(T):
    return np.array([T[t] for t in TR])


def wedge_star(c1, c2):
    """*(x ^ y) for 3-forms given by sorted coefficients"""
    out = np.zeros(84, complex)
    for S in itertools.combinations(range(9), 6):
        tot = 0
        for T in itertools.combinations(S, 3):
            Tc = tuple(x for x in S if x not in T)
            tot += psign(T + Tc) * c1[TI[T]] * c2[TI[Tc]]
        C = tuple(x for x in range(9) if x not in S)
        out[TI[C]] += psign(S + C) * tot
    return out


def _act(A, T):
    return np.einsum("ad,dbc->abc", A, T) + np.einsum("bd,adc->abc", A, T) + np.einsum("cd,abd->abc", A, T)


def _dact(A, S):
    return -(np.einsum("da,dbc->abc", A, S) + np.einsum("db,adc->abc", A, S) + np.einsum("dc,abd->abc", A, S))


def bracket(a, b, gam=GAMMA):
    A1, x1, k1 = a
    A2, x2, k2 = b
    T1, T2, S1, S2 = full(x1), full(x2), full(k1), full(k2)
    x = sorted_c(_act(A1, T2) - _act(A2, T1)) + wedge_star(k1, k2)
    k = sorted_c(_dact(A1, S2) - _dact(A2, S1)) + wedge_star(x1, x2)
    M = np.einsum("iab,jab->ij", T1, S2) / 2 - np.einsum("iab,jab->ij", T2, S1) / 2
    M = M - np.trace(M) / 9 * np.eye(9)
    return (A1 @ A2 - A2 @ A1 + gam * M, x, k)


def _zero():
    return (np.zeros((9, 9), complex), np.zeros(84, complex), np.zeros(84, complex))


def _rnd(rng, kind):
    A, x, k = _zero()
    if kind == "A":
        A = rng.normal(size=(9, 9)) + 1j * rng.normal(size=(9, 9))
        A -= np.trace(A) / 9 * np.eye(9)
    elif kind == "x":
        x = rng.normal(size=84) + 1j * rng.normal(size=84)
    else:
        k = rng.normal(size=84) + 1j * rng.normal(size=84)
    return (A, x, k)


def _vec(e):
    return np.concatenate([e[0].ravel(), e[1], e[2]])


def _add(*es):
    return (sum(e[0] for e in es), sum(e[1] for e in es), sum(e[2] for e in es))


def jacobi_certificate(rng):
    a, b, c = _rnd(rng, "x"), _rnd(rng, "x"), _rnd(rng, "k")
    jac = lambda g: _vec(_add(bracket(bracket(a, b, g), c, g), bracket(bracket(b, c, g), a, g),  # noqa: E731
                              bracket(bracket(c, a, g), b, g)))
    r0 = jac(0.0)
    r1 = jac(1.0) - r0
    gam = -np.vdot(r1, r0) / np.vdot(r1, r1)
    worst = 0.0
    for kinds in itertools.product("Axk", repeat=3):
        a, b, c = (_rnd(rng, kd) for kd in kinds)
        worst = max(worst, float(np.abs(_vec(_add(bracket(bracket(a, b), c), bracket(bracket(b, c), a),
                                                   bracket(bracket(c, a), b)))).max()))
    return complex(gam), worst


def cartan_trivectors():
    add = lambda a, b, s=1: tuple((x + s * y) % 3 for x, y in zip(a, b))  # noqa: E731

    def T_u(u):
        T = np.zeros((9, 9, 9), complex)
        for a in PTS:
            T[IDX[a], IDX[add(a, u)], IDX[add(a, u, -1)]] = 1
        return T
    return [sorted_c(T_u(u) - T_u(tuple((-x) % 3 for x in u))) for u in DIRS]


def e8_basis():
    sl = []
    for i in range(9):
        for j in range(9):
            if i != j:
                M = np.zeros((9, 9), complex)
                M[i, j] = 1
                sl.append(M)
    for k in range(8):
        M = np.zeros((9, 9), complex)
        M[k, k], M[k + 1, k + 1] = 1, -1
        sl.append(M)
    Sl = np.array([m.ravel() for m in sl]).T
    Z84 = np.zeros(84, complex)
    Z9 = np.zeros((9, 9), complex)
    basis = ([(m, Z84, Z84) for m in sl] + [(Z9, np.eye(84)[i].astype(complex), Z84) for i in range(84)]
             + [(Z9, Z84, np.eye(84)[i].astype(complex)) for i in range(84)])
    return basis, Sl, np.linalg.pinv(Sl)


def pauli(v):
    return np.kron(np.linalg.matrix_power(X1, v[0]) @ np.linalg.matrix_power(Z1, v[1]),
                   np.linalg.matrix_power(X1, v[2]) @ np.linalg.matrix_power(Z1, v[3]))


def proj(v):
    lead = next(x for x in v if x)
    return tuple((x * lead) % 3 for x in v)


def main():
    rng = np.random.default_rng(11681)
    res = dict(pass_id=11681)
    gam, worst = jacobi_certificate(rng)
    res["gamma_from_jacobi"] = [gam.real, gam.imag]
    res["jacobi_max_residual_27_type_triples"] = worst
    hcoef = cartan_trivectors()
    Z9, Z84 = np.zeros((9, 9), complex), np.zeros(84, complex)
    cart = [(Z9, c, Z84) for c in hcoef] + [(Z9, Z84, c) for c in hcoef]
    basis, Sl, Slp = e8_basis()

    def coords(e):
        return np.concatenate([Slp @ e[0].ravel(), e[1], e[2]])
    res["cartan_brackets_max"] = float(max(np.abs(coords(bracket(a, b))).max() for a in cart for b in cart))
    ad = [np.array([coords(bracket(h, b)) for b in basis]).T for h in cart]
    cg = rng.normal(size=8) + 1j * rng.normal(size=8)
    ev, V = np.linalg.eig(sum(c * a for c, a in zip(cg, ad)))
    nz = np.abs(ev) > 1e-6
    res["ad_h_zero_eigenvalues"] = int((~nz).sum())
    res["roots"] = int(nz.sum())
    R = V[:, nz]
    alpha = np.array([[np.vdot(R[:, i], a @ R[:, i]) / np.vdot(R[:, i], R[:, i]) for a in ad] for i in range(R.shape[1])])
    res["distinct_roots"] = len({tuple(np.round(a, 6)) for a in alpha})
    w4 = alpha[:, :4]
    nrm = np.linalg.norm(w4, axis=1)
    res["trivector_restriction_norms"] = sorted(set(np.round(nrm, 6).tolist()))
    U = w4 / nrm[:, None]
    rays = []
    for u in U:
        if not any(abs(abs(np.vdot(u, r)) - 1) < 1e-6 for r in rays):
            rays.append(u)
    rays = np.array(rays)
    G = np.abs(rays.conj() @ rays.T) ** 2
    res["witting_rays"] = len(rays)
    res["ray_overlaps"] = sorted(set(np.round(G[~np.eye(len(rays), dtype=bool)], 6).tolist()))
    # Pauli degrees
    gensP = [np.kron(X1, np.eye(3)), np.kron(Z1, np.eye(3)), np.kron(np.eye(3), X1), np.kron(np.eye(3), Z1)]

    def pauli_act(D, e):
        A, x, k = e
        Dc = D.conj()
        return (D @ A @ D.conj().T, sorted_c(np.einsum("ai,bj,ck,ijk->abc", D, D, D, full(x))),
                sorted_c(np.einsum("ai,bj,ck,ijk->abc", Dc, Dc, Dc, full(k))))
    deg = []
    for i in range(240):
        e = ((Sl @ R[:80, i]).reshape(9, 9), R[80:164, i], R[164:, i])
        v = []
        for D in gensP:
            f = coords(pauli_act(D, e))
            lam = np.vdot(R[:, i], f) / np.vdot(R[:, i], R[:, i])
            assert np.allclose(f, lam * R[:, i], atol=1e-8)
            v.append(int(round(np.angle(lam) / (2 * np.pi / 3))) % 3)
        deg.append(tuple(v))
    cnt = Counter(deg)
    res["roots_per_pauli_degree"] = sorted(set(cnt.values()))
    res["pauli_degrees_carrying_roots"] = len(cnt)
    ray_of = [next(j for j, r in enumerate(rays) if abs(abs(np.vdot(U[i], r)) - 1) < 1e-6) for i in range(240)]
    res["each_ray_one_w33_point"] = all(len({proj(deg[i]) for i in range(240) if ray_of[i] == j}) == 1 for j in range(40))
    pt = [next(proj(deg[i]) for i in range(240) if ray_of[i] == j) for j in range(40)]
    res["distinct_w33_points"] = len(set(pt))
    om = lambda a, b: (a[0] * b[1] - a[1] * b[0] + a[2] * b[3] - a[3] * b[2]) % 3  # noqa: E731
    res["orthogonal_iff_paulis_commute"] = int(sum((G[i, j] < 1e-9) == (om(pt[i], pt[j]) == 0)
                                                   for i in range(40) for j in range(40) if i != j))
    ph = Counter()
    for j in range(40):
        vs = [w4[i] for i in range(240) if ray_of[i] == j]
        for x in vs:
            ph[round(float(np.angle(np.vdot(vs[0], x) / np.vdot(vs[0], vs[0])) / (np.pi / 3))) % 6] += 1
    res["phases_per_ray_units_pi_over_3"] = {str(k): v for k, v in sorted(ph.items())}
    # Clifford image on the trivector Cartan
    import w33_pass11651_n_qutrit_hesse_space as H
    _, _, _, _, wg = H.setup(2)
    Hc = np.array(hcoef).T / np.linalg.norm(np.array(hcoef).T, axis=0)
    act3 = lambda g, c: sorted_c(np.einsum("ai,bj,ck,ijk->abc", g, g, g, full(c)))  # noqa: E731
    Rm = [Hc.conj().T @ np.array([act3(g, Hc[:, j]) for j in range(4)]).T for g in wg.values()]
    Gc = H.closure(Rm, cap=400000)
    res["clifford_image_order_on_trivector_cartan"] = len(Gc)
    res["clifford_image_scalars"] = int(sum(np.allclose(M, M[0, 0] * np.eye(4)) for M in Gc))
    res["clifford_image_reflections"] = int(sum(H.is_reflection(M) for M in Gc))
    # Codex 11663 comparison (naive basis map)
    oddb = np.array([(np.eye(9)[IDX[u]] - np.eye(9)[IDX[tuple((-x) % 3 for x in u)]]) / np.sqrt(2) for u in DIRS]).T
    P40 = [v for v in itertools.product(range(3), repeat=4) if any(v) and next(x for x in v if x) == 1]
    hil = {}
    for v in P40:
        Dv = pauli(v)
        O = oddb.conj().T @ ((np.eye(9) + Dv + Dv.conj().T) / 3) @ oddb
        e_, V_ = np.linalg.eigh((O + O.conj().T) / 2)
        hil[v] = V_[:, np.argmax(e_)]
    res["codex_rays_matching_root_rays_naive_map"] = int(sum(
        any(abs(abs(np.vdot(hil[v], r / np.linalg.norm(r))) - 1) < 1e-6 for v in P40) for r in rays))
    # time reversal: componentwise conjugation is an antilinear automorphism
    worst_t = 0.0
    for kinds in itertools.product("Axk", repeat=2):
        a, b = (_rnd(rng, kd) for kd in kinds)
        lhs = _vec(bracket(*[tuple(np.conj(t) for t in e) for e in (a, b)]))
        rhs = np.conj(_vec(bracket(a, b)))
        worst_t = max(worst_t, float(np.abs(lhs - rhs).max()))
    res["conjugation_is_antilinear_automorphism_max_residual"] = worst_t
    res["real_form_signature_of_invariant_form"] = "(44 + 84, 36 + 84) = (128, 120): split E8(8)"
    print(res, flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
