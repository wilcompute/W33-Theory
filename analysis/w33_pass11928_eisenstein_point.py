"""Pass 11928: the Eisenstein point of the flavour torus -- residual Z3 charges, a W(3,3) line of fixed points, and
polynomial hierarchies.

Setting: magnetized SU(5) on T4 with the A2 dual pair (10: A2, 5bar: A2' = 3 A2^{-1}; H_u flux 2 A2, H_d flux 4.1).
At the Eisenstein point Omega = w.1 the rotation rho: z -> w z is a lattice automorphism, and every symmetric flux N
(dx^dy block) is rho-invariant, so rho acts on every zero-mode space.

1. rho acts unitarily on the zero modes (residual ~1e-15). Generation charges (eigenphase / (2 pi/3)): 10 = (0,0,2),
   5bar = (0,0,2); H_u (12 modes) has charges 0,1,2 with multiplicities 3,5,4; H_d (16 modes) 5,5,6.
2. The 9 rho-fixed points form A[1-w] = {(x, -x)} in A[3] = F3^4: a totally isotropic plane, i.e. a LINE of W(3,3),
   which for the A2 pair splits as (L cap K10) + (L cap K5), each one-dimensional.
3. Charges localise at the fixed points: at each fixed point the zero-mode vector is an eigenvector of rho -- it lies
   either along the charge-2 generation (an unbiased, stabiliser-type vector in the mode basis) or inside the charge-0
   plane (value vectors transform by R^T; eigen-residual 2e-15): 3 fixed points carry local charge 0 and 6 carry
   charge 2. Hence point-localised (blow-up) Kahler corrections at the fixed points COMMUTE with the residual Z3: they act
   block-diagonally (charge-0 block + charge-2 line), their traceless image has rank 3, and they can split the degenerate
   charge-0 pair without mixing charges. (A draft read the common eigenvector as a vanishing mode; the fixed-point matrix
   has full rank, so that reading is withdrawn.) Among all 130 planes of A[3], only K(L10) and K(L5) give scalar
   point-source sums (on the 10, resp. the 5bar).
4. Near the point, Omega = w.1 + eps (a + b J), with the Higgs in a fixed Z3-charge sector, the up spectrum scales
   POLYNOMIALLY (log-log slopes):
     Higgs charge 0: m_c/m_t -> O(1) constant,      m_u/m_c ~ eps^2;
     Higgs charge 1: m_c/m_t ~ eps,               m_u/m_c -> O(1) constant;
     Higgs charge 2: m_c/m_t -> 1 - O(eps),        m_u/m_c ~ eps^2.
   (the O(1) constants depend on the Higgs combination inside the charge sector).
   Each Higgs charge gives exactly one hierarchical ratio: the two charge-0 generations cannot be split by the residual
   Z3. Proximity to the Eisenstein point supplies a non-Gaussian (polynomial) hierarchy -- the second hierarchy source
   Pass 11921 requires -- but for one up ratio only.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402

OUT = ROOT / "data" / "w33_pass11928_eisenstein_point.json"
W = np.exp(2j * np.pi / 3)
J = np.array([[0, 1], [1, 0]])
A2, A2M, HU, HD = [[2, 1], [1, 2]], [[2, -1], [-1, 2]], [[4, 2], [2, 4]], [[4, 0], [0, 4]]
OM0 = W * np.eye(2)


def zgrid(Om, G):
    xs = (np.arange(G) + 0.5) / G
    X = np.array(np.meshgrid(xs, xs, xs, xs, indexing="ij")).reshape(4, -1).T
    return X[:, :2] + X[:, 2:] @ Om.T


def modes(N, Om, z):
    M = np.array([F.psi_at(z, j, N, Om) for j in F.chars(N)])
    return M / np.sqrt(np.mean(abs(M) ** 2, axis=1))[:, None]


def rho_matrix(N, G=16):
    z = zgrid(OM0, G)
    M0, M1 = modes(N, OM0, z), modes(N, OM0, W * z)
    return (M0.conj() @ M1.T) / z.shape[0]


def charges(R):
    w = np.linalg.eigvals(R)
    return sorted(int(round(np.angle(x) / (2 * np.pi / 3))) % 3 for x in w)


def omega(p, q):
    return (p[0] * q[2] + p[1] * q[3] - p[2] * q[0] - p[3] * q[1]) % 3


def main():
    F.NS = np.array([(a, b) for a in range(-7, 8) for b in range(-7, 8)])
    res = dict(pass_id=11928)
    Rs = {n: rho_matrix(N) for n, N in (("10", A2), ("5bar", A2M), ("Hu", HU), ("Hd", HD))}
    res["unitarity_residual"] = {n: float(np.linalg.norm(R @ R.conj().T - np.eye(len(R)))) for n, R in Rs.items()}
    res["charges"] = {n: charges(R) for n, R in Rs.items()}
    # fixed points and the W(3,3) line
    rot = lambda p: ((-p[2]) % 3, (-p[3]) % 3, (p[0] - p[2]) % 3, (p[1] - p[3]) % 3)
    pts = list(itertools.product(range(3), repeat=4))
    L = [p for p in pts if rot(p) == p]
    res["fixed_points"] = len(L)
    res["fixed_set_isotropic"] = all(omega(p, q) == 0 for p in L for q in L)
    in_K = lambda p, l: all((np.array(p[:2]) * l[::-1] * np.array([1, -1])).sum() % 3 == 0 for _ in [0]) and \
        all((np.array(p[2:]) * l[::-1] * np.array([1, -1])).sum() % 3 == 0 for _ in [0])
    l10, l5 = np.array([1, 2]), np.array([1, 1])        # mod-3 image lines of A2 and A2' (Pass 11917)
    res["L_cap_K10"] = sum(1 for p in L if in_K(p, l5))       # K10 = l5 x l5
    res["L_cap_K5"] = sum(1 for p in L if in_K(p, l10))       # K5 = l10 x l10

    def vec(N, p):
        x, y = np.array(p[:2]) / 3, np.array(p[2:]) / 3
        z = (x + OM0 @ y)[None, :]
        return np.array([F.psi_at(z, j, N, OM0)[0] for j in F.chars(N)])

    V10 = {p: vec(A2, p) for p in pts}
    V5 = {p: vec(A2M, p) for p in pts}
    w10, U10 = np.linalg.eig(Rs["10"])
    u2 = U10[:, [int(round(np.angle(x) / (2 * np.pi / 3))) % 3 for x in w10].index(2)]
    res["charge2_generation_abs"] = [float(x) for x in abs(u2)]
    R10 = Rs["10"].T          # fixed-point VALUE vectors (psi_b(p))_b transform by R^T: sum_a R_ab psi_a(p) = lambda_p psi_b(p)
    loc = []
    for p in L:
        v = V10[p] / np.linalg.norm(V10[p])
        ev = np.vdot(v, R10 @ v)                    # R acts on coefficient vectors in the mode basis
        resid = np.linalg.norm(R10 @ v - ev * v)
        loc.append((int(round(np.angle(ev) / (2 * np.pi / 3))) % 3, float(resid)))
    res["fixed_point_local_charges"] = sorted(c for c, _ in loc)
    res["fixed_point_eigen_residual"] = max(r for _, r in loc)
    Kb = sum(np.outer(V10[p], V10[p].conj()) * w_ for p, w_ in zip(L, np.random.default_rng(7).normal(size=len(L))))
    res["blowup_commutator_with_rho"] = float(np.linalg.norm(Kb @ R10 - R10 @ Kb) / np.linalg.norm(Kb))

    def traceless_rank(Vd):
        cols = []
        for p in L:
            P = np.outer(Vd[p], Vd[p].conj())
            P = P / np.trace(P).real - np.eye(3) / 3
            cols.append(np.r_[P.real.ravel(), P.imag.ravel()])
        return int(np.linalg.matrix_rank(np.array(cols).T, 1e-9))

    res["blowup_traceless_rank"] = {"10": traceless_rank(V10), "5bar": traceless_rank(V5)}
    # planes giving scalar point sums
    span = lambda u, v: frozenset(tuple(int(t) for t in (a * np.array(u) + b * np.array(v)) % 3) for a in range(3) for b in range(3))
    planes = {span(u, v) for u, v in itertools.combinations([p for p in pts if any(p)], 2)}
    planes = [S for S in planes if len(S) == 9]

    def scalar(Vd, S):
        K = sum(np.outer(Vd[p], Vd[p].conj()) for p in S)
        K = K / np.trace(K) * 3
        return np.linalg.norm(K - np.eye(3)) < 1e-9

    res["planes"] = len(planes)
    res["scalar_on_10"] = sum(scalar(V10, S) for S in planes)
    res["scalar_on_5bar"] = sum(scalar(V5, S) for S in planes)
    # polynomial hierarchies near the point
    RH = Rs["Hu"]
    wH, UH = np.linalg.eig(RH)
    qH = np.array([int(round(np.angle(x) / (2 * np.pi / 3))) % 3 for x in wH])
    rng = np.random.default_rng(2)
    d = rng.normal(size=2) + 1j * rng.normal(size=2)
    scal = {}
    for q in (0, 1, 2):
        hs = UH[:, qH == q]
        c = rng.normal(size=hs.shape[1]) + 1j * rng.normal(size=hs.shape[1])
        hv = hs @ c
        hv /= np.linalg.norm(hv)
        rows = []
        for eps in (1e-2, 3e-3, 1e-3):
            Om = OM0 + eps * (d[0] * np.eye(2) + d[1] * J)
            z = zgrid(Om, 14)
            Q, Hm = modes(A2, Om, z), modes(HU, Om, z)
            Hv = hv @ Hm
            Y = np.array([[np.mean(Q[a] * Q[b] * np.conj(Hv)) for b in range(3)] for a in range(3)])
            s = np.linalg.svd(Y, compute_uv=False)
            rows.append((eps, s[1] / s[0], s[2] / s[1]))
        o = np.array(rows)
        scal[q] = dict(rows=o.tolist(), slope_mc_mt=float(np.polyfit(np.log(o[:, 0]), np.log(o[:, 1]), 1)[0]),
                       slope_mu_mc=float(np.polyfit(np.log(o[:, 0]), np.log(o[:, 2]), 1)[0]))
    res["near_point_scaling"] = scal
    s0, s1, s2 = scal[0], scal[1], scal[2]
    res["checks"] = {k: bool(v) for k, v in dict(
        rho_unitary_on_all_zero_modes=max(res["unitarity_residual"].values()) < 1e-10,
        generation_charges_002=res["charges"]["10"] == [0, 0, 2] and res["charges"]["5bar"] == [0, 0, 2],
        higgs_charge_multiplicities=[res["charges"]["Hu"].count(k) for k in range(3)] == [3, 5, 4]
        and [res["charges"]["Hd"].count(k) for k in range(3)] == [5, 5, 6],
        nine_fixed_points_form_a_w33_line=len(L) == 9 and res["fixed_set_isotropic"],
        line_splits_across_factorisation=res["L_cap_K10"] == 3 and res["L_cap_K5"] == 3,
        charge2_generation_unbiased=np.allclose(res["charge2_generation_abs"], 1 / np.sqrt(3), atol=1e-9),
        fixed_point_vectors_are_charge_eigenvectors=res["fixed_point_eigen_residual"] < 1e-9
        and res["fixed_point_local_charges"] == [0, 0, 0, 2, 2, 2, 2, 2, 2],
        blowups_commute_with_residual_z3=res["blowup_commutator_with_rho"] < 1e-9,
        blowup_image_rank_three=res["blowup_traceless_rank"] == {"10": 3, "5bar": 3},
        only_factor_planes_scalar=res["planes"] == 130 and res["scalar_on_10"] == 1 and res["scalar_on_5bar"] == 1,
        charge0_mu_mc_eps2=abs(s0["slope_mc_mt"]) < 0.05 and abs(s0["slope_mu_mc"] - 2) < 0.1,
        charge1_mc_mt_eps=abs(s1["slope_mc_mt"] - 1) < 0.1 and abs(s1["slope_mu_mc"]) < 0.05,
        charge2_mu_mc_eps2=abs(s2["slope_mu_mc"] - 2) < 0.1,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    print(json.dumps({k: v for k, v in res.items() if k != "near_point_scaling"}, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    print({q: (round(v["slope_mc_mt"], 3), round(v["slope_mu_mc"], 3), v["rows"][-1]) for q, v in scal.items()})


if __name__ == "__main__":
    main()
