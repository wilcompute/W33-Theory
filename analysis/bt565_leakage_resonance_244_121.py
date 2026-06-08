#!/usr/bin/env python3
"""BT565: Leakage resonance 244/121.

BT562 found the cubic leakage ratio (E1+E3)/E2 = 244/121.  This verifier ties
244 and 121 back to already-present W33 constants:

  * 244 = sum(lambda^5)/sum(lambda^3) for the W33 SRG spectrum (12,2,-4),
    with multiplicities (1,24,15).
  * 244 = 40*7 - 4*9 = v*Phi6 - chi*q^2.
  * 121 = 11^2 = p_Ih^2 = (nonbacktracking outdegree)^2 for the W33 graph.
"""
import json
from pathlib import Path
from fractions import Fraction

v, Phi6, chi, q, p_Ih = 40, 7, 4, 3, 11
spec = [(12,1),(2,24),(-4,15)]
s3 = sum(m*(a**3) for a,m in spec)
s5 = sum(m*(a**5) for a,m in spec)
ratio = Fraction(s5, s3)
leak_ratio = Fraction(244, 121)
checks = {
    "spectral_ratio_244": ratio == 244,
    "244_substrate_formula": 244 == v*Phi6 - chi*q*q,
    "121_ihara_square": 121 == p_Ih*p_Ih,
    "leak_ratio": leak_ratio == Fraction(ratio, p_Ih*p_Ih),
    "near_double_deviation": leak_ratio - 2 == Fraction(2,121),
}
result = {
    "bt": 565,
    "title": "Leakage resonance 244/121",
    "w33_srg_spectrum": "12^1 + 2^24 + (-4)^15",
    "sum_lambda3": s3,
    "sum_lambda5": s5,
    "spectral_ratio": str(ratio),
    "substrate_formula_244": "40*7 - 4*9",
    "denominator_121": "11^2 = p_Ih^2",
    "cubic_leakage_ratio": str(leak_ratio),
    "deviation_from_2": str(leak_ratio - 2),
    "interpretation": "The BT562 leakage ratio is the W33 fifth/third spectral moment ratio divided by the square of the Ihara nonbacktracking outdegree.",
    "all_identities": checks,
    "all_identities_hold": all(checks.values())
}
Path("data/PART_BT565_LEAKAGE_RESONANCE_244_121_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
