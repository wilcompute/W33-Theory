#!/usr/bin/env python3
r"""Exact 1+24+15 Bose--Mesner packet and rank-78 motivic candidate.

The W(3,3) adjacency algebra has basis I,A,J and multiplication

    A^2 = 8 I - 2 A + 4 J,
    A J = J A = 12 J,
    J^2 = 40 J.

Its primitive idempotents are the spectral projectors for eigenvalues
12, 2, and -4.  Their traces are 1, 24, and 15.  This gives a canonical
rational decomposition of the 40-point permutation module that is invariant
under every graph automorphism.

Combining the 24- and 15-dimensional packets with the two explicit elliptic
curves from the norm-11 bridge gives an honest rank-78 l-adic/motivic candidate

    H^1(E_2)^{\oplus 24} \oplus H^1(E_{-4})^{\oplus 15}.

At p=11 its Frobenius characteristic polynomial equals the complete
nontrivial W33 Ihara inverse factor.  This is an exact local realization and a
concrete global candidate motive.  It is not a proof that W33 geometry itself
constructs this motive, nor that its full L-function is Riemann xi.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

Element = tuple[Fraction, Fraction, Fraction]
I: Element = (Fraction(1), Fraction(0), Fraction(0))
A: Element = (Fraction(0), Fraction(1), Fraction(0))
J: Element = (Fraction(0), Fraction(0), Fraction(1))
ZERO: Element = (Fraction(0), Fraction(0), Fraction(0))


def add(x: Element, y: Element) -> Element:
    return tuple(a + b for a, b in zip(x, y))  # type: ignore[return-value]


def scale(c: Fraction, x: Element) -> Element:
    return tuple(c * a for a in x)  # type: ignore[return-value]


def multiply(x: Element, y: Element) -> Element:
    xi, xa, xj = x
    yi, ya, yj = y
    return (
        xi * yi + 8 * xa * ya,
        xi * ya + xa * yi - 2 * xa * ya,
        xi * yj
        + xj * yi
        + 4 * xa * ya
        + 12 * (xa * yj + xj * ya)
        + 40 * xj * yj,
    )


def trace(x: Element) -> Fraction:
    c_i, _, c_j = x
    return 40 * (c_i + c_j)


def as_strings(x: Element) -> dict[str, str]:
    return {name: str(value) for name, value in zip(("I", "A", "J"), x)}


P12: Element = (Fraction(0), Fraction(0), Fraction(1, 40))
P2: Element = (Fraction(2, 3), Fraction(1, 6), Fraction(-1, 15))
PM4: Element = (Fraction(1, 3), Fraction(-1, 6), Fraction(1, 24))
PROJECTORS = {"12": P12, "2": P2, "-4": PM4}


def count_points_mod_p(a: int, b: int, p: int) -> int:
    total = 1
    for x in range(p):
        rhs = (x**3 + a * x + b) % p
        total += sum(1 for y in range(p) if y * y % p == rhs)
    return total


def local_trace(a: int, b: int, p: int) -> int:
    return p + 1 - count_points_mod_p(a, b, p)


def polynomial_power(base: list[int], exponent: int) -> list[int]:
    result = [1]
    for _ in range(exponent):
        product = [0] * (len(result) + len(base) - 1)
        for i, left in enumerate(result):
            for j, right in enumerate(base):
                product[i + j] += left * right
        result = product
    return result


def polynomial_multiply(left: list[int], right: list[int]) -> list[int]:
    product = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            product[i + j] += x * y
    return product


def build_certificate() -> dict[str, Any]:
    ranks = {label: int(trace(projector)) for label, projector in PROJECTORS.items()}
    pairwise_products = {
        f"{left}*{right}": as_strings(multiply(PROJECTORS[left], PROJECTORS[right]))
        for left in PROJECTORS
        for right in PROJECTORS
    }

    sum_projectors = ZERO
    for projector in PROJECTORS.values():
        sum_projectors = add(sum_projectors, projector)

    curves = {
        "E_2": {"a": 1, "b": -1, "equation": "y^2=x^3+x-1", "multiplicity": 24},
        "E_-4": {"a": 1, "b": 2, "equation": "y^2=x^3+x+2", "multiplicity": 15},
    }
    local_packets = {}
    local_polynomial = [1]
    expected_polynomial = polynomial_multiply(
        polynomial_power([1, -2, 11], 24),
        polynomial_power([1, 4, 11], 15),
    )
    for name, curve in curves.items():
        trace_11 = local_trace(curve["a"], curve["b"], 11)
        factor = [1, -trace_11, 11]
        local_polynomial = polynomial_multiply(
            local_polynomial, polynomial_power(factor, curve["multiplicity"])
        )
        local_packets[name] = {
            **curve,
            "points_F_11": count_points_mod_p(curve["a"], curve["b"], 11),
            "a_11": trace_11,
            "frobenius_factor_coefficients": factor,
            "H1_rank": 2,
            "packet_rank": 2 * curve["multiplicity"],
        }

    checks = {
        "projectors_idempotent": all(
            multiply(projector, projector) == projector
            for projector in PROJECTORS.values()
        ),
        "projectors_pairwise_orthogonal": all(
            multiply(PROJECTORS[left], PROJECTORS[right]) == ZERO
            for left in PROJECTORS
            for right in PROJECTORS
            if left != right
        ),
        "projectors_sum_to_identity": sum_projectors == I,
        "ranks_are_1_24_15": ranks == {"12": 1, "2": 24, "-4": 15},
        "point_module_dimension_is_40": sum(ranks.values()) == 40,
        "nontrivial_motive_rank_is_78": 2 * (ranks["2"] + ranks["-4"]) == 78,
        "explicit_curves_have_W33_traces_at_11": (
            local_packets["E_2"]["a_11"] == 2
            and local_packets["E_-4"]["a_11"] == -4
        ),
        "local_motive_polynomial_equals_W33_nontrivial_factor": (
            local_polynomial == expected_polynomial
        ),
        "local_polynomial_degree_is_78": len(local_polynomial) - 1 == 78,
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "canonical W33 adjacency packets and explicit rank-78 elliptic motive candidate",
        "bose_mesner_algebra": {
            "basis": ["I", "A", "J"],
            "relations": {"A^2": "8I-2A+4J", "AJ=JA": "12J", "J^2": "40J"},
            "primitive_projectors": {
                label: {"coefficients": as_strings(projector), "rank": ranks[label]}
                for label, projector in PROJECTORS.items()
            },
            "pairwise_products": pairwise_products,
            "decomposition": "Q^40 = V_12 direct_sum V_2 direct_sum V_-4 with dimensions 1+24+15",
            "automorphism_invariance": "every graph automorphism commutes with A and therefore preserves all three spectral packets",
        },
        "motivic_candidate": {
            "object": "M_W = H^1(E_2)^{oplus 24} direct_sum H^1(E_-4)^{oplus 15}",
            "rank": 78,
            "local_prime": 11,
            "elliptic_packets": local_packets,
            "local_characteristic_polynomial": "(1-2u+11u^2)^24(1+4u+11u^2)^15",
            "degree": len(local_polynomial) - 1,
            "coefficient_checksum": {
                "constant": local_polynomial[0],
                "linear": local_polynomial[1],
                "middle_39": local_polynomial[39],
                "leading": local_polynomial[-1],
            },
        },
        "claim_boundary": {
            "proved": [
                "the exact rational 1+24+15 primitive-idempotent decomposition",
                "automorphism invariance of the three adjacency packets",
                "an honest global rank-78 direct-sum elliptic motive whose p=11 factor is exactly W33",
            ],
            "not_proved": [
                "that a natural W33 variety or stack has this etale cohomology",
                "that the 24 and 15 packets are globally forced rather than deliberately assigned",
                "that the full L-function of this motive is the completed Riemann zeta function",
            ],
            "next_exact_target": "construct a W33-equivariant correspondence whose cohomological projectors are P2 and P-4 and whose Frobenius at 11 is the two-curve packet",
        },
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_motivic_24_15_packet_certificate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
