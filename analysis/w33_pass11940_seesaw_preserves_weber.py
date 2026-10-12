"""Pass 11940: the Weber invariant is seesaw-invariant -- the mechanism behind m1 m3/m2^2 = m_u m_t/m_c^2.

Correction to Pass 11939. Its shared-home relation cannot mean a shared Omega: if the Weinberg coefficient and the up
coupling were theta nulls of the same Omega they would be proportional, and the whole spectra would coincide
(m2/m3 = m_c/m_t = 3.6e-3 against 0.173 -- excluded by a factor 48). What the relation needs is a shared tau (the complex
structure of the two elliptic factors) with a channel-specific Omega12.

Mechanism. Type-I seesaw, m_nu = Y_D M^-1 Y_D, with the Dirac coupling Y_D and the Majorana coupling M both theta nulls of
swap-symmetric homes with the SAME tau and their own Omega12 (eps_D, eps_M). The heat-equation coefficients x^k/k! are
preserved:  x_nu = x_D^2 / x_M, so
  * R_nu = m1 m3/m2^2 = R(tau) = |f(tau)|^16/4, the same Weber invariant (to O(eps_M); 5 cases, relative error <= 3e-4
    for eps_M <= 1e-2),
  * the neutrino hierarchy parameter is eps_nu = eps_D^2/eps_M (m2/m3 matches kappa eps_D^2/eps_M to 1e-4).
So the complex structure is universal and the hierarchy parameters are channel-specific -- exactly what 11939 needs.

With Y_D = Y_u (SO(10)- / Pati-Salam-type Dirac unification) the right-handed spectrum follows, M_i = m_ui^2/m_nui:
  M = (1.9e6, 4.4e10, 5.7e14) GeV (M_Z-scale masses; running changes these by O(1) factors),
and M1 M3/M2^2 = R(tau) as well: one Weber invariant in all three matrices. M1 is far below the Davidson-Ibarra bound
(~1e9 GeV), so N1 thermal leptogenesis fails; this is the SO(10)-inspired structure, whose N2-dominated leptogenesis
(arXiv:1012.2343) allows, for normal ordering, m1 = 1-5 meV or 30-100 meV. The predicted m1 = 0.80 meV (0.67-0.97) sits
just below the lower window: marginal, recorded as a tension, not a success.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2  # noqa: E402

OUT = ROOT / "data" / "w33_pass11940_seesaw_preserves_weber.json"
P39 = ROOT / "data" / "w33_pass11939_symmetric_weber_neutrinos.json"
M_UP = (1.23e-3, 0.620, 168.26)                                 # GeV, M_Z


def Y(tau, eps):
    return theta_null_2(np.array([[tau, eps], [eps, tau]]), N=60).reshape(3, 3)


def sv(M):
    s = np.linalg.svd(M, compute_uv=False)
    return s / s[0]


def main():
    p39 = json.loads(P39.read_text())
    tau = p39["shared_home_tau"][0] + 1j * p39["shared_home_tau"][1]
    s0 = sv(Y(tau, 1e-4))
    R, kappa = float(s0[2] / s0[1] ** 2), float(s0[1] / 1e-4)
    rows = []
    for eD, eM in ((1e-3, 1e-2), (1e-3, 3e-3), (3e-4, 1e-3), (2e-3, 1e-2 * np.exp(1j)), (1e-3, 1e-1)):
        m = Y(tau, eD) @ np.linalg.inv(Y(tau, eM)) @ Y(tau, eD)
        s = sv(m)
        rows.append(dict(eps_D=abs(eD), eps_M=abs(eM), asym=float(np.abs(m - m.T).max() / np.abs(m).max()),
                         R_nu=float(s[2] / s[1] ** 2), s2=float(s[1]), s2_pred=float(kappa * abs(eD) ** 2 / abs(eM))))
    same = sv(Y(tau, 1e-3))
    nu = next(s for s in p39["spectra"]["up_MZ"] if s["ordering"] == "NO")["masses_meV"]
    mnu = [1e-12 * x for x in nu]                                # GeV
    M = [mu**2 / mn for mu, mn in zip(M_UP, mnu)]
    res = dict(pass_id=11940, tau=[tau.real, tau.imag], R_tau=R, kappa=kappa, seesaw=rows,
               shared_omega_ratios=dict(up_like=[float(x) for x in same], nu_needed_m2_over_m3=nu[1] / nu[2]),
               right_handed_GeV=M, rh_weber=M[0] * M[2] / M[1] ** 2, m1_meV=nu[0],
               so10_inspired_m1_windows_meV=[[1, 5], [30, 100]])
    res["checks"] = {k: bool(v) for k, v in dict(
        tau_reproduces_up_R=abs(R / p39["R_up"]["MZ"] - 1) < 1e-4,
        shared_omega_excluded=(nu[1] / nu[2]) / (0.620 / 168.26) > 10,
        seesaw_symmetric=all(r["asym"] < 1e-9 for r in rows),
        seesaw_preserves_R=all(abs(r["R_nu"] / R - 1) < 5e-4 for r in rows if r["eps_M"] <= 1e-2),
        seesaw_R_correction_is_O_epsM=abs(rows[-1]["R_nu"] / R - 1) > 10 * max(abs(r["R_nu"] / R - 1) for r in rows[:4]),
        eps_nu_is_epsD2_over_epsM=all(abs(r["s2"] / r["s2_pred"] - 1) < 2e-3 for r in rows if r["eps_M"] <= 1e-2),
        rh_spectrum_carries_same_invariant=abs(res["rh_weber"] / p39["R_up"]["MZ"] - 1) < 0.02,
        m1_just_below_so10_window=0.5 < nu[0] < 1.0,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"], R, kappa, ["%.3g" % x for x in M], res["rh_weber"])
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
