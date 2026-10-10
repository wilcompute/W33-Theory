"""Passes 11890-11892: the vacuum phase diagram of the E8 twisted Higgs -- every W(3,3) structure is a vacuum.

Setting: SU(9) + 84 (Passes 11879-11889), the Z3-twisted half of E8, with flat direction the Vinberg Cartan h
(= genus-2 modulus with a Weierstrass point).

  * 11890 HOSOTANI (gauge-Higgs on T^2/Z3). With the 84 as the internal gauge field, the flat set mu = 0 is the set of
    flat connections, and the untwisted one-loop potential is V = -sum_alpha [f(alpha(x)) - n_F f(alpha(x) + s)],
    f(w) = sum_{l in dual lattice} cos(2 pi <l, w>) / |l|^6, alpha(x) the 240 eigenvalues of ad(x) (a linear map on
    h, closed under omega). Bosons alone, or one Scherk-Schwarz adjoint gaugino (s = 1/(1-omega)), have their global
    minimum at x = 0 (SU(9) unbroken, 80 massless vectors); Scherk-Schwarz with n_F = 2..4 also. Periodic adjoint
    fermions with n_F = 2 dominate and break: 48 massless roots in two components of 24 (D4 + D4), 16 massless 4d
    vectors and 16 massless fermions, and the 56-dimensional holonomy centraliser is exactly Fix(P) + Fix(P^perp) for
    a tensor factorisation P + P^perp of the two qutrits (each one-qutrit Pauli centraliser 32-dimensional and
    contained in it): the fermion-dominated Hosotani vacuum is a factorisation point (a product torus).
  * 11891 CUSP DISPLACEMENT. Moving the Cartan vev off a Witting ray by delta and inverting to the torus (Passes
    11879), the largest reduced Im(Omega) grows as (3/pi + o(1)) ln(1/delta): the leading level-3 theta suppression
    |exp(pi i Omega/3)| is proportional to delta. The family-hierarchy parameter of the theta texture is linear in the
    Higgs displacement from the trinification point.
  * 11892 FERMION LOOPS. In the N=1 completion (chiral 84 + gauginos) every massive vector multiplet is degenerate
    along the D-flat direction (scalar/vector mass ratio exactly constant, 11884), so V_1loop = 0 identically. A soft
    scalar mass m^2 shifts the one-loop potential by a positive multiple of m^2 G, G = sum e log e (sum e fixed):
    m^2 > 0 selects the global minimum of G, attained at the C10 curve y^2 = x^5 - 1 (Gottschling's order-10 point)
    with its Z5-fixed Weierstrass point; m^2 < 0 selects the maximum of G, -18 log 3, at the Witting rays
    (trinification). Fermion-dominated non-SUSY loops select the maximum of F = sum e^2 log e, which runs toward a cusp.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares, minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11874_11878_siegel_fixed_points_cp_magic as S  # noqa: E402
import w33_pass11879_11883_e8_higgs_siegel_modulus as M  # noqa: E402
import w33_pass11884_11886_one_loop_trinification as P  # noqa: E402
import w33_pass11887_11889_e6_family_at_w33_point as Q  # noqa: E402
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2  # noqa: E402

E = Q.E
H = Q.H
OUT = ROOT / "data" / "w33_pass11890_11892_vacuum_phase_diagram.json"
W = np.exp(2j * np.pi / 3)
S1 = 1 / (1 - W)

# ---------------------------------------------------------------- Hosotani machinery
_LAT = np.array([a + 1j * (2 * k + a) / np.sqrt(3) for a in range(-14, 15) for k in range(-16, 17)
                 if 0 < abs(a + 1j * (2 * k + a) / np.sqrt(3)) <= 14])
_LW = 1 / abs(_LAT) ** 6
_LC = np.conj(_LAT)


def fper(z):
    return (np.cos(2 * np.pi * np.real(_LC[None, :] * z[:, None])) * _LW[None, :]).sum(1)


def in_lattice(z, tol=1e-5):
    n = np.imag(z) / np.imag(W)
    m = np.real(z) - n * np.real(W)
    return (abs(m - np.round(m)) < tol) & (abs(n - np.round(n)) < tol)


def root_map():
    adh = np.array([Q.ad((np.zeros((9, 9), complex), H[u], Q.Z84.copy())) for u in range(4)])
    rng = np.random.default_rng(3)
    g = rng.normal(size=4) + 1j * rng.normal(size=4)
    ev, Pm = np.linalg.eig(np.tensordot(g, adh, axes=1))
    Pi = np.linalg.inv(Pm)
    A = np.array([np.diag(Pi @ adh[u] @ Pm) for u in range(4)]).T
    return A[np.argsort(abs(ev))[8:]], adh


def components(A, R):
    rows = A[R]

    def isroot(v):
        return np.min(np.max(abs(A - v), axis=1)) < 1e-8
    n = len(R)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if isroot(rows[i] + rows[j]) or isroot(rows[i] - rows[j]):
                adj[i].append(j)
                adj[j].append(i)
    seen, comps = set(), []
    for i in range(n):
        if i in seen:
            continue
        st, comp = [i], {i}
        while st:
            k = st.pop()
            for m in adj[k]:
                if m not in comp:
                    comp.add(m)
                    st.append(m)
        seen |= comp
        comps.append(len(comp))
    return sorted(comps)


def omega_form(u, v):
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % 3


def part_hosotani(rng):
    A, adh = root_map()
    c = rng.normal(size=4) + 1j * rng.normal(size=4)
    lin = abs(np.sort(abs(np.linalg.eigvals(np.tensordot(c, adh, axes=1))))
              - np.sort(abs(np.concatenate([A @ c, np.zeros(8)])))).max()
    omega_closure = max(min(abs(A @ c - W * x)) for x in A @ c)
    out = dict(linear_root_map_error=float(lin), omega_closure=float(omega_closure), regimes={})
    best_periodic = None
    for label, nF, s in (("bosons_only", 0, 0.0), ("SS_nF1", 1, S1), ("SS_nF2", 2, S1), ("SS_nF4", 4, S1),
                         ("periodic_nF2", 2, 0.0)):
        def V(q):
            a = A @ (q[:4] + 1j * q[4:])
            return -(fper(a) - nF * fper(a + s)).sum()
        res = []
        for _ in range(25):
            r = minimize(V, rng.normal(size=8) * rng.uniform(0.2, 1.5), method="BFGS", options=dict(gtol=1e-11))
            res.append(r)
        r = min(res, key=lambda t: t.fun)
        a = A @ (r.x[:4] + 1j * r.x[4:])
        R = np.where(in_lattice(a))[0]
        out["regimes"][label] = dict(V=float(r.fun), V_at_0=float(V(np.zeros(8))), massless_vectors=int(len(R)) // 3,
                                     massless_fermions=int(in_lattice(a + s).sum()) // 3 if nF else 0,
                                     root_components=components(A, R) if 0 < len(R) < 240 else [len(R)])
        if label == "periodic_nF2":
            best_periodic = r.x
    # factorisation test for the periodic vacuum
    c = best_periodic[:4] + 1j * best_periodic[4:]
    ev, Pm = np.linalg.eig(np.tensordot(c, adh, axes=1))
    Cm = np.array([E._vec(Q.to_el(Pm[:, i])) for i in np.where(in_lattice(ev))[0]]).T
    vecs = [v for v in np.ndindex(3, 3, 3, 3) if any(v)]
    planes = set()
    for u in vecs:
        for v in vecs:
            if omega_form(u, v):
                planes.add(frozenset(tuple((a * np.array(u) + b * np.array(v)) % 3) for a in range(3) for b in range(3)))

    def rk(Mx):
        return int(np.sum(np.linalg.svd(Mx, compute_uv=False) > 1e-8))

    def fix_space(Pl):
        gens = [g for g in Pl if any(g)]
        u = gens[0]
        v = next(g for g in gens if omega_form(u, g))
        Mst = np.vstack([np.array([E._vec(Q.act_aut(Q.pauli(*g), b)) - E._vec(b) for b in Q.BASIS]).T for g in (u, v)])
        _, s, vh = np.linalg.svd(Mst)
        k = int(np.sum(s < 1e-9 * s[0]))
        return np.array([E._vec(Q.to_el(cc)) for cc in vh[-k:].conj()]).T

    best = None
    for Pl in planes:
        F = fix_space(Pl)
        inter = F.shape[1] + Cm.shape[1] - rk(np.hstack([F, Cm]))
        if best is None or inter > best[0]:
            best = (inter, Pl, F)
    perp = frozenset([v for v in vecs if all(omega_form(v, p) == 0 for p in best[1])] + [(0, 0, 0, 0)])
    Fp = fix_space(perp)
    out["periodic_vacuum_factorisation"] = dict(
        centraliser_dim=int(Cm.shape[1]), fix_dim=int(best[2].shape[1]), best_intersection=int(best[0]),
        perp_intersection=int(Fp.shape[1] + Cm.shape[1] - rk(np.hstack([Fp, Cm]))),
        spans_centraliser=bool(rk(np.hstack([best[2], Fp])) == Cm.shape[1] == rk(np.hstack([best[2], Fp, Cm]))))
    return out


# ---------------------------------------------------------------- cusp displacement
def invert(c, rng, guess=None):
    q = M.maschke(c)
    q = q / np.linalg.norm(q)

    def unpack(p):
        X = np.array([[p[0], p[1]], [p[1], p[2]]])
        L = np.array([[p[3], 0], [p[4], p[5]]])
        return X + 1j * (L @ L.T + 0.05 * np.eye(2))

    def res(p):
        b, _ = M.coble_point(theta_null_2(unpack(p), N=30))
        ph = np.vdot(b, q) / abs(np.vdot(b, q))
        r = q - ph * b
        return np.concatenate([r.real, r.imag])
    best = None
    starts = ([guess] if guess is not None else []) + [np.concatenate([rng.uniform(-.5, .5, 3), rng.uniform(.6, 3., 3)])
                                                     for _ in range(60)]
    for p0 in starts:
        r = least_squares(res, p0, xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if best is None or r.cost < best.cost:
            best = r
        if best.cost < 1e-24:
            break
    return unpack(best.x), float(np.sqrt(2 * best.cost)), best.x


def part_cusp(rng):
    c0 = np.array([1, 0, 0, 0], complex)
    rows = []
    for _ in range(2):
        d = rng.normal(size=4) + 1j * rng.normal(size=4)
        d -= np.vdot(c0, d) * c0
        d /= np.linalg.norm(d)
        guess, ys, resid = None, [], []
        ds = [0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125]
        for dl in ds:
            Om, r, guess = invert(c0 + dl * d, rng, guess)
            ys.append(float(np.linalg.eigvalsh(S.siegel_reduce(Om).imag).max()))
            resid.append(r)
        slopes = [(ys[i + 1] - ys[i]) / np.log(2) for i in range(len(ys) - 1)]
        rows.append(dict(im_max=ys, slopes=slopes, max_residual=max(resid)))
    return dict(directions=rows, three_over_pi=3 / np.pi)


# ---------------------------------------------------------------- fermion phase diagram
def G_of(e):
    e = e[e > 1e-12]
    return float(np.sum(e * np.log(e)))


def spec(c):
    return P.vec_spectrum((c / np.linalg.norm(c)) @ H)


def part_fermions(rng):
    wit = spec(np.array([1, 0, 0, 0], complex))

    def opt(fun, sign, starts):
        best = None
        for c0 in starts:
            q0 = np.concatenate([c0.real, c0.imag])
            r = minimize(lambda q: sign * fun(spec(q[:4] + 1j * q[4:])), q0, method="Nelder-Mead",
                         options=dict(maxiter=2500, xatol=1e-9, fatol=1e-12))
            r = minimize(lambda q: sign * fun(spec(q[:4] + 1j * q[4:])), r.x, method="BFGS", options=dict(gtol=1e-11))
            if best is None or r.fun < best.fun:
                best = r
        c = best.x[:4] + 1j * best.x[4:]
        return c / np.linalg.norm(c), sign * best.fun
    rand = [rng.normal(size=4) + 1j * rng.normal(size=4) for _ in range(4)]
    cmin, gmin = opt(G_of, 1, rand)
    cmax, gmax = opt(G_of, -1, rand)
    # C10 identification: exact C10 torus and its six odd theta-null Cartan points
    C10 = S.gottschling_points()["y2=x5-1 (C10)"]
    gvals = []
    for al, be in M.CHARS:
        if int(round(4 * np.dot(al, be))) % 2:
            u = M.untwisted(C10, al, be)
            cc = np.array([u[M.IDX[a]] for a in M.DIRS])
            gvals.append(G_of(spec(cc)))
    Om, res, _ = invert(cmin, rng)
    R = S.siegel_reduce(Om)
    dist = min(np.max(abs(x - C10)) for x in (R, R + np.array([[0, 1], [1, 0]]), R - np.array([[0, 1], [1, 0]])))
    fmax_c, fmax = opt(P.F_of, -1, rand[:3])
    Omf, resf, _ = invert(fmax_c, rng)
    return dict(G_witting=G_of(wit), minus_18_log3=-18 * np.log(3), G_min=gmin, G_max=gmax,
                G_at_C10_odd_thetas=sorted(gvals), G_min_torus_distance_to_C10=float(dist), inversion_residual=res,
                F_max=fmax, F_max_reduced_im_max=float(np.linalg.eigvalsh(S.siegel_reduce(Omf).imag).max()),
                F_max_massless_vectors=int(np.sum(spec(fmax_c) < 1e-6)))


def main():
    rng = np.random.default_rng(11890)
    res = dict(pass_ids=[11890, 11891, 11892])
    h = res["11890_hosotani"] = part_hosotani(rng)
    c = res["11891_cusp"] = part_cusp(rng)
    f = res["11892_fermions"] = part_fermions(rng)
    reg = h["regimes"]
    res["checks"] = {k: bool(v) for k, v in dict(
        root_map_linear_and_omega_closed=h["linear_root_map_error"] < 1e-10 and h["omega_closure"] < 1e-10,
        bosons_restore_su9=reg["bosons_only"]["massless_vectors"] == 80 and abs(reg["bosons_only"]["V"] - reg["bosons_only"]["V_at_0"]) < 1e-6,
        ss_keeps_su9=all(reg[k]["massless_vectors"] == 80 for k in ("SS_nF1", "SS_nF2", "SS_nF4")),
        periodic_nF2_breaks_to_D4D4=reg["periodic_nF2"]["massless_vectors"] == 16 and reg["periodic_nF2"]["root_components"] == [24, 24],
        periodic_vacuum_is_factorisation=h["periodic_vacuum_factorisation"]["spans_centraliser"]
        and h["periodic_vacuum_factorisation"]["best_intersection"] == h["periodic_vacuum_factorisation"]["fix_dim"]
        and h["periodic_vacuum_factorisation"]["perp_intersection"] == h["periodic_vacuum_factorisation"]["fix_dim"],
        cusp_log_law=all(max(r["slopes"]) < 3 / np.pi and min(r["slopes"][-2:]) > 3 / np.pi - 0.005
                         and all(np.diff(r["slopes"]) > 0) for r in c["directions"]),
        soft_negative_selects_trinification=abs(f["G_max"] - f["minus_18_log3"]) < 1e-6 and abs(f["G_witting"] - f["minus_18_log3"]) < 1e-9,
        soft_positive_selects_C10_weierstrass=abs(f["G_min"] - min(f["G_at_C10_odd_thetas"])) < 1e-8
        and f["G_min_torus_distance_to_C10"] < 1e-5,
        fermion_dominated_runs_to_cusp=f["F_max_reduced_im_max"] > 4,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(res["checks"], indent=1))
    print(json.dumps(reg, indent=1))
    print("all", res["all_checks_pass"])


if __name__ == "__main__":
    main()
