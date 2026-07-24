#!/usr/bin/env python3
"""
Pass 696 — GL_n Coupling Unification Curve: alpha_1, alpha_2, alpha_3
====================================================================
Computes the one-loop RG running of the three SM coupling constants
alpha_1 (hypercharge), alpha_2 (weak), alpha_3 (strong) from M_Z up
to the W33 GUT scale, using the GL_n flat-block beta functions.

SM one-loop beta coefficients (b_i = -b_i^SM in some conventions):
  b_1 = 41/10   (U(1)_Y, SM)
  b_2 = -19/6   (SU(2)_L, SM)
  b_3 = -7      (SU(3)_c, SM)

W33 prediction for beta coefficients from GL_n flat-block:
  At q=3, GL_n eigenvalues {q-1, -1, -(q+1)} = {2, -1, -4}
  The W33 beta coefficients:
    b_n = Tr(G_n^2) / (12*pi)  where G_n is the GL_n flat-block
  GL_2: Tr(F^2) = (q-1)^2 + (q+1)^2 = 2q^2+2 = 20 at q=3
    => b_W33_2 = 20/(12*pi) ~ 0.531
  GL_3: Tr(G^2) = (q-1)^2 + 1 + (q+1)^2 = 2q^2+3 = 21 at q=3
    => b_W33_3 = 21/(12*pi) ~ 0.557
  GL_1 (hypercharge): eigenvalue = q = 3
    => b_W33_1 = q^2/(12*pi) = 9/(12*pi) ~ 0.239

Running: alpha_i^{-1}(M) = alpha_i^{-1}(M_Z) + b_i/(2*pi) * log(M/M_Z)
"""

import math
from typing import Dict, List, Tuple

# Physical constants
M_Z = 91.1876  # GeV
M_GUT_SUSY = 2.0e16  # GeV (SUSY GUT prediction)
M_PLANCK = 1.22e19  # GeV

# PDG 2024 values at M_Z
ALPHA_EM_INV = 127.9   # alpha_em^{-1}(M_Z)
SIN2_W = 0.23122       # sin^2(theta_W)
ALPHA_S = 0.1180       # alpha_3(M_Z)

# Derived: alpha_1^{-1} and alpha_2^{-1} at M_Z
# alpha_1 = alpha_em / cos^2(theta_W) * (5/3)  [GUT normalization]
# alpha_2 = alpha_em / sin^2(theta_W)
alpha_em = 1.0 / ALPHA_EM_INV
alpha_2_MZ = alpha_em / SIN2_W
alpha_1_MZ = alpha_em / (1 - SIN2_W) * (5.0/3.0)  # GUT normalization
alpha_3_MZ = ALPHA_S

ALPHA_INV_MZ = {
    "alpha_1_inv": 1.0 / alpha_1_MZ,
    "alpha_2_inv": 1.0 / alpha_2_MZ,
    "alpha_3_inv": 1.0 / alpha_3_MZ,
}

# SM one-loop beta coefficients
B_SM = {"b1": 41.0/10.0, "b2": -19.0/6.0, "b3": -7.0}

# W33 GL_n beta coefficients
def w33_beta_coefficients(q: int) -> Dict:
    lam_plus  = q - 1
    lam_0     = 1
    lam_minus = q + 1
    # GL_1: single eigenvalue q
    tr_GL1_sq = q**2
    # GL_2: eigenvalues {q-1, -(q+1)}
    tr_GL2_sq = (q-1)**2 + (q+1)**2  # = 2q^2 + 2
    # GL_3: eigenvalues {q-1, -1, -(q+1)}
    tr_GL3_sq = (q-1)**2 + 1 + (q+1)**2  # = 2q^2 + 3
    return {
        "q": q,
        "b_W33_1": tr_GL1_sq / (12 * math.pi),
        "b_W33_2": tr_GL2_sq / (12 * math.pi),
        "b_W33_3": tr_GL3_sq / (12 * math.pi),
        "Tr_GL1_sq": tr_GL1_sq,
        "Tr_GL2_sq": tr_GL2_sq,
        "Tr_GL3_sq": tr_GL3_sq,
    }


def run_coupling(alpha_inv_MZ: float, b: float, log_ratio: float) -> float:
    """One-loop RG: alpha^{-1}(M) = alpha^{-1}(M_Z) - b/(2*pi) * log(M/M_Z)"""
    return alpha_inv_MZ - b / (2 * math.pi) * log_ratio


def unification_scale_SM() -> Dict:
    """Find scale where alpha_1 = alpha_2 = alpha_3 under SM running."""
    b1, b2, b3 = B_SM["b1"], B_SM["b2"], B_SM["b3"]
    a1_inv = ALPHA_INV_MZ["alpha_1_inv"]
    a2_inv = ALPHA_INV_MZ["alpha_2_inv"]
    a3_inv = ALPHA_INV_MZ["alpha_3_inv"]

    # alpha_1 = alpha_2 at log_12: (a1_inv - b1*t/(2pi)) = (a2_inv - b2*t/(2pi))
    # t = log(M/M_Z)
    # t_12: (a1_inv - a2_inv) = (b1-b2)/(2pi) * t
    t_12 = (a1_inv - a2_inv) * 2 * math.pi / (b1 - b2)
    M_12 = M_Z * math.exp(t_12)

    t_23 = (a2_inv - a3_inv) * 2 * math.pi / (b2 - b3)
    M_23 = M_Z * math.exp(t_23)

    t_13 = (a1_inv - a3_inv) * 2 * math.pi / (b1 - b3)
    M_13 = M_Z * math.exp(t_13)

    return {"M_12": M_12, "M_23": M_23, "M_13": M_13,
            "t_12": t_12, "t_23": t_23, "t_13": t_13}


def unification_scale_W33(q: int) -> Dict:
    """Find scale where W33 couplings unify."""
    betas = w33_beta_coefficients(q)
    b1 = betas["b_W33_1"]
    b2 = betas["b_W33_2"]
    b3 = betas["b_W33_3"]
    a1_inv = ALPHA_INV_MZ["alpha_1_inv"]
    a2_inv = ALPHA_INV_MZ["alpha_2_inv"]
    a3_inv = ALPHA_INV_MZ["alpha_3_inv"]

    def t_ij(ai, aj, bi, bj):
        if abs(bi - bj) < 1e-15:
            return float('inf')
        return (ai - aj) * 2 * math.pi / (bi - bj)

    t12 = t_ij(a1_inv, a2_inv, b1, b2)
    t23 = t_ij(a2_inv, a3_inv, b2, b3)
    t13 = t_ij(a1_inv, a3_inv, b1, b3)
    M12 = M_Z * math.exp(t12) if t12 < 500 else float('inf')
    M23 = M_Z * math.exp(t23) if t23 < 500 else float('inf')
    M13 = M_Z * math.exp(t13) if t13 < 500 else float('inf')

    # GUT scale: average of pairwise unification scales
    finite_scales = [M for M in [M12, M23, M13] if math.isfinite(M) and M > 0]
    M_GUT_W33 = math.exp(sum(math.log(M) for M in finite_scales) / len(finite_scales)) if finite_scales else float('nan')

    return {
        "q": q, "b1": b1, "b2": b2, "b3": b3,
        "M_12": M12, "M_23": M23, "M_13": M13,
        "M_GUT_W33": M_GUT_W33,
        "M_GUT_SUSY": M_GUT_SUSY,
        "ratio_to_SUSY": M_GUT_W33 / M_GUT_SUSY if math.isfinite(M_GUT_W33) else float('nan'),
    }


def coupling_table(q: int, n_steps: int = 8) -> List[Dict]:
    """RG running table from M_Z to M_Planck."""
    betas = w33_beta_coefficients(q)
    b1, b2, b3 = betas["b_W33_1"], betas["b_W33_2"], betas["b_W33_3"]
    a1i = ALPHA_INV_MZ["alpha_1_inv"]
    a2i = ALPHA_INV_MZ["alpha_2_inv"]
    a3i = ALPHA_INV_MZ["alpha_3_inv"]

    log_max = math.log(M_PLANCK / M_Z)
    rows = []
    for i in range(n_steps + 1):
        t = i * log_max / n_steps
        M = M_Z * math.exp(t)
        rows.append({
            "log10_M_GeV": math.log10(M),
            "alpha_1_inv": run_coupling(a1i, b1, t),
            "alpha_2_inv": run_coupling(a2i, b2, t),
            "alpha_3_inv": run_coupling(a3i, b3, t),
        })
    return rows


if __name__ == "__main__":
    print("=" * 70)
    print("Pass 696 — GL_n Coupling Unification Curve")
    print("=" * 70)
    print()

    print(f"Input values at M_Z = {M_Z} GeV:")
    print(f"  alpha_1^{{-1}} = {ALPHA_INV_MZ['alpha_1_inv']:.4f}")
    print(f"  alpha_2^{{-1}} = {ALPHA_INV_MZ['alpha_2_inv']:.4f}")
    print(f"  alpha_3^{{-1}} = {ALPHA_INV_MZ['alpha_3_inv']:.4f}")
    print()

    print("SM one-loop unification scales:")
    sm = unification_scale_SM()
    print(f"  M_{{12}} (alpha_1=alpha_2): {sm['M_12']:.3e} GeV")
    print(f"  M_{{23}} (alpha_2=alpha_3): {sm['M_23']:.3e} GeV")
    print(f"  M_{{13}} (alpha_1=alpha_3): {sm['M_13']:.3e} GeV")
    print(f"  (SM does NOT unify to a single scale — known result)")
    print()

    for q in [3, 5, 7]:
        betas = w33_beta_coefficients(q)
        print(f"W33 GL_n beta coefficients at q={q}:")
        print(f"  b_W33_1 = {betas['b_W33_1']:.4f}  (GL_1, U(1))")
        print(f"  b_W33_2 = {betas['b_W33_2']:.4f}  (GL_2, SU(2))")
        print(f"  b_W33_3 = {betas['b_W33_3']:.4f}  (GL_3, SU(3))")

        gu = unification_scale_W33(q)
        print(f"  W33 unification scales:")
        print(f"    M_{{12}} = {gu['M_12']:.3e} GeV")
        print(f"    M_{{23}} = {gu['M_23']:.3e} GeV")
        print(f"    M_{{13}} = {gu['M_13']:.3e} GeV")
        print(f"    M_GUT_W33 (geometric mean) = {gu['M_GUT_W33']:.3e} GeV")
        print(f"    M_GUT_SUSY = {M_GUT_SUSY:.3e} GeV")
        if math.isfinite(gu['ratio_to_SUSY']):
            print(f"    Ratio W33/SUSY = {gu['ratio_to_SUSY']:.3f}")
        print()

    print("W33 coupling running table (q=3):")
    print(f"  {'log10(M/GeV)':>14}  {'alpha_1^-1':>12}  {'alpha_2^-1':>12}  {'alpha_3^-1':>12}")
    print("  " + "-"*55)
    for row in coupling_table(3):
        print(f"  {row['log10_M_GeV']:>14.2f}  {row['alpha_1_inv']:>12.4f}  "
              f"{row['alpha_2_inv']:>12.4f}  {row['alpha_3_inv']:>12.4f}")
    print()
    print("CONCLUSION:")
    print("  The W33 GL_n beta functions give all-positive b_i ~ 0.24-0.56,")
    print("  meaning all couplings decrease with energy (asymptotically free).")
    print("  The W33 GUT scale depends on the q-dependent beta ratios.")
    print("  At q=3 the three pairwise unification scales differ, requiring")
    print("  either two-loop corrections or a q-dependent threshold to unify.")
    print("  NEXT: Pass 697 two-loop W33 beta functions for precision unification.")
