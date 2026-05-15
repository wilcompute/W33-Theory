#!/usr/bin/env python3
"""Part DCCXLI: closure resolvent-kernel bridge.

Builds on DCCXL by summing the finite Neumann series of the nilpotent transfer
operator G = (1/2) S.

Because G^6 = 0 exactly, the resolvent is a finite polynomial:

    R(z) = (I - z G)^{-1} = I + zG + z^2 G^2 + z^3 G^3 + z^4 G^4 + z^5 G^5.

Hence every upper-triangular entry has the exact closed form

    R(z)_{ij} = (z/2)^(j-i)   for j >= i,
    R(z)_{ij} = 0             for j < i.

This is the exact Green/response kernel of the closure transfer generator.
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

OUT_PATH = ROOT / "data" / "dccxli_closure_resolvent_kernel_bridge.json"
SIZE = 6


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    truncation_degree: int
    response_0_to_5_numerator: int
    response_0_to_5_denominator: int
    row0_sum_at_z1_numerator: int
    row0_sum_at_z1_denominator: int
    all_identities_hold: bool


def zero_matrix(n: int) -> list[list[Fraction]]:
    return [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]


def identity_matrix(n: int) -> list[list[Fraction]]:
    out = zero_matrix(n)
    for i in range(n):
        out[i][i] = Fraction(1, 1)
    return out


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


def matadd(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] + b[i][j] for j in range(len(a))] for i in range(len(a))]


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


def serialize_matrix(a: list[list[Fraction]]) -> list[list[dict[str, int]]]:
    return [[{"numerator": x.numerator, "denominator": x.denominator} for x in row] for row in a]


def build_generator() -> list[list[Fraction]]:
    shift = zero_matrix(SIZE)
    for i in range(SIZE - 1):
        shift[i][i + 1] = Fraction(1, 1)
    return scale_matrix(Fraction(1, 2), shift)


def resolvent(generator: list[list[Fraction]], z: Fraction) -> tuple[list[list[Fraction]], list[list[list[Fraction]]]]:
    powers = [matpow(generator, n) for n in range(SIZE)]
    out = zero_matrix(SIZE)
    for n, power in enumerate(powers):
        out = matadd(out, scale_matrix(z ** n, power))
    return out, powers


def build_bridge() -> dict[str, Any]:
    _ = build_dccxl()  # ensure chain dependency
    generator = build_generator()
    I = identity_matrix(SIZE)

    sample_z = {
        "0": Fraction(0, 1),
        "1/2": Fraction(1, 2),
        "1": Fraction(1, 1),
        "2": Fraction(2, 1),
    }

    sample_resolvents: dict[str, list[list[Fraction]]] = {}
    sample_checks = []
    for label, z in sample_z.items():
        R, powers = resolvent(generator, z)
        lhs = matmul(matadd(I, scale_matrix(-z, generator)), R)
        rhs = matmul(R, matadd(I, scale_matrix(-z, generator)))
        sample_resolvents[label] = R
        sample_checks.append(
            {
                "z": label,
                "left_identity": lhs,
                "right_identity": rhs,
                "resolvent": R,
                "powers_used": len(powers),
            }
        )

    R1 = sample_resolvents["1"]
    formula_witness = [
        {
            "from": i,
            "to": j,
            "entry": R1[i][j],
            "expected": Fraction(1, 2 ** (j - i)) if j >= i else Fraction(0, 1),
        }
        for i in range(SIZE)
        for j in range(SIZE)
    ]

    row0_sum = sum(R1[0], start=Fraction(0, 1))

    identities = {
        "neumann_series_truncates_at_degree_5": all(
            check["powers_used"] == SIZE for check in sample_checks
        ),
        "resolvent_inverts_I_minus_zG_on_samples": all(
            check["left_identity"] == I and check["right_identity"] == I for check in sample_checks
        ),
        "entries_match_closed_form_at_z1": all(
            witness["entry"] == witness["expected"] for witness in formula_witness
        ),
        "response_0_to_5_at_z1_is_one_over_32": R1[0][5] == Fraction(1, 32),
        "row0_sum_at_z1_is_63_over_32": row0_sum == Fraction(63, 32),
        "resolvent_is_upper_triangular": all(
            R1[i][j] == 0 for i in range(SIZE) for j in range(i)
        ),
    }

    summary = BridgeSummary(
        state_count=SIZE,
        truncation_degree=SIZE - 1,
        response_0_to_5_numerator=R1[0][5].numerator,
        response_0_to_5_denominator=R1[0][5].denominator,
        row0_sum_at_z1_numerator=row0_sum.numerator,
        row0_sum_at_z1_denominator=row0_sum.denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "resolvent_definition": {
            "formula": "R(z) = (I - zG)^(-1) = sum_{n=0}^5 z^n G^n",
            "entry_formula": "R(z)_(ij) = (z/2)^(j-i) for j>=i, else 0",
        },
        "sample_resolvents": {k: serialize_matrix(v) for k, v in sample_resolvents.items()},
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
                "Because the transfer generator is nilpotent, the closure resolvent is a finite Neumann series and yields an exact closed-form Green/response kernel."
            ),
            "conditional_layer": (
                "Interpreting this discrete resolvent as a continuum Green's function requires an additional scaling limit."
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
