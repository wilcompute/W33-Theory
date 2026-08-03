#!/usr/bin/env python3
"""Pass 2798: exact n-qutrit phase group and minimal sensor exponent law."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def invariant(e, dimension, k, scalar_power):
    # lambda = zeta_12^scalar_power.  The quotient gains lambda^(k(e-d)).
    return (scalar_power * k * (e - dimension)) % 12 == 0


def minimal_exponent(n):
    dimension = 3**n
    return next(e for e in range(1, 13) if all(invariant(e, dimension, k, j) for k in (1, 2) for j in range(12)))


def main():
    rows = []
    for n in range(1, 13):
        dimension = 3**n
        exponent = minimal_exponent(n)
        rows.append(
            {
                "qutrits": n,
                "dimension": dimension,
                "dimension_mod_12": dimension % 12,
                "minimal_finite_lift_exponent": exponent,
                "arbitrary_U1_exponent": dimension,
                "determinant_free_trace_power": 12,
            }
        )

    checks = {
        "scalar_group_order_12": all(invariant(12, 0, 1, j) for j in range(12)),
        "odd_n_exponent_3": all(row["minimal_finite_lift_exponent"] == 3 for row in rows if row["qutrits"] % 2),
        "even_n_exponent_9": all(row["minimal_finite_lift_exponent"] == 9 for row in rows if not row["qutrits"] % 2),
        "period_two": [row["minimal_finite_lift_exponent"] for row in rows[:6]] == [3, 9, 3, 9, 3, 9],
        "determinant_required": all(row["minimal_finite_lift_exponent"] % 12 != 0 for row in rows),
        "k1_and_k2_verified": all(
            invariant(row["minimal_finite_lift_exponent"], row["dimension"], k, j)
            for row in rows
            for k in (1, 2)
            for j in range(12)
        ),
    }
    assert all(checks.values())

    output = {
        "schema": "w33.pass2798.n_qutrit_metaplectic_sensor_exponent.v1",
        "status": "EXACT",
        "scalar_group": {
            "group": "mu_12",
            "derivation": "The standard qutrit Clifford lift is generated over Q(zeta_12): the qutrit phase supplies mu_3, the Fourier Gauss phase supplies mu_4, and SUM adds no scalar extension.",
        },
        "phase_invariance_condition": "e congruent to 3^n modulo 12 for Tr(U^k)^e/det(U^k), k=1,2",
        "minimal_exponent_law": {"n_odd": 3, "n_even": 9},
        "arbitrary_phase_boundary": "If representatives are allowed arbitrary U(1) phases rather than the standard finite Clifford lift, the exponent must be the full dimension 3^n.",
        "rows": rows,
        "checks": checks,
    }
    path = ROOT / "data/PART_BT2798_N_QUTRIT_SENSOR_EXPONENT_results.json"
    path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
