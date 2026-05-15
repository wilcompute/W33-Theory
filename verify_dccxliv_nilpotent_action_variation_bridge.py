#!/usr/bin/env python3
"""Part DCCXLIV: nilpotent action variation bridge.

Builds on DCCXLIII by differentiating the finite logarithm action

    A(z) = -log(I - zG).

Because G is nilpotent and commutes with every polynomial in itself, the exact
variation law is

    dA/dz = (I - zG)^(-1) G = G (I - zG)^(-1).

Equivalently, for j > i,

    d/dz A(z)_{ij} = z^(j-i-1) / 2^(j-i),

and at z = 1 this becomes the exact geometric kernel

    (A'(1))_{ij} = 1 / 2^(j-i).

This part makes the action variation / stationarity law explicit.
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

from verify_dccxl_closure_transfer_generator_bridge import build_bridge as build_dccxl
from verify_dccxli_closure_resolvent_kernel_bridge import build_bridge as build_dccxli
from verify_dccxliii_nilpotent_logarithm_action_bridge import build_bridge as build_dccxliii

OUT_PATH = ROOT / "data" / "dccxliv_nilpotent_action_variation_bridge.json"
SIZE = 6


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    derivative_0_to_1_numerator: int
    derivative_0_to_1_denominator: int
    derivative_0_to_5_numerator: int
    derivative_0_to_5_denominator: int
    trace_derivative: int
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


def derivative_from_generator_powers(generator_powers: dict[str, list[list[Fraction]]], z: Fraction) -> list[list[Fraction]]:
    out = zero_matrix(SIZE)
    for n in range(1, SIZE):
        out = matadd(out, scale_matrix(z ** (n - 1), generator_powers[f"G^{n}"]))
    return out


def build_bridge() -> dict[str, Any]:
    dccxl = build_dccxl()
    dccxli = build_dccxli()
    dccxliii = build_dccxliii()

    G = deserialize_matrix(dccxl["generator_matrix"])
    G_powers = {k: deserialize_matrix(v) for k, v in dccxl["generator_powers"].items()}
    sample_resolvents = {k: deserialize_matrix(v) for k, v in dccxli["sample_resolvents"].items()}

    sample_z = {
        "0": Fraction(0, 1),
        "1/2": Fraction(1, 2),
        "1": Fraction(1, 1),
        "2": Fraction(2, 1),
    }

    sample_derivatives: dict[str, list[list[Fraction]]] = {}
    sample_checks = []
    for label, z in sample_z.items():
        deriv = derivative_from_generator_powers(G_powers, z)
        sample_derivatives[label] = deriv
        right = matmul(sample_resolvents[label], G)
        left = matmul(G, sample_resolvents[label])
        sample_checks.append(
            {
                "z": label,
                "derivative": deriv,
                "right": right,
                "left": left,
            }
        )

    D1 = sample_derivatives["1"]
    formula_witness = [
        {
            "from": i,
            "to": j,
            "entry": D1[i][j],
            "expected": Fraction(1, 2 ** (j - i)) if j > i else Fraction(0, 1),
        }
        for i in range(SIZE)
        for j in range(SIZE)
    ]

    trace_D1 = sum(D1[i][i] for i in range(SIZE))
    A1 = deserialize_matrix(dccxliii["sample_actions"]["1"])
    stationarity_gap = matadd(D1, scale_matrix(-1, matmul(sample_resolvents["1"], G)))

    identities = {
        "variation_equals_resolvent_times_generator": all(
            check["derivative"] == check["right"] == check["left"] for check in sample_checks
        ),
        "entries_match_closed_form_at_z1": all(item["entry"] == item["expected"] for item in formula_witness),
        "derivative_is_strictly_upper_triangular": all(D1[i][j] == 0 for i in range(SIZE) for j in range(i + 1)) and all(D1[i][i] == 0 for i in range(SIZE)),
        "trace_of_derivative_is_zero": trace_D1 == 0,
        "variation_commutes_with_generator_chain": matmul(D1, G) == matmul(G, D1),
        "stationarity_gap_vanishes_exactly": all(x == 0 for row in stationarity_gap for x in row),
        "action_entries_integrate_derivative_entries": all(
            A1[i][j] == Fraction(1, j - i) * D1[i][j] for i in range(SIZE) for j in range(i + 1, SIZE)
        ),
    }

    summary = BridgeSummary(
        state_count=SIZE,
        derivative_0_to_1_numerator=D1[0][1].numerator,
        derivative_0_to_1_denominator=D1[0][1].denominator,
        derivative_0_to_5_numerator=D1[0][5].numerator,
        derivative_0_to_5_denominator=D1[0][5].denominator,
        trace_derivative=trace_D1.numerator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "variation_definition": {
            "formula": "dA/dz = (I - zG)^(-1) G = G (I - zG)^(-1)",
            "entry_formula": "A'(1)_(ij) = 1 / 2^(j-i) for j>i, else 0",
        },
        "sample_derivatives": {k: serialize_matrix(v) for k, v in sample_derivatives.items()},
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
                "The nilpotent logarithm action has an exact variation law dA/dz = R(z)G = GR(z); its derivative is a strictly upper-triangular geometric kernel and its stationarity gap vanishes identically."
            ),
            "conditional_layer": (
                "Interpreting this finite variation law as a continuum Euler-Lagrange equation requires an additional scaling limit."
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
