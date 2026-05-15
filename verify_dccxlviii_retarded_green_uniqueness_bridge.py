#!/usr/bin/env python3
"""Part DCCXLVIII: retarded Green uniqueness bridge.

DCCXLVII gives the finite Ward recursion for the nilpotent action jets.  This
part proves that the recursion has a unique retarded solution inside the
six-level closure-clock sector:

    K = (I-G)^(-1),
    A^(r)(1) = K S_r = S_r K.

There is no homogeneous branch because I-G has an explicit two-sided inverse.
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
from verify_dccxlvii_nilpotent_ward_recursion_bridge import (  # noqa: E402
    build_bridge as build_dccxlvii,
)


OUT_PATH = ROOT / "data" / "dccxlviii_retarded_green_uniqueness_bridge.json"
SIZE = 6


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    solved_ward_orders: int
    retarded_inverse_top_numerator: int
    retarded_inverse_top_denominator: int
    terminal_solution_is_zero: bool
    no_homogeneous_branch: bool
    all_identities_hold: bool


def deserialize_matrix(a: list[list[dict[str, int]]]) -> list[list[Fraction]]:
    return [[Fraction(x["numerator"], x["denominator"]) for x in row] for row in a]


def identity_matrix(n: int) -> list[list[Fraction]]:
    return [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]


def matsub(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] - b[i][j] for j in range(len(a))] for i in range(len(a))]


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    return [
        [sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def serialize_matrix(a: list[list[Fraction]]) -> list[list[dict[str, int]]]:
    return [[{"numerator": x.numerator, "denominator": x.denominator} for x in row] for row in a]


def is_zero_matrix(a: list[list[Fraction]]) -> bool:
    return all(cell == 0 for row in a for cell in row)


def has_causal_upper_support(a: list[list[Fraction]]) -> bool:
    return all(a[i][j] == 0 for i in range(len(a)) for j in range(i))


def build_bridge() -> dict[str, Any]:
    dccxl = build_dccxl()
    dccxlvi = build_dccxlvi()
    dccxlvii = build_dccxlvii()

    generator = deserialize_matrix(dccxl["generator_matrix"])
    propagator = deserialize_matrix(dccxl["matrices"]["propagator"])
    strict_part = deserialize_matrix(dccxl["matrices"]["strict_part"])
    inverse_factor = matsub(identity_matrix(SIZE), generator)
    jets = {
        int(order): deserialize_matrix(matrix)
        for order, matrix in dccxlvi["jet_tower_at_z1"].items()
    }
    left_sources = {
        int(order): deserialize_matrix(matrix)
        for order, matrix in dccxlvii["left_sources"].items()
    }
    right_sources = {
        int(order): deserialize_matrix(matrix)
        for order, matrix in dccxlvii["right_sources"].items()
    }

    left_green_solutions = {
        order: matmul(propagator, left_sources[order])
        for order in range(1, SIZE + 1)
    }
    right_green_solutions = {
        order: matmul(right_sources[order], propagator)
        for order in range(1, SIZE + 1)
    }

    left_solution_residuals = {
        order: matsub(left_green_solutions[order], jets[order])
        for order in range(1, SIZE + 1)
    }
    right_solution_residuals = {
        order: matsub(right_green_solutions[order], jets[order])
        for order in range(1, SIZE + 1)
    }

    left_inverse_check = matmul(inverse_factor, propagator)
    right_inverse_check = matmul(propagator, inverse_factor)

    identities = {
        "retarded_green_is_left_inverse": left_inverse_check == identity_matrix(SIZE),
        "retarded_green_is_right_inverse": right_inverse_check == identity_matrix(SIZE),
        "left_green_solutions_recover_all_jets": all(
            is_zero_matrix(left_solution_residuals[order])
            for order in range(1, SIZE + 1)
        ),
        "right_green_solutions_recover_all_jets": all(
            is_zero_matrix(right_solution_residuals[order])
            for order in range(1, SIZE + 1)
        ),
        "first_solution_is_strict_propagator_part": left_green_solutions[1] == strict_part,
        "terminal_source_maps_to_zero_jet": is_zero_matrix(left_green_solutions[SIZE])
        and is_zero_matrix(right_green_solutions[SIZE])
        and is_zero_matrix(jets[SIZE]),
        "no_homogeneous_branch_inside_closure_clock_sector": (
            left_inverse_check == identity_matrix(SIZE)
            and right_inverse_check == identity_matrix(SIZE)
        ),
        "retarded_green_has_causal_upper_support": has_causal_upper_support(propagator),
        "source_solutions_have_causal_upper_support": all(
            has_causal_upper_support(left_green_solutions[order])
            and has_causal_upper_support(right_green_solutions[order])
            for order in range(1, SIZE + 1)
        ),
    }

    summary = BridgeSummary(
        state_count=SIZE,
        solved_ward_orders=SIZE,
        retarded_inverse_top_numerator=propagator[0][-1].numerator,
        retarded_inverse_top_denominator=propagator[0][-1].denominator,
        terminal_solution_is_zero=identities["terminal_source_maps_to_zero_jet"],
        no_homogeneous_branch=identities[
            "no_homogeneous_branch_inside_closure_clock_sector"
        ],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "green_definition": {
            "operator": "D = I - G",
            "retarded_green": "K = D^(-1) = I + G + G^2 + G^3 + G^4 + G^5",
            "ward_solution": "A^(r)(1) = K S_r = S_r K for Ward source S_r",
            "homogeneous_boundary": "D H = 0 implies H = K 0 = 0 in this finite sector.",
        },
        "inverse_factor": serialize_matrix(inverse_factor),
        "retarded_green": serialize_matrix(propagator),
        "left_inverse_check": serialize_matrix(left_inverse_check),
        "right_inverse_check": serialize_matrix(right_inverse_check),
        "left_green_solutions": {
            str(k): serialize_matrix(v) for k, v in left_green_solutions.items()
        },
        "right_green_solutions": {
            str(k): serialize_matrix(v) for k, v in right_green_solutions.items()
        },
        "left_solution_residuals": {
            str(k): serialize_matrix(v) for k, v in left_solution_residuals.items()
        },
        "right_solution_residuals": {
            str(k): serialize_matrix(v) for k, v in right_solution_residuals.items()
        },
        "bridge_claim": {
            "exact_layer": (
                "The Ward sources have unique retarded solutions in the closure-clock sector: K is the two-sided inverse of I-G, every source maps back to the corresponding jet, and the zero terminal source maps to the zero sixth jet."
            ),
            "conditional_layer": (
                "This is finite retarded Green uniqueness for the nilpotent clock operator, not a continuum causal Green function without an external scaling theorem."
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
