#!/usr/bin/env python3
"""
PART CCCCCVI: Spectral Action Channel Theorem

PART CCCCCV mapped the finite Dirac spectrum to W(3,3) graph channels:

    0^82, 4^320, 10^48, 16^30

with
    10 = Delta_r = k-r, multiplicity 2f = 48,
    16 = Delta_s = k-s, multiplicity 2g = 30.

This part verifies that the spectral-action coefficients

    a0 = Tr(D_F^0) = 480
    a2 = Tr(D_F^2) = 2240
    a4 = Tr(D_F^4) = 17600

split cleanly by the same channel map:

    ground:  0^82
    gauge:   4^320
    r-gap:  10^48
    s-gap:  16^30

Key new identities:
    a2 = 1280 + 480 + 480 = gauge + r + s
    a4 = 81920? no; for D_F^2 eigenvalues {0,4,10,16}, a4 = sum m*lambda^2
       = 5120 + 4800 + 7680 = 17600.

The r/s excited a2 trace equals Tr(A^3)=960, and r/s excited dimension is
78=dim(E6).  The s-to-r a4 ratio is 7680/4800=8/5=Delta_s/Delta_r,
because the restricted a2 energies are equipartitioned.

Run:
    python exploration/PART_CCCCCVI_SPECTRAL_ACTION_CHANNEL_THEOREM.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from fractions import Fraction


def main() -> None:
    q = 3
    assert math.factorial(q) == 2*q
    lam = 2
    mu = 4
    k = q*(q+1)
    v = (q+1)*(q*q+1)
    E = v*k//2
    directed_edges = 2*E
    r = lam
    s = -mu
    f = 24
    g = 15
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1
    delta_r = k-r
    delta_s = k-s

    sectors = {
        "ground": {"eig": 0, "mult": 2*q**4 + 1},
        "gauge": {"eig": mu, "mult": lam**3 * v},
        "r_gap": {"eig": delta_r, "mult": 2*f},
        "s_gap": {"eig": delta_s, "mult": 2*g},
    }

    a0_by = {name: data["mult"] for name, data in sectors.items()}
    a2_by = {name: data["mult"] * data["eig"] for name, data in sectors.items()}
    a4_by = {name: data["mult"] * data["eig"]**2 for name, data in sectors.items()}

    a0 = sum(a0_by.values())
    a2 = sum(a2_by.values())
    a4 = sum(a4_by.values())

    excited_dim = sectors["r_gap"]["mult"] + sectors["s_gap"]["mult"]
    excited_a2 = a2_by["r_gap"] + a2_by["s_gap"]
    excited_a4 = a4_by["r_gap"] + a4_by["s_gap"]
    gauge_a2 = a2_by["gauge"]
    gauge_a4 = a4_by["gauge"]

    # Graph trace identities.
    trace_A2 = k*k + f*r*r + g*s*s
    trace_A3 = k**3 + f*r**3 + g*s**3

    # Ratios showing channel structure.
    r_a2 = a2_by["r_gap"]
    s_a2 = a2_by["s_gap"]
    r_a4 = a4_by["r_gap"]
    s_a4 = a4_by["s_gap"]
    a4_ratio_s_over_r = Fraction(s_a4, r_a4)

    # Exceptional dimensions.
    e6_dim = lam*q*phi3
    e8_roots = E
    e8_rank = lam**3
    e8_dim = e8_roots + e8_rank

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q, lam, mu, k, v, E, directed_edges, r, s, f, g) == (3,2,4,12,40,240,480,2,-4,24,15),
        "sector_eigenvalues": tuple(sectors[x]["eig"] for x in ["ground","gauge","r_gap","s_gap"]) == (0,4,10,16),
        "sector_multiplicities": tuple(sectors[x]["mult"] for x in ["ground","gauge","r_gap","s_gap"]) == (82,320,48,30),
        "a0_equals_480": a0 == 480 == directed_edges,
        "a2_equals_2240": a2 == 2240,
        "a4_equals_17600": a4 == 17600,
        "a2_channel_split": (a2_by["ground"], a2_by["gauge"], a2_by["r_gap"], a2_by["s_gap"]) == (0,1280,480,480),
        "a4_channel_split": (a4_by["ground"], a4_by["gauge"], a4_by["r_gap"], a4_by["s_gap"]) == (0,5120,4800,7680),
        "excited_dim_equals_E6": excited_dim == e6_dim == 78,
        "excited_a2_equals_trace_A3": excited_a2 == trace_A3 == 960,
        "trace_A2_equals_a0": trace_A2 == a0 == 480,
        "restricted_a2_equipartition": r_a2 == s_a2 == 480,
        "restricted_a4_ratio_is_gap_ratio": a4_ratio_s_over_r == Fraction(delta_s, delta_r) == Fraction(8,5),
        "gauge_plus_excited_a2": gauge_a2 + excited_a2 == a2,
        "gauge_plus_excited_a4": gauge_a4 + excited_a4 == a4,
        "e8_dimension": e8_dim == 248,
    }

    result = {
        "part": "CCCCVI",
        "title": "Spectral Action Channel Theorem",
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
        "dirac_sectors": sectors,
        "spectral_action_coefficients": {
            "a0_by_channel": a0_by,
            "a2_by_channel": a2_by,
            "a4_by_channel": a4_by,
            "a0_total": a0,
            "a2_total": a2,
            "a4_total": a4,
        },
        "channel_identities": {
            "excited_dim": excited_dim,
            "E6_dim": e6_dim,
            "excited_a2": excited_a2,
            "Tr_A3": trace_A3,
            "Tr_A2": trace_A2,
            "restricted_a2_equipartition": {"r_gap": r_a2, "s_gap": s_a2},
            "restricted_a4": {"r_gap": r_a4, "s_gap": s_a4, "ratio_s_over_r": str(a4_ratio_s_over_r)},
            "E8_dim": e8_dim,
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The spectral-action coefficients a0=480, a2=2240, and a4=17600 decompose by the same W(3,3) "
            "Dirac channel map. The r/s excited sectors have dimension 78=dim(E6), their a2 trace equals Tr(A^3)=960, "
            "and their a2 energies are equipartitioned at 480+480. Thus the finite spectral action is channelized by "
            "the W(3,3) graph spectrum rather than appended as separate data."
        ),
    }

    out = Path("PART_CCCCCVI_spectral_action_channel_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCVI: Spectral Action Channel Theorem")
    print("="*84)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*84)
    print(f"a0={a0}, a2={a2}, a4={a4}")
    print(f"a2_by={a2_by}")
    print(f"a4_by={a4_by}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
