"""Pass 12045: the Barr row as geometry. A level-3 theta vector on the 5bar torus turns the Nelson-Barr quark fit
into a square system with isolated solutions, with CP violation carried by one Wilson-line phase. Through the shared
SU(5) matching of Pass 12007 each solution then predicts the charged-lepton ratios. Every branch found is excluded or
in tension (Claude track).

Setting. Codex Pass 12005: CP-real theta Yukawas (the Pass 11942 homes on the T^2-CP locus of Pass 12004) plus ONE
complex vectorlike down row b = B/mu, matched by K = 1 - b^dag b/(1 + |b|^2) and H = m K m^T. There b is three free
complex numbers (5 real parameters after the removable overall phase): 3 + 5 = 8 down parameters for 6 down targets.
Codex 12007 adds the charged leptons with no new parameters: M_e = A^T Theta(Omega_d, 6 z_d)^T with A = sqrt K.

Ansatz (new). The row index of b is the d^c (5bar) index c, which is the index of the tau_d torus in the down theta.
So take
        b_c = lambda * theta_c(tau_d, w) * exp(-3 pi (Im w)^2 / Im tau_d),
        theta_c(tau, w) = sum_n exp(3 pi i tau (n + c/3)^2 + 6 pi i (n + c/3) w).
This is the level-3 genus-1 theta vector of the SAME 5bar torus, with one complex Wilson line w. The row term
B_c D d^c S is hypercharge-neutral, so w is the Wilson line of the CP-breaking scalar's U(1), not of hypercharge.
The down parameters are (Im tau_d, Im eps_d, Im z_d) + (lambda, Re w, Im w): 6 for 6 targets, a square system.

Results.
 1. EXACT, ISOLATED SOLUTIONS. Branch A has Im tau_d = 0.15807, eps_d = 0.058944 i, z_d = 0.028382 i, lambda = 161.4 and
    w = -0.07752 - 0.36736 i. All six down targets (m_s/m_b, m_d/m_s, |V_us|, |V_cb|, |V_ub|, J) fit to 1e-12, and
    the 6x6 Jacobian has full rank. Branches B and C, fitted the same way, are also exact and isolated. A broad-start
    catalogue (frozen record) found at least seven branches that are distinct up to symmetry. The other solutions of
    a branch are symmetry images (sign flips, quasi-period shifts of w) with identical observables.
 2. CP IS ONE NUMBER. Every bare modulus is on the CP locus, and J is an odd function of Re w alone. J = 0 exactly at
    Re w in Z/2, which is the heavy row's own CP-fixed set. Re w in +-1/6 + Z gives J != 0: a Z/3 shift of w is a right
    phase on the row that the light down matrix does not share.
 3. DETERMINANT IDENTITY (exact, independent of the row). With one heavy row and the shared matching, M_d = m A and
    M_e = A^T e, so det A cancels: |det M_e / det M_d| = |det e_bare / det d_bare| for every b (checked to 1e-11 for
    |b| from 0.16 to 135). The Barr row can redistribute masses within a sector, but cannot move this ratio.
 4. LEPTONS, BRANCH BY BRANCH, with no new parameters. The linear sensitivities d ln(lepton)/d ln(quark target) are
    propagated with the comparator errors (m_c/m_t 5%, m_u/m_c 20%, m_s/m_b 8%, m_d/m_s 10%, V_us 0.3%, V_cb 2.5%,
    V_ub 5%, J 4%):
      A: m_mu/m_tau = 0.0193, m_e/m_mu = 0.0364. The prediction is sharp (sigma_ln 0.08, 0.13), so A is excluded at
         13.6 sigma and 15.8 sigma.
      B: 0.528, 8.3e-5. Excluded at 6.3 sigma and 4.7 sigma.
      C: 0.0574, 0.00329, against data 0.0588, 0.00474. Each ratio alone is uninformative: sigma_ln is 2.2 and 4.4,
         dominated by the Weber invariant m_u m_t/m_c^2 (Pass 11938) and |V_us|. The two rows are nearly anti-parallel
         (d ln(m_e/m_mu) ~ -2 d ln(m_mu/m_tau) along the up inputs), so the Weber direction cancels in m_e m_mu/m_tau^2.
         That combination is sharp, and C predicts it at 0.66 x data. Exact nonlinear posterior (homotopy along C,
         5% theory error per lepton ratio): chi^2 = 2.8 for 2 constraints with the comparator errors. With lattice-
         precision quark ratios (m_s/m_b 1%, m_d/m_s 4%, m_u/m_c 5%, m_c/m_t 2%) chi^2 = 10.8, which is 2.8 sigma.
      Other catalogued branches give (0.129, 0.0017), (0.86, 3e-6), (0.77, 1e-5), (0.25, 4.9e-4).
 5. Finite heavy scale: the full 4x4 spectrum converges to the matched one (<= 1e-7 at mu = 10).
Controls. The 12005 and 12007 frozen points reproduce through this code (quarks to 5e-12, leptons exactly). theta1
equals the eps = 0 factor of the genus-2 theta to 5e-16. Theta truncations (N = 12/40, genus-2 N = 60) agree.
Corrections recorded. A first reading of branch C ("m_mu/m_tau within 2.4%") was not significant: propagated through
the quark errors, its prediction spans more than a decade. The first claim of uniqueness up to symmetry (from narrow
starts) was false: broad starts found more branches.
Reading. A geometric Barr row is enough for the quark sector. Two homes on the CP locus plus one theta-vector row give
all 8 quark data, with CP violation in a single Wilson-line phase. That is a fit (8 parameters for 8 data with the up
sector), not a prediction. With the 12007 shared SU(5) matching it becomes predictive for the charged leptons, and
there it fails: every branch found is excluded except C, which sits in 1.7-2.8 sigma tension through m_e m_mu/m_tau^2.
The row-independent determinant identity is why the tension survives any row: within a sector the row can move
masses, but not the e/d determinant ratio. If the theory error after RG running between the matching scale and M_Z is
nearer 10%, branch C is consistent. The concrete open item is therefore the common-scale running of
m_e m_mu/m_tau^2 versus the down ratios (cf. Codex 12011).
Scope: the 11942 homes and the 12005/12007 matching; one heavy row; the ansatz b = theta vector on the shared 5bar
torus; comparisons at the supplied M_Z values. The branch catalogue is search-based, and the sensitivities are linear
except the exact posterior on C.
Not new: Nelson-Barr (Nelson 1984; Barr 1984); single-vectorlike Nelson-Barr flavour (Cherchiglia-De Conto-Nishi
arXiv:2103.04798); modular Nelson-Barr (arXiv:2505.20395); theta-function Yukawas of magnetized tori (Cremades-Ibanez-
Marchesano 2004); 12005 (row), 12007 (shared matching), 11942 (homes, z_e = 6 z_d), 11938 (Weber invariant).
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
sys.path.insert(0, str(ROOT / "analysis" / "search_drivers_12045"))
import barrfit as B  # noqa: E402
from jointlep import leptons  # noqa: E402
from w33_pass11942_hypercharge_wilson_leptons import DATA, LEPTONS, theta  # noqa: E402

OUT = ROOT / "data" / "w33_pass12045_geometric_barr_row.json"
SOL = np.array([-1.8444766914898252, 0.05894435138670266, 0.028382479377949063, 5.083585000284045, -0.0775199696196673,
                -0.3673566495323771])
FIT12005 = np.array([-.8404552787929092, .08087153936666885, .0677453432123109, 6.942570225348479, 6.847783916520845,
                     -8.247969957747468, -.44792758573762237, -13.009011874237432])
FIT12007 = np.array([-.3497011260666278, .09754766874005429, .04188033188719437, 11.279482901951425, 8.059823963649515,
                     -1.904101410788516, -6.844437562070213, -11.79584423547314])
SOL_B = np.array([1.139142, -1.15415, -0.238268, 5.502257, 0.403614, -0.99549])
SOL_C = np.array([0.995395, 0.44687, 1.105663, 5.106863, -0.003056, -6.817541])
ERR = dict(mc_mt=.05, mu_mc=.20, ms_mb=.08, md_ms=.10, Vus=.003, Vcb=.025, Vub=.05, J=.04)
PRECISE = dict(mc_mt=.02, mu_mc=.05, ms_mb=.01, md_ms=.04, Vus=.003, Vcb=.025, Vub=.05, J=.04)
SEARCH_RECORD = dict(
    catalogue_distinct_branches_at_least=7,
    catalogue_keys=[[0.15811, 0.05894, 0.02838, 161.351, 0.019343, 0.0363623], [3.12, 1.15415, 0.238268, 245.2, 0.527886, 8.3e-5],
                    [2.70579, 0.44687, 1.10566, 165.152, 0.057392, 0.0032927], [2.5743, 0.79419, 1.54575, 121.143, 0.128886, 0.0016754],
                    [2.9767, 1.34809, 0.2709, 409.431, 0.85854, 3.2e-06], [3.03755, 1.34976, 0.29812, 420.875, 0.766254, 9.8e-06],
                    [3.09694, 1.15387, 0.25387, 204.068, 0.254507, 0.0004902]],
    key_fields="Im tau_d, |eps_d|, |Im z_d|, lambda, m_mu/m_tau, m_e/m_mu",
    pulls_sigma=dict(A=[13.62, -15.81], B=[-6.32, 4.72], C=[0.01, 0.08]),
    exact_posterior_C=dict(comparator_errors_th5=dict(chi2=2.814, weber_log_shift=-0.0432, weber_sigma=0.0526),
                           comparator_errors_th2=dict(chi2=3.412, weber_log_shift=-0.0502, weber_sigma=0.0537),
                           precise_errors_th5=dict(chi2=10.769, weber_log_shift=-0.0400, weber_sigma=0.0213)),
    first_reading_C_mc_spread="homotopy-tracked Monte Carlo: m_mu/m_tau 0.02-0.28, m_e/m_mu 3e-5-0.025 (not significant)")


def sensitivities(x0):
    """d ln(lepton ratios)/d ln(quark targets) along the branch through x0 (up home re-solved for up targets)."""
    import mcC as M
    from w33_pass11942_hypercharge_wilson_leptons import DATA as D0

    def solve(tgt, xs):
        ru = least_squares(M.up_resid, [B.Y_UP, B.EU], args=(tgt,), xtol=1e-15, ftol=1e-15)
        M.set_up(*ru.x)
        B.DATA = tgt
        rd = least_squares(B.resid, xs, args=("shared",), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        assert np.abs(rd.fun).max() < 1e-9 and np.abs(ru.fun).max() < 1e-9
        return rd.x
    x0 = solve(dict(D0), x0)
    out = {}
    for k in D0:
        tp, tm = dict(D0), dict(D0)
        tp[k] *= np.exp(1e-3)
        tm[k] *= np.exp(-1e-3)
        out[k] = ((np.log(leptons(solve(tp, x0))) - np.log(leptons(solve(tm, x0)))) / 2e-3).tolist()
    M.set_up(B.Y_UP, B.EU)
    B.DATA = dict(D0)
    return out


def invariants(x):
    return np.array([x[0], abs(x[1]), abs(x[2]), x[3], abs(((x[4] + 0.5) % 1) - 0.5)])


def main():
    checks, res = {}, {}
    r = least_squares(B.resid, SOL, args=("shared",), xtol=1e-15, ftol=1e-15, gtol=1e-15)
    x = r.x
    m = B.down_real(*x[:3])
    b = B.brow(x, "shared")
    o = B.obs(m, b)
    res["solution"] = dict(x=x.tolist(), Im_tau_d=float(np.exp(x[0])), eps_d=float(x[1]), Im_z_d=float(x[2]), lam=float(np.exp(x[3])),
                           w=[float(x[4]), float(x[5])], abs_b=float(np.linalg.norm(b)), observables={k: float(v) for k, v in o.items()})
    checks["geometric row fits all six down targets exactly (square 6x6 system)"] = bool(np.abs(r.fun).max() < 1e-9)

    Jm = np.array([(B.resid(x + 1e-6 * e, "shared") - B.resid(x - 1e-6 * e, "shared")) / 2e-6 for e in np.eye(6)]).T
    sv = np.linalg.svd(Jm, compute_uv=False)
    res["jacobian_singular_values"] = sv.tolist()
    checks["isolated: 6x6 Jacobian of full rank"] = bool(sv[-1] > 1e-2)

    b40 = np.exp(x[3]) * B.theta1(1j * np.exp(x[0]), x[4] + 1j * x[5], N=40) * np.exp(-3 * np.pi * x[5] ** 2 / np.exp(x[0]))
    Od = np.array([[B.TAU, 1j * x[1]], [1j * x[1], 1j * np.exp(x[0])]])
    n = np.arange(-60, 61)
    xx, yy = np.meshgrid(n, n, indexing="ij")
    D60 = np.array([[np.exp(3j * np.pi * (Od[0, 0] * (xx + a / 3) ** 2 + 2 * Od[0, 1] * (xx + a / 3) * (yy + c / 3) + Od[1, 1] * (yy + c / 3) ** 2)
                            + 6j * np.pi * (yy + c / 3) * 1j * x[2]).sum() for c in range(3)] for a in range(3)])
    T = theta(Od, (0, 1j * x[2]))
    fac = theta(np.array([[1 + .9j, 0], [0, .4j]]), (0, .05 + .03j)) / np.outer(B.theta1(1 + .9j, 0), B.theta1(.4j, .05 + .03j))
    res["accuracy"] = dict(theta1_N12_vs_N40=float(np.abs(b - b40).max() / np.abs(b).max()),
                           genus2_vs_N60=float(np.abs(T / np.linalg.norm(T) - D60 / np.linalg.norm(D60)).max()),
                           theta1_is_genus2_factor=float(np.abs(fac - fac[0, 0]).max()))
    checks["theta evaluations accurate (truncation, genus-2 factorisation)"] = bool(max(res["accuracy"].values()) < 1e-12)

    cp = {}
    for rw in (0.0, 0.5, -0.5, 1.0, 1 / 6, -1 / 6, 1 / 3):
        xc = x.copy()
        xc[4] = rw
        cp[f"{rw:.4f}"] = B.obs(m, B.brow(xc, "shared"))["J"]
    xm = x.copy()
    xm[4] = -x[4]
    res["J_vs_Re_w"] = cp
    checks["CP is one number: J = 0 at Re w in Z/2, nonzero at +-1/6, odd in Re w"] = bool(
        max(abs(cp[k]) for k in ("0.0000", "0.5000", "-0.5000", "1.0000")) < 1e-15 and min(abs(cp["0.1667"]), abs(cp["0.3333"])) > 1e-6
        and abs(B.obs(m, B.brow(xm, "shared"))["J"] + o["J"]) < 1e-15)

    dec = []
    K = np.eye(3) - np.outer(b.conj(), b) / (1 + np.vdot(b, b).real)
    sd = np.linalg.svd(m @ np.linalg.cholesky(K), compute_uv=False)
    for mu in (10., 100., 1000.):
        full = np.zeros((4, 4), complex)
        full[:3, :3] = m
        full[3, :3] = mu * b
        full[3, 3] = mu
        sf = np.linalg.svd(full, compute_uv=False)
        dec.append(float(np.abs(sf[1:] / sd - 1).max()))
    res["finite_mu_spectrum_error"] = dec
    checks["finite heavy scale: 4x4 light spectrum converges to the matched one"] = bool(max(dec) < 1e-6)

    images = [np.array([-1.844477, -0.058944, -0.028382, 5.083585, 0.07752, 0.683573]),
              np.array([-1.844477, -0.058944, 0.028382, 5.083585, -1.07752, 0.106967]),
              np.array([-1.844477, -0.058944, 0.028382, 5.083585, -0.07752, -0.051141]),
              np.array([-1.84448, 0.05894, -0.02838, 5.08359, 0.07752, -0.58129])]
    imgs = []
    for xi in images:
        ri = least_squares(B.resid, xi, args=("shared",), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        lp = leptons(ri.x)
        imgs.append(dict(resid=float(np.abs(ri.fun).max()), inv_diff=float(np.abs(invariants(ri.x) - invariants(x)).max()),
                         lepton_diff=float(max(abs(lp[0] - leptons(x)[0]), abs(lp[1] - leptons(x)[1])))))
    res["symmetry_images"] = imgs
    checks["the other exact solutions found are symmetry images (same invariants, same leptons)"] = bool(
        all(d["resid"] < 1e-9 and d["inv_diff"] < 1e-8 and d["lepton_diff"] < 1e-9 for d in imgs))

    # determinant identity: |det M_e / det M_d| is independent of the row
    Od0 = np.array([[B.TAU, 1j * x[1]], [1j * x[1], 1j * np.exp(x[0])]])
    from w33_pass11942_hypercharge_wilson_leptons import normalised
    d0 = (B.PH.conj()[:, None] * normalised(Od0, (0, 1j * x[2]))).real
    e0 = (B.PH.conj()[:, None] * normalised(Od0, (0, 6j * x[2]))).real
    rng = np.random.default_rng(12045)
    ratios = []
    for _ in range(5):
        bb = (rng.normal(size=3) + 1j * rng.normal(size=3)) * 10 ** rng.uniform(-1, 2.5)
        Kb = np.eye(3) - np.outer(bb.conj(), bb) / (1 + np.vdot(bb, bb).real)
        ev, Ob = np.linalg.eigh(Kb)
        Ab = (Ob * np.sqrt(ev)) @ Ob.conj().T
        ratios.append(np.prod(np.linalg.svd(Ab.T @ e0.T, compute_uv=False)) / np.prod(np.linalg.svd(d0 @ Ab, compute_uv=False)))
    target = abs(np.linalg.det(e0) / np.linalg.det(d0))
    res["determinant_identity"] = dict(det_ratio=float(target), max_rel_dev=float(max(abs(r / target - 1) for r in ratios)))
    checks["determinant identity: |det M_e/det M_d| = |det e/det d| for any row"] = bool(res["determinant_identity"]["max_rel_dev"] < 1e-9)

    # branches A, B, C: exact, isolated, and their parameter-free lepton predictions
    br = {}
    for name, xs in (("A", x), ("B", SOL_B), ("C", SOL_C)):
        rb = least_squares(B.resid, xs, args=("shared",), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        Jb = np.array([(B.resid(rb.x + 1e-6 * e, "shared") - B.resid(rb.x - 1e-6 * e, "shared")) / 2e-6 for e in np.eye(6)]).T
        lb = leptons(rb.x)
        br[name] = dict(x=rb.x.tolist(), resid=float(np.abs(rb.fun).max()), jac_min_sv=float(np.linalg.svd(Jb, compute_uv=False)[-1]),
                        mmu_mtau=float(lb[0]), me_mmu=float(lb[1]), emu_over_tau2_ratio=float(lb[1] * lb[0] ** 2 / (LEPTONS["me_mmu"] * LEPTONS["mmu_mtau"] ** 2)))
    res["branches"] = br
    checks["branches A, B, C: exact (1e-9) and isolated (full-rank Jacobian), pairwise distinct"] = bool(
        all(v["resid"] < 1e-9 and v["jac_min_sv"] > 1e-2 for v in br.values())
        and len({round(v["x"][0], 3) for v in br.values()}) == 3)

    data_l = np.log([LEPTONS["mmu_mtau"], LEPTONS["me_mmu"]])
    pulls = {}
    for name in ("A", "C"):
        S = sensitivities(np.array(br[name]["x"]))
        Sm = np.array([S[k] for k in ERR])
        sig = np.sqrt(((Sm * np.array(list(ERR.values()))[:, None]) ** 2).sum(0))
        pred = np.log([br[name]["mmu_mtau"], br[name]["me_mmu"]])
        comb = Sm[:, 1] + 2 * Sm[:, 0]
        pulls[name] = dict(sensitivities=S, sigma_ln=sig.tolist(), pulls=((data_l - pred) / sig).tolist(),
                           comb_sigma_comparator=float(np.sqrt(((comb * np.array(list(ERR.values()))) ** 2).sum())),
                           comb_sigma_precise=float(np.sqrt(((comb * np.array(list(PRECISE.values()))) ** 2).sum())))
    res["lepton_tests"] = pulls
    checks["branch A predicts the leptons sharply and is excluded (> 10 sigma on both ratios)"] = bool(
        min(abs(p) for p in pulls["A"]["pulls"]) > 10)
    checks["branch B excluded (lepton ratios off by > x8 and < x0.05)"] = bool(
        br["B"]["mmu_mtau"] / LEPTONS["mmu_mtau"] > 8 and br["B"]["me_mmu"] / LEPTONS["me_mmu"] < 0.05)
    cC = pulls["C"]
    checks["branch C: single ratios uninformative (sigma_ln > 1), but m_e m_mu/m_tau^2 sharp and low (0.66 x data)"] = bool(
        min(cC["sigma_ln"]) > 1 and cC["comb_sigma_precise"] < 0.1 and cC["comb_sigma_comparator"] < 0.3
        and abs(br["C"]["emu_over_tau2_ratio"] - 0.662) < 0.01)

    c5 = np.abs(B.resid(FIT12005, "row")).max()
    l7 = leptons(FIT12007, "row")
    res["controls"] = dict(row_12005_quark_resid=float(c5), row_12007_quark_resid=float(np.abs(B.resid(FIT12007, "row")).max()),
                           row_12007_leptons=[float(l7[0]), float(l7[1])])
    checks["positive controls: 12005 and 12007 frozen points reproduce (quarks, leptons)"] = bool(
        c5 < 1e-10 and abs(l7[0] / LEPTONS["mmu_mtau"] - 1) < 1e-8 and abs(l7[1] / LEPTONS["me_mmu"] - 1) < 1e-8)

    res["search_record"] = SEARCH_RECORD
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
