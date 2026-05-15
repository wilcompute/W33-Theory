#!/usr/bin/env python3
"""Part DCCXLVII: nilpotent Ward-recursion bridge.

DCCXLVI proves the complete finite jet tower for

    A(z) = -log(I-zG).

This verifier proves the corresponding finite Ward / Schwinger-Dyson
recursion at z=1:

    (I-G) A'(1) = G,
    (I-G) A^(r)(1) = (r-1) G A^(r-1)(1),  r = 2..6.

Because all jets are polynomials in the same nilpotent generator, the right
Ward equations hold too, and the sixth-order source vanishes exactly.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxl_closure_jordan_resolvent_bridge import (  # noqa: E402
    build_bridge as build_dccxl,
)
from verify_dccxlvi_nilpotent_action_jet_tower_bridge import (  # noqa: E402
    build_bridge as build_dccxlvi,
)


OUT_PATH = ROOT / "data" / "dccxlvii_nilpotent_ward_recursion_bridge.json"
SIZE = 6


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    ward_orders_checked: int
    first_source_numerator: int
    first_source_denominator: int
    terminal_source_is_zero: bool
    left_and_right_constraints_hold: bool
    all_identities_hold: bool


def deserialize_matrix(a: list[list[dict[str, int]]]) -> list[list[Fraction]]:
    return [[Fraction(x["numerator"], x["denominator"]) for x in row] for row in a]


def zero_matrix(n: int) -> list[list[Fraction]]:
    return [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]


def identity_matrix(n: int) -> list[list[Fraction]]:
    return [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]


def matadd(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]


def matsub(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] - b[i][j] for j in range(len(a))] for i in range(len(a))]


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    return [
        [sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def scale_matrix(c: Fraction, a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[c * a[i][j] for j in range(len(a))] for i in range(len(a))]


def serialize_matrix(a: list[list[Fraction]]) -> list[list[dict[str, int]]]:
    return [[{"numerator": x.numerator, "denominator": x.denominator} for x in row] for row in a]


def is_zero_matrix(a: list[list[Fraction]]) -> bool:
    return all(cell == 0 for row in a for cell in row)


def build_bridge() -> dict[str, Any]:
    dccxl = build_dccxl()
    dccxlvi = build_dccxlvi()

    generator = deserialize_matrix(dccxl["generator_matrix"])
    identity_minus_generator = matsub(identity_matrix(SIZE), generator)
    jets = {
        int(order): deserialize_matrix(matrix)
        for order, matrix in dccxlvi["jet_tower_at_z1"].items()
    }

    left_sources: dict[int, list[list[Fraction]]] = {}
    right_sources: dict[int, list[list[Fraction]]] = {}
    left_residuals: dict[int, list[list[Fraction]]] = {}
    right_residuals: dict[int, list[list[Fraction]]] = {}

    for order in range(1, SIZE + 1):
        if order == 1:
            left_source = generator
            right_source = generator
        else:
            left_source = scale_matrix(
                Fraction(order - 1, 1),
                matmul(generator, jets[order - 1]),
            )
            right_source = scale_matrix(
                Fraction(order - 1, 1),
                matmul(jets[order - 1], generator),
            )

        left_sources[order] = left_source
        right_sources[order] = right_source
        left_residuals[order] = matsub(
            matmul(identity_minus_generator, jets[order]),
            left_source,
        )
        right_residuals[order] = matsub(
            matmul(jets[order], identity_minus_generator),
            right_source,
        )

    commutators = {
        order: matsub(matmul(generator, jets[order]), matmul(jets[order], generator))
        for order in range(SIZE + 1)
    }

    identities = {
        "left_ward_equations_hold_for_orders_1_through_6": all(
            is_zero_matrix(left_residuals[order]) for order in range(1, SIZE + 1)
        ),
        "right_ward_equations_hold_for_orders_1_through_6": all(
            is_zero_matrix(right_residuals[order]) for order in range(1, SIZE + 1)
        ),
        "all_jets_commute_with_nilpotent_generator": all(
            is_zero_matrix(commutators[order]) for order in range(SIZE + 1)
        ),
        "first_ward_source_is_the_generator": left_sources[1] == generator,
        "sixth_jet_is_zero": is_zero_matrix(jets[SIZE]),
        "sixth_ward_source_is_zero": is_zero_matrix(left_sources[SIZE])
        and is_zero_matrix(right_sources[SIZE]),
        "terminal_residual_is_zero": is_zero_matrix(left_residuals[SIZE])
        and is_zero_matrix(right_residuals[SIZE]),
        "source_recursion_is_symmetric": all(
            left_sources[order] == right_sources[order] for order in range(1, SIZE + 1)
        ),
    }

    summary = BridgeSummary(
        state_count=SIZE,
        ward_orders_checked=SIZE,
        first_source_numerator=generator[0][1].numerator,
        first_source_denominator=generator[0][1].denominator,
        terminal_source_is_zero=identities["sixth_ward_source_is_zero"],
        left_and_right_constraints_hold=(
            identities["left_ward_equations_hold_for_orders_1_through_6"]
            and identities["right_ward_equations_hold_for_orders_1_through_6"]
        ),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "ward_definition": {
            "first_equation": "(I-G) A'(1) = G",
            "higher_equations": "(I-G) A^(r)(1) = (r-1) G A^(r-1)(1), r=2..6",
            "right_equations": "A^(r)(1) (I-G) = (r-1) A^(r-1)(1) G, r=2..6",
            "reason_right_equals_left": "Each jet is a polynomial in the same nilpotent generator G.",
        },
        "identity_minus_generator": serialize_matrix(identity_minus_generator),
        "left_sources": {str(k): serialize_matrix(v) for k, v in left_sources.items()},
        "right_sources": {str(k): serialize_matrix(v) for k, v in right_sources.items()},
        "left_residuals": {str(k): serialize_matrix(v) for k, v in left_residuals.items()},
        "right_residuals": {str(k): serialize_matrix(v) for k, v in right_residuals.items()},
        "generator_commutators": {str(k): serialize_matrix(v) for k, v in commutators.items()},
        "bridge_claim": {
            "exact_layer": (
                "The nilpotent closure action obeys exact finite Ward recursions: every higher jet is sourced by the previous jet through the same generator, and the recursion terminates when G kills the fifth jet."
            ),
            "conditional_layer": (
                "Calling this a continuum Schwinger-Dyson equation requires a separate scaling limit; this verifier proves the finite operator identity."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
