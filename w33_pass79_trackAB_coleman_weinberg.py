#!/usr/bin/env python3
"""
PASS 79 — TRACK AB: COLEMAN-WEINBERG HIGGS MASS FROM W33
=========================================================

The W33 one-loop effective potential:

  V_CW(phi) = (1/64pi^2) * sum_i n_i * M_i(phi)^4 * [ln(M_i^2/mu^2) - 3/2]

where M_i(phi) = lambda_i * phi / sqrt(2) are field-dependent masses
from the GQ(3,3) eigenvalues, and phi is the Higgs field.

The physical Higgs mass:
  m_H^2 = d^2 V_CW / dphi^2 |_{phi=v_EW}

This is the W33 analogue of the Coleman-Weinberg mechanism for
radiative electroweak symmetry breaking.
"""

import numpy as np
import json

# Physical constants
V_EW   = 246.22   # GeV
M_H_PDG = 125.25  # GeV
SIGMA_H = 0.17    # GeV
MU_REN  = None    # set dynamically

# W33 parameters
sqrt97  = np.sqrt(97)
lambda1 = 12.0
lambda2 = (1 + sqrt97) / 2
lambda3 = 3.0
lambda4 = 1.0
epsilon = (lambda2 - 2*np.sqrt(7)) / (2*np.sqrt(7))
M_GUT   = 2.0e16
LAM_W33 = M_GUT * np.sqrt(epsilon)

# GQ(3,3) eigenvalue spectrum with multiplicities
SPECTRUM = [
    (12.0,        1),
    (lambda2,     9),
    (3.0,        10),
    (1.0,        10),
    (-1.0,        5),
    (-3.0,        4),
    (-4.0,        1),
]
assert sum(m for _, m in SPECTRUM) == 40


def V_CW(phi, mu_ren):
    """
    Coleman-Weinberg potential at field value phi.
    Uses lambda_i * phi / sqrt(2) as field-dependent mass for mode i.
    Only bosonic modes contribute (positive eigenvalues).
    Fermionic mirror modes (negative eigenvalues) enter with a minus sign.
    """
    V = 0.0
    for lam, n in SPECTRUM:
        M2 = (lam * phi / np.sqrt(2))**2
        if M2 < 1e-30:
            continue
        log_term = np.log(M2 / mu_ren**2) - 1.5
        sign = 1.0 if lam > 0 else -1.0   # fermions subtract
        V += sign * n * M2**2 * log_term / (64 * np.pi**2)
    return V


def dV2_dphi2(phi, mu_ren, dphi=1e-4):
    """Numerical second derivative of V_CW."""
    return (V_CW(phi+dphi, mu_ren) - 2*V_CW(phi, mu_ren) + V_CW(phi-dphi, mu_ren)) / dphi**2


def find_vev(mu_ren):
    """
    Find the VEV phi_0 where dV/dphi = 0 (not trivially phi=0).
    For the CW potential the true minimum is set by the renormalisation
    condition: we impose phi_0 = v_EW and mu = Lambda_W33.
    The CW Higgs mass is then m_H^2 = d^2V/dphi^2 at phi_0.
    """
    return V_EW


def analytic_mH_squared(phi, mu_ren):
    """
    Analytic formula for m_H^2 from differentiating V_CW twice:
    m_H^2 = d^2V/dphi^2 = (1/16pi^2) * sum_i n_i * lambda_i^4 * phi^2/2
                          * [ln(lambda_i^2 phi^2/(2 mu^2)) - 1]
            + (1/32pi^2) * sum_i n_i * lambda_i^4 * phi^2/2
    
    Simplified leading term:
    m_H^2 ~ (3/16pi^2) * sum_i_{bose} n_i * lambda_i^4 * v^2/2
             * [ln(lambda_i^2 v^2/(2 mu^2)) - 1]
    """
    mH2 = 0.0
    factor = phi**2 / 2.0
    for lam, n in SPECTRUM:
        M_i2 = lam**2 * factor
        if M_i2 < 1e-30:
            continue
        log_term = np.log(M_i2 / mu_ren**2) - 1.0
        sign = 1.0 if lam > 0 else -1.0
        # d^2/dphi^2 of n*M_i^4*log(...) / (64pi^2)
        # = n * [4*3*lambda_i^4*phi^2/4 * log + 4*lambda_i^4*phi^2/4] / (64pi^2)
        # = n * lambda_i^4 * phi^2 * (3*log + 1) / (16pi^2)
        mH2 += sign * n * lam**4 * phi**2 * (3*log_term + 1) / (16 * np.pi**2 * 2)
    return mH2


def scan_mu_for_mH():
    """
    Scan the renormalisation scale mu to find which value gives m_H = 125.25 GeV.
    Physical prediction: mu = Lambda_W33 (the W33 GUT scale).
    """
    results = []
    # Scan mu from M_Z to Lambda_W33
    for log_mu in np.linspace(np.log(91.2), np.log(LAM_W33), 500):
        mu = np.exp(log_mu)
        mH2 = analytic_mH_squared(V_EW, mu)
        if mH2 > 0:
            mH = np.sqrt(mH2)
            pull = (mH - M_H_PDG) / SIGMA_H
            results.append({
                "mu_GeV": mu,
                "log_mu_over_MZ": round(np.log(mu/91.2), 3),
                "mH_GeV": round(mH, 4),
                "pull": round(pull, 4),
                "abs_pull": abs(pull),
            })
    results.sort(key=lambda x: x['abs_pull'])
    return results


def w33_prediction_at_Lambda_W33():
    """The natural W33 prediction: mu = Lambda_W33."""
    mu = LAM_W33
    mH2 = analytic_mH_squared(V_EW, mu)
    mH2_numerical = dV2_dphi2(V_EW, mu)
    if mH2 > 0:
        mH_analytic = np.sqrt(abs(mH2))
    else:
        mH_analytic = None
    if mH2_numerical > 0:
        mH_numerical = np.sqrt(abs(mH2_numerical))
    else:
        mH_numerical = None
    return {
        "mu_GeV": mu,
        "mH2_analytic": mH2,
        "mH2_numerical": mH2_numerical,
        "mH_analytic_GeV": round(mH_analytic, 4) if mH_analytic else None,
        "mH_numerical_GeV": round(mH_numerical, 4) if mH_numerical else None,
        "pull_analytic": round((mH_analytic - M_H_PDG)/SIGMA_H, 4) if mH_analytic else None,
        "pull_numerical": round((mH_numerical - M_H_PDG)/SIGMA_H, 4) if mH_numerical else None,
    }


def main():
    print("=" * 72)
    print(" PASS 79 — TRACK AB: COLEMAN-WEINBERG HIGGS MASS")
    print("=" * 72)
    print(f"\n  Target: m_H = {M_H_PDG} ± {SIGMA_H} GeV")
    print(f"  Lambda_W33 = {LAM_W33:.4e} GeV")
    print(f"  epsilon = {epsilon:.6f}")
    print(f"  v_EW = {V_EW} GeV")

    # Natural prediction
    nat = w33_prediction_at_Lambda_W33()
    print(f"\n  W33 CW prediction at mu = Lambda_W33:")
    print(f"    m_H (analytic) = {nat['mH_analytic_GeV']} GeV  "
          f"(pull = {nat['pull_analytic']:+.4f})")
    print(f"    m_H (numerical) = {nat['mH_numerical_GeV']} GeV  "
          f"(pull = {nat['pull_numerical']:+.4f})")

    # Scan for best mu
    scan = scan_mu_for_mH()
    best = scan[0]
    within_1sig = [r for r in scan if r['abs_pull'] <= 1.0]
    print(f"\n  Best mu from scan:")
    print(f"    mu = {best['mu_GeV']:.4e} GeV  "
          f"(log(mu/M_Z) = {best['log_mu_over_MZ']})")
    print(f"    m_H = {best['mH_GeV']} GeV  (pull = {best['pull']:+.4f})")
    print(f"  Mus giving m_H within 1-sigma: {len(within_1sig)}")

    # Key result
    exact_match = nat['pull_analytic'] is not None and abs(nat['pull_analytic']) <= 1.0
    near_miss   = nat['pull_analytic'] is not None and abs(nat['pull_analytic']) <= 3.0
    verdict = "EXACT MATCH" if exact_match else "NEAR-MISS" if near_miss else "OFF-TARGET"
    print(f"\n  Verdict at mu = Lambda_W33: {verdict}")

    result = {
        "pass": 79,
        "track": "AB",
        "title": "Coleman-Weinberg Higgs Mass from W33",
        "target_mH": M_H_PDG,
        "sigma_H": SIGMA_H,
        "Lambda_W33_GeV": LAM_W33,
        "epsilon": round(epsilon, 6),
        "natural_prediction": nat,
        "best_from_scan": best,
        "n_within_1sigma": len(within_1sig),
        "verdict": verdict,
        "key_theorem": (
            f"W33 CW potential at mu=Lambda_W33: "
            f"m_H = {nat['mH_analytic_GeV']} GeV (pull {nat['pull_analytic']:+.3f}). "
            f"Verdict: {verdict}. "
            f"Best scan: m_H = {best['mH_GeV']} GeV at mu = {best['mu_GeV']:.3e} GeV."
        ),
        "status": "COMPLETE",
    }

    with open("w33_pass79_trackAB_coleman_weinberg.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n  Witness JSON -> w33_pass79_trackAB_coleman_weinberg.json")
    return result


if __name__ == "__main__":
    main()
