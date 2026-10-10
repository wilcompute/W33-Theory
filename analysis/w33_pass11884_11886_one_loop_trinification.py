"""Passes 11884-11886: one loop selects trinification at the W(3,3) points of the E8 Higgs flat direction.

Setting (Passes 11879-11883): SU(9) with one 84 = Lambda^3 C^9, renormalizable potential
V = -m^2 |x|^2 + lam1 |x|^4 + lam2 ||mu(x)||^2 (mu = moment map; lam2 > 0), whose vacua are the Kempf-Ness set
SU(9) . h with h the Vinberg Cartan (the Siegel modulus with a Weierstrass point).

  * 11884 THE ONE-LOOP FUNCTION. On the flat set, with x normalised, the vector mass-squared eigenvalues e_i (80 of them)
    satisfy sum e = 20 and sum e^2 = 8 identically (a Casimir and a quartic invariant), and the non-Goldstone scalar
    Hessian of ||mu||^2 has exactly the vector spectrum times 8/3 (moment-map identity Hess ||mu||^2 = 2 dmu^T dmu).
    Hence every bosonic Coleman-Weinberg contribution along the flat direction is a positive multiple of
    F = sum e^2 log e (the m^4 and scale terms are constant), for all couplings.
    F is minimised exactly at the 40 Witting rays (the W(3,3) points): F = -6 log 3, spectrum 0^24 (1/3)^54 1^2, i.e.
    SU(9) -> SU(3)^3 with 54 bifundamental and 2 U(1) vectors massive; generic Cartan points have F ~ -6.23.
  * 11885 STABILITY AND THE PHASE. At a Witting ray the tree-flat, non-gauge, non-radial directions are 55 = 54 + 1:
    F strictly increases along every one of them at finite displacement except the overall phase of the 84, which is
    exactly flat at one loop. The phase is physical: the degree-12 and degree-18 Cartan invariants are nonzero at the
    ray, so e^{i phi} acts as gauge only for phi in 2 pi Z/6. It is lifted only by the dimension-12 operator, whose
    complex coefficient is the CP datum of Passes 11870/11878.
  * 11886 synthesis in PASS11884_11886_ONE_LOOP_TRINIFICATION.md.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402
import w33_pass11879_11883_e8_higgs_siegel_modulus as P  # noqa: E402

OUT = ROOT / "data" / "w33_pass11884_11886_one_loop_trinification.json"
H = P.H


def su9_basis():
    B = []
    for i in range(9):
        for j in range(i + 1, 9):
            A = np.zeros((9, 9), complex)
            A[i, j], A[j, i] = 1, -1
            B.append(A / np.sqrt(2))
            A = np.zeros((9, 9), complex)
            A[i, j], A[j, i] = 1j, 1j
            B.append(A / np.sqrt(2))
    for k in range(8):
        d = np.zeros(9)
        d[:k + 1] = 1
        d[k + 1] = -(k + 1)
        B.append(1j * np.diag(d) / np.linalg.norm(d))
    return np.array(B)


SU9 = su9_basis()


def vec_spectrum(x):
    T = E.full(x)
    T = T / np.linalg.norm(T)
    V = np.array([E._act(A, T).ravel() for A in SU9])
    return np.sort(np.linalg.eigvalsh((V.conj() @ V.T).real))


def F_of(e):
    e = e[e > 1e-12]
    return float(np.sum(e ** 2 * np.log(e)))


def mu_real(p):
    x = p[:84] + 1j * p[84:]
    T = E.full(x)
    rho = np.einsum("acd,bcd->ab", T, T.conj())
    m = rho - np.trace(rho) / 9 * np.eye(9)
    return np.concatenate([m.real.ravel(), m.imag.ravel()])


def dmu(p):
    return np.array([(mu_real(p + 1e-6 * e) - mu_real(p - 1e-6 * e)) / 2e-6 for e in np.eye(168)]).T


def unit_point(c):
    x = c @ H
    x = x / np.linalg.norm(E.full(x))
    return x, np.concatenate([x.real, x.imag])


def part_one_loop(rng):
    pts = {"witting_e0": np.array([1, 0, 0, 0], complex), "witting_011": np.array([0, 1, 1, 1], complex)}
    for k in range(3):
        pts[f"generic_{k}"] = rng.normal(size=4) + 1j * rng.normal(size=4)
    rows = {}
    for name, c in pts.items():
        x, p = unit_point(c)
        e = vec_spectrum(x)
        J = dmu(p)
        hs = np.sort(np.linalg.eigvalsh(J.T @ J))
        hs = hs[hs > 1e-9]
        ev = e[e > 1e-9]
        rows[name] = dict(sum_e=float(e.sum()), sum_e2=float(np.sum(e ** 2)), zeros=int(np.sum(e < 1e-9)), F=F_of(e),
                          scalar_over_vector_min=float((hs / ev).min()), scalar_over_vector_max=float((hs / ev).max()),
                          distinct=sorted(set(np.round(e, 6).tolist()))[:6])

    def Fc(q):
        c = q[:4] + 1j * q[4:]
        return F_of(vec_spectrum((c / np.linalg.norm(c)) @ H))
    mins = []
    for _ in range(5):
        r = minimize(Fc, rng.normal(size=8), method="Nelder-Mead", options=dict(maxiter=2500, xatol=1e-8, fatol=1e-11))
        for _ in range(2):  # polishing restarts
            r = minimize(Fc, r.x, method="Nelder-Mead", options=dict(maxiter=2500, xatol=1e-9, fatol=1e-12))
        c = r.x[:4] + 1j * r.x[4:]
        mins.append(dict(F=float(r.fun), zeros=int(np.sum(vec_spectrum((c / np.linalg.norm(c)) @ H) < 1e-6))))
    return dict(points=rows, minimisations=mins, minus_6_log3=-6 * np.log(3))


def part_stability(rng):
    x0, p0 = unit_point(np.array([1, 0, 0, 0], complex))
    J = dmu(p0)
    _, s, vh = np.linalg.svd(J)
    K = vh[int(np.sum(s > 1e-7 * s[0])):]
    orb = np.array([np.concatenate([E.sorted_c(E._act(A, E.full(x0))).real, E.sorted_c(E._act(A, E.full(x0))).imag])
                    for A in SU9])
    so = np.linalg.svd(orb, compute_uv=False)
    orbit_rank = int(np.sum(so > 1e-7 * so[0]))
    S = np.vstack([orb, p0[None, :]])
    Us, sS, _ = np.linalg.svd(S.T, full_matrices=False)
    Q = Us[:, sS > 1e-7 * sS[0]]
    Kp = K - (K @ Q) @ Q.T
    _, ss, vv = np.linalg.svd(Kp)
    flat = vv[:int(np.sum(ss > 1e-4))]
    f0 = F_of(vec_spectrum(x0))

    def Fx(t):
        p = p0 + t @ flat
        return F_of(vec_spectrum(p[:84] + 1j * p[84:]))
    n = flat.shape[0]
    tests = {}
    for t in (0.02, 0.05):
        basis_min = min(min(Fx(t * np.eye(n)[i]) - f0, Fx(-t * np.eye(n)[i]) - f0) for i in range(n))
        rand = []
        for _ in range(40):
            v = rng.normal(size=n)
            rand.append(Fx(t * v / np.linalg.norm(v)) - f0)
        tests[str(t)] = dict(basis_min=float(basis_min), random_min=float(min(rand)))
    phase = F_of(vec_spectrum(np.exp(0.3j) * x0)) - f0
    # nonzero holomorphic invariants at the ray
    F3 = np.array([[P.W ** (a * b) for b in range(3)] for a in range(3)]) / np.sqrt(3)
    D = np.diag([1, 1, P.W])
    I3 = np.eye(3)
    gens = [P.cartan_action(g) for g in (np.kron(F3, I3), np.kron(I3, F3), np.kron(D, I3), np.kron(I3, D),
                                         np.diag([P.W ** (a * b) for a, b in P.C2]))]
    import itertools
    mons = list(itertools.combinations_with_replacement(range(4), 12))
    Z = rng.normal(size=(len(mons) + 20, 4)) + 1j * rng.normal(size=(len(mons) + 20, 4))

    def V(Zs):
        return np.array([[np.prod(z[list(m)]) for m in mons] for z in Zs])
    A = np.vstack([V(Z @ np.linalg.inv(g).T) - V(Z) for g in gens])
    _, sv, vh2 = np.linalg.svd(A)
    inv = vh2[-1].conj()
    I12_ray = abs(sum(inv[i] * np.prod(np.array([1, 0, 0, 0], complex)[list(m)]) for i, m in enumerate(mons)))
    return dict(ker_dmu=int(K.shape[0]), orbit_rank=orbit_rank, tree_flat_nongauge=n, finite_tests=tests,
                phase_flatness=float(phase), I12_at_ray=float(I12_ray))


def main():
    rng = np.random.default_rng(11884)
    res = dict(pass_ids=[11884, 11885, 11886])
    a = res["11884_one_loop"] = part_one_loop(rng)
    b = res["11885_stability"] = part_stability(rng)
    pts = a["points"]
    gen = [v for k, v in pts.items() if k.startswith("generic")]
    wit = [v for k, v in pts.items() if k.startswith("witting")]
    res["checks"] = {k: bool(v) for k, v in dict(
        traces_constant=all(abs(v["sum_e"] - 20) < 1e-9 and abs(v["sum_e2"] - 8) < 1e-9 for v in pts.values()),
        scalars_proportional_to_vectors=all(abs(v["scalar_over_vector_min"] - 8 / 3) < 1e-6
                                            and abs(v["scalar_over_vector_max"] - 8 / 3) < 1e-6 for v in pts.values()),
        witting_is_trinification_spectrum=all(v["zeros"] == 24 and abs(v["F"] + 6 * np.log(3)) < 1e-9 for v in wit),
        generic_higher=all(v["zeros"] == 0 and v["F"] > -6 * np.log(3) + 0.1 for v in gen),
        global_minimum_at_witting=all(abs(m["F"] + 6 * np.log(3)) < 1e-6 and m["zeros"] == 24 for m in a["minimisations"]),
        flat_count_55=b["tree_flat_nongauge"] == 55 and b["ker_dmu"] == 112 and b["orbit_rank"] == 56,
        strict_local_min=all(t["basis_min"] > 0 and t["random_min"] > 0 for t in b["finite_tests"].values()),
        phase_exactly_flat=abs(b["phase_flatness"]) < 1e-12,
        phase_physical=b["I12_at_ray"] > 1e-6,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(res["checks"], indent=1))
    print(json.dumps(b, indent=1))
    print("all", res["all_checks_pass"])


if __name__ == "__main__":
    main()
