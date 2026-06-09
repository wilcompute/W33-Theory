#!/usr/bin/env python3
"""BT594: Ihara-cubic leakage lock.

Home-run exploration: the raw cubic leakage ratio 244/121 is not only a
Bose-Mesner coefficient ratio.  It is exactly the even Ihara transfer value at
the W33 nonbacktracking radius.

Let d=12 be the W33 collinearity valency.  The nonbacktracking outdegree is
p=d-1=11.  Then

  244/121 = 2*(1 + 1/p^2).

The multiplicity-weighted ratio is chi/F5 times the same transfer:

  976/605 = (4/5)*(244/121).

This script verifies the exact substrate identities and writes a compact result.
"""
from fractions import Fraction
import json
from pathlib import Path

q = 3
v = 40
k = 12
Phi6 = 7
chi = 4
F5 = 5
p_ih = k - 1
leak_ratio = Fraction(244, 121)
weighted_ratio = Fraction(976, 605)
ihara_transfer = 2 * (Fraction(1, 1) + Fraction(1, p_ih * p_ih))
substrate_numerator = v * Phi6 - chi * q * q
p_squared = p_ih * p_ih
checks = {
    "p_ihara_is_k_minus_one": p_ih == 11,
    "denominator_is_ihara_square": leak_ratio.denominator == p_squared,
    "numerator_is_two_p_square_plus_two": leak_ratio.numerator == 2 * (p_squared + 1),
    "numerator_is_v_phi6_minus_chi_q2": leak_ratio.numerator == substrate_numerator,
    "leak_ratio_is_ihara_transfer": leak_ratio == ihara_transfer,
    "weighted_ratio_is_chi_over_F5_times_leak": weighted_ratio == Fraction(chi, F5) * leak_ratio,
    "weighted_numerator_is_chi_times_leak_numerator": weighted_ratio.numerator == chi * leak_ratio.numerator,
    "weighted_denominator_is_F5_times_ihara_square": weighted_ratio.denominator == F5 * p_squared,
}
result = {
    "bt": 594,
    "title": "Ihara-cubic leakage lock",
    "constants": {
        "q": q,
        "v": v,
        "k": k,
        "Phi6": Phi6,
        "chi": chi,
        "F5": F5,
        "p_Ihara": p_ih,
        "p_Ihara_squared": p_squared,
    },
    "identities": {
        "raw_leakage_ratio": str(leak_ratio),
        "ihara_transfer": "2*(1 + 1/p_Ihara^2)",
        "ihara_transfer_value": str(ihara_transfer),
        "numerator_decomposition_1": "244 = 2*(11^2 + 1)",
        "numerator_decomposition_2": "244 = v*Phi6 - chi*q^2 = 40*7 - 4*9",
        "weighted_ratio": str(weighted_ratio),
        "weighted_ratio_decomposition": "976/605 = (chi/F5)*(244/121)",
    },
    "interpretation": "The cubic leakage ratio is locked to the W33 Ihara nonbacktracking radius: 244/121 = 2*(1+1/11^2). The trace-weighted ratio is the same lock modulated by chi/F5.",
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}
Path("data/PART_BT594_IHARA_CUBIC_LEAKAGE_LOCK_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
