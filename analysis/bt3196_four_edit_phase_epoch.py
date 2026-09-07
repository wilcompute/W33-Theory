#!/usr/bin/env python3
"""Pass 3196: optimal twelve-phase epoch family correcting four arbitrary edits."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3196_FOUR_EDIT_PHASE_EPOCH_results.json"
Q = 24
N = 9
T = 4
PAYLOAD = (7, 2, 16, 23, 20, 15, 0, 2, 7, 11, 16, 19)
PHASE = (1, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 17)


def ball_count() -> tuple[dict[str, int], int]:
    by_length: dict[str, int] = {}
    for m in range(N - T, N + T + 1):
        total = 0
        for c in range(m + 1):
            if max(N, m) - min(N, c) <= T:
                total += math.comb(m, c) * (Q - 1) ** (m - c)
        by_length[str(m)] = total
    return by_length, sum(by_length.values())


def main() -> None:
    assert set(PHASE).isdisjoint(PAYLOAD)
    assert len(set(PHASE)) == 12
    by_length, total = ball_count()
    assert total == 536_484_991
    result = {
        "schema": "w33.pass3196.four_edit_phase_epoch.v1",
        "alphabet_size": Q,
        "phases": 12,
        "phase_symbols": list(PHASE),
        "marker_length": N,
        "corrected_edits": T,
        "marker_family": "M_p=u_p^9",
        "minimum_marker_distance": 9,
        "minimum_marker_to_payload_distance": 9,
        "optimality": "unique correction of t=4 adversarial substitutions/insertions/deletions requires d_min>=2t+1=9",
        "radius_four_ball_by_received_length": by_length,
        "radius_four_ball_size_per_phase": total,
        "total_distinct_phase_labelled_traces": 12 * total,
        "clean_payload_symbols_after_marker": 0,
        "decoder_statistic": "received length m and the twelve phase-symbol counts c_p",
        "proof": "For constant marker a^9 and received word y of length m containing c copies of a, d_L(a^9,y)=max(9,m)-min(9,c).",
        "boundary": "Exact bounded-marker combinatorics. Continuous streaming acquisition, physical symbol confusion and marker cadence are separate engineering gates."
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"per_phase": total, "all_phases": 12 * total}, sort_keys=True))


if __name__ == "__main__":
    main()
