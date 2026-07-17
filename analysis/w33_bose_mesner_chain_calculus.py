#!/usr/bin/env python3
"""Integer Bose-Mesner chain calculus for W(3,3).

The chain-operator completion found that G40 = 2I-A is rank 16 and misses the
24-dimensional A=2 sector.  This script promotes that observation into the full
integer spectral calculus of the W33 Bose-Mesner algebra.

Scaled primitive channels:

    U40 = J                  = 40 * E_12   rank 1
    R40 = 20I + 5A - 2J      = 30 * E_2    rank 24
    S40 = 8I - 4A + J        = 24 * E_-4   rank 15

They are pairwise orthogonal scaled projectors and sum, after normalization, to
I.  The old candidate G40 is not primitive:

    G40 = 2I - A = (S40 - U40) / 4.

So G40 is the difference of the trivial and -4 channels and is completely blind
to the 24-dimensional A=2 channel.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from w33_chain_operator_spectral_completion import (
    Matrix,
    adjacency,
    identity,
    matadd,
    matmul,
    matscale,
    ones,
    rank_mod,
)
from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_bose_mesner_chain_calculus.json"
DEFAULT_MD = ROOT / "docs" / "w33_bose_mesner_chain_calculus.md"


def zero_matrix(n: int) -> Matrix:
    return [[0 for _ in range(n)] for _ in range(n)]


def equal(a: Matrix, b: Matrix) -> bool:
    return a == b


def trace(a: Matrix) -> int:
    return sum(a[i][i] for i in range(len(a)))


def build_channels() -> dict[str, Matrix]:
    a = adjacency()
    n = len(a)
    i = identity(n)
    j = ones(n)
    return {
        "I": i,
        "A": a,
        "J": j,
        "U40": j,
        "R40": matadd(matscale(20, i), matscale(5, a), matscale(-2, j)),
        "S40": matadd(matscale(8, i), matscale(-4, a), j),
        "G40": matadd(matscale(2, i), matscale(-1, a)),
    }


def matdiff(a: Matrix, b: Matrix) -> Matrix:
    return matadd(a, matscale(-1, b))


def scalar_divisible(a: Matrix, divisor: int) -> bool:
    return all(value % divisor == 0 for row in a for value in row)


def div_matrix(a: Matrix, divisor: int) -> Matrix:
    if not scalar_divisible(a, divisor):
        raise ValueError(f"matrix is not divisible by {divisor}")
    return [[value // divisor for value in row] for row in a]


def build_payload() -> dict[str, Any]:
    channels = build_channels()
    n = len(channels["A"])
    z = zero_matrix(n)
    u, r, s, g = (channels[key] for key in ("U40", "R40", "S40", "G40"))
    normalized_identity_num = matadd(
        matscale(3, u),
        matscale(4, r),
        matscale(5, s),
    )
    # This is 120*I because U/40 + R/30 + S/24 = I.
    ranks = {
        key: rank_mod(channels[key], 7)
        for key in ("U40", "R40", "S40", "G40")
    }
    traces = {key: trace(channels[key]) for key in ("U40", "R40", "S40", "G40")}
    multiplication = {
        "U40^2": "40 U40",
        "R40^2": "30 R40",
        "S40^2": "24 S40",
        "U40*R40": "0",
        "U40*S40": "0",
        "R40*S40": "0",
    }
    checks = {
        "rank_U40_1": ranks["U40"] == 1,
        "rank_R40_24": ranks["R40"] == 24,
        "rank_S40_15": ranks["S40"] == 15,
        "rank_sum_40": ranks["U40"] + ranks["R40"] + ranks["S40"] == 40,
        "trace_scaled_projectors": traces == {
            "U40": 40,
            "R40": 720,
            "S40": 360,
            "G40": 80,
        },
        "U40_scaled_idempotent": equal(matmul(u, u), matscale(40, u)),
        "R40_scaled_idempotent": equal(matmul(r, r), matscale(30, r)),
        "S40_scaled_idempotent": equal(matmul(s, s), matscale(24, s)),
        "pairwise_orthogonal": (
            equal(matmul(u, r), z)
            and equal(matmul(u, s), z)
            and equal(matmul(r, s), z)
        ),
        "normalized_projectors_sum_to_identity": equal(normalized_identity_num, matscale(120, channels["I"])),
        "G40_equals_S40_minus_U40_over_4": scalar_divisible(matdiff(s, u), 4)
        and equal(g, div_matrix(matdiff(s, u), 4)),
        "G40_blind_to_R40": equal(matmul(g, r), z) and equal(matmul(r, g), z),
    }
    return {
        "schema": "w33.bose_mesner_chain_calculus.v1",
        "theorem": "W33 chain diagnostics live in the integer-scaled Bose-Mesner projector basis",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scaled_channels": {
            "U40": {
                "formula": "J = 40*E_12",
                "rank": ranks["U40"],
                "trace": traces["U40"],
                "scaled_idempotent": "U40^2 = 40 U40",
            },
            "R40": {
                "formula": "20I + 5A - 2J = 30*E_2",
                "rank": ranks["R40"],
                "trace": traces["R40"],
                "scaled_idempotent": "R40^2 = 30 R40",
            },
            "S40": {
                "formula": "8I - 4A + J = 24*E_-4",
                "rank": ranks["S40"],
                "trace": traces["S40"],
                "scaled_idempotent": "S40^2 = 24 S40",
            },
        },
        "candidate_shadow": {
            "G40": "2I - A",
            "decomposition": "G40 = (S40 - U40)/4",
            "rank": ranks["G40"],
            "blind_channel": "R40 / A=2 / rank 24",
        },
        "multiplication_table": multiplication,
        "identity_resolution": "U40/40 + R40/30 + S40/24 = I",
        "checks": checks,
        "interpretation": (
            "The right object is not a single candidate matrix. W33 supplies an "
            "integer spectral control panel with three orthogonal channels. G40 "
            "is only a signed combination of U40 and S40; any final chain boundary "
            "that ignores R40 discards the 24D packet/eigenvalue-2 sector."
        ),
        "honesty_boundary": (
            "This is exact Bose-Mesner algebra inside W33. It constrains the "
            "chain-boundary search but does not by itself produce a boundary map."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for name, row in payload["scaled_channels"].items():
        rows.append(
            f"| {name} | `{row['formula']}` | {row['rank']} | {row['trace']} | `{row['scaled_idempotent']}` |"
        )
    return f"""# W(3,3) Bose-Mesner Chain Calculus

The full integer spectral control panel is:

| Channel | Formula | Rank | Trace | Law |
|---|---|---:|---:|---|
{chr(10).join(rows)}

Resolution:

```text
U40/40 + R40/30 + S40/24 = I
G40 = 2I - A = (S40 - U40)/4
```

Conclusion: `G40` is not primitive. It is blind to the rank-24 `R40` channel.
The chain-boundary search must either use the full `{{U40,R40,S40}}` calculus or
explicitly quotient out the `A=2` sector.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")
    print(f"status: {payload['status']}")
    for name, row in payload["scaled_channels"].items():
        print(f"{name}: rank={row['rank']}, formula={row['formula']}")
    print(f"shadow: {payload['candidate_shadow']['decomposition']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
