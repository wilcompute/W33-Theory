#!/usr/bin/env python3
"""
PART CCCCCIII: s-Channel Heavy Kernel Theorem

Parts CCCCC and CCCCCI/CCCC CII identified the Perron/global and r-gap-square
channels.  This part tests the missing restricted channel:

    s = -mu = -4, multiplicity g = 15.

Its Laplacian gap is

    Delta_s = k - s = 12 - (-4) = 16 = lambda^4.

The W(3,3) spectral triple repeatedly treats 16 as a heavy/excited scale.
This verifier consolidates the s-channel identities:

  - Delta_s = 16 = lambda^mu = lambda^4.
  - g * Delta_s = 15 * 16 = 240 = |E(W(3,3))| = |E8 roots|.
  - f * Delta_r = 24 * 10 = 240 as the companion r-channel equipartition.
  - Delta_s / Delta_r = 16/10 = 8/5 = lambda^3/(mu+1).
  - Delta_s - Delta_r = 6 = q! = 2q.
  - Delta_s + Delta_r = 26 = 2 Phi_3.

Interpretation:
  The s-channel is the heavy/root completion channel.  Its gap-16 sector is
  not just another denominator: with multiplicity g=15 it exactly reconstructs
  the 240-edge/E8-root carrier.

Run:
    python exploration/PART_CCCCCIII_S_CHANNEL_HEAVY_KERNEL_THEOREM.py
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
    directed_edges = 2 * E

    r = lam
    s = -mu
    f = 24
    g = 15
    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1

    delta_r = k - r
    delta_s = k - s

    r_energy = f * delta_r
    s_energy = g * delta_s
    total_restricted_energy = r_energy + s_energy

    # Prior two-channel observables for continuity.
    lambda_H = Fraction(phi3, delta_r * delta_r)
    A_ckm = Fraction(q**4, delta_r * delta_r)
    pmns_theta13 = Fraction(q * q, (lam * phi4) ** 2)

    # Heavy/root channel identities.
    s_gap_ratio_to_r_gap = Fraction(delta_s, delta_r)
    s_gap_minus_r_gap = delta_s - delta_r
    s_gap_plus_r_gap = delta_s + delta_r
    e8_dim_from_edges_rank = E + lam**3

    # Possible heavy gauge numerators from s-channel scale.
    x_y_heavy_gap_pair = (delta_r, delta_s)
    su5_dim = f
    so10_dim = q * q * (mu + 1)
    e6_dim = lam * q * phi3

    checks = {
        "true_master_equation": math.factorial(q) == 2 * q,
        "w33_atoms": (q, lam, mu, k, v, E, directed_edges) == (3, 2, 4, 12, 40, 240, 480),
        "restricted_eigenvalues_and_multiplicities": (r, s, f, g) == (2, -4, 24, 15),
        "delta_r_is_phi4": delta_r == phi4 == 10,
        "delta_s_is_lambda_fourth": delta_s == lam**mu == lam**4 == 16,
        "delta_s_minus_delta_r_is_q_factorial": s_gap_minus_r_gap == math.factorial(q) == 6,
        "delta_s_plus_delta_r_is_2_phi3": s_gap_plus_r_gap == 2 * phi3 == 26,
        "gap_ratio_is_8_over_5": s_gap_ratio_to_r_gap == Fraction(8, 5),
        "r_energy_equals_edges": r_energy == E == 240,
        "s_energy_equals_edges": s_energy == E == 240,
        "restricted_energy_total_is_480": total_restricted_energy == directed_edges == 480,
        "e8_dim_from_edges_plus_rank": e8_dim_from_edges_rank == 248,
        "lambda_H_still_13_over_100": lambda_H == Fraction(13, 100),
        "A_ckm_still_81_over_100": A_ckm == Fraction(81, 100),
        "pmns_theta13_still_9_over_400": pmns_theta13 == Fraction(9, 400),
        "su5_so10_e6_dims": (su5_dim, so10_dim, e6_dim) == (24, 45, 78),
    }

    result = {
        "part": "CCCCCIII",
        "title": "s-Channel Heavy Kernel Theorem",
        "atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "k": k,
            "v": v,
            "E": E,
            "directed_edges": directed_edges,
            "r": r,
            "s": s,
            "f": f,
            "g": g,
            "Phi3": phi3,
            "Phi4": phi4,
            "Phi6": phi6,
        },
        "spectral_gaps": {
            "Delta_r": delta_r,
            "Delta_s": delta_s,
            "Delta_s_over_Delta_r": str(s_gap_ratio_to_r_gap),
            "Delta_s_minus_Delta_r": s_gap_minus_r_gap,
            "Delta_s_plus_Delta_r": s_gap_plus_r_gap,
        },
        "equipartition": {
            "f_times_Delta_r": r_energy,
            "g_times_Delta_s": s_energy,
            "edge_count": E,
            "restricted_total": total_restricted_energy,
            "directed_edges": directed_edges,
            "statement": "both restricted channels carry 240 units; together they carry the 480-dimensional directed-edge/spectral-triple carrier",
        },
        "heavy_root_channel": {
            "Delta_s": delta_s,
            "multiplicity_g": g,
            "g_Delta_s": s_energy,
            "E8_roots": 240,
            "E8_dim_edges_plus_rank": e8_dim_from_edges_rank,
            "interpretation": "s-channel gap 16 with multiplicity 15 reconstructs the 240-edge/E8-root carrier",
        },
        "two_channel_context": {
            "lambda_H": str(lambda_H),
            "A_CKM": str(A_ckm),
            "PMNS_theta13": str(pmns_theta13),
            "SU5_dim": su5_dim,
            "SO10_dim": so10_dim,
            "E6_dim": e6_dim,
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The missing s=-4 channel is the heavy/root completion channel. Its gap Delta_s=16=lambda^4, "
            "and its multiplicity g=15 gives g*Delta_s=240, exactly the W(3,3) edge count and E8 root count. "
            "Together with the r-channel identity f*Delta_r=240, the restricted spectrum splits into two equal "
            "240-unit carriers whose sum is the 480 directed-edge/spectral-triple dimension."
        ),
    }

    out = Path("PART_CCCCCIII_s_channel_heavy_kernel_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCIII: s-Channel Heavy Kernel Theorem")
    print("=" * 82)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-" * 82)
    print(f"Delta_r={delta_r}, f*Delta_r={r_energy}")
    print(f"Delta_s={delta_s}, g*Delta_s={s_energy}")
    print(f"restricted_total={total_restricted_energy}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
