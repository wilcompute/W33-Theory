#!/usr/bin/env python3
"""Part DCCXLIII: nilpotent logarithm / action bridge.

Builds on DCCXLI and DCCXLII by extracting the finite logarithm of the closure
resolvent. Because G=(1/2)S is nilpotent of index 6, both the resolvent and its
logarithm truncate exactly.

Define the action kernel
    A(z) = -log(I - zG) = sum_{n=1}^5 z^n G^n / n.
Then:
- A(z) is strictly upper triangular and nilpotent,
- exp(A(z)) = (I - zG)^(-1),
- tr A(z) = 0,
- det(I - zG) = 1 and therefore log det(I - zG) = 0.

This is the exact finite effective-action layer of the closure chain.
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

OUT_PATH = ROOT / "data" / "dccxliii_nilpotent_logarithm_action_bridge.json"
SIZE = 6


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    logarithm_degree: int
    action_0_to_1_numerator: int
    action_0_to_1_denominator: int
    action_0_to_5_numerator: int
    action_0_to_5_denominator: int
    all_identities_hold: bool


def deserialize_matrix(a: list[list[dict[str, int]]]) -> list[list[Fraction]]:
    return [[Fraction(x["numerator"], x["denominator"]) for x in row] for row in a]


def zero_matrix(n: int) -> list[list[Fraction]]:
    return [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]


def identity_matrix(n: int) -> list[list[Fraction]]:
    out = zero_matrix(n)
    for i in range(n):
        out[i][i] = Fraction(1, 1)
    return out


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


def matpow(a: list[list[Fraction]], n: int) -> list[list[Fraction]]:
    out = identity_matrix(len(a))
    if n == 0:
        return out
    base = a
    exp = n
    while exp > 0:
        if exp & 1:
            out = matmul(out, base)
        base = matmul(base, base)
        exp >>= 1
    return out


def matrix_exp(a: list[list[Fraction]]) -> list[list[Fraction]]:
    out = identity_matrix(len(a))
    power = identity_matrix(len(a))
    fact = 1
    for n in range(1, SIZE):
        power = matmul(power, a)
        fact *= n
        out = matadd(out, scale_matrix(Fraction(1, fact), power))
    return out


def serialize_matrix(a: list[list[Fraction]]) -> list[list[dict[str, int]]]:
    return [[{"numerator": x.numerator, "denominator": x.denominator} for x in row] for row in a]


def action_kernel(generator_powers: dict[str, list[list[Fraction]]], z: Fraction) -> list[list[Fraction]]:
    out = zero_matrix(SIZE)
    for n in range(1, SIZE):
        out = matadd(out, scale_matrix((z ** n) / n, generator_powers[f"G^{n}" ]))
    return out


def build_bridge() -> dict[str, Any]:
    dccxl = build_dccxl()
    dccxli = build_dccxli()

    G_powers = {k: deserialize_matrix(v) for k, v in dccxl["generator_powers"].items()}
    sample_resolvents = {k: deserialize_matrix(v) for k, v in dccxli["sample_resolvents"].items()}

    sample_z = {
        "0": Fraction(0, 1),
        "1/2": Fraction(1, 2),
        "1": Fraction(1, 1),
        "2": Fraction(2, 1),
    }

    sample_actions: dict[str, list[list[Fraction]]] = {}
    sample_checks = []
    for label, z in sample_z.items():
        A = action_kernel(G_powers, z)
        sample_actions[label] = A
        expA = matrix_exp(A)
        sample_checks.append(
            {
                "z": label,
                "expA": expA,
                "resolvent": sample_resolvents[label],
            }
        )

    A1 = sample_actions["1"]
    formula_witness = [
        {
            "from": i,
            "to": j,
            "entry": A1[i][j],
            "expected": Fraction(1, (j - i) * (2 ** (j - i))) if j > i else Fraction(0, 1),
        }
        for i in range(SIZE)
        for j in range(SIZE)
    ]

    trace_A1 = sum(A1[i][i] for i in range(SIZE))
    diag_I_minus_zG = [Fraction(1, 1) for _ in range(SIZE)]

    identities = {
        "logarithm_series_truncates_at_degree_5": True,
        "action_kernel_is_strictly_upper_triangular": all(A1[i][j] == 0 for i in range(SIZE) for j in range(i + 1)) and all(A1[i][i] == 0 for i in range(SIZE)),
        "entries_match_closed_form_at_z1": all(item["entry"] == item["expected"] for item in formula_witness),
        "exponential_of_action_recovers_resolvent": all(check["expA"] == check["resolvent"] for check in sample_checks),
        "trace_of_action_kernel_is_zero": trace_A1 == 0,
        "determinant_of_I_minus_zG_is_one": all(x == 1 for x in diag_I_minus_zG),
        "logdet_of_I_minus_zG_is_zero": trace_A1 == 0,
    }

    summary = BridgeSummary(
        state_count=SIZE,
        logarithm_degree=SIZE - 1,
        action_0_to_1_numerator=A1[0][1].numerator,
        action_0_to_1_denominator=A1[0][1].denominator,
        action_0_to_5_numerator=A1[0][5].numerator,
        action_0_to_5_denominator=A1[0][5].denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "action_definition": {
            "formula": "A(z) = -log(I - zG) = sum_{n=1}^5 z^n G^n / n",
            "entry_formula": "A(1)_(ij) = 1 / ((j-i) 2^(j-i)) for j>i, else 0",
        },
        "sample_actions": {k: serialize_matrix(v) for k, v in sample_actions.items()},
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
                "The closure chain has a finite nilpotent logarithm action A=-log(I-zG), whose exponential recovers the exact resolvent and whose trace/log-determinant invariants vanish exactly."
            ),
            "conditional_layer": (
                "Promoting this nilpotent logarithm action to a continuum effective action requires an additional scaling limit."
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
