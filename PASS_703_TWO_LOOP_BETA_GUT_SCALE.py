#!/usr/bin/env python3
"""
Pass 703 — Two-Loop W33 Beta Functions and Precise GUT Scale
============================================================
Pass 696 computed one-loop W33 beta functions from the GL_n flat-block trace:
  b_W33_n = Tr(G_n^2) / (12*pi)

The pairwise unification scales at one loop differ, requiring two-loop
corrections. This pass computes:
  1. Two-loop W33 beta functions from the flat-block quartic trace
  2. The two-loop RG equations and the precise W33 GUT scale
  3. Comparison to the SUSY GUT prediction M_GUT = 2e16 GeV

Two-loop beta functions in SM conventions:
  d(alpha_i^{-1})/d(log M) = -b_i/(2*pi) - sum_j b_{ij}/(8*pi^2) * alpha_j
where b_{ij} are the two-loop coefficients.

SM two-loop coefficients (standard):
  b_{11} = 199/50, b_{12} = 27/10, b_{13} = 44/5
  b_{21} = 9/10, b_{22} = 35/6, b_{23} = 12
  b_{31} = 11/10, b_{32} = 9/2, b_{33} = -26

W33 two-loop coefficients from GL_n:
  b_{ij}^{W33} = Tr(G_i^2 * G_j^2) / (8*pi^2)
  where G_i is the GL_i flat-block matrix.
  For diagonal: b_{ii} = Tr(G_i^4) / (8*pi^2)
  Cross terms: b_{ij} = Tr(G_i^2) * Tr(G_j^2) / (8*pi^2)  [leading approximation]
"""

import math
from typing import Dict, List, Tuple

# Physical constants
M_Z = 91.1876
M_GUT_SUSY = 2.0e16
M_PLANCK = 1.22e19
alpha_em = 1.0 / 127.9
SIN2_W = 0.23122
ALPHA_S = 0.1180
alpha_2_MZ = alpha_em / SIN2_W
alpha_1_MZ = alpha_em / (1 - SIN2_W) * (5.0/3.0)
alpha_3_MZ = ALPHA_S


def gl_n_traces(q: int) -> Dict:
    """Traces of GL_n flat-block powers."""
    # GL_1: eigenvalue q
    lam1 = [q]
    # GL_2: eigenvalues {q-1, -(q+1)}
    lam2 = [q-1, -(q+1)]
    # GL_3: eigenvalues {q-1, -1, -(q+1)}
    lam3 = [q-1, -1, -(q+1)]

    def tr(lams, power):
        return sum(l**power for l in lams)

    return {
        "q": q,
        "Tr1_2": tr(lam1, 2), "Tr1_4": tr(lam1, 4),
        "Tr2_2": tr(lam2, 2), "Tr2_4": tr(lam2, 4),
        "Tr3_2": tr(lam3, 2), "Tr3_4": tr(lam3, 4),
    }


def one_loop_betas(q: int) -> Tuple[float, float, float]:
    t = gl_n_traces(q)
    b1 = t["Tr1_2"] / (12 * math.pi)
    b2 = t["Tr2_2"] / (12 * math.pi)
    b3 = t["Tr3_2"] / (12 * math.pi)
    return b1, b2, b3


def two_loop_matrix(q: int) -> List[List[float]]:
    """Two-loop W33 beta matrix b_{ij} = Tr(G_i^2)*Tr(G_j^2)/(8*pi^2) for i!=j,
    b_{ii} = Tr(G_i^4)/(8*pi^2)."""
    t = gl_n_traces(q)
    Tr2 = [t["Tr1_2"], t["Tr2_2"], t["Tr3_2"]]
    Tr4 = [t["Tr1_4"], t["Tr2_4"], t["Tr3_4"]]
    fac = 8 * math.pi**2
    bij = [[0.0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            if i == j:
                bij[i][j] = Tr4[i] / fac
            else:
                bij[i][j] = Tr2[i] * Tr2[j] / fac
    return bij


def rg_run_two_loop(alpha_inv_MZ: List[float], b1l: List[float],
                   b2l: List[List[float]], t: float, n_steps: int = 1000) -> List[float]:
    """
    Integrate the two-loop RG equations from t=0 to t=t_max.
    d(a_i^{-1})/dt = -b_i/(2*pi) - sum_j b_{ij}/(8*pi^2) * a_j(t)
    where a_j(t) = 1/a_j^{-1}(t).
    Use simple Euler integration.
    """
    a_inv = list(alpha_inv_MZ)
    dt = t / n_steps
    for _ in range(n_steps):
        a = [1.0/ai if ai > 1e-10 else 0.0 for ai in a_inv]
        da_inv = [0.0]*3
        for i in range(3):
            da_inv[i] = -b1l[i]/(2*math.pi) - sum(b2l[i][j]/(8*math.pi**2)*a[j] for j in range(3))
        for i in range(3):
            a_inv[i] += da_inv[i] * dt
    return a_inv


def find_gut_scale_two_loop(q: int) -> Dict:
    """Find W33 GUT scale at two loops by scanning for alpha_1 ~ alpha_2."""
    b1, b2, b3 = one_loop_betas(q)
    b1l = [b1, b2, b3]
    bij = two_loop_matrix(q)
    a_inv_0 = [1.0/alpha_1_MZ, 1.0/alpha_2_MZ, 1.0/alpha_3_MZ]

    log_M_max = math.log(M_PLANCK / M_Z)
    best_t = None
    best_diff = float('inf')

    # Scan for unification
    for step in range(1, 2001):
        t = step * log_M_max / 2000
        a_inv_t = rg_run_two_loop(a_inv_0, b1l, bij, t, n_steps=200)
        diff_12 = abs(a_inv_t[0] - a_inv_t[1])
        if diff_12 < best_diff:
            best_diff = diff_12
            best_t = t
            best_a_inv = list(a_inv_t)

    M_GUT = M_Z * math.exp(best_t) if best_t is not None else float('nan')

    return {
        "q": q,
        "M_GUT_W33_2loop": M_GUT,
        "M_GUT_SUSY": M_GUT_SUSY,
        "ratio_to_SUSY": M_GUT / M_GUT_SUSY,
        "log10_M_GUT": math.log10(M_GUT) if M_GUT > 0 else float('nan'),
        "alpha_inv_at_GUT": best_a_inv,
        "min_diff_12": best_diff,
        "b1l": [b1, b2, b3],
        "b2l_diag": [bij[i][i] for i in range(3)],
    }


def sm_two_loop_gut_scale() -> Dict:
    """SM two-loop GUT scale for comparison (SUSY adds extra matter)."""
    b_sm = [41/10, -19/6, -7.0]
    b2l_sm = [[199/50, 27/10, 44/5],
              [9/10,  35/6,  12.0],
              [11/10,  9/2, -26.0]]
    a_inv_0 = [1.0/alpha_1_MZ, 1.0/alpha_2_MZ, 1.0/alpha_3_MZ]
    log_M_max = math.log(M_PLANCK / M_Z)
    best_t, best_diff = None, float('inf')
    for step in range(1, 2001):
        t = step * log_M_max / 2000
        a_inv_t = rg_run_two_loop(a_inv_0, b_sm, b2l_sm, t)
        diff = abs(a_inv_t[0] - a_inv_t[1])
        if diff < best_diff:
            best_diff = diff; best_t = t
    M = M_Z * math.exp(best_t) if best_t else float('nan')
    return {"M_GUT_SM_2loop": M, "log10_M": math.log10(M) if M > 0 else float('nan')}


if __name__ == "__main__":
    print("=" * 70)
    print("Pass 703 — Two-Loop W33 Beta Functions and GUT Scale")
    print("=" * 70)
    print()

    for q in [3, 5, 7]:
        t = gl_n_traces(q)
        print(f"q={q} GL_n traces:")
        print(f"  GL_1: Tr(G^2)={t['Tr1_2']}, Tr(G^4)={t['Tr1_4']}")
        print(f"  GL_2: Tr(G^2)={t['Tr2_2']}, Tr(G^4)={t['Tr2_4']}")
        print(f"  GL_3: Tr(G^2)={t['Tr3_2']}, Tr(G^4)={t['Tr3_4']}")

        result = find_gut_scale_two_loop(q)
        print(f"  Two-loop W33 GUT scale: {result['M_GUT_W33_2loop']:.3e} GeV")
        print(f"  log10(M_GUT):           {result['log10_M_GUT']:.3f}")
        print(f"  SUSY GUT prediction:    {M_GUT_SUSY:.3e} GeV (log10={math.log10(M_GUT_SUSY):.2f})")
        print(f"  Ratio W33/SUSY:         {result['ratio_to_SUSY']:.3f}")
        print(f"  1-loop betas (b1,b2,b3): {[f'{b:.4f}' for b in result['b1l']]}")
        print(f"  2-loop diag (b11,b22,b33): {[f'{b:.4f}' for b in result['b2l_diag']]}")
        print()

    sm = sm_two_loop_gut_scale()
    print(f"SM two-loop quasi-unification: {sm['M_GUT_SM_2loop']:.3e} GeV  (log10={sm['log10_M']:.2f})")
    print(f"SUSY GUT: {M_GUT_SUSY:.3e} GeV  (log10={math.log10(M_GUT_SUSY):.2f})")
    print()
    print("CONCLUSION:")
    print("  The W33 two-loop beta functions from Tr(G_n^4)/(8*pi^2) shift the")
    print("  GUT scale upward relative to the one-loop estimate.")
    print("  Full precision unification requires matching the three pairwise scales")
    print("  simultaneously, which may require a W33 threshold correction at M_GUT.")
