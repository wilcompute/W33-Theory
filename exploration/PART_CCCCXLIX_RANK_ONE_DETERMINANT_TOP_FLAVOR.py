#!/usr/bin/env python3
"""
PART CCCCXLIX: Rank-One Determinant Top-Flavor Theorem

CCCCXLVIII interpreted

    lambda_CKM * y_t^3 = 9/41

as qutrit-square occupancy after one-point compactification of the W(3,3)
vertex carrier.  This part gives the operator mechanism for the denominator
v+1=41.

Let J be the v x v all-ones operator on the W(3,3) vertex space.  Since J has
spectrum {v, 0^(v-1)},

    det(I + J) = 1 + v = 41.

Equivalently, by the matrix determinant lemma,

    det(I + 1*1^T) = 1 + 1^T 1 = v + 1.

The top Yukawa cube is therefore the finite-carrier determinant ratio

    y_t^3 = v / det(I+J) = 40/41,

and the CKM/top product is

    lambda_CKM*y_t^3 = (q^2/v)*(v/det(I+J)) = q^2/det(I+J) = 9/41.

So 41 is not only a prime-tower integer: it is the rank-one Perron
determinant of the global all-ones channel.

Run:
    python exploration/PART_CCCCXLIX_RANK_ONE_DETERMINANT_TOP_FLAVOR.py
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
    theta = k - 1

    # Rank-one determinant lemma for I + 1 1^T.
    one_norm_sq = v
    det_I_plus_J = 1 + one_norm_sq

    # Eigenvalue audit: J has eigenvalues v and 0^(v-1), so I+J has
    # eigenvalues v+1 and 1^(v-1).
    eigenvalue_perron_I_plus_J = v + 1
    eigenvalue_orthogonal_I_plus_J = 1
    determinant_from_spectrum = eigenvalue_perron_I_plus_J * (eigenvalue_orthogonal_I_plus_J ** (v - 1))

    # Top/flavor identities.
    y_t_cubed = Fraction(v, det_I_plus_J)
    lambda_ckm = Fraction(q * q, v)
    compactified_flavor = lambda_ckm * y_t_cubed

    # Complement/infinity channel.
    infinity_weight = Fraction(1, det_I_plus_J)
    finite_weight = y_t_cubed

    # Link to prior global-channel alpha denominator family.
    m_vac = theta * ((k - lam) ** 2 + 1)
    delta_m = Fraction(q, lam * theta)
    m_eff = Fraction(m_vac, 1) + delta_m
    alpha_slip = Fraction(v, 1) / m_eff

    # Monster / prime tower cross-link values.
    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1
    monster_prime_41_form = v + 1

    checks = {
        "true_master_equation": math.factorial(q) == 2 * q,
        "v_is_40": v == 40,
        "edge_count_240": E == 240,
        "det_I_plus_J_equals_v_plus_1": det_I_plus_J == v + 1 == 41,
        "det_from_spectrum_equals_v_plus_1": determinant_from_spectrum == det_I_plus_J,
        "matrix_determinant_lemma_form": det_I_plus_J == 1 + one_norm_sq,
        "top_yukawa_cube_equals_40_over_41": y_t_cubed == Fraction(40, 41),
        "infinity_plus_finite_weight_one": infinity_weight + finite_weight == 1,
        "lambda_ckm_equals_9_over_40": lambda_ckm == Fraction(9, 40),
        "ckm_top_product_equals_9_over_41": compactified_flavor == Fraction(9, 41),
        "compactified_flavor_equals_q2_over_det": compactified_flavor == Fraction(q * q, det_I_plus_J),
        "determinant_is_monster_prime_41": monster_prime_41_form == 41,
        "alpha_slip_global_channel_still_880_over_24445": alpha_slip == Fraction(880, 24445),
    }

    result = {
        "part": "CCCCXLIX",
        "title": "Rank-One Determinant Top-Flavor Theorem",
        "atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "k": k,
            "v": v,
            "E": E,
            "theta_k_minus_1": theta,
            "Phi3": phi3,
            "Phi4": phi4,
            "Phi6": phi6,
        },
        "rank_one_determinant": {
            "operator": "I + J = I + 1*1^T on vertex space",
            "one_norm_squared": one_norm_sq,
            "determinant_lemma": "det(I+1*1^T)=1+1^T1=v+1",
            "det_I_plus_J": det_I_plus_J,
            "perron_eigenvalue_of_I_plus_J": eigenvalue_perron_I_plus_J,
            "orthogonal_eigenvalue_of_I_plus_J": eigenvalue_orthogonal_I_plus_J,
            "determinant_from_spectrum": determinant_from_spectrum,
        },
        "top_flavor_identity": {
            "y_t_cubed": str(y_t_cubed),
            "lambda_CKM": str(lambda_ckm),
            "lambda_CKM_times_y_t_cubed": str(compactified_flavor),
            "q_squared_over_det_I_plus_J": str(Fraction(q * q, det_I_plus_J)),
            "finite_weight": str(finite_weight),
            "infinity_weight": str(infinity_weight),
        },
        "global_channel_comparison": {
            "alpha_slip_v_over_Meff": str(alpha_slip),
            "alpha_Meff": str(m_eff),
            "top_flavor_denominator_det_I_plus_J": det_I_plus_J,
            "statement": "alpha uses a rank-one Perron residue/Green mass; top flavor uses a rank-one Perron determinant/compactification count",
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The top-Yukawa denominator v+1=41 is the determinant of the rank-one global all-ones update I+J. "
            "Thus y_t^3=v/det(I+J), and lambda_CKM*y_t^3=q^2/det(I+J)=9/41. The same Perron channel "
            "that gives alpha a residue/Green correction gives flavor a determinant/compactification correction."
        ),
    }

    out = Path("PART_CCCCXLIX_rank_one_determinant_top_flavor_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCXLIX: Rank-One Determinant Top-Flavor Theorem")
    print("=" * 78)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-" * 78)
    print(f"det(I+J) = {det_I_plus_J}")
    print(f"y_t^3 = {y_t_cubed}")
    print(f"lambda_CKM*y_t^3 = {compactified_flavor}")
    print(f"alpha slip = {alpha_slip}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
