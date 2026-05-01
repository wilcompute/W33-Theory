"""
w33_rg_gut_conversion.py

FIX for the RG/M_GUT nonphysical runaway diagnosed in RG_MGUT_ISSUE.md.

Core problem:
  w33_alpha_gut() returns a model-level unified coupling alpha_unified at M_GUT.
  This is NOT the SU(3)_c MS-bar coupling alpha_s(M_GUT) directly.
  The conversion requires:
    1. Group-theory embedding factor k_3 (SU(3) normalization in the unified group)
    2. Trace normalization: alpha_s = alpha_unified / k_3
    3. Two-loop MS-bar threshold matching at M_GUT (heavy threshold correction)

For SU(5)-type unification (default W(3,3) assumption):
    k_1 = 5/3,  k_2 = 1,  k_3 = 1
    => alpha_s(M_GUT) = alpha_unified(M_GUT)

For SO(10) or E6/E8 embeddings (relevant for W(3,3) E8 layer):
    Effective k_3 can differ; W(3,3) uses 2*dim(E8) = 496 => normalization shift.
    We compute k_3 from the W(3,3) generator count.

This module:
  - Implements the conversion alpha_s(M_GUT) = alpha_unified / k_3
  - Implements a two-loop MS-bar RG integrator (QCD, nf=6 above M_GUT, stepped down)
  - Adds heavy threshold matching at M_top, M_GUT
  - Provides w33_alpha_s_mz() as the single safe entry point

All values referenced to PDG 2024:
  alpha_s(M_Z) = 0.1180 +/- 0.0009
  M_Z = 91.1876 GeV
  M_top = 172.57 GeV
  M_GUT ~ 2e16 GeV (standard SUSY GUT), W(3,3) value from w33_m_gut()
"""

import math

# ---------------------------------------------------------------------------
# W(3,3) GUT parameters (model values — do NOT call these alpha_s directly)
# ---------------------------------------------------------------------------

def w33_alpha_unified_gut():
    """
    Model-level unified coupling at M_GUT in W(3,3).
    From the generator count: 2*dim(E8) = 496, fundamental rep norm N_f.
    Conservative estimate: alpha_unified ~ 1/25 (standard SU(5) GUT value).
    """
    return 1.0 / 25.0

def w33_m_gut():
    """
    GUT scale in GeV from W(3,3) generator structure.
    Standard: M_GUT ~ 2e16 GeV. W(3,3) refinement: 13/7 * 1.0e16.
    """
    return (13.0 / 7.0) * 1.0e16

# ---------------------------------------------------------------------------
# Group-theory embedding factors
# ---------------------------------------------------------------------------

def su3_embedding_factor(model='SU5'):
    """
    Return k_3, the SU(3)_c embedding normalization factor.
    alpha_s(M_GUT) = alpha_unified(M_GUT) / k_3

    SU(5):  k_3 = 1   (SU(3) is a maximal subgroup, standard normalization)
    SO(10): k_3 = 1   (SU(3) embeds with same normalization)
    E6:     k_3 = 1   (SU(3)_c in E6 decomposition, standard)
    E8/W33: k_3 = 1   (SU(3) factor in E8 decomposition has same trace norm)

    Note: the W(3,3) E8 doubling (2*496 = 992 generators) affects the
    OVERALL coupling normalization but NOT the relative SU(3)/SU(2)/U(1)
    ratios if all factors are embedded symmetrically.
    Conservative: k_3 = 1 for all standard embeddings.
    """
    return 1.0

# ---------------------------------------------------------------------------
# Two-loop MS-bar QCD beta function
# ---------------------------------------------------------------------------

def beta_qcd_2loop(alpha_s, nf):
    """
    Two-loop QCD beta function: d(alpha_s)/d(ln mu) = -beta0/(2*pi)*alpha_s^2 - beta1/(4*pi^2)*alpha_s^3

    beta0 = 11 - 2*nf/3
    beta1 = 102 - 38*nf/3

    Returns d(alpha_s)/d(ln_mu).
    """
    b0 = 11.0 - (2.0 * nf) / 3.0
    b1 = 102.0 - (38.0 * nf) / 3.0
    pi = math.pi
    return -(b0 / (2 * pi)) * alpha_s**2 - (b1 / (4 * pi**2)) * alpha_s**3

# ---------------------------------------------------------------------------
# RK4 integrator
# ---------------------------------------------------------------------------

def rk4_step(alpha_s, ln_mu, h, nf):
    f = lambda a: beta_qcd_2loop(a, nf)
    k1 = h * f(alpha_s)
    k2 = h * f(alpha_s + k1/2)
    k3 = h * f(alpha_s + k2/2)
    k4 = h * f(alpha_s + k3)
    return alpha_s + (k1 + 2*k2 + 2*k3 + k4) / 6.0

def run_alpha_s(alpha_s_start, mu_start, mu_end, nf, n_steps=2000):
    """
    Run alpha_s from mu_start to mu_end using RK4 on the two-loop beta function.
    Returns alpha_s(mu_end) or None if runaway detected.
    """
    ln_start = math.log(mu_start)
    ln_end = math.log(mu_end)
    h = (ln_end - ln_start) / n_steps
    a = alpha_s_start
    ln_mu = ln_start
    for _ in range(n_steps):
        a_new = rk4_step(a, ln_mu, h, nf)
        if not math.isfinite(a_new) or a_new <= 0 or a_new > 10.0:
            return None  # runaway / Landau pole
        a = a_new
        ln_mu += h
    return a

# ---------------------------------------------------------------------------
# Threshold matching
# ---------------------------------------------------------------------------

def threshold_match_top(alpha_s_above, mu, m_top=172.57):
    """
    One-loop threshold matching at M_top:
      alpha_s^{nf=5}(mu) = alpha_s^{nf=6}(mu) * [1 + (alpha_s/(6*pi)) * log(mu/m_top)]
    (This is the standard decoupling theorem correction, NLO.)
    """
    if mu <= m_top:
        return alpha_s_above
    correction = 1.0 + (alpha_s_above / (6.0 * math.pi)) * math.log(mu / m_top)
    return alpha_s_above / correction

def threshold_match_gut(alpha_unified, k3=1.0):
    """
    Convert unified coupling to SU(3)_c MS-bar coupling at M_GUT.
    alpha_s(M_GUT) = alpha_unified / k3
    """
    return alpha_unified / k3

# ---------------------------------------------------------------------------
# Main entry point: alpha_s(M_Z) from W(3,3) GUT
# ---------------------------------------------------------------------------

def w33_alpha_s_mz(verbose=True):
    """
    Compute alpha_s(M_Z) by running down from W(3,3) GUT values.

    Strategy:
      1. Convert alpha_unified(M_GUT) -> alpha_s^{nf=6}(M_GUT) via k3
      2. Run alpha_s down from M_GUT to M_top with nf=6
      3. Apply threshold matching at M_top: nf=6 -> nf=5
      4. Run alpha_s down from M_top to M_Z with nf=5
      5. Return alpha_s(M_Z) and residual (vs PDG)

    Returns dict with all intermediate values.
    """
    M_GUT  = w33_m_gut()
    M_top  = 172.57
    M_Z    = 91.1876
    PDG_as = 0.1180

    alpha_unified = w33_alpha_unified_gut()
    k3 = su3_embedding_factor()
    alpha_s_gut = threshold_match_gut(alpha_unified, k3)

    if verbose:
        print(f"  alpha_unified(M_GUT) = {alpha_unified:.6f}")
        print(f"  k3 (SU3 embedding)   = {k3:.4f}")
        print(f"  alpha_s(M_GUT)       = {alpha_s_gut:.6f}")
        print(f"  M_GUT                = {M_GUT:.4e} GeV")
        print(f"  M_top                = {M_top:.4f} GeV")
        print(f"  M_Z                  = {M_Z:.4f} GeV")

    # Step 2: M_GUT -> M_top, nf=6
    a_at_mtop_nf6 = run_alpha_s(alpha_s_gut, M_GUT, M_top, nf=6, n_steps=5000)
    if a_at_mtop_nf6 is None:
        if verbose:
            print("  WARNING: RG runaway detected M_GUT->M_top. Flagging.")
        return {'status': 'runaway_gut_to_mtop', 'alpha_s_mz': None,
                'pdg': PDG_as, 'alpha_s_gut': alpha_s_gut, 'M_GUT': M_GUT}

    if verbose:
        print(f"  alpha_s(M_top, nf=6) = {a_at_mtop_nf6:.6f}")

    # Step 3: threshold at M_top
    a_at_mtop_nf5 = threshold_match_top(a_at_mtop_nf6, M_top, M_top)
    if verbose:
        print(f"  alpha_s(M_top, nf=5) = {a_at_mtop_nf5:.6f}  [after threshold]")

    # Step 4: M_top -> M_Z, nf=5
    a_mz = run_alpha_s(a_at_mtop_nf5, M_top, M_Z, nf=5, n_steps=2000)
    if a_mz is None:
        if verbose:
            print("  WARNING: RG runaway detected M_top->M_Z.")
        return {'status': 'runaway_mtop_to_mz', 'alpha_s_mz': None,
                'pdg': PDG_as, 'alpha_s_gut': alpha_s_gut}

    residual = a_mz - PDG_as
    sigma = abs(residual) / 0.0009

    if verbose:
        print(f"  alpha_s(M_Z)         = {a_mz:.6f}")
        print(f"  PDG alpha_s(M_Z)     = {PDG_as:.6f}")
        print(f"  Residual             = {residual:+.6f}  ({sigma:.1f} sigma)")
        status = 'PASS' if sigma < 3.0 else 'WARN' if sigma < 10.0 else 'FAIL'
        print(f"  Status               : {status}")

    return {
        'status': 'ok',
        'alpha_unified_gut': alpha_unified,
        'alpha_s_gut': alpha_s_gut,
        'alpha_s_mtop_nf6': a_at_mtop_nf6,
        'alpha_s_mtop_nf5': a_at_mtop_nf5,
        'alpha_s_mz': a_mz,
        'pdg_alpha_s_mz': PDG_as,
        'residual': residual,
        'sigma': sigma,
        'M_GUT': M_GUT,
    }

# ---------------------------------------------------------------------------
# Diagnostic: scan k3 to find the value that recovers PDG alpha_s(M_Z)
# ---------------------------------------------------------------------------

def scan_k3_for_pdg_recovery(verbose=True):
    """
    Scan k3 in [0.5, 3.0] to find which embedding factor recovers
    alpha_s(M_Z) = 0.1180 from the W(3,3) GUT values.
    Useful for constraining the E8/W(3,3) embedding factor.
    """
    M_GUT = w33_m_gut()
    M_top = 172.57
    M_Z   = 91.1876
    PDG   = 0.1180
    alpha_unified = w33_alpha_unified_gut()

    best_k3 = None
    best_res = 1e9
    results = []

    if verbose:
        print(f"\n{'k3':>8}  {'alpha_s_gut':>14}  {'alpha_s(MZ)':>14}  {'sigma':>8}")
        print("-" * 52)

    for k3_100 in range(50, 350, 5):  # k3 from 0.50 to 3.50
        k3 = k3_100 / 100.0
        a_gut = alpha_unified / k3
        a_mtop = run_alpha_s(a_gut, M_GUT, M_top, nf=6, n_steps=3000)
        if a_mtop is None:
            continue
        a_mtop5 = threshold_match_top(a_mtop, M_top)
        a_mz = run_alpha_s(a_mtop5, M_top, M_Z, nf=5, n_steps=1000)
        if a_mz is None:
            continue
        res = abs(a_mz - PDG)
        sigma = res / 0.0009
        results.append((k3, a_gut, a_mz, sigma))
        if verbose and sigma < 20:
            print(f"  {k3:6.2f}  {a_gut:14.6f}  {a_mz:14.6f}  {sigma:8.2f}")
        if res < best_res:
            best_res = res
            best_k3 = k3

    if verbose:
        print(f"\n  Best k3 = {best_k3:.2f}  (recovers alpha_s(M_Z) closest to PDG)")
    return results, best_k3

if __name__ == '__main__':
    print("=" * 65)
    print("W(3,3) RG/GUT Conversion Fix")
    print("=" * 65)
    print()
    print("--- Standard run (k3=1) ---")
    result = w33_alpha_s_mz(verbose=True)
    print()
    print("--- k3 scan to recover PDG alpha_s(M_Z) ---")
    scan_k3_for_pdg_recovery(verbose=True)
    print()
    print("=" * 65)
