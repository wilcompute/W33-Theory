"""Passes 11879-11883: the Siegel modulus of W(3,3) is the flat direction of an E8 Higgs field.

E8 = sl9 + Lambda^3 C^9 + Lambda^6 C^9 for two qutrits (Pass 11681); the 84 = Lambda^3 C^9 is the Z3-twisted (W(3,3)
twist) matter of E8, its Vinberg Cartan subspace h = C^4 is the odd Weil module "Di" (Passes 11680/11699), and the GSW
Coble covariant maps h to the Burkhardt quartic by Maschke's quartics (Pass 11699).

  * 11879 WEIERSTRASS. For a genus-2 modulus Omega, the six odd half-integer characteristics give six level-3
    theta-null vectors theta[c/3 + alpha, beta](0, 3 Omega); after the Pauli twist diag(w^{c.2beta}) they lie exactly in
    the odd Weil 4 = h, and their Maschke image is the Coble point of the even theta-null of Omega. The ten even
    characteristics do not. Conversely every random Cartan point is (projectively) an odd theta-null of a torus whose
    Coble point is its Maschke image. So h = P^3 is the moduli of level-3 genus-2 curves WITH A WEIERSTRASS POINT, the
    6:1 Maschke map forgets it (degree 6: Bruin-Filatov 2022, here with explicit theta functions), and Di = the odd
    spin structures, the ones that carry Dirac zero modes.
  * 11880 SU(9) BROKEN BY THE 84. A generic Cartan vev has zero stabiliser Lie algebra in gl(9): SU(9) is broken to a
    finite group, which contains the two-qutrit Pauli group exactly (and omega I; zeta_9 I is broken). W(3,3) is the
    commutation geometry of the unbroken discrete gauge group. At each of the 40 Witting rays (E8 root rays = W(3,3)
    points) the stabiliser is 24-dimensional of rank 6 with no centre: SU(3)^3, trinification.
  * 11881 THE RENORMALIZABLE POTENTIAL. Sym^2(84) has exactly two quartic SU(9) invariants, (tr rho)^2 and tr rho^2,
    rho = x x^dagger (contraction over two indices). tr rho^2 >= (tr rho)^2 / 9 with equality iff rho ~ I, which holds at
    every Cartan point (all 40 Witting rays included): for lambda2 > 0 the vacuum manifold is the Kempf-Ness set
    mu^{-1}(0) = SU(9) . h, locally of real dimension 88 = 80 + 8 (orbit + Cartan). For lambda2 < 0 the vacuum is a
    decomposable trivector, ratio 1/3: u(9) stabiliser of dimension 44 = su(3) + su(6) + u(1)', the u(1)' a
    combination of an SU(9) generator with the accidental phase symmetry of the renormalizable potential.
  * 11882 FLAT TO ALL RENORMALIZABLE ORDERS. The normaliser acts on h by the Witting group; its lowest holomorphic
    invariant has degree 12 (none in degrees 1..11, one in 12; the scratch run to degree 18 finds one in 18, the
    Vinberg-Elashvili degrees 12, 18, 24, 30): the genus-2 modulus and the phase of x are lifted only by
    dimension-12 operators.
  * 11883 synthesis in PASS11879_11883_E8_HIGGS_SIEGEL_MODULUS.md.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402
from w33_pass11869_11873_siegel_level3_two_qutrits import IDX, rand_Om, theta_null_2  # noqa: E402

OUT = ROOT / "data" / "w33_pass11879_11883_e8_higgs_siegel_modulus.json"
W = np.exp(2j * np.pi / 3)
C2 = [(a, b) for a in range(3) for b in range(3)]
DIRS = [(0, 1), (1, 0), (1, 1), (1, 2)]
H = np.array(E.cartan_trivectors())
LINES = {d: {tuple(sorted((a, ((a[0] + d[0]) % 3, (a[1] + d[1]) % 3), ((a[0] - d[0]) % 3, (a[1] - d[1]) % 3))))
             for a in C2} for d in DIRS}
GL9 = [np.eye(9)[:, [i]] @ np.eye(9)[[j], :] for i in range(9) for j in range(9)]


def witting_rays():
    rays = [np.eye(4, dtype=complex)[i] for i in range(4)]
    for i, j in itertools.product(range(3), repeat=2):
        rays += [np.array([0, 1, W ** i, W ** j]), np.array([1, 0, W ** i, -W ** j]),
                 np.array([1, -W ** i, 0, W ** j]), np.array([1, W ** i, -W ** j, 0])]
    return rays


# ------------------------------------------------------------------ Coble / Maschke (Pass 11663 basis)
def coble_gradients(x):
    G = np.zeros((9, 5), complex)
    for a in C2:
        G[IDX[a], 0] += x[IDX[a]] ** 2 / 2
    for k, d in enumerate(DIRS):
        for L in LINES[d]:
            i, j, l = [IDX[t] for t in L]
            G[i, k + 1] += x[j] * x[l]
            G[j, k + 1] += x[i] * x[l]
            G[l, k + 1] += x[i] * x[j]
    return G


def coble_point(x):
    _, s, Vh = np.linalg.svd(coble_gradients(x / np.linalg.norm(x)))
    b = Vh[-1].conj()
    return b / np.linalg.norm(b), s[-1] / s[0]


def maschke(c):
    a, b, cc, d = c
    return -2 * np.array([-12 * a * b * cc * d, 2 * a * (b ** 3 + cc ** 3 + d ** 3), 2 * b * (-a ** 3 - cc ** 3 + d ** 3),
                          2 * cc * (-a ** 3 + b ** 3 - d ** 3), 2 * d * (-a ** 3 - b ** 3 + cc ** 3)])


def burkhardt(y):
    return (y[1] * y[2] * y[3] * y[4] + y[0] * np.sum(y[1:] ** 3) / 6 + y[0] ** 4 / 48) / np.linalg.norm(y) ** 4


def theta_char(Om, al, be, N=16):
    n = np.arange(-N, N + 1)
    n1, n2 = np.meshgrid(n, n, indexing="ij")
    out = []
    for c1, c2 in C2:
        v1, v2 = n1 + c1 / 3 + al[0], n2 + c2 / 3 + al[1]
        Qf = Om[0, 0] * v1 * v1 + 2 * Om[0, 1] * v1 * v2 + Om[1, 1] * v2 * v2
        out.append(np.sum(np.exp(3j * np.pi * Qf + 2j * np.pi * (v1 * be[0] + v2 * be[1]))))
    return np.array(out)


CHARS = [(al, be) for al in itertools.product((0, 0.5), repeat=2) for be in itertools.product((0, 0.5), repeat=2)]
NEG = [IDX[((-a) % 3, (-b) % 3)] for a, b in C2]


def untwisted(Om, al, be):
    p = theta_char(Om, al, be)
    bp = 2 * np.array(be)
    u = np.array([W ** (c1 * bp[0] + c2 * bp[1]) for c1, c2 in C2]) * p
    return u


def proj_match(a, b):
    a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
    return abs(abs(np.vdot(a, b)) - 1)


def part_weierstrass(rng):
    rows = []
    for _ in range(3):
        Om = rand_Om(rng)
        beta, _ = coble_point(theta_null_2(Om))
        odd, even, odd_pts = [], [], []
        for al, be in CHARS:
            u = untwisted(Om, al, be)
            c = np.array([u[IDX[a]] for a in DIRS])
            m = proj_match(maschke(c), beta)
            if int(round(4 * np.dot(al, be))) % 2:
                odd.append(dict(oddness=float(np.max(abs(u + u[NEG])) / np.max(abs(u))), maschke_vs_coble=float(m)))
                odd_pts.append(c / np.linalg.norm(c))
            else:
                even.append(float(m))
        distinct = min(1 - abs(np.vdot(odd_pts[i], odd_pts[j])) for i in range(6) for j in range(i + 1, 6))
        rows.append(dict(burkhardt_residual=float(abs(burkhardt(beta))), odd=odd, even_min_mismatch=min(even),
                         odd_points_pairwise_min_separation=float(distinct)))
    inverse = []

    def unpack(p):
        X = np.array([[p[0], p[1]], [p[1], p[2]]])
        L = np.array([[p[3], 0], [p[4], p[5]]])
        return X + 1j * (L @ L.T + 0.05 * np.eye(2))
    for _ in range(3):
        c = rng.normal(size=4) + 1j * rng.normal(size=4)
        q = maschke(c) / np.linalg.norm(maschke(c))
        best = None
        for _ in range(30):
            def res(p):
                b, _ = coble_point(theta_null_2(unpack(p), N=12))
                ph = np.vdot(b, q) / abs(np.vdot(b, q))
                r = q - ph * b
                return np.concatenate([r.real, r.imag])
            r = least_squares(res, np.concatenate([rng.uniform(-0.5, 0.5, 3), rng.uniform(0.6, 1.3, 3)]),
                              xtol=1e-14, ftol=1e-14)
            if best is None or r.cost < best.cost:
                best = r
            if best.cost < 1e-22:
                break
        Om = unpack(best.x)
        dist = min(proj_match(np.array([untwisted(Om, al, be)[IDX[a]] for a in DIRS]), c)
                   for al, be in CHARS if int(round(4 * np.dot(al, be))) % 2)
        inverse.append(dict(coble_fit_residual=float(np.sqrt(2 * best.cost)), c_vs_nearest_odd_theta=float(dist)))
    return dict(forward=rows, inverse=inverse)


# ------------------------------------------------------------------ stabilisers in gl(9) and u(9)
def stab_dim_gl(T):
    M = np.array([E._act(A, T).ravel() for A in GL9]).T
    s = np.linalg.svd(M, compute_uv=False)
    return int(np.sum(s < 1e-9 * s[0]))


def stab_algebra(T):
    M = np.array([E._act(A, T).ravel() for A in GL9]).T
    _, s, Vh = np.linalg.svd(M)
    null = Vh[int(np.sum(s > 1e-9 * s[0])):]
    return [(v.conj() @ np.array(GL9).reshape(81, 81)).reshape(9, 9) for v in null]


def algebra_rank_center(B, rng):
    Bf = np.array([b.ravel() for b in B])
    g = sum(rng.normal() * b for b in B)

    def coords(m):
        return np.linalg.lstsq(Bf.T, m.ravel(), rcond=None)[0]
    ad = np.array([coords(g @ b - b @ g) for b in B]).T
    rank = int(np.sum(np.linalg.svd(ad, compute_uv=False) < 1e-8))
    Cm = np.vstack([np.array([coords(b @ a - a @ b) for b in B]).T for a in B])
    center = int(np.sum(np.linalg.svd(Cm, compute_uv=False) < 1e-8))
    return rank, center


def unitary_stab_dim(T):
    basis = []
    for i in range(9):
        for j in range(9):
            if i == j:
                A = np.zeros((9, 9), complex)
                A[i, i] = 1j
                basis.append(A)
            elif i < j:
                A = np.zeros((9, 9), complex)
                A[i, j], A[j, i] = 1, -1
                basis.append(A)
                A = np.zeros((9, 9), complex)
                A[i, j], A[j, i] = 1j, 1j
                basis.append(A)
    M = np.array([np.concatenate([E._act(A, T).real.ravel(), E._act(A, T).imag.ravel()]) for A in basis]).T
    s = np.linalg.svd(M, compute_uv=False)
    return int(np.sum(s < 1e-9 * s[0]))


def part_breaking(rng):
    c = rng.normal(size=4) + 1j * rng.normal(size=4)
    T = E.full(c @ H)
    X1, Z1 = E.X1, E.Z1
    paulis = [np.kron(X1, np.eye(3)), np.kron(np.eye(3), X1), np.kron(Z1, np.eye(3)), np.kron(np.eye(3), Z1)]

    def act(g, T):
        return np.einsum("ai,bj,ck,ijk->abc", g, g, g, T)
    pauli_fix = max(float(np.max(abs(act(g, T) - T))) for g in paulis)
    z9 = np.exp(2j * np.pi / 9)
    witt = []
    for r in witting_rays():
        Tr = E.full(r @ H)
        witt.append(stab_dim_gl(Tr))
    B = stab_algebra(E.full(witting_rays()[0] @ H))
    rank, center = algebra_rank_center(B, rng)
    return dict(generic_stabiliser_dim=stab_dim_gl(T), random_84_stabiliser_dim=stab_dim_gl(E.full(rng.normal(size=84) + 1j * rng.normal(size=84))),
                pauli_generators_fix_vev=pauli_fix, pauli_dets=[float(abs(np.linalg.det(g))) for g in paulis],
                omega_I_fixes=float(np.max(abs(act(W * np.eye(9), T) - T))),
                zeta9_I_moves=float(np.max(abs(act(z9 * np.eye(9), T) - T))),
                witting_stabiliser_dims=sorted(set(witt)), witting_count=len(witt),
                witting_algebra_rank=rank, witting_algebra_center=center,
                witting_unitary_stabiliser_dim=unitary_stab_dim(E.full(witting_rays()[0] @ H)),
                generic_unitary_stabiliser_dim=unitary_stab_dim(T))


# ------------------------------------------------------------------ potential
def rho_of(T):
    return np.einsum("acd,bcd->ab", T, T.conj())


def quartic_candidates(x):
    T = E.full(x)
    rho = rho_of(T)
    M = np.einsum("abe,cde->abcd", T, T.conj()).reshape(81, 81)
    return np.array([np.trace(rho).real ** 2, np.trace(rho @ rho).real, np.linalg.norm(M) ** 2, np.trace(M @ M).real])


def ratio_of(T):
    rho = rho_of(T)
    return float(np.trace(rho @ rho).real / np.trace(rho).real ** 2)


def part_potential(rng):
    X = np.array([quartic_candidates(rng.normal(size=84) + 1j * rng.normal(size=84)) for _ in range(30)])
    sv = np.linalg.svd(X, compute_uv=False)
    n_quartic = int(np.sum(sv > 1e-9 * sv[0]))
    cart = [ratio_of(E.full((rng.normal(size=4) + 1j * rng.normal(size=4)) @ H)) for _ in range(5)]
    witt = [ratio_of(E.full(r @ H)) for r in witting_rays()]
    rnd = [ratio_of(E.full(rng.normal(size=84) + 1j * rng.normal(size=84))) for _ in range(5)]
    c = rng.normal(size=4) + 1j * rng.normal(size=4)
    x0 = c @ H
    p0 = np.concatenate([x0.real, x0.imag])

    def mu(p):
        x = p[:84] + 1j * p[84:]
        rho = rho_of(E.full(x))
        m = rho - np.trace(rho) / 9 * np.eye(9)
        return np.concatenate([m.real.ravel(), m.imag.ravel()])
    J = np.array([(mu(p0 + 1e-6 * e) - mu(p0 - 1e-6 * e)) / 2e-6 for e in np.eye(168)]).T
    rank_mu = int(np.sum(np.linalg.svd(J, compute_uv=False) > 1e-6 * np.linalg.norm(J, 2)))
    Td = np.zeros((9, 9, 9), complex)
    for pm in itertools.permutations(range(3)):
        Td[tuple(pm)] = np.linalg.det(np.eye(3)[list(pm)])
    return dict(independent_quartic_invariants=n_quartic, cartan_ratio_minus_ninth=max(abs(v - 1 / 9) for v in cart),
                witting_ratio_minus_ninth=max(abs(v - 1 / 9) for v in witt), random_ratio_min=min(rnd),
                moment_map_rank=rank_mu, kempf_ness_local_dim=168 - rank_mu,
                decomposable_ratio=ratio_of(Td), decomposable_unitary_stabiliser_dim=unitary_stab_dim(Td))


# ------------------------------------------------------------------ holomorphic invariants on the Cartan
def cartan_action(g):
    g = g / np.linalg.det(g) ** (1 / 9)
    cols = []
    for u in range(4):
        y = E.sorted_c(np.einsum("ai,bj,ck,ijk->abc", g, g, g, E.full(H[u])))
        cvec = np.linalg.lstsq(H.T, y, rcond=None)[0]
        assert np.allclose(H.T @ cvec, y, atol=1e-10)
        cols.append(cvec)
    return np.array(cols).T


def part_invariants(rng, dmax=12):
    F = np.array([[W ** (a * b) for b in range(3)] for a in range(3)]) / np.sqrt(3)
    D = np.diag([1, 1, W])
    I3 = np.eye(3)
    gens = [cartan_action(g) for g in (np.kron(F, I3), np.kron(I3, F), np.kron(D, I3), np.kron(I3, D),
                                       np.diag([W ** (a * b) for a, b in C2]))]
    counts = {}
    for d in range(1, dmax + 1):
        mons = list(itertools.combinations_with_replacement(range(4), d))
        n = len(mons)
        Z = rng.normal(size=(n + 20, 4)) + 1j * rng.normal(size=(n + 20, 4))

        def V(Zs):
            return np.array([[np.prod(z[list(m)]) for m in mons] for z in Zs])
        V0 = V(Z)
        rows = [V(Z @ np.linalg.inv(g).T) - V0 for g in gens]
        A = np.vstack(rows)
        sv = np.linalg.svd(A / np.linalg.norm(V0), compute_uv=False)
        counts[d] = int(np.sum(sv < 1e-9 * sv[0]))
    return dict(invariant_counts_by_degree=counts)


def main():
    rng = np.random.default_rng(11879)
    res = dict(pass_ids=[11879, 11880, 11881, 11882, 11883])
    res["11879_weierstrass"] = part_weierstrass(rng)
    res["11880_breaking"] = part_breaking(rng)
    res["11881_potential"] = part_potential(rng)
    res["11882_invariants"] = part_invariants(rng)
    w, b, p, iv = (res[k] for k in ("11879_weierstrass", "11880_breaking", "11881_potential", "11882_invariants"))
    cnt = iv["invariant_counts_by_degree"]
    res["checks"] = {k: bool(v) for k, v in dict(
        coble_on_burkhardt=all(r["burkhardt_residual"] < 1e-12 for r in w["forward"]),
        six_odd_thetas_are_odd_and_map_to_coble=all(o["oddness"] < 1e-12 and o["maschke_vs_coble"] < 1e-12
                                                     for r in w["forward"] for o in r["odd"]),
        ten_even_fail=all(r["even_min_mismatch"] > 1e-6 for r in w["forward"]),
        six_points_distinct=all(r["odd_points_pairwise_min_separation"] > 1e-6 for r in w["forward"]),
        every_cartan_point_is_an_odd_theta=all(r["coble_fit_residual"] < 1e-10 and r["c_vs_nearest_odd_theta"] < 1e-10
                                               for r in w["inverse"]),
        generic_vev_breaks_su9_to_finite=b["generic_stabiliser_dim"] == 0 and b["random_84_stabiliser_dim"] == 0
        and b["generic_unitary_stabiliser_dim"] == 0,
        pauli_group_unbroken=b["pauli_generators_fix_vev"] < 1e-12 and b["omega_I_fixes"] < 1e-12 and b["zeta9_I_moves"] > 1,
        witting_rays_trinification=b["witting_stabiliser_dims"] == [24] and b["witting_count"] == 40
        and b["witting_algebra_rank"] == 6 and b["witting_algebra_center"] == 0 and b["witting_unitary_stabiliser_dim"] == 24,
        two_quartic_invariants=p["independent_quartic_invariants"] == 2,
        cartan_saturates_bound=p["cartan_ratio_minus_ninth"] < 1e-12 and p["witting_ratio_minus_ninth"] < 1e-12
        and p["random_ratio_min"] > 1 / 9 + 1e-3,
        kempf_ness_dim_88=p["kempf_ness_local_dim"] == 88,
        negative_branch_su3_su6=abs(p["decomposable_ratio"] - 1 / 3) < 1e-12 and p["decomposable_unitary_stabiliser_dim"] == 44,
        lowest_holomorphic_invariant_degree_12=all(cnt[d] == 0 for d in range(1, 12)) and cnt[12] == 1,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(res["checks"], indent=1))
    print("invariant counts", cnt)
    print("all", res["all_checks_pass"])


if __name__ == "__main__":
    main()
