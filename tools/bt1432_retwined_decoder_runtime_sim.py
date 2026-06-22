#!/usr/bin/env python3
"""BT1432: retwined decoder runtime simulation.

This script links BT1425 and BT1429: representative active and guard faults are
pushed through the tracked frame rule, and syndrome equivalence is verified in
both X and Z checks.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from bt1425_retwined_css_frame_correction import (  # noqa: E402
    build_w33,
    dense_hx,
    dense_hz,
    gf_rank,
    guard_shear_perm,
    permute_columns,
    permute_vector,
    syndrome,
)

OUT = ROOT / "data" / "bt1432_retwined_decoder_runtime_sim.json"


def basis_error(col: int, value: int, n: int = 240) -> list[int]:
    e = [0] * n
    e[col] = value % 3
    return e


def main() -> None:
    _points, edges, triangles = build_w33()
    hx = dense_hx(edges)
    hz = dense_hz(edges, triangles)
    perm = guard_shear_perm()
    hx_r = permute_columns(hx, perm)
    hz_r = permute_columns(hz, perm)

    active_cols = [0, 1, 7, 21, 55, 89, 120, 167]
    guard_cols = list(range(216, 240))
    samples = active_cols + guard_cols
    rows = []
    for col in samples:
        for value in (1, 2):
            err = basis_error(col, value)
            err_r = permute_vector(err, perm)
            rows.append(
                {
                    "col": col,
                    "value": value,
                    "is_guard_tail": col >= 216,
                    "retwined_col": err_r.index(value),
                    "x_equiv": syndrome(hx, err) == syndrome(hx_r, err_r),
                    "z_equiv": syndrome(hz, err) == syndrome(hz_r, err_r),
                }
            )
    nontrivial_guard_moves = [row for row in rows if row["is_guard_tail"] and row["col"] != row["retwined_col"]]
    checks = {
        "rank_HX_is_39": gf_rank(hx) == 39 and gf_rank(hx_r) == 39,
        "rank_HZ_is_120": gf_rank(hz) == 120 and gf_rank(hz_r) == 120,
        "sample_count_is_64": len(rows) == 64,
        "all_x_syndromes_equivariant": all(row["x_equiv"] for row in rows),
        "all_z_syndromes_equivariant": all(row["z_equiv"] for row in rows),
        "nontrivial_guard_moves_are_24_sample_rows": len(nontrivial_guard_moves) == 24,
        "active_samples_do_not_move_under_guard_shear": all(row["col"] == row["retwined_col"] for row in rows if not row["is_guard_tail"]),
    }
    result = {
        "bt": 1432,
        "title": "Retwined decoder runtime simulation",
        "verified": all(checks.values()),
        "sample_policy": "8 representative active coordinates plus all 24 guard-tail coordinates, each with qutrit values 1 and 2",
        "css_ranks": {"HX": gf_rank(hx), "HZ": gf_rank(hz), "k": 240 - gf_rank(hx) - gf_rank(hz)},
        "sample_rows": rows,
        "interpretation": "Active faults remain in the identity frame. Guard-tail faults are decoded after applying the same D4 permutation to the tracked error coordinate and the CSS stabilizer frame.",
        "boundary": "This is a representative runtime simulation; BT1425 remains the exhaustive basis-coordinate proof.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1432, "verified": result["verified"], "samples": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
