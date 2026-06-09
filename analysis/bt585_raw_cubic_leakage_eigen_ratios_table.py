#!/usr/bin/env python3
"""BT585: canonical raw cubic leakage eigen-ratios table.

This collects the BT555/BT558/BT562 coefficients into a single exact artifact.
"""
import json
from pathlib import Path
import sympy as sp

sqrt6 = sp.sqrt(6)
labels = ["E0", "E1", "E2", "E3", "E4"]
mult = {"E0": 1, "E1": 24, "E2": 30, "E3": 24, "E4": 81}
coeff = {
    "E0": sp.Rational(17205568, 243),
    "E1": -sp.Rational(734384, 2187) * (-244 + 9*sqrt6),
    "E2": sp.Rational(177720928, 2187),
    "E3": sp.Rational(734384, 2187) * (244 + 9*sqrt6),
    "E4": sp.Rational(1751954560, 19683),
}
conj_sum = sp.simplify(coeff["E1"] + coeff["E3"])
conj_diff = sp.simplify(coeff["E3"] - coeff["E1"])
ratio_unweighted = sp.simplify(conj_sum / coeff["E2"])
ratio_weighted = sp.simplify((24*coeff["E1"] + 24*coeff["E3"]) / (30*coeff["E2"]))
trace_terms = {k: sp.simplify(mult[k] * coeff[k]) for k in labels}
total_trace = sp.simplify(sum(trace_terms.values()))
checks = {
    "E1_E3_conjugate_sum_ratio": ratio_unweighted == sp.Rational(244, 121),
    "weighted_companion_ratio": ratio_weighted == sp.Rational(976, 605),
    "total_trace": total_trace == sp.Integer(13651200),
    "multiplicity_sum": sum(mult.values()) == 160,
}
result = {
    "bt": 585,
    "title": "Raw cubic leakage eigen-ratios table",
    "coefficients": {k: str(sp.factor(coeff[k])) for k in labels},
    "multiplicities": mult,
    "trace_terms": {k: str(sp.factor(trace_terms[k])) for k in labels},
    "E1_plus_E3": str(sp.factor(conj_sum)),
    "E3_minus_E1": str(sp.factor(conj_diff)),
    "ratio_E1_plus_E3_over_E2": str(ratio_unweighted),
    "weighted_ratio_24E1_plus_24E3_over_30E2": str(ratio_weighted),
    "total_trace": str(total_trace),
    "interpretation": "The conjugate 24+24 leakage is locked to the 30-sector by 244/121 before multiplicity weighting and by 976/605 after trace weighting.",
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}
Path("data/PART_BT585_RAW_CUBIC_LEAKAGE_EIGEN_RATIOS_TABLE_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
