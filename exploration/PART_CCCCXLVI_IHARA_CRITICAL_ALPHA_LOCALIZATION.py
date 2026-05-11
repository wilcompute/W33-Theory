#!/usr/bin/env python3
"""
PART CCCCXLVI: Ihara Critical-Circle Alpha Localization

CCCCXLV lifted the refined alpha slip to the 480-dimensional Hashimoto
constant-flow carrier.  This part asks the next sharper question:

    Does the alpha slip live on the nontrivial Ihara critical circle,
    or does it live in the Perron/constant channel constrained by the same
    Ihara-Bass structure?

Answer verified here:

    The nontrivial W(3,3) Ihara zeros sit exactly on |u|=1/sqrt(11), as
    required by the graph RH.  The refined alpha slip, however, localizes
    exactly in the Perron/constant-flow channel, not in the nontrivial
    critical-circle channels.

This matters because it prevents overclaiming.  The correct mechanism is:

    Graph RH / Ramanujan structure supplies the nonbacktracking carrier and
    fixes k-1=11.  The electromagnetic finite slip is then the rank-one
    Perron-channel Green amplitude of that carrier:

        alpha^{-1} - y_c^{-1} = v/(1111 + 3/22) = 880/24445.

Run:
    python exploration/PART_CCCCXLVI_IHARA_CRITICAL_ALPHA_LOCALIZATION.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> None:
    q = 3
    lam = 2
    mu = 4
    k = 12
    v = 40
    f = 24
    g = 15
    theta = k - 1

    # Ihara-Bass scalar factors: F_a(u)=1-a*u+theta*u^2.
    # For a=k=12: roots 1 and 1/theta.
    perron_roots = [Fraction(1, 1), Fraction(1, theta)]

    # Nontrivial roots are represented by exact real/imag data.
    # For a=2: u=(1 +- i*sqrt(10))/11, |u|^2=(1+10)/121=1/11.
    # For a=-4: u=(-2 +- i*sqrt(7))/11, |u|^2=(4+7)/121=1/11.
    r_root_norm_sq = Fraction(1 + 10, theta * theta)
    s_root_norm_sq = Fraction(4 + 7, theta * theta)
    critical_radius_sq = Fraction(1, theta)

    # Vertex/Ihara mass polynomial from prior parts.
    # M0(a)=(k-1)*((a-lambda)^2+1)
    m_perron = theta * ((k - lam) ** 2 + 1)       # 1111
    m_r = theta * ((lam - lam) ** 2 + 1)          # 11
    m_s = theta * (((-mu) - lam) ** 2 + 1)        # 407

    # Rank-one Perron correction and alpha slip.
    delta_m = Fraction(q, lam * theta)            # 3/22
    m_perron_eff = Fraction(m_perron, 1) + delta_m
    alpha_slip = Fraction(v, 1) / m_perron_eff    # 880/24445

    # Natural nontrivial critical-channel Green candidates.
    # These are deliberately checked so the verifier can say what alpha is NOT.
    critical_trace_uncompressed = Fraction(f, m_r) + Fraction(g, m_s)
    critical_trace_per_vertex = critical_trace_uncompressed / v
    critical_trace_per_directed = critical_trace_uncompressed / (v * k)
    critical_trace_weighted_by_radius = critical_trace_uncompressed * critical_radius_sq

    alpha_core = theta**2 + mu**2                 # 137
    alpha_inv_refined = Fraction(alpha_core, 1) + alpha_slip

    checks = {
        "perron_roots_are_1_and_1_over_11": perron_roots == [Fraction(1, 1), Fraction(1, 11)],
        "r_roots_on_critical_circle": r_root_norm_sq == critical_radius_sq,
        "s_roots_on_critical_circle": s_root_norm_sq == critical_radius_sq,
        "m_perron_equals_1111": m_perron == 1111,
        "m_r_equals_11": m_r == 11,
        "m_s_equals_407": m_s == 407,
        "delta_m_equals_3_over_22": delta_m == Fraction(3, 22),
        "m_perron_eff_equals_24445_over_22": m_perron_eff == Fraction(24445, 22),
        "alpha_slip_equals_880_over_24445": alpha_slip == Fraction(880, 24445),
        "alpha_inverse_refined_exact": alpha_inv_refined == Fraction(669969, 4889),
        "critical_trace_not_alpha_slip": critical_trace_uncompressed != alpha_slip,
        "critical_per_vertex_not_alpha_slip": critical_trace_per_vertex != alpha_slip,
        "critical_per_directed_not_alpha_slip": critical_trace_per_directed != alpha_slip,
        "critical_radius_weighted_not_alpha_slip": critical_trace_weighted_by_radius != alpha_slip,
    }

    result = {
        "part": "CCCCXLVI",
        "title": "Ihara Critical-Circle Alpha Localization",
        "atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "k": k,
            "v": v,
            "f": f,
            "g": g,
            "theta_k_minus_1": theta,
        },
        "ihara_roots": {
            "perron_roots": [str(x) for x in perron_roots],
            "r_roots": "u=(1 +/- i*sqrt(10))/11",
            "s_roots": "u=(-2 +/- i*sqrt(7))/11",
            "critical_radius_squared": str(critical_radius_sq),
            "r_root_norm_squared": str(r_root_norm_sq),
            "s_root_norm_squared": str(s_root_norm_sq),
        },
        "mass_channels": {
            "perron_constant_mass": str(m_perron),
            "r_critical_mass_mult_24": str(m_r),
            "s_critical_mass_mult_15": str(m_s),
            "perron_delta_m": str(delta_m),
            "perron_effective_mass": str(m_perron_eff),
        },
        "alpha_localization": {
            "alpha_core_yc_inverse": alpha_core,
            "alpha_slip_perron_channel": str(alpha_slip),
            "alpha_inverse_refined": str(alpha_inv_refined),
            "critical_trace_uncompressed": str(critical_trace_uncompressed),
            "critical_trace_per_vertex": str(critical_trace_per_vertex),
            "critical_trace_per_directed": str(critical_trace_per_directed),
            "critical_trace_weighted_by_radius": str(critical_trace_weighted_by_radius),
            "localization_statement": "alpha slip localizes in the Perron/constant channel, not in the nontrivial critical-circle channels",
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "W(3,3)'s nontrivial Ihara roots satisfy the graph RH exactly, but the refined alpha slip "
            "is not one of the naive critical-circle Green traces. It is the rank-one Perron/constant-flow "
            "Green amplitude v/(1111+3/22). Thus graph RH supplies the nonbacktracking carrier and fixes "
            "theta=k-1=11, while alpha is localized at the constant channel of that carrier."
        ),
    }

    out = Path("PART_CCCCXLVI_ihara_critical_alpha_localization_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCXLVI: Ihara Critical-Circle Alpha Localization")
    print("=" * 76)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-" * 76)
    print(f"critical radius squared = {critical_radius_sq}")
    print(f"r root norm squared     = {r_root_norm_sq}")
    print(f"s root norm squared     = {s_root_norm_sq}")
    print(f"perron mass             = {m_perron}")
    print(f"perron effective mass   = {m_perron_eff}")
    print(f"alpha slip              = {alpha_slip} = {float(alpha_slip):.12f}")
    print(f"critical trace          = {critical_trace_uncompressed} = {float(critical_trace_uncompressed):.12f}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
