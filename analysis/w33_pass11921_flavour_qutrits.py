"""Pass 11921: the flux factorises W(3,3) into two flavour qutrits, and the radiatively preferred up Higgs is a flavour
qutrit.

1. Factorisation. For a det-3 dual pair (N10, N5 = 3 N10^{-1}) the translation groups of the two matter bundles inside
   A[3] = F3^4 (the W(3,3) space, Pass 11869) are K(L10) = l5 x l5 and K(L5) = l10 x l10, where l_N is the mod-3 image
   line of N. They are orthogonal, nondegenerate hyperbolic planes for the principal Weil pairing and A[3] = K10 + K5:
   a two-qutrit tensor factorisation chosen by the flux. The 10 is qutrit 1, the 5bar qutrit 2; the up Higgs (flux
   2 N10) has 3-torsion part exactly K10 and the down Higgs (flux m 1, gcd(m,3) = 1) has none.
   Consequences: the up Yukawa lives on qutrit 1 alone (monomial, Pass 11918); the down Yukawa is a two-qutrit theta
   state across the factorisation (Pass 11917).
2. Flavour-qutrit Higgs. The K10 translations act on Q, u^c and H_u and permute the three Z3 classes of up Higgs modes,
   so the top-Yukawa (Gram) eigenspace of the up Higgs is EXACTLY 3-dimensional for every modulus and Wilson line, and
   the cross-class Gram entries vanish. In it,  Y_u(h)_{ab} = h_{a+b} g_{a-b}  (a, b in Z3): the Higgs is a qutrit
   state h and g = (g0, g+, g-) are three theta values (g0 dominant; g+ = g- without GUT breaking). The down Gram top
   eigenvector is nondegenerate.
3. Correction to Pass 11918. Its "V_cb = 0 exactly in 87% of aligned rows" is wrong as stated: the small values are
   Gaussian suppression exp(-pi (m/3) Im|q|^2), not a selection rule. Of 12712 aligned rows of the (1,1,4) scan, 4550
   are below 1e-12 (the double-precision floor), 6483 between 1e-12 and 1e-5, 1679 above; V_cb scales like m_s/m_b
   (log-slope 1.04) with median prefactor 4e-7 (data: about 2). A re-run sample has V_cb = 6.1e-6, identical at theta
   truncation K = 4 and 7. The physical conclusion stands and sharpens: aligned mixing is Gaussian-suppressed far below
   the mass ratios.
4. Frozen qutrit scans (data/w33_pass11921_qutrit_scan_frozen.json; analysis/w33_pass11921_qutrit_scan.py), H_d radiative:
   (a) Haar: 12 stabiliser + 200 Haar-random h at 237 moduli (50244 rows): no row has realistic up masses (m_u/m_c and
   m_c/m_t within x3), although the CKM alone is reached in 257 rows; (b) targeted: at each of 87 moduli h is fitted
   (4 real dof, 3 orderings x 12 starts) to m_u/m_c, m_c/m_t, V_us, V_cb, V_ub -- best log-rms 1.54 (1,1,4) and 1.45 (A2),
   i.e. a factor ~4 per observable; the fitted m_c/m_t tracks eps = |g+/g0| (correlation 0.87, 0.97): the charm mass is
   floored by the off-diagonal theta value, and a small eps kills the mixing. The flavour-qutrit Higgs alone does not
   produce quark flavour.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402
import w33_pass11918_hypercharge_wilson_scan as S  # noqa: E402
import w33_pass11921_qutrit_scan as Q  # noqa: E402

OUT = ROOT / "data" / "w33_pass11921_flavour_qutrits.json"
FROZEN = ROOT / "data" / "w33_pass11921_qutrit_scan_frozen.json"
SUPP = ROOT / "data" / "w33_pass11921_mixing_suppression_frozen.json"
PAIRS = [([[1, 0], [0, 3]], [[3, 0], [0, 1]]), ([[2, 1], [1, 2]], [[2, -1], [-1, 2]]),
         ([[1, 1], [1, 4]], [[4, -1], [-1, 1]]), ([[3, 3], [3, 4]], [[4, -3], [-3, 3]])]


def line(N):
    M = np.array(N) % 3
    c = M[:, 0] if M[:, 0].any() else M[:, 1]
    return c % 3


def span2(u, v):
    return {tuple(int(t) for t in (a * u + b * v) % 3) for a in range(3) for b in range(3)}


def omega(p, q):
    return (p[0] * q[2] + p[1] * q[3] - p[2] * q[0] - p[3] * q[1]) % 3


def K(N):
    S_ = set()
    Ni = np.linalg.inv(np.array(N, float))
    for m in itertools.product(range(-3, 4), repeat=4):
        v = np.r_[Ni @ m[:2], Ni @ m[2:]]
        if np.allclose(3 * v, np.round(3 * v)):
            S_.add(tuple(int(t) for t in np.round(3 * v) % 3))
    return S_


def factorisation():
    out = []
    for N10, N5 in PAIRS:
        z = np.zeros(2, int)
        l10, l5 = line(N10), line(N5)
        K10, K5 = span2(np.r_[l5, z], np.r_[z, l5]), span2(np.r_[l10, z], np.r_[z, l10])
        out.append(dict(
            N10=N10, K_matches=K(N10) == K10 and K(N5) == K5,
            orthogonal=all(omega(p, q) == 0 for p in K10 for q in K5),
            nondegenerate=all(any(omega(p, q) for q in K10) for p in K10 if any(p))
            and all(any(omega(p, q) for q in K5) for p in K5 if any(p)),
            spans=len({tuple((np.array(p) + np.array(q)) % 3) for p in K10 for q in K5}) == 81,
            hu_part_is_K10=K((2 * np.array(N10)).tolist()) == K10,
            hd_neutral=K((np.array(N10) + np.array(N5)).tolist()) == {(0, 0, 0, 0)}))
    return out


def qutrit_structure(pair, seed):
    rng = np.random.default_rng(seed)
    N10 = S.PAIRS[pair]
    N5 = np.round(3 * np.linalg.inv(N10)).astype(int).tolist()
    Om = 1j * (1.1 * np.eye(2) + 0.15 * np.array(N10, float)) + 0.1 * np.eye(2)
    T = F.T4(Om, 12)

    def lat(v):
        return v[:2] + Om @ v[2:]

    P = S.positions(N10, N5, lat(rng.random(4)), lat(rng.random(4)), lat(rng.random(4) - 0.5))
    Ys = np.array(F.yukawas(T, N10, N10, P["Q"], P["u"]))
    M = Ys.reshape(len(Ys), 9)
    C = M.conj() @ M.T
    w = np.linalg.eigvalsh(C)[::-1] / np.linalg.eigvalsh(C)[-1]
    supp = [tuple(np.flatnonzero(abs(Y.ravel()) > 1e-9 * abs(Y).max())) for Y in Ys]
    cls = {}
    for k, s_ in enumerate(supp):
        cls.setdefault(s_, []).append(k)
    cross = max(abs(C[i, j]) for a in cls.values() for b in cls.values() if a is not b for i in a for j in b) / abs(C).max()
    g = {}
    for ks in cls.values():
        ww, vv = np.linalg.eigh(C[np.ix_(ks, ks)])
        Mk = np.tensordot(vv[:, -1], Ys[ks], 1)
        nz = np.argwhere(abs(Mk) > 1e-9 * abs(Mk).max())
        ksum = {int((a + b) % 3) for a, b in nz}
        assert len(ksum) == 1
        g[ksum.pop()] = {int((a - b) % 3): Mk[a, b] for a, b in nz}
    # same g up to a class phase: g_k(d) / g_0(d) independent of d
    ratios = [[g[k][d] / g[0][d] for d in range(3)] for k in (1, 2)]
    spread = max(float(np.ptp(abs(np.array(r))) / abs(np.array(r)).mean() + np.ptp(np.angle(np.array(r) / r[0]))) for r in ratios)
    Yd = np.array(F.yukawas(T, N10, N5, P["Q"], P["d"])).reshape(-1, 9)
    wd = np.linalg.eigvalsh(Yd.conj() @ Yd.T)
    gabs = sorted(abs(np.array(list(g[0].values()))) / max(abs(np.array(list(g[0].values())))))
    return dict(pair=pair, top_gram_eigs=[float(x) for x in w[:5]], cross_class=float(cross), classes=len(cls),
                supports_are_a_plus_b=sorted(g) == [0, 1, 2], same_g_up_to_phase_spread=spread,
                g_abs_normalised=[float(x) for x in gabs], down_gap_ratio=float(wd[-2] / wd[-1]))


def main():
    saved = F.NS
    F.NS = np.array([(a, b) for a in range(-6, 7) for b in range(-6, 7)])
    fac = factorisation()
    qs = [qutrit_structure(p, s) for p, s in (("A2", 31), ("114", 32), ("A2", 33))]
    F.NS = saved
    # correction: re-run sample 1 of the 11918 scan seed 1 with K = 4 and 7
    vcb = []
    for Kt in (4, 7):
        R = S.sample(1, 2, "114", only=[1], K=Kt)
        Ra = R[(R[:, 11] < 0.5) & (R[:, 12] < 0.2) & (R[:, 13] < 0.05)]
        vcb.append(float(Ra[:, 12].min()))
    sup = json.loads(SUPP.read_text())
    fz = json.loads(FROZEN.read_text()) if FROZEN.exists() else None
    res = dict(pass_id=11921, factorisation=fac, qutrit_structure=qs, rerun_min_aligned_vcb_K4_K7=vcb,
               mixing_suppression=sup, qutrit_scan=fz)
    checks = dict(
        factorisation_all_pairs=all(all(v for k, v in f.items() if k != "N10") for f in fac),
        up_top_space_exactly_three=all(abs(q["top_gram_eigs"][2] - 1) < 1e-9 and q["top_gram_eigs"][3] < 0.99 for q in qs),
        cross_class_zero=all(q["cross_class"] < 1e-12 and q["classes"] == 3 for q in qs),
        y_equals_h_aplusb_g_aminusb=all(q["supports_are_a_plus_b"] and q["same_g_up_to_phase_spread"] < 1e-8 for q in qs),
        down_radiative_unique=all(q["down_gap_ratio"] < 0.99 for q in qs),
        vcb_small_not_zero=vcb[0] > 1e-8 and abs(vcb[0] - vcb[1]) / vcb[0] < 1e-4,
        aligned_mixing_suppressed=sup["median_vcb_over_ms_mb"] < 1e-4,
    )
    # frozen qutrit scans, with one Haar sample and one fit row re-derived
    hz = Q.haar(fz["check_seed"], 1, "A2")[:12]
    res["haar_repro_max_diff"] = float(np.max(abs(hz - np.array(fz["check_rows_stabiliser_sample0"]))))
    fr = Q.fit(fz["fit_check"]["seed"], 1, fz["fit_check"]["pair"])[0]
    res["fit_repro_max_diff"] = float(np.max(abs(fr - np.array(fz["fit_check"]["row0"]))))
    hq, ft = fz["haar"], fz["fit"]
    checks.update(
        haar_never_realistic_up=all(hq[p]["up_masses_ok"] == 0 and hq[p]["ckm_ok_and_up_ok"] == 0 for p in ("114", "A2")),
        haar_ckm_alone_reachable=all(hq[p]["ckm_ok"] > 0 for p in ("114", "A2")),
        targeted_fit_fails=all(ft[p]["best_rms_log"] > 1.0 for p in ("114", "A2")),
        charm_floored_by_eps=all(ft[p]["corr_log_fitted_mc_mt_vs_log_eps"] > 0.8 for p in ("114", "A2")),
        scans_reproduce=res["haar_repro_max_diff"] < 1e-10 and res["fit_repro_max_diff"] < 1e-6,
    )
    res["checks"] = {k: bool(v) for k, v in checks.items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
