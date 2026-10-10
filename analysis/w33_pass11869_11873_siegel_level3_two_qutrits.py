"""Passes 11869-11873: two qutrits are the level-3 theta functions of a genus-2 modulus.

A principally polarised abelian surface A = C^2 / (Z^2 + Omega Z^2) carries nine level-3 theta functions
    f_c(z) = theta[c/3, 0](3z, 3 Omega),   c in F_3^2,
on which translation by the 3-torsion points acts as the two-qutrit Pauli group (Mumford's theta group) and the
Siegel modular group Sp(4, Z) acts, through its level-3 quotient Gamma_{2,3} = Sp(4, F_3), as the Clifford group.
The theta-null vector psi(Omega)_c = f_c(0) is therefore a two-qutrit state that depends on the modulus.

  * 11869 SIEGEL = CLIFFORD. Omega -> -Omega^{-1} acts as F x F (qutrit Hadamards) with the weight-1/2 factor
    sqrt(det(-i Omega)); the shear Omega_12 -> Omega_12 + 1 acts as CZ_3 exactly; Omega_ii -> Omega_ii + 2 as a
    local phase gate; Omega -> -conj(Omega) (the multiplier -1 element diag(I, -I) of GSp(4, Z)) acts as complex
    conjugation. The reductions mod 3 of these generators give Sp(4, 3) (order 51840); on the 40 points of W(3,3)
    they act as PSp(4, 3) (25920), and with diag(I, -I) as PGSp(4, 3) = W(E6) (51840).
  * 11870 GENUS ONE: the Hesse cubic through the theta-null qutrit state psi(tau) is the elliptic curve E_tau itself,
    j(E_psi(tau)) = j(tau). With Pass 11645 (sign W = sign Im j) the qutrit arrow of a theta-null state is the
    modular CP sign sign Im j(tau); it vanishes exactly on the CP-conserving locus of modular flavour models.
  * 11871 GENUS TWO: every theta-null state is a singular point of a Heisenberg-invariant cubic (the Coble cubic of
    the surface), and the coefficient vector of that cubic lies on the Burkhardt quartic of Pass 11657; random even
    two-qutrit states are singular points of no such cubic (control).
  * 11872 FACTORISATION: psi(Omega) is a product state iff the torus factorises (Omega_12 = 0); its Schmidt spectrum
    near a factorised torus is (1, eps, eps^2) with eps proportional to Omega_12.
  * 11873 the review synthesis is in PASS11869_11873_SIEGEL_LEVEL3_TWO_QUTRITS.md.
"""

import itertools
import json
from pathlib import Path

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11869_11873_siegel_level3_two_qutrits.json"
W = np.exp(2j * np.pi / 3)
C2 = [(a, b) for a in range(3) for b in range(3)]
IDX = {c: i for i, c in enumerate(C2)}


def theta_null_1(tau, N=30):
    n = np.arange(-N, N + 1)
    return np.array([np.sum(np.exp(1j * np.pi * 3 * tau * (n + c / 3) ** 2)) for c in range(3)])


def theta_null_2(Om, N=16):
    n = np.arange(-N, N + 1)
    n1, n2 = np.meshgrid(n, n, indexing="ij")
    out = []
    for c1, c2 in C2:
        v1, v2 = n1 + c1 / 3, n2 + c2 / 3
        Q = Om[0, 0] * v1 * v1 + 2 * Om[0, 1] * v1 * v2 + Om[1, 1] * v2 * v2
        out.append(np.exp(3j * np.pi * Q).sum())
    return np.array(out)


def rand_Om(rng, im=(0.9, 1.6)):
    X = rng.uniform(-0.5, 0.5, (2, 2))
    A = rng.normal(size=(2, 2))
    return (X + X.T) / 2 + 1j * (A @ A.T * 0.1 + np.diag(rng.uniform(*im, 2)))


def j_of_tau(tau):
    mp.mp.dps = 30
    q = mp.exp(2j * mp.pi * tau)
    E4 = 1 + 240 * mp.nsum(lambda n: n**3 * q**n / (1 - q**n), [1, mp.inf])
    return complex(E4**3 / (q * mp.qp(q) ** 24))


def j_of_mu(m):
    m3 = m**3
    return 27 * m3 * (m3 + 8) ** 3 / (m3 - 1) ** 3


# ---------------------------------------------------------------- 11869
def part_siegel_clifford(rng):
    res = {}
    F = np.array([[W ** (a * b) for b in range(3)] for a in range(3)]) / np.sqrt(3)
    FF = np.kron(F, F)
    worst = dict(S=0.0, S_factor=0.0, shear_CZ=0.0, diag_shift_phase=0.0, CP=0.0, swap=0.0)
    CZ = np.array([W ** (a * b) for a, b in C2])
    PH = np.array([W ** (a * a) for a, b in C2])
    SW = np.zeros((9, 9))
    for a, b in C2:
        SW[IDX[(b, a)], IDX[(a, b)]] = 1
    for _ in range(12):
        Om = rand_Om(rng)
        p = theta_null_2(Om)
        r = theta_null_2(-np.linalg.inv(Om)) / (FF @ p)
        worst["S"] = max(worst["S"], float(np.ptp(r.real) + np.ptp(r.imag)))
        worst["S_factor"] = max(worst["S_factor"], abs(r[0] / np.sqrt(np.linalg.det(-1j * Om)) - 1))
        O = Om.copy()
        O[0, 1] += 1
        O[1, 0] += 1
        worst["shear_CZ"] = max(worst["shear_CZ"], float(np.max(abs(theta_null_2(O) - CZ * p))))
        O = Om.copy()
        O[0, 0] += 2
        worst["diag_shift_phase"] = max(worst["diag_shift_phase"], float(np.max(abs(theta_null_2(O) - PH * p))))
        worst["CP"] = max(worst["CP"], float(np.max(abs(theta_null_2(-Om.conj()) - p.conj()))))
        worst["swap"] = max(worst["swap"], float(np.max(abs(theta_null_2(Om[::-1, ::-1]) - SW @ p))))
    res["max_errors"] = worst
    res["all_exact"] = bool(max(worst.values()) < 1e-10)
    # the generating symplectic matrices, reduced mod 3
    Z, I2 = np.zeros((2, 2), int), np.eye(2, dtype=int)

    def blk(A, B, Cc, D):
        return np.block([[A, B], [Cc, D]]) % 3
    gens = [
        blk(Z, -I2, I2, Z),  # S : Omega -> -Omega^{-1}
        blk(I2, np.array([[0, 1], [1, 0]]), Z, I2),  # shear Omega_12 + 1 (CZ)
        blk(I2, np.array([[2, 0], [0, 0]]), Z, I2),  # Omega_11 + 2 (phase gate)
        blk(np.array([[0, 1], [1, 0]]), Z, Z, np.array([[0, 1], [1, 0]])),  # swap of the two tori (SWAP)
    ]
    J = blk(Z, I2, -I2, Z)
    assert all(((g.T @ J @ g - J) % 3 == 0).all() for g in gens)
    seen = {tuple(np.eye(4, dtype=int).ravel())}
    frontier = [np.eye(4, dtype=int)]
    while frontier:
        nf = []
        for m in frontier:
            for g in gens:
                x = (g @ m) % 3
                k = tuple(x.ravel())
                if k not in seen:
                    seen.add(k)
                    nf.append(x)
        frontier = nf
    res["order_generated_mod3"] = len(seen)
    # action on the 40 points of W(3,3) (projective points of F_3^4)
    pts = [v for v in itertools.product(range(3), repeat=4) if any(v) and next(x for x in v if x) == 1]
    pidx = {p: i for i, p in enumerate(pts)}

    def norm(v):
        v = tuple(int(x) % 3 for x in v)
        s = next(x for x in v if x)
        return tuple((x * s) % 3 for x in v)  # s is its own inverse mod 3

    def perm(g):
        return tuple(pidx[norm(g @ np.array(p))] for p in pts)
    from sympy.combinatorics import Permutation, PermutationGroup
    G = PermutationGroup([Permutation(list(perm(g))) for g in gens])
    cp = np.diag([1, 1, -1, -1]) % 3
    assert ((cp.T @ J @ cp + J) % 3 == 0).all()  # multiplier -1
    Gcp = PermutationGroup(list(G.generators) + [Permutation(list(perm(cp)))])
    res["order_on_40_points"] = int(G.order())
    res["order_on_40_points_with_CP"] = int(Gcp.order())
    # adjacency preserved by CP: W(3,3) collinearity
    Jn = J
    coll = lambda a, b: int(np.array(a) @ Jn @ np.array(b)) % 3 == 0  # noqa: E731
    pc = perm(cp)
    res["CP_preserves_W33"] = all(coll(pts[pc[i]], pts[pc[k]]) == coll(pts[i], pts[k]) for i in range(40) for k in range(40))
    return res


# ---------------------------------------------------------------- 11870
def part_genus_one(rng):
    worst = 0.0
    for _ in range(30):
        tau = complex(rng.uniform(-0.5, 0.5), rng.uniform(0.9, 2.0))
        p = theta_null_1(tau)
        mu = (p**3).sum() / (3 * p.prod())
        jt = j_of_tau(tau)
        worst = max(worst, abs(j_of_mu(mu) - jt) / abs(jt))
    cp_loci = []
    for tau in [0.0 + 1.3j, 0.5 + 1.1j, -0.5 + 1.7j, np.exp(1j * 1.2), np.exp(1j * 1.9)]:
        p = theta_null_1(tau)
        mu = (p**3).sum() / (3 * p.prod())
        jj = j_of_mu(mu)
        cp_loci.append(abs(jj.imag) / abs(jj))
    generic = []
    for _ in range(10):
        tau = complex(rng.uniform(0.05, 0.45), rng.uniform(1.05, 1.8))
        p = theta_null_1(tau)
        mu = (p**3).sum() / (3 * p.prod())
        jj = j_of_mu(mu)
        generic.append(abs(jj.imag) / abs(jj))
    p = theta_null_1(0.31 + 1.17j)
    return dict(
        max_rel_err_j_hesse_vs_j_tau=worst,
        CP_conj=float(np.max(abs(theta_null_1(-(0.31 - 1.17j)) - p.conj()))),
        max_rel_Im_j_on_CP_loci=max(cp_loci),
        min_rel_Im_j_generic=min(generic),
    )


# ---------------------------------------------------------------- 11871
def hesse_space():
    """Basis of the five Heisenberg-invariant cubic tensors and the Clifford group on them (Passes 11651/11657)."""
    import sys
    sys.path.insert(0, str(ROOT / "analysis"))
    import w33_pass11651_n_qutrit_hesse_space as H
    _, pts, _, B, wg = H.setup(2)
    assert [tuple(p) for p in pts] == C2
    G = np.array(H.closure([H.R_of(B, g) for g in wg.values()]))
    return B.T.reshape(5, 9, 9, 9), G


def part_coble_burkhardt(rng):
    T, G = hesse_space()
    r = np.random.default_rng(3)
    lv = r.normal(size=5) + 1j * r.normal(size=5)

    def I4(v):
        return np.mean(((G @ v) @ lv) ** 4)

    def coble(x):
        Gm = 3 * np.einsum("iabc,b,c->ai", T, x, x)
        _, s, Vh = np.linalg.svd(Gm)
        return Vh[-1].conj(), s[-1] / s[0]
    neg = [IDX[((-a) % 3, (-b) % 3)] for a, b in C2]
    th_sv, th_I4, ctl_sv, rnd_I4 = [], [], [], []
    for _ in range(25):
        x = theta_null_2(rand_Om(rng))
        x /= np.linalg.norm(x)
        k, sr = coble(x)
        th_sv.append(sr)
        th_I4.append(abs(I4(k / np.linalg.norm(k))))
        y = rng.normal(size=9) + 1j * rng.normal(size=9)
        y = (y + y[neg]) / 2
        y /= np.linalg.norm(y)
        ctl_sv.append(coble(y)[1])
        z = rng.normal(size=5) + 1j * rng.normal(size=5)
        rnd_I4.append(abs(I4(z / np.linalg.norm(z))))
    return dict(
        cubic_group_order=len(G),
        theta_null_max_gradient_sv_ratio=float(max(th_sv)),
        random_even_min_gradient_sv_ratio=float(min(ctl_sv)),
        theta_null_max_abs_I4_of_coble=float(max(th_I4)),
        random_min_abs_I4=float(min(rnd_I4)),
    )


# ---------------------------------------------------------------- 11872
def part_factorisation(rng):
    rows = []
    for _ in range(3):
        Om0 = np.diag([complex(rng.uniform(-0.5, 0.5), rng.uniform(0.8, 1.5)) for _ in range(2)])
        s0 = np.linalg.svd(theta_null_2(Om0).reshape(3, 3), compute_uv=False)
        sv = []
        for eps in [0.04, 0.02, 0.01]:
            O = Om0.copy()
            O[0, 1] = O[1, 0] = eps * np.exp(0.7j)
            s = np.linalg.svd(theta_null_2(O, N=20).reshape(3, 3), compute_uv=False)
            sv.append(s / s[0])
        rows.append(dict(
            diagonal_sv2_over_sv1=float(s0[1] / s0[0]),
            slope_sv2=float(np.log(sv[1][1] / sv[2][1]) / np.log(2)),
            slope_sv3=float(np.log(sv[1][2] / sv[2][2]) / np.log(2)),
            sv1_sv3_over_sv2sq=float(sv[2][2] / sv[2][1] ** 2),
        ))
    return rows


def main():
    rng = np.random.default_rng(11869)
    res = dict(pass_ids=[11869, 11870, 11871, 11872, 11873])
    res["11869_siegel_is_clifford"] = part_siegel_clifford(rng)
    res["11870_genus_one_arrow_is_modular_cp"] = part_genus_one(rng)
    res["11871_coble_on_burkhardt"] = part_coble_burkhardt(rng)
    res["11872_product_iff_factorised"] = part_factorisation(rng)
    a, b, c, d = (res[k] for k in list(res)[1:])
    res["checks"] = {k: bool(v) for k, v in dict(
        siegel_generators_act_exactly_as_clifford=a["all_exact"],
        level3_quotient_is_Sp43=a["order_generated_mod3"] == 51840,
        on_points_PSp43=a["order_on_40_points"] == 25920,
        with_CP_PGSp43_WE6=a["order_on_40_points_with_CP"] == 51840 and a["CP_preserves_W33"],
        genus1_hesse_j_is_j_tau=b["max_rel_err_j_hesse_vs_j_tau"] < 1e-10,
        genus1_CP_loci_real_j=b["max_rel_Im_j_on_CP_loci"] < 1e-10 and b["min_rel_Im_j_generic"] > 1e-4,
        coble_singular_at_theta_null=c["theta_null_max_gradient_sv_ratio"] < 1e-12 < c["random_even_min_gradient_sv_ratio"],
        coble_on_burkhardt=c["theta_null_max_abs_I4_of_coble"] < 1e-12 < c["random_min_abs_I4"],
        product_iff_factorised=all(r["diagonal_sv2_over_sv1"] < 1e-12 for r in d),
        schmidt_1_eps_eps2=all(abs(r["slope_sv2"] - 1) < 0.02 and abs(r["slope_sv3"] - 2) < 0.02 for r in d),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, default=lambda o: complex(o).__repr__()))
    print(json.dumps(res["checks"], indent=1))
    print("all", res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
