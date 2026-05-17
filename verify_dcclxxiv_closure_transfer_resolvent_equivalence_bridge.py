#!/usr/bin/env python3
"""Part DCCLXXIV: closure transfer / resolvent equivalence bridge.

The old local transfer-generator draft and the promoted DCCXL Jordan-resolvent
bridge describe the same finite operator:

    G = (1/2)S,
    K = I + G + G^2 + G^3 + G^4 + G^5 = (I-G)^(-1).

This verifier makes that equivalence explicit under the current numbering so
the project has one canonical DCCXL surface rather than two conflicting Part
DCCXL definitions.
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

from verify_dccxxxix_closure_semigroup_propagator_bridge import (  # noqa: E402
    build_bridge as build_semigroup,
)
from verify_dccxl_closure_jordan_resolvent_bridge import (  # noqa: E402
    build_bridge as build_resolvent,
)


OUT_PATH = ROOT / "data" / "dcclxxiv_closure_transfer_resolvent_equivalence_bridge.json"


Matrix = list[list[Fraction]]


@dataclass(frozen=True)
class BridgeSummary:
    causal_class_count: int
    generator_weight_num: int
    generator_weight_den: int
    nilpotent_index: int
    maximal_transfer_denominator: int
    all_identities_hold: bool


def _zero(n: int) -> Matrix:
    return [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]


def _identity(n: int) -> Matrix:
    out = _zero(n)
    for i in range(n):
        out[i][i] = Fraction(1, 1)
    return out


def _add(a: Matrix, b: Matrix) -> Matrix:
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def _mul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    out = _zero(n)
    for i in range(n):
        for k in range(n):
            if a[i][k] == 0:
                continue
            aik = a[i][k]
            for j in range(n):
                out[i][j] += aik * b[k][j]
    return out


def _pow(a: Matrix, exponent: int) -> Matrix:
    n = len(a)
    out = _identity(n)
    base = a
    exp = exponent
    while exp > 0:
        if exp & 1:
            out = _mul(out, base)
        base = _mul(base, base)
        exp >>= 1
    return out


def _deserialize_matrix(rows: list[list[dict[str, int]]]) -> Matrix:
    return [
        [Fraction(cell["numerator"], cell["denominator"]) for cell in row]
        for row in rows
    ]


def _deserialize_table(rows: list[list[dict[str, int]]]) -> Matrix:
    return _deserialize_matrix(rows)


def _serialize_fraction(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def build_bridge() -> dict[str, Any]:
    semigroup = build_semigroup()
    resolvent = build_resolvent()

    generator = _deserialize_matrix(resolvent["generator_matrix"])
    powers = {
        name: _deserialize_matrix(rows)
        for name, rows in resolvent["generator_powers"].items()
    }
    propagator = _deserialize_table(semigroup["propagator_table"])
    canonical_propagator = _deserialize_matrix(resolvent["matrices"]["propagator"])

    n = len(generator)
    expected_shift = _zero(n)
    for i in range(n - 1):
        expected_shift[i][i + 1] = Fraction(1, 2)

    transfer_power_checks: list[dict[str, Any]] = []
    for delta in range(n + 1):
        direct_power = _pow(generator, delta)
        canonical_power = powers[f"G^{delta}"]
        expected_power = _zero(n)
        if delta == 0:
            expected_power = _identity(n)
        elif delta < n:
            for i in range(n - delta):
                expected_power[i][i + delta] = Fraction(1, 2**delta)

        transfer_power_checks.append(
            {
                "delta": delta,
                "canonical_matches_direct_power": canonical_power == direct_power,
                "direct_power_matches_transfer_rule": direct_power == expected_power,
            }
        )

    resolvent_sum = _zero(n)
    for delta in range(n):
        resolvent_sum = _add(resolvent_sum, powers[f"G^{delta}"])

    entry_rows: list[dict[str, Any]] = []
    for i in range(n):
        for j in range(i, n):
            delta = j - i
            entry_rows.append(
                {
                    "from": i,
                    "to": j,
                    "delta": delta,
                    "semigroup_entry": _serialize_fraction(propagator[i][j]),
                    "power_entry": _serialize_fraction(powers[f"G^{delta}"][i][j]),
                    "resolvent_entry": _serialize_fraction(canonical_propagator[i][j]),
                }
            )

    identities = {
        "canonical_dccxl_summary_holds": bool(resolvent["summary"]["all_identities_hold"]),
        "dccxxxix_semigroup_summary_holds": bool(semigroup["summary"]["all_identities_hold"]),
        "generator_is_half_shift": generator == expected_shift,
        "all_generator_powers_match_transfer_rule": all(
            row["canonical_matches_direct_power"] and row["direct_power_matches_transfer_rule"]
            for row in transfer_power_checks
        ),
        "semigroup_entries_equal_power_entries": all(
            Fraction(row["semigroup_entry"]["numerator"], row["semigroup_entry"]["denominator"])
            == Fraction(row["power_entry"]["numerator"], row["power_entry"]["denominator"])
            for row in entry_rows
        ),
        "semigroup_entries_equal_resolvent_entries": all(
            Fraction(row["semigroup_entry"]["numerator"], row["semigroup_entry"]["denominator"])
            == Fraction(row["resolvent_entry"]["numerator"], row["resolvent_entry"]["denominator"])
            for row in entry_rows
        ),
        "resolvent_is_sum_of_transfer_powers": canonical_propagator == resolvent_sum,
        "nilpotence_terminates_at_six": powers["G^6"] == _zero(n) and powers["G^5"] != _zero(n),
        "maximal_transfer_is_one_over_32": powers["G^5"][0][5] == Fraction(1, 32),
    }

    summary = BridgeSummary(
        causal_class_count=n,
        generator_weight_num=1,
        generator_weight_den=2,
        nilpotent_index=n,
        maximal_transfer_denominator=32,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "equivalence": {
            "transfer_generator": "G=(1/2)S",
            "power_rule": "(G^d)_{i,i+d}=2^{-d}",
            "semigroup_rule": "K(i,j)=2^{-(j-i)}",
            "resolvent_rule": "K=sum_{d=0}^5 G^d=(I-G)^(-1)",
        },
        "transfer_power_checks": transfer_power_checks,
        "entry_rows": entry_rows,
        "identities": identities,
        "theorem": (
            "Closure Transfer-Resolvent Equivalence Theorem. The DCCXXXIX "
            "semigroup table, the transfer-generator power rule G=(1/2)S, and "
            "the promoted DCCXL Jordan resolvent K=(I-G)^(-1) are exactly the "
            "same six-level finite operator package."
        ),
        "honesty_boundary": (
            "This resolves an internal finite-operator equivalence and numbering "
            "hygiene issue. It does not add a continuum Hamiltonian, heat kernel, "
            "or Lorentzian propagator interpretation."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    payload = build_bridge()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")


if __name__ == "__main__":
    main()
