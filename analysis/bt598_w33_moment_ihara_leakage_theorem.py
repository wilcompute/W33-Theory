#!/usr/bin/env python3
"""BT598: W33 moment-Ihara leakage theorem.

This is the stronger mechanism behind BT594/BT595.

For the W33 collinearity graph with spectrum

    12^1, 2^24, (-4)^15,

odd spectral moments satisfy

    M3 = Tr(A^3) = 960,
    M5 = Tr(A^5) = 234240,
    M5/M3 = 244.

The raw cubic leakage ratio is therefore

    (M5/M3)/(d-1)^2 = 244/121,

where d-1=11 is the Ihara/nonbacktracking outdegree.

So the leakage ratio is the normalized odd-moment transport of W33 by the square
of the nonbacktracking scale.
"""
from fractions import Fraction
import json
from pathlib import Path

spectrum = [(12, 1), (2, 24), (-4, 15)]
d = 12
p = d - 1
M3 = sum(mult * (lam ** 3) for lam, mult in spectrum)
M5 = sum(mult * (lam ** 5) for lam, mult in spectrum)
odd_moment_ratio = Fraction(M5, M3)
leakage_ratio = Fraction(244, 121)
normalized_moment = odd_moment_ratio / (p * p)

# Triangle check: Tr(A^3)=6*triangles for simple graph.
triangles = M3 // 6
# Known W33 triangle count = 160.

# Alternative closed form using W33 constants.
q = 3
v = 40
Phi6 = 7
chi = 4
moment_ratio_substrate = v * Phi6 - chi * q * q

checks = {
    "spectrum_multiplicity_sum_is_40": sum(mult for _lam, mult in spectrum) == 40,
    "M3_is_960": M3 == 960,
    "triangles_are_160": triangles == 160,
    "M5_is_234240": M5 == 234240,
    "moment_ratio_is_244": odd_moment_ratio == 244,
    "moment_ratio_substrate_identity": odd_moment_ratio == moment_ratio_substrate,
    "ihara_square_is_121": p * p == 121,
    "normalized_moment_is_leakage": normalized_moment == leakage_ratio,
}

result = {
    "bt": 598,
    "title": "W33 moment-Ihara leakage theorem",
    "spectrum": {str(lam): mult for lam, mult in spectrum},
    "degree": d,
    "nonbacktracking_outdegree": p,
    "moments": {
        "M3": M3,
        "M5": M5,
        "M5_over_M3": str(odd_moment_ratio),
        "triangles_from_M3_over_6": triangles,
    },
    "leakage_identity": {
        "raw_cubic_leakage_ratio": str(leakage_ratio),
        "normalized_odd_moment_ratio": "(M5/M3)/(d-1)^2",
        "value": str(normalized_moment),
    },
    "substrate_identity": "M5/M3 = 244 = v*Phi6 - chi*q^2 = 40*7 - 4*9",
    "interpretation": "The cubic leakage ratio is the W33 odd spectral moment ratio normalized by the Ihara nonbacktracking square. The numerator is graph-walk transport; the denominator is nonbacktracking propagation scale.",
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}

Path("data/PART_BT598_W33_MOMENT_IHARA_LEAKAGE_THEOREM_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
