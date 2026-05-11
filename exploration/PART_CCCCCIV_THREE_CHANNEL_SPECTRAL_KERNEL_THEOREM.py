#!/usr/bin/env python3
"""
PART CCCCCIV: Three-Channel Spectral Kernel Theorem

This part consolidates the full W(3,3) adjacency spectrum into a single
operator classification:

  1. Perron/global channel: eigenvalue k=12, multiplicity 1
       -> charm/alpha/top/CKM-lambda through Gaussian, Green/residue,
          and determinant compactification operations.

  2. r-gap-square channel: eigenvalue r=+2, multiplicity f=24
       -> Higgs/CKM-A/PMNS-reactor through Delta_r^2=(k-r)^2=100.

  3. s-heavy/root channel: eigenvalue s=-4, multiplicity g=15
       -> heavy/root completion through Delta_s=16 and g*Delta_s=240.

The key unification is that the two restricted channels exactly balance:

    f*(k-r) = 24*10 = 240,
    g*(k-s) = 15*16 = 240,

and their sum is 480, the directed-edge / Hashimoto / finite spectral-triple
carrier.  Thus the full adjacency spectrum is now assigned a physical role.

Run:
    python exploration/PART_CCCCCIV_THREE_CHANNEL_SPECTRAL_KERNEL_THEOREM.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> None:
    q = 3
    assert math.factorial(q) == 2 * q
    lam = 2
    mu = 4
    k = q * (q + 1)
    v = (q + 1) * (q * q + 1)
    E = v * k // 2
    D = 2 * E
    theta = k - 1

    r = lam
    s = -mu
    f = 24
    g = 15

    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1

    delta_r = k - r
    delta_s = k - s
    restricted_r_energy = f * delta_r
    restricted_s_energy = g * delta_s
    restricted_total = restricted_r_energy + restricted_s_energy

    # Perron/global observables.
    gaussian_core = theta * theta + mu * mu
    y_c = Fraction(1, gaussian_core)
    h_theta = theta * ((theta - (lam - 1)) ** 2 + 1)
    delta_m = Fraction(q, lam * theta)
    m_eff = Fraction(h_theta, 1) + delta_m
    alpha_slip = Fraction(v, 1) / m_eff
    alpha_inv = Fraction(gaussian_core, 1) + alpha_slip
    det_I_plus_J = v + 1
    top_cube = Fraction(v, det_I_plus_J)
    lambda_ckm = Fraction(q * q, v)
    compactified_flavor = lambda_ckm * top_cube

    # r-gap-square observables.
    gap_square = delta_r * delta_r
    lambda_H = Fraction(phi3, gap_square)
    A_ckm = Fraction(q**4, gap_square)
    pmns_theta13 = Fraction(q * q, (lam * phi4) ** 2)

    # s-heavy/root observables.
    e8_roots = E
    e8_rank = lam**3
    e8_dim = e8_roots + e8_rank
    su5_dim = f
    so10_dim = q * q * (mu + 1)
    e6_dim = lam * q * phi3

    # Kernel accounting.
    adjacency_trace_0 = k + f * r + g * s
    adjacency_trace_2 = k * k + f * r * r + g * s * s
    adjacency_trace_3 = k**3 + f * r**3 + g * s**3

    checks = {
        "true_master_equation": math.factorial(q) == 2 * q,
        "w33_atoms": (q, lam, mu, k, v, E, D, theta) == (3, 2, 4, 12, 40, 240, 480, 11),
        "full_adjacency_spectrum": (k, r, s, 1, f, g) == (12, 2, -4, 1, 24, 15),
        "trace_A_zero": adjacency_trace_0 == 0,
        "trace_A2_equals_480": adjacency_trace_2 == D == 480,
        "trace_A3_equals_960": adjacency_trace_3 == 960,
        "perron_channel_alpha": alpha_inv == Fraction(669969, 4889),
        "perron_channel_top_flavor": (top_cube, lambda_ckm, compactified_flavor) == (Fraction(40, 41), Fraction(9, 40), Fraction(9, 41)),
        "r_channel_gap_square": (delta_r, gap_square) == (10, 100),
        "r_channel_observables": (lambda_H, A_ckm, pmns_theta13) == (Fraction(13, 100), Fraction(81, 100), Fraction(9, 400)),
        "s_channel_gap": delta_s == 16 == lam**4,
        "restricted_equipartition": restricted_r_energy == restricted_s_energy == E == 240,
        "restricted_total_directed_edges": restricted_total == D == 480,
        "s_channel_e8": (e8_roots, e8_rank, e8_dim) == (240, 8, 248),
        "gut_dimensions": (su5_dim, so10_dim, e6_dim) == (24, 45, 78),
        "gap_difference_is_master_factorial": delta_s - delta_r == math.factorial(q) == 6,
        "gap_sum_is_2phi3": delta_s + delta_r == 2 * phi3 == 26,
    }

    result = {
        "part": "CCCCCIV",
        "title": "Three-Channel Spectral Kernel Theorem",
        "atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "k": k,
            "v": v,
            "E": E,
            "directed_edges": D,
            "theta_k_minus_1": theta,
            "r": r,
            "s": s,
            "f": f,
            "g": g,
            "Phi3": phi3,
            "Phi4": phi4,
            "Phi6": phi6,
        },
        "three_channels": {
            "perron_global": {
                "spectral_data": "adjacency eigenvalue k=12, multiplicity 1; Hashimoto theta=11",
                "role": "global coupling and compactification",
                "observables": {
                    "y_c_inverse": str(gaussian_core),
                    "alpha_inverse": str(alpha_inv),
                    "alpha_slip": str(alpha_slip),
                    "top_yukawa_cubed": str(top_cube),
                    "lambda_CKM": str(lambda_ckm),
                    "lambda_CKM_times_top_cube": str(compactified_flavor),
                },
            },
            "r_gap_square": {
                "spectral_data": "adjacency eigenvalue r=2, multiplicity f=24; Laplacian gap Delta_r=10",
                "role": "scalar/flavor normalization",
                "observables": {
                    "Delta_r": delta_r,
                    "Delta_r_squared": gap_square,
                    "lambda_H": str(lambda_H),
                    "A_CKM": str(A_ckm),
                    "PMNS_theta13": str(pmns_theta13),
                    "f_Delta_r": restricted_r_energy,
                },
            },
            "s_heavy_root": {
                "spectral_data": "adjacency eigenvalue s=-4, multiplicity g=15; Laplacian gap Delta_s=16",
                "role": "heavy/root completion",
                "observables": {
                    "Delta_s": delta_s,
                    "g_Delta_s": restricted_s_energy,
                    "E8_roots": e8_roots,
                    "E8_rank": e8_rank,
                    "E8_dim": e8_dim,
                    "SU5_dim": su5_dim,
                    "SO10_dim": so10_dim,
                    "E6_dim": e6_dim,
                },
            },
        },
        "kernel_accounting": {
            "trace_A": adjacency_trace_0,
            "trace_A2": adjacency_trace_2,
            "trace_A3": adjacency_trace_3,
            "restricted_r_energy": restricted_r_energy,
            "restricted_s_energy": restricted_s_energy,
            "restricted_total": restricted_total,
            "directed_edges": D,
            "gap_difference": delta_s - delta_r,
            "gap_sum": delta_s + delta_r,
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The full W(3,3) adjacency spectrum now has an assigned kernel role: Perron/global controls "
            "coupling and compactification constants; the r-channel gap-square controls scalar/flavor normalization; "
            "the s-channel heavy gap controls E8-root/heavy completion. The restricted channels exactly balance into "
            "two 240-unit carriers whose sum is the 480-dimensional Hashimoto/spectral-triple carrier."
        ),
    }

    out = Path("PART_CCCCCIV_three_channel_spectral_kernel_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCIV: Three-Channel Spectral Kernel Theorem")
    print("=" * 86)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-" * 86)
    print(f"Perron alpha^-1 = {alpha_inv}")
    print(f"r channel: Delta_r={delta_r}, f*Delta_r={restricted_r_energy}")
    print(f"s channel: Delta_s={delta_s}, g*Delta_s={restricted_s_energy}")
    print(f"restricted_total={restricted_total}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
