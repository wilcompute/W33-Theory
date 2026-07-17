#!/usr/bin/env python3
"""Spectral completion test for the W33 chain A/2 candidate.

The remote BT1885-BT1889 line sharpened the open boundary to:

    prove or replace G40 = 2I - A_W33 as the actual Z^40 chain A/2 operator.

This witness tests that candidate by its exact W(3,3) spectral behavior.  The
result is useful and restrictive:

* G40 is not full-rank.  It has rank 16 and a 24-dimensional kernel.
* The missing channel is not mysterious: it is the r=2 eigenspace of W(3,3).
* There is an integral complementary operator

      R40 = 20I + 5A - 2J = 30 * P_r

  with rank 24, R40^2 = 30 R40, and G40 R40 = R40 G40 = 0.

So G40 alone is a metric/boundary shadow, not a complete chain diagnostic.
The exact two-channel completion is (G40, R40), or equivalently H40=G40+R40,
which has full rank over Q as witnessed by rank over F7.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_uor_runtime_model import ROOT, point_id


DEFAULT_JSON = ROOT / "data" / "w33_chain_operator_spectral_completion.json"
DEFAULT_MD = ROOT / "docs" / "w33_chain_operator_spectral_completion.md"


Matrix = list[list[int]]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    m = len(b[0])
    kdim = len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(kdim)) for j in range(m)]
        for i in range(n)
    ]


def matscale(c: int, a: Matrix) -> Matrix:
    return [[c * value for value in row] for row in a]


def matadd(*terms: Matrix) -> Matrix:
    n = len(terms[0])
    m = len(terms[0][0])
    return [[sum(term[i][j] for term in terms) for j in range(m)] for i in range(n)]


def identity(n: int) -> Matrix:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def ones(n: int) -> Matrix:
    return [[1 for _ in range(n)] for _ in range(n)]


def adjacency() -> Matrix:
    n = len(hn.POINTS)
    a = [[0] * n for _ in range(n)]
    for i, left in enumerate(hn.POINTS):
        for j in range(i + 1, n):
            right = hn.POINTS[j]
            if hn.symplectic(left, right) == 0:
                a[i][j] = a[j][i] = 1
    return a


def rank_mod(matrix: Matrix, prime: int) -> int:
    rows = [[value % prime for value in row] for row in matrix if any(value % prime for value in row)]
    if not rows:
        return 0
    rank = 0
    col_count = len(rows[0])
    row = 0
    for col in range(col_count):
        pivot = next((idx for idx in range(row, len(rows)) if rows[idx][col] % prime), None)
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        inv = pow(rows[row][col], -1, prime)
        rows[row] = [(value * inv) % prime for value in rows[row]]
        for idx in range(len(rows)):
            if idx != row and rows[idx][col] % prime:
                factor = rows[idx][col] % prime
                rows[idx] = [
                    (rows[idx][j] - factor * rows[row][j]) % prime
                    for j in range(col_count)
                ]
        row += 1
        rank += 1
        if row == len(rows):
            break
    return rank


def quadratic_energy(vec: list[int], matrix: Matrix) -> int:
    return sum(vec[i] * matrix[i][j] * vec[j] for i in range(len(vec)) for j in range(len(vec)))


def delta_vec(left: int, right: int, n: int = 40) -> list[int]:
    out = [0] * n
    out[left] = 1
    out[right] = -1
    return out


def build_operators() -> dict[str, Matrix]:
    a = adjacency()
    n = len(a)
    i = identity(n)
    j = ones(n)
    g = matadd(matscale(2, i), matscale(-1, a))
    r = matadd(matscale(20, i), matscale(5, a), matscale(-2, j))
    h = matadd(g, r)
    return {"A": a, "I": i, "J": j, "G40": g, "R40": r, "H40": h}


def build_payload() -> dict[str, Any]:
    ops = build_operators()
    a, i, j, g, r, h = (ops[key] for key in ("A", "I", "J", "G40", "R40", "H40"))
    n = len(a)
    a2 = matmul(a, a)
    srg_rhs = matadd(matscale(8, i), matscale(-2, a), matscale(4, j))
    gr = matmul(g, r)
    rg = matmul(r, g)
    r2 = matmul(r, r)
    edge_energies = []
    nonedge_energies = []
    for left in range(n):
        for right in range(left + 1, n):
            vec = delta_vec(left, right, n)
            row = {
                "points": [point_id(hn.POINTS[left]), point_id(hn.POINTS[right])],
                "G40": quadratic_energy(vec, g),
                "R40": quadratic_energy(vec, r),
                "H40": quadratic_energy(vec, h),
            }
            if a[left][right]:
                edge_energies.append(row)
            else:
                nonedge_energies.append(row)

    ranks_mod7 = {
        "G40": rank_mod(g, 7),
        "R40": rank_mod(r, 7),
        "H40": rank_mod(h, 7),
        "stacked_G40_R40": rank_mod(g + r, 7),
    }
    checks = {
        "forty_points": n == 40,
        "degree_twelve": all(sum(row) == 12 for row in a),
        "srg_adjacency_identity": a2 == srg_rhs,
        "G40_rank_16_mod7": ranks_mod7["G40"] == 16,
        "R40_rank_24_mod7": ranks_mod7["R40"] == 24,
        "H40_full_rank_mod7": ranks_mod7["H40"] == 40,
        "stacked_pair_full_rank_mod7": ranks_mod7["stacked_G40_R40"] == 40,
        "G40_R40_orthogonal": all(value == 0 for row in gr for value in row)
        and all(value == 0 for row in rg for value in row),
        "R40_projector_scaled": r2 == matscale(30, r),
        "edge_energy_constant": {
            tuple((row["G40"], row["R40"], row["H40"]) for row in edge_energies)
        }
        == {((6, 30, 36),) * len(edge_energies)},
        "nonedge_energy_constant": {
            tuple((row["G40"], row["R40"], row["H40"]) for row in nonedge_energies)
        }
        == {((4, 40, 44),) * len(nonedge_energies)},
    }
    return {
        "schema": "w33.chain_operator_spectral_completion.v1",
        "theorem": "G40 is a rank-16 chain shadow; R40 is the exact integral rank-24 missing channel",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "operators": {
            "G40": "2I - A_W33",
            "R40": "20I + 5A_W33 - 2J = 30*P_(A=2)",
            "H40": "G40 + R40",
            "pair": "(G40, R40)",
        },
        "ranks_mod7": ranks_mod7,
        "spectral_reading": {
            "A_eigenvalues": {"12": 1, "2": 24, "-4": 15},
            "G40_eigenvalues": {"-10": 1, "0": 24, "6": 15},
            "R40_eigenvalues": {"0": 16, "30": 24},
            "H40_eigenvalues": {"-10": 1, "30": 24, "6": 15},
        },
        "identities": {
            "A2": "A^2 = 8I - 2A + 4J",
            "orthogonality": "G40*R40 = R40*G40 = 0",
            "scaled_projector": "R40^2 = 30 R40",
        },
        "edge_energy": {
            "count": len(edge_energies),
            "per_edge_delta": {"G40": 6, "R40": 30, "H40": 36},
        },
        "nonedge_energy": {
            "count": len(nonedge_energies),
            "per_nonedge_delta": {"G40": 4, "R40": 40, "H40": 44},
        },
        "checks": checks,
        "interpretation": (
            "G40 cannot be the complete chain A/2 diagnostic by itself because it "
            "annihilates the 24-dimensional A=2 sector. The missing sector has an "
            "exact integral carrier R40=20I+5A-2J. The next chain-boundary test "
            "should therefore validate the two-channel object (G40,R40), or prove "
            "why the 24D sector is intentionally quotiented out."
        ),
        "honesty_boundary": (
            "This proves exact W33 spectral/operator identities. It does not prove "
            "the final chain boundary map; it proves a necessary diagnostic that "
            "any final map must address."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    return f"""# W(3,3) Chain Operator Spectral Completion

Remote BT1885-BT1889 sharpened the open boundary to proving or replacing
`G40 = 2I - A_W33` as the actual `Z^40` chain `A/2` operator. This witness
tests that candidate exactly.

Result: `G40` is rank `{payload['ranks_mod7']['G40']}` and has a
`24`-dimensional kernel. It is therefore a chain/metric shadow, not a complete
diagnostic by itself. The missing integral channel is:

```text
R40 = 20I + 5A_W33 - 2J = 30 * P_(A=2)
```

Checks:

- `G40*R40 = R40*G40 = 0`
- `R40^2 = 30 R40`
- `rank(G40) = 16`, `rank(R40) = 24`, `rank(G40+R40) = 40` over `F7`
- every W33 edge delta has chain bill `G40=6`, `R40=30`, `H40=36`

Interpretation: the next boundary proof should test the two-channel object
`(G40, R40)`, or explicitly prove that the `24`-dimensional `A=2` sector is
supposed to be quotiented out.
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
    print(f"ranks_mod7: {payload['ranks_mod7']}")
    print(f"edge_delta: {payload['edge_energy']['per_edge_delta']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
