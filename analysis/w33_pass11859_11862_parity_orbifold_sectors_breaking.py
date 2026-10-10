"""Passes 11859, 11860, 11862: parity orbifold, central-charge sectors, Lorentz-invariant breaking.

11859  Parity (Lorentz-normalising) orbifold.  The stabiliser of a Kramers reversal in Sp(4,3) is SL(2,9).2 (Pass 11832);
       its anticentraliser coset (g J0 g^-1 = -J0, the F9-antilinear "parity") normalises the Lorentz group SL(2,9)
       without centralising it.  Each such h is lifted to E8 through its Weil action on Di as diag(D_h, det^-1) in
       SU(5)_L (Pass 11849).  The h-invariant part of the spinorial block (32, Di) is decomposed under su(5)_GUT by
       hypercharge counts: net chirality n(10) - n(10bar) and n(5bar) - n(5).  Pass 11855 proved Lorentz-COMMUTING
       projections are vector-like; this tests the normalising ones.
11860  Generations.  (a) E8 under (Lorentz commutant) x (Lorentz) is multiplicity-free in the spinorial embedding
       (components (55,1), (11,5'), (32,Di), (1,Sym2 Di) distinct and irreducible), so no multiplet repeats.
       (b) The translation group Z3.M has three central-charge sectors of characters (k = 0, 1, 2); their A6-orbit
       structures are computed (k = 0 is Minkowski momentum space 1+20+30+30).
11862  Breaking.  The centre of the commutant of SL(2,9) x Z3 (su(3)+so(5)+u(1), Pass 11857): its charge pattern on E8
       (B-L test), whether the commutant contains the Standard-Model algebra, and the rank argument (Lorentz-invariant
       vevs lie in the commutant, adjoint vevs preserve rank 5).
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11831_11833_finite_ads4 as F  # noqa: E402
import w33_pass11834_11837_singletons_bulk_poincare_e8 as S  # noqa: E402
import w33_pass11843_e8_tits_lorentz_commutant as T  # noqa: E402
import w33_pass11844_11846_e8_poincare_lifts_matter as L  # noqa: E402
import w33_pass11849_11851_spinor_lorentz_central_z3_generations as M  # noqa: E402

OUT = ROOT / "data" / "w33_pass11859_11862_parity_orbifold_sectors_breaking.json"
N = T.N


def frac(x, d=6):
    return str(Fraction(float(x)).limit_denominator(d))


def weil_data():
    keys, mats, Vs, index, _ = S.weil_group()
    k0 = next(k for k in F.PTS if F.Q[k] == 2)
    J0 = F.JM[k0]
    cent = [i for i, g in enumerate(mats) if np.array_equal(F.m(g, J0), F.m(J0, g))]
    anti = [i for i, g in enumerate(mats) if np.array_equal(F.m(g, J0), (-F.m(J0, g)) % 3)]
    P = Vs[index[F.key((-F.I4) % 3)]]
    w, U = np.linalg.eigh(P)
    Q = U[:, np.isclose(w, -1)]
    return mats, Vs, index, cent, anti, Q


def sectors():
    """central-charge sectors of the characters of the sum-zero module S (dual = F3^6 / <1>), A6 orbits."""
    gens = []
    for k in (2, 3, 4, 5):
        gens.append([1 if i == 0 else (k if i == 1 else (0 if i == k else i)) for i in range(6)])
    # group closure on permutations
    G = {tuple(range(6))}
    fr = [tuple(range(6))]
    while fr:
        nx = []
        for p in fr:
            for g in gens:
                q = tuple(p[g[i]] for i in range(6))
                if q not in G:
                    G.add(q)
                    nx.append(q)
        fr = nx
    assert len(G) == 360
    def canon(a):
        return min(tuple((x + c) % 3 for x in a) for c in range(3))
    classes = {canon(a) for a in itertools.product(range(3), repeat=6)}
    out = {}
    for k in range(3):
        sec = [a for a in classes if sum(a) % 3 == k]
        seen, orbs = set(), []
        for a in sec:
            if a in seen:
                continue
            o = {canon(tuple(a[p[i]] for i in range(6))) for p in G}
            seen |= o
            orbs.append(len(o))
        out[str(k)] = dict(size=len(sec), orbits=sorted(orbs))
    out["k1_k2_isomorphic_orbit_structure"] = out["1"]["orbits"] == out["2"]["orbits"]
    out["k1_matches_k0"] = out["1"]["orbits"] == out["0"]["orbits"]
    return out


def lorentz_parts_irreducible():
    """norms on SL(2,9) of the Lorentz parts of E8 = (55,1)+(11,5')+(32,Di)+(1,Sym2 Di): all 1 => multiplicity-free."""
    mats, Vs, index, cent, anti, Q = weil_data()
    di = np.array([np.trace(Q.conj().T @ Vs[i] @ Q) for i in cent])
    sq = [index[F.key(F.m(mats[i], mats[i]))] for i in cent]
    di2 = np.array([np.trace(Q.conj().T @ Vs[j] @ Q) for j in sq])
    sym2 = (di**2 + di2) / 2
    alt2m1 = (di**2 - di2) / 2 - 1
    nrm = lambda c: round(float(np.real(np.mean(abs(c) ** 2))), 6)  # noqa: E731
    ov = lambda a, b: round(float(np.real(np.mean(a * np.conj(b)))), 6)  # noqa: E731
    return dict(Di=nrm(di), vector5=nrm(alt2m1), Sym2Di=nrm(sym2), overlaps=dict(Di_vector5=ov(di, alt2m1), Di_Sym2=ov(di, sym2),
                vector5_Sym2=ov(alt2m1, sym2)))


def main():
    rng = np.random.default_rng(11859)
    B, sub = L.setup(rng)
    chain = sub["chain"]
    tits = [T.tits(B, b) for b in chain]
    adj_gens = [tits[i] @ tits[i + 1] for i in range(4)]
    ext_gens = [a @ b for a, b in itertools.permutations(tits, 2)]
    C_gut = T.fixed_subalgebra(adj_gens)
    C_ext = T.fixed_subalgebra(ext_gens)
    Y = L.centraliser_within(B, C_gut, C_ext)[:, 0]
    adY = T.ad(B, Y)
    ev = np.linalg.eigvals(adY)
    adY = adY / ev[np.argmax(abs(ev))]
    C_L = M.centraliser(B, C_gut)
    phi, herr, _ = M.chevalley_sl5(B, C_L, rng)
    mats, Vs, index, cent, anti, Q = weil_data()

    def auto5(D4, last=None):
        g5 = np.eye(5, dtype=complex)
        g5[:4, :4] = D4
        g5[4, 4] = 1 / np.linalg.det(D4) if last is None else last
        return expm(T.ad(B, phi(M.log_su(g5))))
    # Lorentz lift (two generators) and its commutant, the -1 element Z
    gens4, minus4, *_ = M.di_generators(rng)
    A = [auto5(D) for D in gens4]
    Z = auto5(minus4)
    C_spin = M.fixed_c(A)
    P128 = (np.eye(N) - Z) / 2
    u_, s_, _ = np.linalg.svd(P128)
    V128 = u_[:, s_ > 0.5]
    res = {"pass_ids": [11859, 11860, 11862], "sl5_hom_error": herr}

    # ---------------- 11859 parity orbifold
    def hyper_content(Vsub):
        if Vsub.shape[1] == 0:
            return {}, 0, 0
        Yr = np.linalg.pinv(Vsub) @ adY @ Vsub
        cnt = Counter(frac(np.real(x)) for x in np.linalg.eigvals(Yr))
        n10 = cnt.get("1", 0) - cnt.get("-1", 0)
        n5b = (cnt.get("1/3", 0) - cnt.get("-1/3", 0)) / 3
        return dict(sorted(cnt.items())), n10, n5b
    parity = []
    sample = list(rng.choice(anti, 24, replace=False))
    for i in sample:
        D = Q.conj().T @ Vs[i] @ Q
        p = auto5(D)
        normalises = float(abs(p @ C_spin - C_spin @ (np.linalg.pinv(C_spin) @ p @ C_spin)).max())
        # kept part of the spinorial block: p-fixed vectors inside the 128 block
        pr = np.linalg.pinv(V128) @ p @ V128
        w, Vv = np.linalg.eig(pr)
        keep = V128 @ Vv[:, np.isclose(w, 1, atol=1e-7)]
        cnt, n10, n5b = hyper_content(keep)
        order = next(n for n in range(1, 50) if np.allclose(np.linalg.matrix_power(D, n), np.eye(4), atol=1e-8) or n == 49)
        parity.append(dict(h_order_on_Di=int(order), kept_dim=int(keep.shape[1]), net_10=float(n10), net_5bar=float(n5b),
                           normalises_so11=normalises < 1e-6))
    res["parity_orbifold"] = dict(samples=parity, any_chiral=any(abs(r["net_10"]) > 1e-9 or abs(r["net_5bar"]) > 1e-9 for r in parity),
                                  kept_dims=sorted(Counter(r["kept_dim"] for r in parity).items()))
    print("11859", res["parity_orbifold"]["any_chiral"], res["parity_orbifold"]["kept_dims"],
          Counter((r["net_10"], r["net_5bar"]) for r in parity), flush=True)
    # control: a Lorentz element (commuting) projection
    ctrl = []
    for i in list(rng.choice(cent, 6, replace=False)):
        D = Q.conj().T @ Vs[i] @ Q
        p = auto5(D)
        pr = np.linalg.pinv(V128) @ p @ V128
        w, Vv = np.linalg.eig(pr)
        keep = V128 @ Vv[:, np.isclose(w, 1, atol=1e-7)]
        _, n10, n5b = hyper_content(keep)
        ctrl.append(dict(kept_dim=int(keep.shape[1]), net_10=float(n10), net_5bar=float(n5b)))
    res["parity_orbifold"]["control_lorentz_elements"] = ctrl
    # ---- combined test: GUT-side Spin(10)-centre phase s = exp(2 pi i X/4) times a parity (or Lorentz) element
    Xb = M.nullspace(np.vstack([np.linalg.pinv(C_spin) @ T.ad(B, C_gut[:, j]) @ C_spin for j in range(C_gut.shape[1])]))
    X = C_spin @ Xb[:, 0]
    adX = T.ad(B, X)
    wx, Vx = np.linalg.eig(adX)
    xr = np.linalg.pinv(V128) @ adX @ V128
    e128 = np.linalg.eigvals(xr)
    scale = 5 / e128[np.argmax(abs(e128))]
    lam = wx * scale
    assert np.allclose(lam, np.round(lam.real), atol=1e-6), "X charges not integral"
    lam = np.round(lam.real)
    s_el = (Vx @ np.diag(np.exp(2j * np.pi * lam / 4)) @ np.linalg.inv(Vx))
    xcharges = Counter(int(round(float(np.real(v)))) for v in e128 * scale)
    comb = []
    for nm, pool in (("parity", sample[:16]), ("lorentz", list(rng.choice(cent, 16, replace=False)))):
        for i in pool:
            D = Q.conj().T @ Vs[i] @ Q
            evD = np.linalg.eigvals(D)
            paired = bool(all(np.min(abs(evD - np.conj(x))) < 1e-7 for x in evD))
            g = s_el @ auto5(D)
            pr = np.linalg.pinv(V128) @ g @ V128
            w, Vv = np.linalg.eig(pr)
            keep = V128 @ Vv[:, np.isclose(w, 1, atol=1e-7)]
            _, n10, n5b = hyper_content(keep)
            comb.append(dict(kind=nm, Di_eigenvalues_conjugate_paired=paired, kept_dim=int(keep.shape[1]),
                             net_10=float(n10), net_5bar=float(n5b)))
    res["gut_phase_times_element"] = dict(X_charges_on_spinor_block=dict(sorted(xcharges.items())), rows=comb,
                                          any_chiral=any(abs(r["net_10"]) > 1e-9 for r in comb),
                                          chiral_iff_unpaired=all((abs(r["net_10"]) > 1e-9) == (not r["Di_eigenvalues_conjugate_paired"]) for r in comb))
    print("combined", res["gut_phase_times_element"]["any_chiral"], res["gut_phase_times_element"]["chiral_iff_unpaired"],
          Counter((r["kind"], r["Di_eigenvalues_conjugate_paired"], r["net_10"], r["net_5bar"]) for r in comb), flush=True)

    # ---------------- 11860 generations

    res["sectors"] = sectors()
    res["lorentz_parts"] = lorentz_parts_irreducible()
    print("11860", res["sectors"], flush=True)

    # ---------------- 11862 breaking: centre of the commutant of SL(2,9) x Z3
    Gmod3 = L.weyl_mod3(chain)
    subs = L.submodules(Gmod3)
    W5 = next(s for s in subs if len(s) == 5)
    c = next(v for v in L.span_vectors(W5) if any(v) and all(T.ip(v, w) % 3 == 0 for w in W5))
    tc = L.torus_order3(np.array(c))
    C_both = M.fixed_c(A + [tc])
    C_sm = T.fixed_subalgebra(adj_gens + [tc])
    # centre: elements of C_both commuting with all of C_both
    adC = [np.linalg.pinv(C_both) @ T.ad(B, C_both[:, i]) @ C_both for i in range(C_both.shape[1])]
    cz = M.nullspace(np.vstack([np.column_stack([adC[i][:, j] for i in range(len(adC))]) for j in range(len(adC))]))
    zc = C_both @ cz[:, 0]
    adz = T.ad(B, zc)
    ez = np.linalg.eigvals(adz)
    ez = ez / ez[np.argmax(abs(ez))]
    assert np.allclose(ez.imag, 0, atol=1e-6)
    spec_all = Counter(frac(np.real(x), 12) for x in ez)
    top = np.linalg.eigvals(adz)
    top = top[np.argmax(abs(top))]
    zr = np.linalg.pinv(V128) @ adz @ V128
    ez128 = np.linalg.eigvals(zr) / top
    spec128 = Counter(frac(np.real(x), 12) for x in ez128)
    res["breaking"] = dict(commutant_dim=int(C_both.shape[1]), centre_dim=int(cz.shape[1]),
                           contains_SM_algebra=L.basis_contains(C_sm, C_both),
                           centre_spectrum_on_E8=dict(sorted(spec_all.items(), key=lambda t: float(Fraction(t[0])))),
                           centre_spectrum_on_spinor_block=dict(sorted(spec128.items(), key=lambda t: float(Fraction(t[0])))),
                           rank=int(L.analyse_complex(B, C_both, rng)["rank"]))
    # the central translation is the colour-centre (triality) element: t_c = exp(8 pi i Y)
    wy, Vy = np.linalg.eig(adY)
    hyp_rot = Vy @ np.diag(np.exp(8j * np.pi * wy.real)) @ np.linalg.inv(Vy)
    res["breaking"]["tc_equals_exp_8pi_i_Y"] = float(abs(hyp_rot - tc).max())
    trial = Counter()
    for k in range(N):
        v = Vy[:, k]
        y = float(np.real(wy[k]))
        ph = (np.linalg.pinv(Vy[:, [k]]) @ tc @ Vy[:, [k]])[0, 0]
        q = int(round(np.angle(ph) / (2 * np.pi / 3))) % 3
        trial[(frac(y), q)] += 1
    res["breaking"]["central_charge_by_hypercharge"] = {f"Y={a}": {"q": b, "count": n} for (a, b), n in sorted(trial.items(), key=lambda t: float(Fraction(t[0][0])))}
    res["breaking"]["q_equals_12Y_mod_3"] = all((b - round(12 * float(Fraction(a)))) % 3 == 0 for (a, b) in trial)
    print("11862", res["breaking"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
