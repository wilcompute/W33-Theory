#!/usr/bin/env python3
"""Generating-function layer of the toroidal metric moment operator.

The metric multiplicity histogram across the seven Csaszar/Szilassi
realizations is

    1^12, 2^48, 4^4, 5^1, 6^3.

The binomial moment sequence is

    B_k = sum_classes C(m,k) = 68,147,127,86,54,19,3.

This script packages those moments into the polynomial

    P(t)=sum_k B_k t^k
        = 68 + 147t + 127t^2 + 86t^3 + 54t^4 + 19t^5 + 3t^6.

New exact identities:

    P(-1)=0,
    P(t)=(1+t) Q(t),
    Q(t)=68 + 79t + 48t^2 + 38t^3 + 16t^4 + 3t^5,
    Q(-1)=12,
    Q(1)=252=21*12,
    P(1)=504=7*72.

So the metric moment polynomial has a parity-null factor (1+t), and the
quotient has the phase-kernel coefficient 79 and returns the genus numerator
12 at t=-1.

Cyclotomic residues add another exact checksum:

    P mod Phi_3 = 11 + 55 t = 11(1+5t),

whose Eisenstein norm is

    11^2 * 21.

Thus the Phi_3 evaluation sees the Ihara prime 11 and the toroidal edge count
21 simultaneously.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "w33_toroidal_metric_generating_function.json"

# B_k = sum C(m,k) for the seven-realization metric edge multiplicity packet.
B = [68, 147, 127, 86, 54, 19, 3]
# P(t) coefficients low-to-high.
P = B[:]
# Q(t) = P(t)/(1+t), coefficients low-to-high.
Q = [68, 79, 48, 38, 16, 3]


def poly_eval(coeffs: list[int], x: int) -> int:
    return sum(c * (x ** i) for i, c in enumerate(coeffs))


def poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            out[i + j] += ca * cb
    return out


def rem_mod_quadratic(coeffs: list[int], relation: str) -> tuple[int, int]:
    """Return a+b*x modulo a quadratic cyclotomic relation.

    relation='phi3': x^2+x+1=0 => x^2=-x-1.
    relation='phi4': x^2+1=0 => x^2=-1.
    relation='phi6': x^2-x+1=0 => x^2=x-1.
    """
    a, b = 0, 0
    powers: list[tuple[int, int]] = [(1, 0), (0, 1)]
    for n in range(2, len(coeffs)):
        prev2 = powers[n - 2]
        prev1 = powers[n - 1]
        if relation == "phi3":
            # x^n = x^(n-2) x^2 = -x^(n-1)-x^(n-2)
            powers.append((-prev1[0] - prev2[0], -prev1[1] - prev2[1]))
        elif relation == "phi4":
            # x^n = -x^(n-2)
            powers.append((-prev2[0], -prev2[1]))
        elif relation == "phi6":
            # x^n = x^(n-1)-x^(n-2)
            powers.append((prev1[0] - prev2[0], prev1[1] - prev2[1]))
        else:
            raise ValueError(relation)
    for c, (pa, pb) in zip(coeffs, powers):
        a += c * pa
        b += c * pb
    return a, b


def norm_phi3(a: int, b: int) -> int:
    # Norm in Z[omega], omega^2+omega+1=0: N(a+b omega)=a^2-ab+b^2.
    return a * a - a * b + b * b


def norm_phi4(a: int, b: int) -> int:
    # Gaussian norm.
    return a * a + b * b


def norm_phi6(a: int, b: int) -> int:
    # Norm for zeta_6 with zeta^2-zeta+1=0: a^2+ab+b^2.
    return a * a + a * b + b * b


def build_payload() -> dict[str, Any]:
    P_from_Q = poly_mul([1, 1], Q)
    p1 = poly_eval(P, 1)
    pm1 = poly_eval(P, -1)
    q1 = poly_eval(Q, 1)
    qm1 = poly_eval(Q, -1)

    phi3_rem = rem_mod_quadratic(P, "phi3")
    phi4_rem = rem_mod_quadratic(P, "phi4")
    phi6_rem = rem_mod_quadratic(P, "phi6")
    phi3_norm = norm_phi3(*phi3_rem)
    phi4_norm = norm_phi4(*phi4_rem)
    phi6_norm = norm_phi6(*phi6_rem)

    identities = {
        "factorization": P_from_Q == P,
        "parity_null": pm1 == 0,
        "quotient_kernel_coefficient": Q[1] == 79,
        "quotient_minus_one_genus": qm1 == 12,
        "quotient_plus_one": q1 == 252 == 21 * 12,
        "boolean_total_middle_eigenvalue": p1 == 504 == 7 * 72 == 21 * 24,
        "B0_B1_kernel": B[1] - B[0] == 79,
        "B2_heptad_boolean": B[2] == 127 == 2**7 - 1,
        "phi3_residue": phi3_rem == (11, 55),
        "phi3_norm": phi3_norm == 11 * 11 * 21,
        "phi4_residue": phi4_rem == (-8, 80),
        "phi4_norm": phi4_norm == 6464,
        "phi6_residue": phi6_rem == (-123, 201),
        "phi6_norm": phi6_norm == 30807,
    }

    theorem = (
        "Toroidal Metric Generating Function Theorem.  The binomial moment "
        "sequence of the seven-realization metric edge spectrum defines "
        "P(t)=68+147t+127t^2+86t^3+54t^4+19t^5+3t^6.  This polynomial has "
        "the exact factorization P(t)=(1+t)(68+79t+48t^2+38t^3+16t^4+3t^5). "
        "The factor (1+t) is the parity-null/euler cancellation; the quotient "
        "contains the phase-kernel coefficient 79 and evaluates to the genus "
        "numerator 12 at t=-1.  Its Boolean value gives P(1)=504=7*72, "
        "so the middle eigenvalue 72 is the per-realization Boolean lift.  "
        "Modulo Phi_3, P reduces to 11(1+5t), whose Eisenstein norm is "
        "11^2*21, exposing the Ihara prime and toroidal edge count together."
    )

    return {
        "summary": {
            "P_coefficients_low_to_high": P,
            "Q_coefficients_low_to_high": Q,
            "factorization": "P(t)=(1+t)Q(t)",
            "P_minus_1": pm1,
            "Q_minus_1": qm1,
            "P_plus_1": p1,
            "Q_plus_1": q1,
            "all_identities_hold": all(identities.values()),
        },
        "polynomial": {
            "P": "68 + 147 t + 127 t^2 + 86 t^3 + 54 t^4 + 19 t^5 + 3 t^6",
            "Q": "68 + 79 t + 48 t^2 + 38 t^3 + 16 t^4 + 3 t^5",
            "factorization": "P=(1+t)Q",
            "evaluations": {
                "P(-1)": pm1,
                "Q(-1)": qm1,
                "P(1)": p1,
                "Q(1)": q1,
            },
        },
        "cyclotomic_residues": {
            "Phi3": {
                "relation": "t^2+t+1=0",
                "residue_a_plus_b_t": list(phi3_rem),
                "residue_closed_form": "11 + 55 t = 11(1+5t)",
                "norm": phi3_norm,
                "norm_closed_form": "11^2 * 21",
            },
            "Phi4": {
                "relation": "t^2+1=0",
                "residue_a_plus_b_t": list(phi4_rem),
                "residue_closed_form": "-8 + 80 t = 8(-1+10t)",
                "norm": phi4_norm,
            },
            "Phi6": {
                "relation": "t^2-t+1=0",
                "residue_a_plus_b_t": list(phi6_rem),
                "residue_closed_form": "-123 + 201 t = 3(-41+67t)",
                "norm": phi6_norm,
            },
        },
        "closed_forms": {
            "parity_null": "P(-1)=0",
            "kernel_in_quotient": "coefficient of t in Q is 79",
            "genus_from_quotient": "Q(-1)=12",
            "middle_eigenvalue": "P(1)/7=72",
            "half_boolean_lift": "Q(1)=252=21*12",
            "heptad_subsets": "B2=127=2^7-1",
            "Ihara_toroidal_norm": "Norm_{Phi3}(P)=11^2*21",
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": "This is an exact finite generating-function identity for the toroidal metric edge spectrum. It does not by itself prove physical dynamics or empirical observables.",
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
