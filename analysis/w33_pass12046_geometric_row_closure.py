"""Pass 12046: closing the geometric Barr row. Torsion Wilson lines can only predict sin(delta); the CM points do not
"miss" the Weber invariant (only the elliptic ones do), but running makes any CM identification scale-dependent; and
under SM running, no branch of the 12045 theta-vector row matches the charged leptons at any matching scale from M_Z
to 2e16 GeV, with either lepton rule (Claude track).

1. CP STRENGTH. With |V_us|, |V_cb|, |V_ub| fixed, J = c12 s12 c23 s23 c13^2 s13 sin(delta), so
   |J| <= J_max = 3.44e-5 at the comparators, and the data need sin(delta) = 0.896. Any mechanism that fixes the CP
   phase discretely -- such as a Wilson line pinned at an order-3 or order-6 torsion point (Re w in Z/6, the
   quantised Wilson lines of Z3/Z6 orbifolds, 'calculable phases' of geometrical CP violation) -- predicts sin(delta)
   and nothing more. A random delta lands within 4% of the data 10% of the time, so such a test is weak.
   Frozen record: following branch A of 12045 by pseudo-arclength continuation of the five CP-even targets, J sweeps
   [9.0e-6, 3.44e-5] (it reaches J_max) while Re w stays in [-0.078, -0.049]; no torsion value is reached on the
   traced arc.
2. CM POINTS (correction of an over-read). Pass 11938 tested only the elliptic CM points (i, omega, 1+i), all giving
   W = m_u m_t/m_c^2 >= 1. The paper then wrote that the measured 0.54 is "missed by the CM points". On the CP line
   Re tau = 1, tau = 1 + i y is CM iff y^2 is rational, so CM points are dense there. Fitting eps_u to m_c/m_t at each
   one: the Eisenstein-field point tau = 1 + i sqrt3/2 (discriminant -48) gives W = 0.513, against 0.534 +- 3.5%
   (lattice m_u/m_c) at M_Z -- 1.1 sigma. But W runs: +13% from M_Z to 2e16 GeV in the SM (Codex 12011 running).
   Other CM points (D = -252 at 0.561, D = -80 at 0.600) match at higher matching scales. A CM identification of the
   up modulus therefore needs the matching scale; it is not a prediction.
3. LEPTON CLOSURE. Frozen record: branches A, B, C, D and G of 12045, each followed in the matching scale (12011 SM
   running, up home and six row parameters re-solved at each of 8 scales from M_Z to 2e16 GeV). Two lepton rules were
   used:
   (a) the 12007 shared SU(5) matching;
   (b) a colour-triplet-only heavy state (bare theta leptons, the E6 exotic-D option).
   No branch comes close at any scale under either rule. The best case anywhere remains branch C at M_Z under (a),
   where m_e m_mu/m_tau^2 = 0.66 x data; under running it stays between 0.52 and 0.72 x data, while its m_mu/m_tau
   rises to 0.27 against 0.059. Branches E and F are far off at M_Z. The charged-lepton ratios themselves do not run
   (one loop, SM).
Reading. The theta-vector Barr row of 12045 solves the quark sector, but it cannot also produce the charged leptons,
whatever the matching scale -- with the shared SU(5) matching or without it. The lepton sector needs structure the
row does not carry (a separate heavy lepton row, a different flux for the lepton partner, or non-minimal Clebsches).
Scope: the catalogued branches (search-based), one-loop SM running without thresholds, the 11942 homes. Not new:
Branco-Gerard-Grimus 1984 and de Medeiros Varzielas et al. (geometrical CP violation); Ibanez-Nilles-Quevedo 1987
(quantised orbifold Wilson lines); Codex 12011 (the running used here); 11938 (Weber law).
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, least_squares

ROOT = Path(__file__).resolve().parents[1]
for p in ("analysis", "analysis/search_drivers_12045", "analysis/search_drivers_12046"):
    sys.path.insert(0, str(ROOT / p))
import barrfit as B  # noqa: E402
import mcC as M  # noqa: E402
import w33_pass12011_12015_scale_flavour_internal_index as R  # noqa: E402
from jointlep import leptons  # noqa: E402
from w33_pass11942_hypercharge_wilson_leptons import DATA, LEPTONS, normalised, theta  # noqa: E402

OUT = ROOT / "data" / "w33_pass12046_geometric_row_closure.json"
SOL_C = np.array([0.995395, 0.44687, 1.105663, 5.106863, -0.003056, -6.817541])
SOL_A = np.array([-1.8444766914898252, 0.05894435138670266, 0.028382479377949063, 5.083585000284045, -0.0775199696196673, -0.3673566495323771])
W_LATTICE = (1.967e-3, 0.019)          # FLAG-era m_u/m_c and its relative error
SCALE_RECORD = {  # branch: list of (mu GeV, shared m_mu/m_tau, shared m_e/m_mu, comb ratio, bare m_mu/m_tau, bare m_e/m_mu) at 8 scales
    "A": [[91.2, 0.01934, 0.036362, 0.830, 0.00078, 0.175219], [2e16, 0.02215, 0.032268, 0.966, 0.00169, 0.156546]],
    "B": [[91.2, 0.52789, 0.000083, 1.419, 0.53140, 0.020014], [2e16, 0.40929, 0.000202, 2.065, 0.42310, 0.043545]],
    "C": [[91.2, 0.05739, 0.003293, 0.662, 0.05527, 0.198785], [1.28e8, 0.13269, 0.000673, 0.723, 0.10530, 0.049729],
          [2e16, 0.26956, 0.000117, 0.517, 0.22745, 0.007342]],
    "D": [[91.2, 0.12889, 0.001675, 1.698, 0.16408, 0.090661], [2e16, 0.13674, 0.002441, 2.785, 0.17014, 0.109438]],
    "G": [[91.2, 0.25451, 0.000490, 1.937, 0.29058, 0.076653], [2e16, 0.20789, 0.001058, 2.790, 0.30314, 0.095058]],
    "E_F_at_MZ": [[0.85854, 3.2e-06], [0.766254, 9.8e-06]],
    "comb_ratio_range_C": [0.517, 0.723]}
ARC_RECORD = dict(branch="A", points=464, rew_range=[-0.0778, -0.0494], J_range=[8.966e-06, 3.439e-05])


def jmax(vus, vcb, vub):
    s13 = vub
    c13 = np.sqrt(1 - s13 ** 2)
    s12, s23 = vus / c13, vcb / c13
    return np.sqrt(1 - s12 ** 2) * s12 * np.sqrt(1 - s23 ** 2) * s23 * c13 ** 2 * s13


def up_W(y, mcmt):
    def rat(e):
        O = np.array([[1 + 1j * y, 1j * e], [1j * e, 1 + 1j * y]])
        s = np.linalg.svd(theta(O), compute_uv=False)
        return s[1] / s[0], s[2] / s[1]
    e = brentq(lambda e: rat(e)[0] - mcmt, 1e-5, 0.3)
    r = rat(e)
    return r[1] / r[0], e


def targets(t):
    return dict(zip(R.NAMES, R.shape_observables(R.unpack(R.running().sol(t))[1])))


def follow_C_to(t_end, steps=8):
    x, pu = SOL_C.copy(), np.array([B.Y_UP, B.EU])
    for t in np.linspace(0, t_end, steps):
        tg = targets(t)
        q = {k: tg[k] for k in ("mc_mt", "mu_mc", "ms_mb", "md_ms", "Vus", "Vcb", "Vub", "J")}
        ru = least_squares(M.up_resid, pu, args=(q,), xtol=1e-15, ftol=1e-15)
        M.set_up(*ru.x)
        B.DATA = q
        rd = least_squares(B.resid, x, args=("shared",), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        assert np.abs(rd.fun).max() < 1e-9 and np.abs(rd.x - x).max() < 0.3
        x, pu = rd.x, ru.x
    a, b = leptons(x)
    Od = np.array([[B.TAU, 1j * x[1]], [1j * x[1], 1j * np.exp(x[0])]])
    s = np.linalg.svd(B.PH.conj()[:, None] * normalised(Od, (0, 6j * x[2])), compute_uv=False)
    M.set_up(B.Y_UP, B.EU)
    B.DATA = dict(DATA)
    return dict(shared=[float(a), float(b)], bare=[float(s[1] / s[0]), float(s[2] / s[1])],
                comb=float(b * a * a / (tg["me_mmu"] * tg["mmu_mtau"] ** 2)), targets=[float(tg["mmu_mtau"]), float(tg["me_mmu"])])


def main():
    checks, res = {}, {}
    jm = jmax(DATA["Vus"], DATA["Vcb"], DATA["Vub"])
    # independent check of the J formula on a random unitary CKM in standard parametrisation
    rng = np.random.default_rng(12046)
    t12, t23, t13, d = rng.uniform(.05, 1.4, 3).tolist() + [rng.uniform(0, 2 * np.pi)]
    c12, s12, c23, s23, c13, s13 = np.cos(t12), np.sin(t12), np.cos(t23), np.sin(t23), np.cos(t13), np.sin(t13)
    V = np.array([[c12 * c13, s12 * c13, s13 * np.exp(-1j * d)],
                  [-s12 * c23 - c12 * s23 * s13 * np.exp(1j * d), c12 * c23 - s12 * s23 * s13 * np.exp(1j * d), s23 * c13],
                  [s12 * s23 - c12 * c23 * s13 * np.exp(1j * d), -c12 * s23 - s12 * c23 * s13 * np.exp(1j * d), c23 * c13]])
    Jv = (V[0, 0] * V[1, 1] * V[0, 1].conj() * V[1, 0].conj()).imag
    res["cp_strength"] = dict(J_max=float(jm), sin_delta_data=float(DATA["J"] / jm), arc_record=ARC_RECORD,
                              formula_check=float(abs(abs(Jv) - jmax(abs(V[0, 1]), abs(V[1, 2]), abs(V[0, 2])) * abs(np.sin(d)))))
    checks["J = J_max sin(delta): J_max = 3.44e-5, data sin(delta) = 0.896; branch-A arc reaches J_max"] = bool(
        res["cp_strength"]["formula_check"] < 1e-12 and abs(jm - 3.44e-5) < 0.01e-5 and abs(DATA["J"] / jm - 0.896) < 0.003
        and abs(ARC_RECORD["J_range"][1] / jm - 1) < 0.01)

    mcmt = DATA["mc_mt"]
    W_data = W_LATTICE[0] / mcmt
    W_err = np.sqrt(W_LATTICE[1] ** 2 + 0.027 ** 2 + 0.005 ** 2)       # m_u/m_c, m_c(M_Z), m_t
    cm = {}
    for D, (p, q) in {-48: (3, 4), -80: (4, 5), -252: (7, 9), -24: (2, 3), -140: (5, 7)}.items():
        W, e = up_W(np.sqrt(p / q), mcmt)
        cm[str(D)] = dict(y2=f"{p}/{q}", W=float(W), eps_u=float(e), pull=float(np.log(W / W_data) / W_err))
    res["cm_points"] = dict(W_data=float(W_data), W_rel_err=float(W_err), table=cm)
    tmax = np.log(2e16 / R.MZ)
    W0 = targets(0)["mu_mc"] / targets(0)["mc_mt"]
    Wg = targets(tmax)["mu_mc"] / targets(tmax)["mc_mt"]
    res["W_running"] = dict(W_MZ=float(W0), W_2e16=float(Wg), ratio=float(Wg / W0))
    checks["CM correction: Eisenstein point D=-48 within 1.5 sigma at M_Z; W runs > 10% to 2e16, so CM fits are scale-dependent"] = bool(
        abs(cm["-48"]["pull"]) < 1.5 and abs(cm["-24"]["pull"]) > 5 and Wg / W0 > 1.10)

    rC0 = follow_C_to(0.0, steps=1)
    rCg = follow_C_to(tmax, steps=8)
    res["lepton_closure_recomputed"] = dict(C_MZ=rC0, C_2e16=rCg)
    res["lepton_closure_record"] = SCALE_RECORD
    L = (LEPTONS["mmu_mtau"], LEPTONS["me_mmu"])
    off = lambda pr: max(abs(np.log(pr[0] / L[0])), abs(np.log(pr[1] / L[1])))  # noqa: E731
    rec_ok = all(off([r[1], r[2]]) > 0.36 and off([r[4], r[5]]) > 0.36 for k in "ABCDG" for r in SCALE_RECORD[k])
    checks["no branch matches the leptons at any recorded scale under either rule (some ratio off by > 43%)"] = bool(
        rec_ok and off(rCg["shared"]) > 1 and off(rCg["bare"]) > 1 and abs(rC0["comb"] - 0.662) < 0.01 and abs(rCg["comb"] - 0.517) < 0.01)
    checks["lepton ratios do not run at one loop in the SM (control)"] = bool(abs(rCg["targets"][0] / L[0] - 1) < 1e-3)

    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
