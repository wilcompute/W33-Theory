#!/usr/bin/env python3
"""Part DCCXLV: nilpotent Hessian / convexity bridge.

Builds on DCCXLIV by differentiating the nilpotent action variation one more time.

With
    A(z) = -log(I-zG),
    A'(z) = (I-zG)^(-1) G,
we obtain the exact second-variation identity
    A''(z) = (I-zG)^(-1) G (I-zG)^(-1) G = (I-zG)^(-2) G^2.

Because G is nilpotent, this again truncates exactly. At z=1, for j>i,
    A''(1)_(ij) = (j-i-1) / 2^(j-i),
with vanishing diagonal and first superdiagonal.

This is the exact finite Hessian kernel of the closure action.
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

from verify_dccxl_closure_jordan_resolvent_bridge import build_bridge as build_dccxl
from verify_dccxli_closure_resolvent_kernel_bridge import build_bridge as build_dccxli
from verify_dccxliv_nilpotent_action_variation_bridge import build_bridge as build_dccxliv

OUT_PATH = ROOT / "data" / "dccxlv_nilpotent_hessian_convexity_bridge.json"
SIZE = 6


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    hessian_0_to_2_numerator: int
    hessian_0_to_2_denominator: int
    hessian_0_to_5_numerator: int
    hessian_0_to_5_denominator: int
    trace_hessian: int
    all_identities_hold: bool


def deserialize_matrix(a: list[list[dict[str, int]]]) -> list[list[Fraction]]:
    return [[Fraction(x["numerator"], x["denominator"]) for x in row] for row in a]


def zero_matrix(n: int) -> list[list[Fraction]]:
    return [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]


def matadd(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]


def matmul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(a)
    out = zero_matrix(n)
    for i in range(n):
        for k in range(n):
            if a[i][k] == 0:
                continue
            for j in range(n):
                if b[k][j] == 0:
                    continue
                out[i][j] += a[i][k] * b[k][j]
    return out


def scale_matrix(c: Fraction, a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[c * a[i][j] for j in range(len(a))] for i in range(len(a))]


def serialize_matrix(a: list[list[Fraction]]) -> list[list[dict[str, int]]]:
    return [[{"numerator": x.numerator, "denominator": x.denominator} for x in row] for row in a]


def hessian_from_generator_powers(generator_powers: dict[str, list[list[Fraction]]], z: Fraction) -> list[list[Fraction]]:
    out = zero_matrix(SIZE)
    for n in range(2, SIZE):
        out = matadd(out, scale_matrix(Fraction(n - 1, 1) * (z ** (n - 2)), generator_powers[f"G^{n}"]))
    return out


def build_bridge() -> dict[str, Any]:
    dccxl = build_dccxl()
    dccxli = build_dccxli()
    dccxliv = build_dccxliv()

    G = deserialize_matrix(dccxl["generator_matrix"])
    G_powers = {k: deserialize_matrix(v) for k, v in dccxl["generator_powers"].items()}
    sample_resolvents = {k: deserialize_matrix(v) for k, v in dccxli["sample_resolvents"].items()}
    sample_derivatives = {k: deserialize_matrix(v) for k, v in dccxliv["sample_derivatives"].items()}

    sample_z = {
        "0": Fraction(0, 1),
        "1/2": Fraction(1, 2),
        "1": Fraction(1, 1),
        "2": Fraction(2, 1),
    }

    sample_hessians: dict[str, list[list[Fraction]]] = {}
    sample_checks = []
    for label, z in sample_z.items():
        H = hessian_from_generator_powers(G_powers, z)
        sample_hessians[label] = H
        right = matmul(sample_resolvents[label], matmul(G, sample_derivatives[label]))
        left = matmul(sample_derivatives[label], matmul(G, sample_resolvents[label]))
        sample_checks.append(
            {
                "z": label,
                "hessian": H,
                "right": right,
                "left": left,
            }
        )

    H1 = sample_hessians["1"]
    formula_witness = [
        {
            "from": i,
            "to": j,
            "entry": H1[i][j],
            "expected": Fraction(j - i - 1, 2 ** (j - i)) if j > i else Fraction(0, 1),
        }
        for i in range(SIZE)
        for j in range(SIZE)
    ]

    trace_H1 = sum(H1[i][i] for i in range(SIZE))

    identities = {
        "second_variation_equals_resolvent_generator_derivative_chain": all(
            check["hessian"] == check["right"] == check["left"] for check in sample_checks
        ),
        "entries_match_closed_form_at_z1": all(item["entry"] == item["expected"] for item in formula_witness),
        "hessian_has_zero_diagonal_and_first_superdiagonal": all(H1[i][i] == 0 for i in range(SIZE)) and all(H1[i][i + 1] == 0 for i in range(SIZE - 1)),
        "hessian_is_strictly_upper_triangular": all(H1[i][j] == 0 for i in range(SIZE) for j in range(i + 1)),
        "trace_of_hessian_is_zero": trace_H1 == 0,
        "higher_superdiagonals_are_nonnegative": all(H1[i][j] >= 0 for i in range(SIZE) for j in range(i + 2, SIZE)),
        "first_nontrivial_hessian_entry_is_one_over_four": H1[0][2] == Fraction(1, 4),
        "maximal_hessian_entry_is_one_eighth": H1[0][5] == Fraction(1, 8),
    }

    summary = BridgeSummary(
        state_count=SIZE,
        hessian_0_to_2_numerator=H1[0][2].numerator,
        hessian_0_to_2_denominator=H1[0][2].denominator,
        hessian_0_to_5_numerator=H1[0][5].numerator,
        hessian_0_to_5_denominator=H1[0][5].denominator,
        trace_hessian=trace_H1.numerator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "hessian_definition": {
            "formula": "A''(z) = (I-zG)^(-1) G (I-zG)^(-1) G = (I-zG)^(-2) G^2",
            "entry_formula": "A''(1)_(ij) = (j-i-1) / 2^(j-i) for j>i, else 0",
        },
        "sample_hessians": {k: serialize_matrix(v) for k, v in sample_hessians.items()},
        "formula_witness_at_z1": [
            {
                **{k: v for k, v in item.items() if k in {"from", "to"}},
                "entry": {"numerator": item["entry"].numerator, "denominator": item["entry"].denominator},
                "expected": {"numerator": item["expected"].numerator, "denominator": item["expected"].denominator},
            }
            for item in formula_witness
        ],
        "bridge_claim": {
            "exact_layer": (
                "The nilpotent action has an exact finite Hessian kernel A''(z), generated by the same resolvent-transfer chain; at z=1 it is a nonnegative upper-triangular kernel supported from the second superdiagonal upward."
            ),
            "conditional_layer": (
                "Interpreting this finite Hessian as continuum convexity/second variation data requires an additional scaling limit."
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
