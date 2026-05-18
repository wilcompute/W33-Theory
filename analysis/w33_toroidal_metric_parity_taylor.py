#!/usr/bin/env python3
"""Parity Taylor expansion of the toroidal metric generating function.

Previous layer:

    P(t)=68+147t+127t^2+86t^3+54t^4+19t^5+3t^6
         =(1+t)Q(t),
    Q(-1)=12,
    P(1)/7=72.

This layer expands P at the parity/Euler-cancellation point t=-1.  Write
u=1+t.  Since P(t)=sum_m c_m (1+t)^m where c_m counts metric edge classes
of multiplicity m, the Taylor coefficients at t=-1 are the edge multiplicity
histogram itself:

    P(t)=12 u + 48 u^2 + 0 u^3 + 4 u^4 + 1 u^5 + 3 u^6.

Thus

    P^(m)(-1)/m! = c_m,

with

    c_1,c_2,c_3,c_4,c_5,c_6 = 12,48,0,4,1,3.

The missing cubic slot c_3=0 is especially suggestive: the metric packet has
no classes of multiplicity q=3 even though q=3 controls the whole substrate.
The q-sector is displaced to the top multiplicity count c_6=3.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "w33_toroidal_metric_parity_taylor.json"

# Low-to-high coefficients of P(t)=sum_k B_k t^k.
P = [68, 147, 127, 86, 54, 19, 3]
# Histogram c_m of metric edge-class multiplicities m=0..6.
C = [0, 12, 48, 0, 4, 1, 3]

Q = 3
F = 24
MU = 4
PHI6 = 7
MIDDLE_EIGENVALUE = 72
GENUS_NUMERATOR = 12
PHASE_KERNEL = 79


def poly_eval(coeffs: list[int], x: int) -> int:
    return sum(c * (x**i) for i, c in enumerate(coeffs))


def derivative_at(coeffs: list[int], order: int, x: int) -> int:
    total = 0
    for i, c in enumerate(coeffs):
        if i < order:
            continue
        falling = 1
        for j in range(order):
            falling *= i - j
        total += c * falling * (x ** (i - order))
    return total


def binomial_from_histogram(c: list[int]) -> list[int]:
    max_m = len(c) - 1
    return [sum(c[m] * math.comb(m, k) for m in range(k, max_m + 1)) for k in range(max_m + 1)]


def build_payload() -> dict[str, Any]:
    derivatives = {m: derivative_at(P, m, -1) for m in range(1, 7)}
    normalized = {m: derivatives[m] // math.factorial(m) for m in range(1, 7)}
    B_from_C = binomial_from_histogram(C)

    metric_classes = sum(C)
    edge_instances = sum(m * C[m] for m in range(len(C)))
    boolean_lift = sum((2**m) * C[m] for m in range(len(C)))
    raw_second = sum((m**2) * C[m] for m in range(len(C)))

    identities = {
        "B_reconstruction": B_from_C == P,
        "taylor_coefficients": [normalized[m] for m in range(1, 7)] == C[1:],
        "no_constant_term": poly_eval(P, -1) == 0,
        "genus_first_taylor": normalized[1] == GENUS_NUMERATOR == 12,
        "two_bosonic_24": normalized[2] == 2 * F == 48,
        "missing_cubic_slot": normalized[3] == 0,
        "quartic_mu": normalized[4] == MU == 4,
        "quintic_center": normalized[5] == 1,
        "sextic_q": normalized[6] == Q == 3,
        "metric_classes": metric_classes == 68,
        "edge_instances": edge_instances == 147,
        "phase_kernel": edge_instances - metric_classes == PHASE_KERNEL == 79,
        "boolean_lift": boolean_lift == PHI6 * MIDDLE_EIGENVALUE == 504,
        "raw_second": raw_second == 401,
    }

    theorem = (
        "Toroidal Metric Parity-Taylor Theorem.  The toroidal metric moment "
        "generating function P(t) has Taylor expansion at the parity/Euler "
        "point t=-1 given by P(t)=12u+48u^2+0u^3+4u^4+u^5+3u^6, where "
        "u=1+t.  Therefore the metric edge-class multiplicity histogram is "
        "exactly the normalized derivative ladder P^(m)(-1)/m!.  The ladder "
        "reads 12,48,0,4,1,3: genus numerator, two 24-sectors, missing cubic "
        "q-slot, quartic mu/root-4 slot, center, and q at the sextic cap."
    )

    return {
        "summary": {
            "P_coefficients_t_basis": P,
            "P_coefficients_u_basis_u_equals_1_plus_t": C,
            "normalized_derivatives_m1_to_m6": [normalized[m] for m in range(1, 7)],
            "metric_classes": metric_classes,
            "edge_instances": edge_instances,
            "phase_kernel": edge_instances - metric_classes,
            "boolean_lift": boolean_lift,
            "all_identities_hold": all(identities.values()),
        },
        "parity_taylor_expansion": {
            "u_definition": "u = 1 + t",
            "P_in_u_basis": "12 u + 48 u^2 + 0 u^3 + 4 u^4 + u^5 + 3 u^6",
            "normalized_derivatives": {str(m): normalized[m] for m in range(1, 7)},
            "raw_derivatives": {str(m): derivatives[m] for m in range(1, 7)},
        },
        "histogram_reading": {
            "multiplicity_histogram": {"1": 12, "2": 48, "3": 0, "4": 4, "5": 1, "6": 3},
            "closed_forms": {
                "c1": "12 = genus numerator = 2*centered shell",
                "c2": "48 = 2*24 = two bosonic/f-sector copies",
                "c3": "0 = missing cubic/q slot",
                "c4": "4 = mu = d_Z = q+1",
                "c5": "1 = center/mean line",
                "c6": "3 = q at the sextic cap",
            },
        },
        "reconstructed_moments": {
            "B_from_histogram": B_from_C,
            "metric_classes_sum_c": metric_classes,
            "edge_instances_sum_m_c": edge_instances,
            "raw_second_sum_m2_c": raw_second,
            "boolean_lift_sum_2m_c": boolean_lift,
            "kernel_sum_m_minus_1_c": edge_instances - metric_classes,
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": "This is an exact finite Taylor/generating-function identity. It interprets the metric edge histogram as derivatives at the parity point; it does not prove physical dynamics or empirical observables by itself.",
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
