#!/usr/bin/env python3
"""Part DCCXLVI: nilpotent action jet-tower bridge.

DCCXLIII-DCCXLV established the nilpotent logarithm action, its first
variation, and its Hessian.  Since

    A(z) = -log(I-zG) = sum_{d=1}^5 z^d G^d / d

is a degree-5 polynomial, the entire variation hierarchy is finite.

At z=1, the r-th derivative has closed-form entries

    A^(r)(1)_(ij) = ((d-1)! / (d-r)!) / 2^d,  d=j-i >= r >= 1,
    A(1)_(ij)    = 1 / (d 2^d),              d=j-i >= 1,

and vanishes otherwise.  The sixth derivative is zero.
"""

from __future__ import annotations

import json
import math
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


OUT_PATH = ROOT / "data" / "dccxlvi_nilpotent_action_jet_tower_bridge.json"
SIZE = 6


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    highest_nonzero_derivative_order: int
    first_zero_derivative_order: int
    top_path_fifth_derivative_numerator: int
    top_path_fifth_derivative_denominator: int
    all_identities_hold: bool


def deserialize_matrix(a: list[list[dict[str, int]]]) -> list[list[Fraction]]:
    return [[Fraction(x["numerator"], x["denominator"]) for x in row] for row in a]


def zero_matrix(n: int) -> list[list[Fraction]]:
    return [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]


def matadd(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]


def scale_matrix(c: Fraction, a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[c * a[i][j] for j in range(len(a))] for i in range(len(a))]


def serialize_matrix(a: list[list[Fraction]]) -> list[list[dict[str, int]]]:
    return [[{"numerator": x.numerator, "denominator": x.denominator} for x in row] for row in a]


def jet_kernel(generator_powers: dict[str, list[list[Fraction]]], order: int) -> list[list[Fraction]]:
    out = zero_matrix(SIZE)
    if order == 0:
        for d in range(1, SIZE):
            out = matadd(out, scale_matrix(Fraction(1, d), generator_powers[f"G^{d}"]))
        return out

    for d in range(order, SIZE):
        coefficient = Fraction(math.factorial(d - 1), math.factorial(d - order))
        out = matadd(out, scale_matrix(coefficient, generator_powers[f"G^{d}"]))
    return out


def expected_entry(order: int, i: int, j: int) -> Fraction:
    d = j - i
    if d <= 0:
        return Fraction(0, 1)
    if order == 0:
        return Fraction(1, d * (2 ** d))
    if d < order:
        return Fraction(0, 1)
    return Fraction(math.factorial(d - 1), math.factorial(d - order) * (2 ** d))


def build_bridge() -> dict[str, Any]:
    dccxl = build_dccxl()
    generator_powers = {
        k: deserialize_matrix(v) for k, v in dccxl["generator_powers"].items()
    }
    jets = {order: jet_kernel(generator_powers, order) for order in range(SIZE + 1)}

    formula_witness = [
        {
            "order": order,
            "from": i,
            "to": j,
            "entry": jets[order][i][j],
            "expected": expected_entry(order, i, j),
        }
        for order in range(SIZE + 1)
        for i in range(SIZE)
        for j in range(SIZE)
    ]

    top_path_profile = {
        str(order): jets[order][0][SIZE - 1] for order in range(SIZE + 1)
    }

    identities = {
        "jet_orders_are_zero_through_six": set(jets) == set(range(SIZE + 1)),
        "closed_form_entries_hold_for_all_orders": all(
            item["entry"] == item["expected"] for item in formula_witness
        ),
        "zeroth_order_matches_logarithm_action": (
            jets[0][0][1] == Fraction(1, 2)
            and jets[0][0][2] == Fraction(1, 8)
            and jets[0][0][5] == Fraction(1, 160)
        ),
        "first_order_matches_variation_kernel": (
            jets[1][0][1] == Fraction(1, 2)
            and jets[1][0][2] == Fraction(1, 4)
            and jets[1][0][5] == Fraction(1, 32)
        ),
        "second_order_matches_hessian_kernel": (
            jets[2][0][1] == 0
            and jets[2][0][2] == Fraction(1, 4)
            and jets[2][0][5] == Fraction(1, 8)
        ),
        "support_starts_on_the_order_superdiagonal": all(
            jets[order][i][j] == 0
            for order in range(1, SIZE)
            for i in range(SIZE)
            for j in range(SIZE)
            if j - i < order
        ),
        "sixth_derivative_vanishes": all(
            jets[SIZE][i][j] == 0 for i in range(SIZE) for j in range(SIZE)
        ),
        "all_z1_jet_entries_are_nonnegative": all(
            jets[order][i][j] >= 0
            for order in range(SIZE + 1)
            for i in range(SIZE)
            for j in range(SIZE)
        ),
        "top_path_profile_is_exact": top_path_profile == {
            "0": Fraction(1, 160),
            "1": Fraction(1, 32),
            "2": Fraction(1, 8),
            "3": Fraction(3, 8),
            "4": Fraction(3, 4),
            "5": Fraction(3, 4),
            "6": Fraction(0, 1),
        },
    }

    summary = BridgeSummary(
        state_count=SIZE,
        highest_nonzero_derivative_order=SIZE - 1,
        first_zero_derivative_order=SIZE,
        top_path_fifth_derivative_numerator=top_path_profile["5"].numerator,
        top_path_fifth_derivative_denominator=top_path_profile["5"].denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "jet_definition": {
            "action": "A(z) = sum_{d=1}^5 z^d G^d / d",
            "closed_form": (
                "A^(r)(1)_(ij)=((d-1)!/(d-r)!)/2^d for d=j-i>=r>=1; "
                "A(1)_(ij)=1/(d 2^d) for d>=1"
            ),
            "first_zero_derivative": "A^(6)(z)=0",
        },
        "jet_tower_at_z1": {str(k): serialize_matrix(v) for k, v in jets.items()},
        "top_path_profile": {
            k: {"numerator": v.numerator, "denominator": v.denominator}
            for k, v in top_path_profile.items()
        },
        "formula_witness": [
            {
                "order": item["order"],
                "from": item["from"],
                "to": item["to"],
                "entry": {
                    "numerator": item["entry"].numerator,
                    "denominator": item["entry"].denominator,
                },
                "expected": {
                    "numerator": item["expected"].numerator,
                    "denominator": item["expected"].denominator,
                },
            }
            for item in formula_witness
        ],
        "bridge_claim": {
            "exact_layer": (
                "The nilpotent closure action has a complete finite jet tower: orders 0 through 5 are nonzero finite upper-triangular kernels with closed-form entries, and order 6 vanishes exactly."
            ),
            "conditional_layer": (
                "Interpreting this finite jet tower as a continuum variational calculus requires a separate scaling limit."
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
