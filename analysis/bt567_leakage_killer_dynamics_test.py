#!/usr/bin/env python3
"""BT567: Leakage-killer dynamics test.

BT566 produced the Bose--Mesner leakage-killer filter P_{E0+E4}.  BT567 applies
that filter to the BT558 cubic Hamiltonian H3=C3(G), where G=(1/81)CC^T.

Result: P_{E0+E4} kills the companion leakage E1+E2+E3 exactly and keeps only
E0 plus the protected H1=81 sector E4.  On the centered leakage L3=H3-h0E0,
the same filter keeps only the E4 self-feedback coefficient.
"""
import json
from pathlib import Path
import sympy as sp

s = sp.sqrt(6)
mult = [1, 24, 30, 24, 81]
labels = ["E0_uniform", "E1_24_plus", "E2_30", "E3_24_minus", "E4_H1_81"]
H3 = [
    sp.Rational(17205568, 243),
    sp.Rational(179189696, 2187) - sp.Rational(734384, 243)*s,
    sp.Rational(177720928, 2187),
    sp.Rational(179189696, 2187) + sp.Rational(734384, 243)*s,
    sp.Rational(1751954560, 19683),
]
filter_E0_E4 = [1, 0, 0, 0, 1]
kept_H3 = [sp.simplify(H3[i]*filter_E0_E4[i]) for i in range(5)]
removed_H3 = [sp.simplify(H3[i]-kept_H3[i]) for i in range(5)]
L3 = [0] + H3[1:]
kept_L3 = [sp.simplify(L3[i]*filter_E0_E4[i]) for i in range(5)]
removed_L3 = [sp.simplify(L3[i]-kept_L3[i]) for i in range(5)]
trace = lambda coeffs: sp.simplify(sum(coeffs[i]*mult[i] for i in range(5)))
checks = {
    "companion_killed_on_H3": kept_H3[1] == kept_H3[2] == kept_H3[3] == 0,
    "E0_and_E4_survive_on_H3": kept_H3[0] == H3[0] and kept_H3[4] == H3[4],
    "centered_filter_keeps_only_E4": kept_L3[:4] == [0,0,0,0] and kept_L3[4] == H3[4],
    "removed_centered_is_exact_companion": removed_L3 == [0] + H3[1:4] + [0],
    "trace_partition_H3": sp.simplify(trace(kept_H3)+trace(removed_H3)-trace(H3)) == 0,
    "known_total_trace": trace(H3) == sp.Integer(13651200),
}
result = {
    "bt": 567,
    "title": "Leakage-killer dynamics test",
    "input": "H3=C3(G), G=(1/81)CC^T=(160/81)E4",
    "filter": "P_{E0+E4}",
    "H3_coefficients": dict(zip(labels, [str(sp.factor(c)) for c in H3])),
    "kept_H3_coefficients": dict(zip(labels, [str(sp.factor(c)) for c in kept_H3])),
    "removed_H3_coefficients": dict(zip(labels, [str(sp.factor(c)) for c in removed_H3])),
    "kept_centered_L3_coefficients": dict(zip(labels, [str(sp.factor(c)) for c in kept_L3])),
    "traces": {
        "total_H3": str(trace(H3)),
        "kept_H3": str(sp.factor(trace(kept_H3))),
        "removed_H3": str(sp.factor(trace(removed_H3))),
        "kept_centered_L3": str(sp.factor(trace(kept_L3))),
        "removed_centered_L3": str(sp.factor(trace(removed_L3))),
    },
    "interpretation": "The BT566 leakage-killer exactly removes E1+E2+E3.  Applied to centered cubic leakage, the only survivor is the E4/H1 self-feedback term.",
    "all_identities": {k: bool(v) for k, v in checks.items()},
    "all_identities_hold": all(bool(v) for v in checks.values()),
}
Path("data/PART_BT567_LEAKAGE_KILLER_DYNAMICS_TEST_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
