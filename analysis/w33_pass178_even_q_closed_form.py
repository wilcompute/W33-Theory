#!/usr/bin/env python3
"""Pass 178: the theorem-backed even-q incidence-rank transfer matrix.

Pass 171 left the exact even-order binary incidence ranks

    10, 50, 298, 1890       (q = 2, 4, 8, 16)

after refuting a cubic interpolant.  Sastry--Sin's theorem supplies the
closed form for q = 2^n:

    rank_2 M(2^n)
      = 1 + ((1 + sqrt(17))/2)^(2n)
          + ((1 - sqrt(17))/2)^(2n).

The useful exact normal form is integral.  If

        B = [[4, 2], [2, 5]],

then B has eigenvalues (9 +- sqrt(17))/2, the squares of the two radical
bases above, and

    rank_2 M(2^n) = 1 + trace(B^n).

Consequently r_n = 9 r_(n-1) - 16 r_(n-2) + 8, or homogeneously
r_n = 10 r_(n-1) - 25 r_(n-2) + 16 r_(n-3).  This witness rederives the
small geometries, checks the committed q=16 anchor, and extends the exact
theorem sequence without fitting any coefficients.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass171_even_q_rank_ladder import build_w3q, f2_rank

OUT = ROOT / "data" / "w33_pass178_even_q_closed_form.json"
PASS171 = ROOT / "data" / "w33_pass171_even_q_rank_ladder.json"

B = ((4, 2), (2, 5))
IDENTITY = ((1, 0), (0, 1))


def matmul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )


def matpow(matrix, exponent):
    result = IDENTITY
    power = matrix
    while exponent:
        if exponent & 1:
            result = matmul(result, power)
        power = matmul(power, power)
        exponent >>= 1
    return result


def theorem_rank(n):
    power = matpow(B, n)
    return 1 + power[0][0] + power[1][1]


def main():
    checks = {}

    # Re-derive the first three incidence ranks from the finite geometries.
    measured = {}
    for n, q in ((1, 2), (2, 4), (3, 8)):
        points, lines = build_w3q(q)
        incidence = np.zeros((len(lines), len(points)), dtype=np.uint8)
        for row, line in enumerate(lines):
            for point in line:
                incidence[row, point] = 1
        measured[n] = int(f2_rank(incidence))
    checks["small_anchors_rederived"] = measured == {1: 10, 2: 50, 3: 298}

    # Read the independently computed q=16 anchor from Pass 171.
    stored = json.loads(PASS171.read_text(encoding="utf-8"))
    measured[4] = int(stored["table"]["16"]["rank2_M"])
    checks["q16_anchor_is_1890"] = measured[4] == 1890

    sequence = {n: theorem_rank(n) for n in range(1, 9)}
    checks["transfer_matches_all_measured_anchors"] = all(
        sequence[n] == rank for n, rank in measured.items()
    )
    checks["integral_transfer_matrix"] = all(
        isinstance(entry, int)
        for n in range(1, 9)
        for row in matpow(B, n)
        for entry in row
    )

    # Characteristic polynomial x^2 - 9x + 16 and its induced recurrences.
    checks["transfer_trace_9_determinant_16"] = (
        B[0][0] + B[1][1] == 9
        and B[0][0] * B[1][1] - B[0][1] * B[1][0] == 16
    )
    checks["affine_recurrence"] = all(
        sequence[n] == 9 * sequence[n - 1] - 16 * sequence[n - 2] + 8
        for n in range(3, 9)
    )
    checks["homogeneous_recurrence"] = all(
        sequence[n]
        == 10 * sequence[n - 1] - 25 * sequence[n - 2] + 16 * sequence[n - 3]
        for n in range(4, 9)
    )
    expected = [10, 50, 298, 1890, 12250, 80018, 524170, 3437250]
    checks["exact_sequence_through_q256"] = [sequence[n] for n in range(1, 9)] == expected
    checks["false_four_anchor_interpolant_refuted_at_q32"] = sequence[5] != 12794

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass178.even_q_closed_form.v2",
        "status": "PASS" if all_pass else "FAIL",
        "theorem": {
            "source": (
                "Sastry--Sin, The Code of a Regular Generalized Quadrangle "
                "of Even Order, Theorem 1"
            ),
            "radical_form": (
                "rank_2 M(2^n) = 1 + ((1+sqrt(17))/2)^(2n) "
                "+ ((1-sqrt(17))/2)^(2n)"
            ),
            "integral_transfer_matrix": [list(row) for row in B],
            "integral_form": "rank_2 M(2^n) = 1 + trace(B^n)",
            "affine_recurrence": "r_n = 9*r_(n-1) - 16*r_(n-2) + 8",
            "homogeneous_recurrence": (
                "r_n = 10*r_(n-1) - 25*r_(n-2) + 16*r_(n-3)"
            ),
            "characteristic_roots": [
                "1",
                "(9+sqrt(17))/2",
                "(9-sqrt(17))/2",
            ],
        },
        "ranks": {str(2**n): sequence[n] for n in range(1, 9)},
        "measured_anchors": {str(2**n): rank for n, rank in measured.items()},
        "q32_correction": {
            "theorem_value": sequence[5],
            "rejected_interpolant_value": 12794,
            "difference": sequence[5] - 12794,
        },
        "reading": (
            "the even-order rank ladder is governed by a two-state integral "
            "transfer matrix, not by the four-anchor {1,6,13} interpolation; "
            "q=32 is the first separating value"
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
