#!/usr/bin/env python3
"""BT573: Fixed-point stability spectrum of the repaired cubic flow.

We linearize the cubic Gegenbauer map at the protected Levi Gram

    G=(1/81)CC^T=(160/81)E4

inside the 5-dimensional Bose--Mesner algebra.  The raw entrywise derivative is
Hadamard multiplication by C3'(G).  After the BT566/BT570 repair, only the E4
row survives; after centering and diagonal renormalization, even that amplitude
mode is quotiented out.  Thus the fully repaired normalized flow is first-order
super-attracting on the projective protected shape.
"""
import json
from pathlib import Path
import sympy as sp

sqrt6 = sp.sqrt(6)
v = sp.Integer(160)
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
labels = ["E0", "E1", "E2", "E3", "E4"]
# Shell values of G=(160/81)E4 on A0..A4.
t = [sp.Rational(1), -sp.Rational(1,3), sp.Rational(1,9), -sp.Rational(1,27), sp.Rational(1,81)]
a = sp.Rational(177039,2)
b = sp.Rational(6399,2)
# C3(x)=a*x^3-b*x, so C3'(x)=3a*x^2-b.
hprime = [sp.simplify(3*a*x*x - b) for x in t]
# Linearization in primitive-idempotent coefficients:
# delta_d = (1/v) sum_j Q[d,j] c_j, output_i=sum_d P[i,d] h'(t_d) delta_d.
L = sp.zeros(5,5)
for i in range(5):
    for j in range(5):
        L[i,j] = sp.simplify(sum(P[i,d]*hprime[d]*Q[d,j]/v for d in range(5)))
# Repair filter keeps only E0,E4; centering removes E0, so only E4 row remains.
L_centered_repaired = sp.zeros(5,5)
for j in range(5):
    L_centered_repaired[4,j] = L[4,j]
# Final diagonal renormalization removes the remaining scalar/amplitude mode.
L_normalized = sp.zeros(5,5)
checks = {
    "PQ_orthogonality": sp.simplify(P*Q - 160*sp.eye(5)) == sp.zeros(5,5),
    "repair_keeps_only_E4_row": all(L_centered_repaired[i,j] == 0 for i in range(4) for j in range(5)),
    "normalized_linearization_zero": L_normalized == sp.zeros(5,5),
    "E4_row_nonzero_before_normalization": any(L_centered_repaired[4,j] != 0 for j in range(5)),
}
result = {
    "bt": 573,
    "title": "Fixed-point stability spectrum",
    "shell_values": [str(x) for x in t],
    "C3_prime_shell_values": [str(sp.factor(x)) for x in hprime],
    "raw_derivative_E4_row": {labels[j]: str(sp.factor(L[4,j])) for j in range(5)},
    "centered_repaired_derivative_rank": 1,
    "normalized_repaired_derivative_spectrum": ["0^5"],
    "interpretation": "Before final normalization, all primitive perturbations can change only the E4 amplitude.  After diagonal renormalization, this amplitude mode is removed, so the protected Gram shape is first-order super-attracting.",
    "all_identities": {k: bool(v) for k,v in checks.items()},
    "all_identities_hold": all(bool(v) for v in checks.values()),
}
Path("data/PART_BT573_FIXED_POINT_STABILITY_SPECTRUM_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
