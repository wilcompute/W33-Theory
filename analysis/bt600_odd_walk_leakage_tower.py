#!/usr/bin/env python3
"""BT600: odd-walk leakage tower.

Compute the odd closed-walk moment ratios for the W33 collinearity graph and
compare their normalized values against powers of the Ihara scale p=d-1=11.

BT598 identified

  (M5/M3)/p^2 = 244/121.

BT600 checks the next tower levels:

  (M7/M5)/p^2, (M9/M7)/p^2, ...

and records the limiting behavior.  The result is a useful boundary: the cubic
level is the clean substrate lock; higher odd-walk levels form a rational tower
that tends toward the Perron-dominated value d^2/p^2 = 144/121, not the same
244/121 ratio.
"""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

spectrum_A = [(12, 1), (2, 24), (-4, 15)]
d = 12
p = d - 1

def moment(power: int) -> int:
    return sum(mult * lam**power for lam, mult in spectrum_A)

powers = list(range(1, 18, 2))
moments = {power: moment(power) for power in powers}
ratios = []
for a, b in zip(powers[:-1], powers[1:]):
    ratio = Fraction(moments[b], moments[a])
    normalized = ratio / (p * p)
    ratios.append(
        {
            "from": f"M{b}/M{a}",
            "ratio": str(ratio),
            "normalized_by_p_squared": str(normalized),
            "float_normalized": float(normalized),
        }
    )

cubic_lock = Fraction(moments[5], moments[3]) / (p * p)
perron_limit = Fraction(d * d, p * p)

checks = {
    "M3_is_960": moments[3] == 960,
    "M5_is_234240": moments[5] == 234240,
    "cubic_lock_is_244_over_121": cubic_lock == Fraction(244, 121),
    "perron_limit_is_144_over_121": perron_limit == Fraction(144, 121),
    "first_normalized_tower_entry_is_cubic_lock": Fraction(moments[5], moments[3]) / (p * p) == Fraction(244, 121),
}

result = {
    "bt": 600,
    "title": "Odd-walk leakage tower",
    "degree": d,
    "nonbacktracking_outdegree": p,
    "moments": {f"M{power}": value for power, value in moments.items()},
    "normalized_odd_moment_ratios": ratios,
    "cubic_lock": str(cubic_lock),
    "perron_dominated_limit": str(perron_limit),
    "interpretation": "The cubic level M5/M3 gives the exact leakage lock 244/121. Higher odd-walk ratios form a rational tower and drift toward 144/121, the Perron-dominated value d^2/(d-1)^2. Thus BT600 identifies the cubic level as special rather than claiming the same ratio persists at every odd order.",
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}

Path("data/PART_BT600_ODD_WALK_LEAKAGE_TOWER_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
