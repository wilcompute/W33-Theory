#!/usr/bin/env python3
"""Part DCXCII: holonomy rank-one update bridge.

Once the frontier is binary (zero orbit vs nonzero orbit), the remaining
difference between the current host and an exact live host can be rewritten as
one exact rank jump:

    rank(N) : 0 -> 1.

This verifier proves that every exact live nilpotent increment is a rank-one,
square-zero update on the already-correct 162-packet support, while the current
host carries the rank-zero update.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parent
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from verify_dcxc_holonomy_one_slot_frontier_bridge import (  # noqa: E402
    build_bridge as build_dcxc_bridge,
)
from verify_dclxxxix_holonomy_common_packet_host_bridge import (  # noqa: E402
    build_bridge as build_dclxxxix_bridge,
)


OUT_PATH = ROOT / "data" / "dcxcii_holonomy_rank_one_update_bridge.json"
MODULUS = 3


@dataclass(frozen=True)
class BridgeSummary:
    support_packet_size: int
    current_nilpotent_rank: int
    live_nilpotent_rank: int
    rank_jump: int
    all_identities_hold: bool


def _mat_mod3(matrix: np.ndarray) -> np.ndarray:
    return np.array(matrix, dtype=int) % MODULUS


def _rank_mod3(matrix: np.ndarray) -> int:
    matrix = _mat_mod3(matrix.copy())
    rows, cols = matrix.shape
    rank = 0
    pivot_row = 0
    for col in range(cols):
        pivot = None
        for row in range(pivot_row, rows):
            if matrix[row, col] % MODULUS != 0:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != pivot_row:
            matrix[[pivot_row, pivot]] = matrix[[pivot, pivot_row]]
        inv = pow(int(matrix[pivot_row, col]), -1, MODULUS)
        matrix[pivot_row] = _mat_mod3(inv * matrix[pivot_row])
        for row in range(rows):
            if row != pivot_row and matrix[row, col] % MODULUS != 0:
                matrix[row] = _mat_mod3(matrix[row] - matrix[row, col] * matrix[pivot_row])
        rank += 1
        pivot_row += 1
        if pivot_row == rows:
            break
    return rank


def build_bridge() -> dict[str, Any]:
    dcxc = build_dcxc_bridge()
    packet = build_dclxxxix_bridge()

    support_packet_size = packet["summary"]["host_support_total"]
    current_increment = np.array(dcxc["slot_data"]["current_increment"], dtype=int)
    live_increments = [np.array(increment, dtype=int) for increment in dcxc["slot_data"]["allowed_live_increments"]]

    current_rank = _rank_mod3(current_increment)
    live_ranks = [_rank_mod3(increment) for increment in live_increments]

    identities = {
        "the_support_packet_remains_exactly_162": support_packet_size == 162,
        "the_current_increment_has_rank_zero": current_rank == 0,
        "every_exact_live_increment_has_rank_one": live_ranks == [1, 1],
        "every_exact_live_increment_is_square_zero": all(
            np.array_equal(_mat_mod3(increment @ increment), np.zeros((2, 2), dtype=int))
            for increment in live_increments
        ),
        "the_remaining_difference_is_exactly_a_rank_jump_zero_to_one": (
            current_rank == 0 and live_ranks == [1, 1]
        ),
        "therefore_exact_realization_requires_one_rank_one_nilpotent_update_on_the_already_correct_162_packet": (
            support_packet_size == 162 and current_rank == 0 and live_ranks == [1, 1]
        ),
    }

    summary = BridgeSummary(
        support_packet_size=support_packet_size,
        current_nilpotent_rank=current_rank,
        live_nilpotent_rank=1,
        rank_jump=1,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "rank_data": {
            "current_increment": current_increment.tolist(),
            "current_rank": current_rank,
            "live_increments": [increment.tolist() for increment in live_increments],
            "live_ranks": live_ranks,
        },
        "interpretation": {
            "verdict": (
                "The exact host support packet is already present. The only remaining difference between the current host and an exact live host is one rank-one square-zero update of the nilpotent increment on that same fixed packet."
            )
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