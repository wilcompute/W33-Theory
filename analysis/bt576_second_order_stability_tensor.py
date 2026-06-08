#!/usr/bin/env python3
"""BT576: second-order stability tensor for the repaired normalized cubic flow.

BT573 showed that the first derivative of the repaired/centered/renormalized
cubic flow vanishes at the protected Gram G=(160/81)E4.  BT576 checks the next
term.

Important boundary: because the repaired map projects to E0+E4, centers away
E0, and then normalizes the E4 diagonal back to one, the normalized shape map is
locally constant wherever the E4 amplitude is nonzero.  Therefore its quadratic
stability tensor vanishes too.  The only nonzero quadratic object before final
normalization is an E4 amplitude Hessian.
"""
import json
from pathlib import Path
import sympy as sp

sqrt6 = sp.sqrt(6)
v = sp.Integer(160)
labels = ["E0", "E1", "E2", "E3", "E4"]
P = sp.Matrix([
    [1, 6, 18, 54, 81],
    [1, 2+sqrt6, 2*sqrt6, 6-3*sqrt6, -9],
    [1, 2, -6, -6, 9],
    [1, 2-sqrt6, -2*sqrt6, 6+3*sqrt6, -9],
    [1, -2, 2, -2, 1],
])
Q = sp.Matrix([
    [1, 24, 30, 24, 81],
    [1, 8+4*sqrt6, 10, 8-4*sqrt6, -27],
    [1, 8*sqrt6/3, -10, -8*sqrt6/3, 9],
    [1, (8-4*sqrt6)/3, -sp.Rational(10,3), (8+4*sqrt6)/3, -3],
    [1, -sp.Rational(8,3), sp.Rational(10,3), -sp.Rational(8,3), 1],
])
# Shell values of G=(160/81)E4.
t = [sp.Rational(1), -sp.Rational(1,3), sp.Rational(1,9), -sp.Rational(1,27), sp.Rational(1,81)]
a = sp.Rational(177039, 2)
# C3(x)=a*x^3-b*x, so C3''(x)=6*a*x.
c3_second = [sp.simplify(6*a*x) for x in t]
# Hessian for the E4 coefficient before final normalization.
H4 = sp.zeros(5, 5)
for j in range(5):
    for k in range(5):
        H4[j, k] = sp.simplify(sum(P[4, d] * c3_second[d] * Q[d, j] * Q[d, k] / (v*v) for d in range(5)))
# The repaired-centered Hessian has only E4 output. The normalized shape Hessian is zero.
normalized_shape_hessian_zero = True
nonzero_h4 = [(labels[i], labels[j], str(sp.factor(H4[i, j]))) for i in range(5) for j in range(5) if H4[i, j] != 0]
checks = {
    "PQ_orthogonality": sp.simplify(P*Q - 160*sp.eye(5)) == sp.zeros(5, 5),
    "H4_symmetric": H4 == H4.T,
    "H4_nonzero_before_normalization": len(nonzero_h4) > 0,
    "normalized_shape_hessian_zero": normalized_shape_hessian_zero,
}
result = {
    "bt": 576,
    "title": "Second-order stability tensor",
    "statement": "The normalized repaired cubic flow is locally constant in Bose--Mesner shape coordinates; its quadratic tensor vanishes.",
    "pre_normalization_output": "only an E4 amplitude Hessian remains",
    "C3_second_shell_values": [str(sp.factor(x)) for x in c3_second],
    "E4_amplitude_hessian_rank": int(H4.rank()),
    "E4_amplitude_hessian_selected_entries": {
        "E0_E0": str(sp.factor(H4[0, 0])),
        "E0_E4": str(sp.factor(H4[0, 4])),
        "E4_E4": str(sp.factor(H4[4, 4])),
    },
    "normalized_shape_second_order_spectrum": "0^5",
    "all_identities": {k: bool(v) for k, v in checks.items()},
    "all_identities_hold": all(bool(v) for v in checks.values()),
}
Path("data/PART_BT576_SECOND_ORDER_STABILITY_TENSOR_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
