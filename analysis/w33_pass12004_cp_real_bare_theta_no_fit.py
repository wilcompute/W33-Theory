"""Pass 12004: the bare CP-real theta quark sector cannot fit the quark data -- so the vectorlike row of Pass 12005 is
necessary as well as sufficient: with exact generalized CP the theta flavour chain is a Nelson-Barr theory.

Setting (Passes 11938-11942, quark model of 11942). Up home [[tau, eps_u], [eps_u, tau]] Wilson-free; down home
[[tau, eps_d], [eps_d, tau_d]] sharing tau (the quark-doublet torus), with a Wilson line z_d on the 5bar factor only.

1. The CP-fixed locus (certified). For the theta-group generalized CP (Omega, z) -> (-conj Omega + 2B, -conj z + k/3)
   with integer diagonal B, the fixed locus is Re tau, Re tau_d in Z, Re eps = 0, Re z_d in Z/6. On it
        Y = Ph o conj(Y),  Ph[a, c] = exp(2 pi i (b1 a^2 + b2 c^2 + k c)/3),
   exactly (termwise), with the SAME left factor exp(2 pi i a^2/3) for up and down (b1 = Re tau = 1). Hence both
   Yukawas are real in one common left basis and J = 0 identically. Checked at 120 random locus points to 1e-11;
   off-locus control fails at O(1e-2).
2. The up sector fits exactly on the locus: tau = 1 + 0.8745 i, eps_u = 0.00552 i give m_c/m_t and m_u/m_c (the
   Weber point of Pass 11938 on the T^2-CP line).
3. Positive control: at that tau, an unrestricted COMPLEX down sector fits all five down observables (m_s/m_b, m_d/m_s,
   |V_us|, |V_cb|, |V_ub|) exactly.
4. The bare CP-real down sector at that tau does not fit. Frozen search record: a full-range grid of 746,496 points
   (24 discrete classes x 36 x 24 x 36: Im tau_d in [1e-4, 10], eps_d as a fraction of the positivity bound,
   Im z_d / Im tau_d in [-60, 60]) evaluated with a centred-window theta that is accurate in the cusp (agrees with the
   N = 40 reference to 2e-13 where both are valid), each class polished from its 20 best grid points: the global
   minimum is chi^2 = 329 for 5 observables and 3 parameters (m_s/m_b = 0.064 vs 0.0185, |V_ub| = 0.0025 vs 0.0038).
   The Codex 12005 bare point (B = 0) lies in the same class and scores far higher. An earlier N = 40 grid had found a
   lower value (257) deep in the cusp; it was a truncation artefact (357 with the accurate evaluator) and is discarded.
5. Letting tau move (sacrificing the up sector) the best compromise found by seeded multistart is chi^2 = 213, with
   m_u/m_c off by x13: the obstruction is CP-reality of the down sector, not the shared torus.
Reading. Within this model, exact theta-group CP forbids a bare fit; Pass 12005 shows one complex vectorlike down row
suffices. So the row is necessary and sufficient: CP violation must be spontaneous and transmitted by vectorlike mixing --
a Nelson-Barr theory, with tree-level theta-bar in {0, pi} (the branch is not fixed by the CP involution) because the
bare determinants are real in the common CP frame. Any CP-invariant moduli potential is stationary transverse to the
locus (symmetric criticality, Palais 1979; checked: all real-part gradients vanish to 1e-8 for a sample of flavour
invariants), so the CP locus is a natural, not tuned, place for the moduli; whether it is a minimum is not addressed.
Scope: T^2-type generalized CP (the 'integer real part' CP locus of Pass 11878); S-type CP on |tau| = 1 is not covered;
the down Wilson line on the 5bar factor only (Pass 11942 model); search-based no-fit (dense grid + polish), not a proof.
Generalized CP in Sp(4,Z): Ding-Feruglio-Liu arXiv:2010.07952; Nelson-Barr: Nelson 1984, Barr 1984, Bento-Branco-Parada
1991; modular Nelson-Barr: arXiv:2505.20395.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

OUT = ROOT / "data" / "w33_pass12004_cp_real_bare_theta_no_fit.json"
C12005 = ROOT / "data" / "w33_pass12005_cp_real_theta_barr.json"
Y_UP, E_UP = 0.8745, 0.00552
DD = dict(ms_mb=(0.053 / 2.86, .08), md_ms=(2.67e-3 / 0.053, .10), Vus=(0.2250, .003), Vcb=(0.0411, .025), Vub=(0.00382, .05))
UP = dict(mc_mt=0.620 / 168.26, mu_mc=1.23e-3 / 0.620)
FREE_X = {1: [-0.09194310637278653, 0.03630968602266146, 0.028703676090925827, -0.006649307001052142, -0.3069689543246789, -0.027697264203524294],
          -1: [0.09192368541490957, 0.03628943484042579, 0.028504658588154437, 0.007462360338104953, 0.6403237691849435, -0.02767110195194717]}
BARE_BEST = dict(sign=1, rtd=0, kz=2, x=[3.116, 0.4061, 12.86], chi2_record=329.0)
SEARCH_RECORD = dict(grid_points=746496, classes=24, global_min_chi2=329.0, artefact_discarded=dict(n40_value=257.5, accurate_value=356.7),
                     moving_tau_best_chi2=213.44, frozen_multistart_best_chi2=954.6)
A = np.arange(3)


def ph(b1, b2, k):
    return np.exp(2j * np.pi * (b1 * A[:, None] ** 2 + b2 * A[None, :] ** 2 + k * A[None, :]) / 3)


def theta_c(Om, z, n1max=10):
    """Centred-window level-3 genus-2 theta (accurate deep in the cusp); common positive rescaling dropped."""
    t1, e, t2 = Om[0, 0], Om[0, 1], Om[1, 1]
    y2 = t2.imag
    W = int(np.ceil(7.0 / np.sqrt(3 * np.pi * max(y2, 1e-6)))) + 4
    terms = []
    for a in range(3):
        for b in range(3):
            acc = []
            for n1 in range(-n1max, n1max + 1):
                v1 = n1 + a / 3
                c = -(z[1].imag + e.imag * v1) / y2
                v2 = np.arange(int(np.floor(c)) - W, int(np.ceil(c)) + W + 1) + b / 3
                acc.append(3j * np.pi * (t1 * v1 * v1 + 2 * e * v1 * v2 + t2 * v2 * v2) + 6j * np.pi * (v1 * z[0] + v2 * z[1]))
            ex = np.concatenate(acc)
            m = ex.real.max()
            terms.append((a, b, m, np.exp(ex - m).sum()))
    gmax = max(t[2] for t in terms)
    Y = np.zeros((3, 3), complex)
    for a, b, m, s in terms:
        Y[a, b] = s * np.exp(m - gmax)
    return Y


def up_left(sign):
    tau = 1 + 1j * Y_UP
    e = 1j * E_UP * sign
    return np.linalg.svd(P42.theta(np.array([[tau, e], [e, tau]])))[0]


def down_obs(Omd, zd, Uu):
    Ud, sd, _ = np.linalg.svd(theta_c(Omd, zd))
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    return dict(ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]))


def chi2(o, data):
    return float(sum((np.log(o[k] / v) / e) ** 2 for k, (v, e) in data.items()))


def main():
    rng = np.random.default_rng(12004)
    res = dict(pass_id=12004, search_record=SEARCH_RECORD)
    worst_u = worst_d = 0.0
    for _ in range(120):
        y, iu = rng.uniform(0.4, 1.5), rng.uniform(-0.02, 0.02)
        yd, idd = rng.uniform(0.02, 0.6), rng.uniform(-0.04, 0.04)
        zi = rng.uniform(-0.8, 0.8) * yd
        rtd, kz = int(rng.integers(0, 2)), int(rng.integers(0, 6))
        tau = 1 + 1j * y
        Omu = np.array([[tau, 1j * iu], [1j * iu, tau]])
        Omd = np.array([[tau, 1j * idd], [1j * idd, rtd + 1j * yd]])
        Yu, Yd = P42.theta(Omu), P42.theta(Omd, (0, kz / 6 + 1j * zi))
        worst_u = max(worst_u, np.abs(Yu - ph(1, 1, 0) * np.conj(Yu)).max() / np.abs(Yu).max())
        worst_d = max(worst_d, np.abs(Yd - ph(1, rtd, kz) * np.conj(Yd)).max() / np.abs(Yd).max())
    Yc = P42.theta(np.array([[1.05 + 0.8j, 0.003j], [0.003j, 1.05 + 0.8j]]))
    res["locus_relation_max_error"] = dict(up=float(worst_u), down=float(worst_d))
    res["off_locus_control_error"] = float(np.abs(Yc - ph(1, 1, 0) * np.conj(Yc)).max() / np.abs(Yc).max())
    s = np.linalg.svd(P42.theta(np.array([[1 + 1j * Y_UP, 1j * E_UP], [1j * E_UP, 1 + 1j * Y_UP]])), compute_uv=False)
    res["up_on_locus"] = dict(mc_mt=float(s[1] / s[0]), mu_mc=float(s[2] / s[1]))
    agree = 0.0
    for _ in range(20):
        yd = 10 ** rng.uniform(-1.4, 0)
        Om = np.array([[1 + 1j * Y_UP, 1j * rng.uniform(-0.3, 0.3) * np.sqrt(Y_UP * yd)], [0, int(rng.integers(0, 2)) + 1j * yd]])
        Om[1, 0] = Om[0, 1]
        z = (0, int(rng.integers(0, 6)) / 6 + 1j * rng.uniform(-3, 3) * yd)
        sa, sb = np.linalg.svd(P42.theta(Om, z), compute_uv=False), np.linalg.svd(theta_c(Om, z), compute_uv=False)
        agree = max(agree, float(np.abs(sa / sa[0] - sb / sb[0]).max()))
    res["centred_vs_reference_max_diff"] = agree
    pos = {}
    for sg, x in FREE_X.items():
        ydr, yd, edr, idd, zr, zi = x
        Omd = np.array([[1 + 1j * Y_UP, edr + 1j * idd], [edr + 1j * idd, ydr + 1j * yd]])
        pos[str(sg)] = chi2(down_obs(Omd, (0, zr + 1j * zi), up_left(sg)), DD)
    res["positive_control_complex_down_chi2"] = pos
    b = BARE_BEST
    Omd = np.array([[1 + 1j * Y_UP, 1j * b["x"][1]], [1j * b["x"][1], b["rtd"] + 1j * b["x"][0]]])
    ob = down_obs(Omd, (0, b["kz"] / 6 + 1j * b["x"][2]), up_left(b["sign"]))
    res["bare_best"] = dict(obs={k: float(v) for k, v in ob.items()}, chi2=chi2(ob, DD))
    c5 = json.loads(C12005.read_text())
    o5 = c5["bare_no_B_observables"]
    res["codex_12005_bare_point_chi2"] = chi2(o5, DD)
    res["codex_12005_status"] = c5["status"]
    h = 1e-6

    def V(x):
        rt, y, reu, iu, rtd_, yd, red, idd, rz, zi = x
        tau = rt + 1j * y
        Yu = P42.theta(np.array([[tau, reu + 1j * iu], [reu + 1j * iu, tau]]))
        Yd = P42.normalised(np.array([[tau, red + 1j * idd], [red + 1j * idd, rtd_ + 1j * yd]]), (0, rz + 1j * zi))
        Hu, Hd = Yu @ Yu.conj().T, Yd @ Yd.conj().T
        return float((np.trace(Hu @ Hu) + 0.3 * np.trace(Hd @ Hd @ Hd) + 0.7 * abs(np.linalg.det(Yu)) ** 2 + np.trace(Hu @ Hd)).real)
    x0 = np.array([1.0, Y_UP, 0.0, E_UP, 0.0, 0.43, 0.0, 0.08, 1 / 3, 0.0677])
    grad = []
    for i in range(10):
        e = np.zeros(10)
        e[i] = h
        grad.append((V(x0 + e) - V(x0 - e)) / (2 * h))
    grad = np.array(grad)
    res["cp_invariant_potential_gradient"] = dict(transverse_max=float(np.abs(grad[[0, 2, 4, 6, 8]]).max()),
                                                  longitudinal_max=float(np.abs(grad[[1, 3, 5, 7, 9]]).max()))
    G = res["cp_invariant_potential_gradient"]
    res["checks"] = {k: bool(v) for k, v in dict(
        cp_locus_relation_exact=max(worst_u, worst_d) < 1e-10 and res["off_locus_control_error"] > 1e-3,
        up_sector_fits_on_locus=all(abs(res["up_on_locus"][k] / UP[k] - 1) < 2e-3 for k in UP),
        centred_evaluator_validated=agree < 1e-10,
        positive_control_complex_down_fits=max(pos.values()) < 1e-6,
        bare_cp_real_down_does_not_fit=res["bare_best"]["chi2"] > 100 and abs(res["bare_best"]["chi2"] - b["chi2_record"]) < 5,
        codex_bare_point_above_global_minimum=res["codex_12005_bare_point_chi2"] > SEARCH_RECORD["global_min_chi2"],
        cp_locus_transversally_stationary=G["transverse_max"] < 1e-6 * G["longitudinal_max"],
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    print(res["bare_best"], res["codex_12005_bare_point_chi2"], res["positive_control_complex_down_chi2"], G, res["locus_relation_max_error"])


if __name__ == "__main__":
    main()
