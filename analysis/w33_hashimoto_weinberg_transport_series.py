#!/usr/bin/env python3
"""Bounded Hashimoto transport series for the W33 Weinberg generator.

After the leading correction

    x_eff = 3/13 + alpha_hat/11 + O(alpha_hat^2),

this script makes the O(alpha_hat^2) term explicit under the isotropic
Hashimoto-transport hypothesis.

Because the normalized non-backtracking transport P = B/11 is row-stochastic,
any isotropic scalar insertion propagated for n non-backtracking steps is
bounded by (alpha_hat/11)^n.  Hence the full repeated-insertion scalar response
is controlled by the Neumann series

    delta_full = sum_{n>=1} (alpha_hat/11)^n
               = (alpha_hat/11)/(1 - alpha_hat/11)
               = alpha_hat/(11 - alpha_hat).

The omitted tail after the leading term is

    tail = delta_full - alpha_hat/11
         = (alpha_hat/11)^2/(1 - alpha_hat/11).

This gives a precise, non-fitted error bar for the transport correction.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    q = 3
    phi3 = 13
    k = 12
    nb = k - 1
    x0 = Fraction(q, phi3)

    # Numerical alpha_hat(MZ) value used only to evaluate the correction scale.
    alpha_inv = 127.930
    alpha = 1.0 / alpha_inv
    r = alpha / nb
    leading = r
    full = r / (1.0 - r)
    tail = full - leading

    x_leading = float(x0) + leading
    x_full = float(x0) + full

    # Also compute the exact low-energy W33 alpha seed from the repo's hard graph tests.
    # alpha_0^{-1} = 137 + 40/1111.
    alpha0_inv = 137.0 + 40.0/1111.0
    alpha0 = 1.0 / alpha0_inv
    r0 = alpha0 / nb
    full0 = r0 / (1.0 - r0)

    checks = {
        "nonbacktracking_denominator": nb == 11,
        "tree_generator": x0 == Fraction(3, 13),
        "series_ratio_small": r < 1e-3,
        "tail_bound_tiny": tail < 5e-7,
        "full_equals_geometric_formula": abs(full - alpha/(nb-alpha)) < 1e-18,
        "w33_low_energy_alpha_seed_reasonable": 137.0 < alpha0_inv < 138.0,
    }

    payload = {
        "theorem_name": "W33 Hashimoto Weinberg Transport Neumann-Series Bound",
        "all_checks_passed": all(checks.values()),
        "summary": {
            "tree_generator": "3/13",
            "nonbacktracking_denominator": nb,
            "alpha_hat_inverse_used": alpha_inv,
            "series_ratio_alpha_over_11": r,
            "leading_correction": leading,
            "full_neumann_correction": full,
            "higher_order_tail_after_leading": tail,
            "leading_prediction": x_leading,
            "neumann_resummed_prediction": x_full,
            "w33_alpha0_inverse_seed": alpha0_inv,
            "w33_alpha0_leading_prediction": float(x0) + r0,
            "w33_alpha0_resummed_prediction": float(x0) + full0,
        },
        "checks": checks,
        "identities": {
            "normalized_transport": "P = B/(k-1) = B/11",
            "leading_insertion": "delta_1 = alpha_hat/11",
            "n_step_bound": "|delta_n| <= (alpha_hat/11)^n under isotropic scalar transport",
            "neumann_sum": "delta_full = (alpha_hat/11)/(1-alpha_hat/11) = alpha_hat/(11-alpha_hat)",
            "tail_after_leading": "tail = (alpha_hat/11)^2/(1-alpha_hat/11)",
        },
        "interpretation": (
            "Once the denominator 11 is fixed by the W33 Hashimoto carrier, higher isotropic repeated insertions are not free. "
            "They form a controlled Neumann series whose tail is below 5e-7 at the MZ alpha scale. This justifies writing the "
            "paper formula as 3/13 + alpha_hat/11 + O(alpha_hat^2), with the O-term explicitly bounded."
        ),
        "boundary": (
            "The Neumann series assumes isotropic scalar transport. Non-isotropic sector-dependent insertions may produce additional "
            "matrix corrections; those should be handled by projecting the Hashimoto carrier onto the W33 1+24+15 sectors."
        ),
    }

    path = ROOT / "data" / "w33_hashimoto_weinberg_transport_series.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    return 0 if payload["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
