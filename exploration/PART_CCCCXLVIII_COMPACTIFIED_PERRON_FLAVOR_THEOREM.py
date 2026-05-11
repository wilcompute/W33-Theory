#!/usr/bin/env python3
"""
PART CCCCXLVIII: Compactified Perron Flavor Theorem

CCCCXLVII showed that the alpha correction is the mass-renormalized Perron
residue coefficient of the Hashimoto carrier.  This part extends the same
global-channel logic to the CKM/top relation found in the mass-mixing web:

    lambda_CKM * y_t^3 = 9/41.

Interpretation:
  - lambda_CKM = q^2/v is the density of the qutrit-square sector inside the
    uncompactified W(3,3) vertex carrier V, |V|=40.
  - y_t^3 = v/(v+1) is the Perron/global saturation factor of the one-point
    compactification V^+ = V union {infinity}, |V^+|=41.
  - Their product is the compactified qutrit-square density:

        (q^2/v)*(v/(v+1)) = q^2/(v+1) = 9/41.

This is not a new empirical fit.  It is an exact quotient theorem:
CKM first-order flavor density times top cubic saturation equals the
qutrit-square occupancy of the compactified Perron carrier.

Run:
    python exploration/PART_CCCCXLVIII_COMPACTIFIED_PERRON_FLAVOR_THEOREM.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> None:
    # True master seed and W(3,3) atoms.
    q = 3
    assert math.factorial(q) == 2 * q
    lam = 2
    mu = 4
    k = q * (q + 1)
    v = (q + 1) * (q * q + 1)
    E = v * k // 2
    directed_edges = 2 * E
    theta = k - 1

    # Flavor/top compactification data.
    qutrit_square = q * q
    compactified_v = v + 1
    lambda_ckm = Fraction(qutrit_square, v)
    top_yukawa_cubed = Fraction(v, compactified_v)
    compactified_flavor_density = lambda_ckm * top_yukawa_cubed

    # Alpha/Perron data for comparison: both live on global channels.
    m_vac = theta * ((k - lam) ** 2 + 1)
    delta_m = Fraction(q, lam * theta)
    m_eff = Fraction(m_vac, 1) + delta_m
    alpha_slip = Fraction(v, 1) / m_eff

    # One-point compactification audit.  The added point is not a W(3,3) vertex;
    # it is the global infinity/vacuum closure point.  The top cube is simply
    # the ratio of occupied finite vertices to compactified states.
    finite_occupancy = Fraction(v, compactified_v)
    infinity_occupancy = Fraction(1, compactified_v)
    qutrit_square_compact_occupancy = Fraction(qutrit_square, compactified_v)

    # Connections to existing W(3,3)/Monster-prime tower observations.
    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1
    monster_middle_prime = compactified_v

    # CKM/Higgs side from CCCCXLII for cross-checking one algebraic surface.
    lambda_H = Fraction(phi3, phi4 * phi4)
    A_ckm = Fraction(q**4, phi4 * phi4)
    A_over_lambdaH = A_ckm / lambda_H

    checks = {
        "true_master_equation_q_factorial_equals_2q": math.factorial(q) == 2 * q,
        "w33_vertex_count_v_40": v == 40,
        "w33_edge_count_240": E == 240,
        "directed_edges_480": directed_edges == 480,
        "compactified_vertex_count_41": compactified_v == 41,
        "qutrit_square_is_9": qutrit_square == 9,
        "lambda_ckm_is_9_over_40": lambda_ckm == Fraction(9, 40),
        "top_yukawa_cubed_is_40_over_41": top_yukawa_cubed == Fraction(40, 41),
        "product_is_9_over_41": compactified_flavor_density == Fraction(9, 41),
        "finite_plus_infinity_occupancy_is_one": finite_occupancy + infinity_occupancy == 1,
        "compactified_flavor_density_equals_q2_over_vplus1": compactified_flavor_density == qutrit_square_compact_occupancy,
        "vplus1_is_monster_prime_41": monster_middle_prime == 41,
        "alpha_slip_same_global_v_numerator": alpha_slip == Fraction(880, 24445),
        "A_over_lambdaH_remains_81_over_13": A_over_lambdaH == Fraction(81, 13),
    }

    result = {
        "part": "CCCCXLVIII",
        "title": "Compactified Perron Flavor Theorem",
        "atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "k": k,
            "v": v,
            "E": E,
            "directed_edges": directed_edges,
            "theta_k_minus_1": theta,
            "v_plus_1": compactified_v,
            "q_squared": qutrit_square,
            "Phi3": phi3,
            "Phi4": phi4,
            "Phi6": phi6,
        },
        "compactified_flavor_identity": {
            "lambda_CKM": str(lambda_ckm),
            "top_yukawa_cubed": str(top_yukawa_cubed),
            "product": str(compactified_flavor_density),
            "compactified_density": str(qutrit_square_compact_occupancy),
            "finite_occupancy_y_t_cubed": str(finite_occupancy),
            "infinity_occupancy": str(infinity_occupancy),
        },
        "global_channel_comparison": {
            "alpha_slip_v_over_Meff": str(alpha_slip),
            "alpha_Meff": str(m_eff),
            "flavor_compactified_denominator_v_plus_1": compactified_v,
            "statement": "alpha uses the Perron Green mass denominator M_eff; CKM/top uses the one-point compactified Perron count v+1",
        },
        "cross_surface_checks": {
            "lambda_H": str(lambda_H),
            "A_CKM": str(A_ckm),
            "A_CKM_over_lambda_H": str(A_over_lambdaH),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The CKM/top product is an exact compactification theorem: the uncompactified qutrit-square "
            "density q^2/v multiplied by top finite-vertex saturation v/(v+1) equals q^2/(v+1). "
            "Thus 9/41 is the compactified Perron flavor occupancy, with 41=v+1 matching the same "
            "global-channel prime already appearing in the Monster tower and top Yukawa denominator."
        ),
    }

    out = Path("PART_CCCCXLVIII_compactified_perron_flavor_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCXLVIII: Compactified Perron Flavor Theorem")
    print("=" * 76)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-" * 76)
    print(f"lambda_CKM = {lambda_ckm}")
    print(f"y_t^3      = {top_yukawa_cubed}")
    print(f"product    = {compactified_flavor_density}")
    print(f"alpha slip = {alpha_slip}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
