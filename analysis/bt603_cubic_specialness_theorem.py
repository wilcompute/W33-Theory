#!/usr/bin/env python3
"""BT603: Cubic specialness theorem.

BT600 showed that the odd-walk tower does not preserve the 244/121 ratio at all
orders.  BT603 isolates why the cubic level is special: it is the first
nonlinear odd closed-walk transport above the triangle substrate M3, and it is
the unique adjacent odd-moment ratio in the tested tower that simultaneously
matches the W33 substrate expression v*Phi6-chi*q^2 and gives the BT562/BT585
cubic leakage numerator.
"""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

spectrum_A = [(12, 1), (2, 24), (-4, 15)]
d = 12
p = d - 1
q = 3
v = 40
phi6 = 7
chi = 4
substrate_244 = v * phi6 - chi * q * q

def moment(power: int) -> int:
    return sum(mult * lam**power for lam, mult in spectrum_A)

odd_powers = list(range(1, 20, 2))
moments = {n: moment(n) for n in odd_powers}
ratios = []
for lower, upper in zip(odd_powers[:-1], odd_powers[1:]):
    if moments[lower] == 0:
        ratio = None
        normalized = None
    else:
        ratio = Fraction(moments[upper], moments[lower])
        normalized = ratio / (p * p)
    ratios.append({
        "ratio": f"M{upper}/M{lower}",
        "value": None if ratio is None else str(ratio),
        "normalized_by_p_squared": None if normalized is None else str(normalized),
        "equals_244": ratio == substrate_244 if ratio is not None else False,
        "is_cubic_level": lower == 3 and upper == 5,
    })

# M1=trace(A)=0 for a simple regular graph, so the first meaningful adjacent
# odd ratio is M5/M3.
first_meaningful = next(r for r in ratios if r["value"] is not None)
unique_244 = [r for r in ratios if r["equals_244"]]

checks = {
    "M1_is_zero": moments[1] == 0,
    "M3_is_triangle_substrate": moments[3] == 960,
    "M3_over_6_is_160_triangles": moments[3] // 6 == 160,
    "M5_over_M3_is_244": Fraction(moments[5], moments[3]) == 244,
    "244_substrate_identity": substrate_244 == 244,
    "cubic_normalized_ratio_is_244_over_121": Fraction(moments[5], moments[3]) / (p * p) == Fraction(244, 121),
    "first_meaningful_ratio_is_M5_over_M3": first_meaningful["ratio"] == "M5/M3",
    "unique_tested_adjacent_odd_ratio_equal_244": len(unique_244) == 1 and unique_244[0]["ratio"] == "M5/M3",
}

result = {
    "bt": 603,
    "title": "Cubic specialness theorem",
    "odd_moments": {f"M{n}": value for n, value in moments.items()},
    "adjacent_odd_ratios": ratios,
    "special_ratio": {
        "M5_over_M3": str(Fraction(moments[5], moments[3])),
        "normalized_by_11_squared": str(Fraction(moments[5], moments[3]) / (p * p)),
        "substrate_identity": "244 = v*Phi6 - chi*q^2 = 40*7 - 4*9",
    },
    "interpretation": "The cubic level is the first meaningful odd-walk transport above the triangle substrate and the unique adjacent odd-moment level in the tested tower whose ratio equals the W33 substrate number 244. Higher odd ratios drift toward the Perron limit instead of repeating the cubic lock.",
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}

Path("data/PART_BT603_CUBIC_SPECIALNESS_THEOREM_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
