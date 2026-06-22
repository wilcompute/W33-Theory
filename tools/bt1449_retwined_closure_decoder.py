#!/usr/bin/env python3
"""BT1449: insert the Szilassi closure tick into the retwined CSS decoder."""
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

OUT = ROOT / "data" / "bt1449_retwined_closure_decoder.json"


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

    closure_ticks = [{"strand": s, "active_col": s * 14 + 13, "guard_cols": [216 + 2 * s, 216 + 2 * s + 1]} for s in range(12)]
    trials = []
    for row in closure_ticks:
        for col_kind, cols in (("active_closure", [row["active_col"]]), ("guard_closure", row["guard_cols"])):
            for col in cols:
                for value in (1, 2):
                    e = basis_error(col, value)
                    er = permute_vector(e, perm)
                    trials.append({
                        "strand": row["strand"],
                        "kind": col_kind,
                        "col": col,
                        "value": value,
                        "retwined_col": er.index(value),
                        "moved": er.index(value) != col,
                        "x_equiv": syndrome(hx, e) == syndrome(hx_r, er),
                        "z_equiv": syndrome(hz, e) == syndrome(hz_r, er),
                    })
    guard_trials = [t for t in trials if t["kind"] == "guard_closure"]
    active_trials = [t for t in trials if t["kind"] == "active_closure"]
    checks = {
        "css_ranks_are_39_120_81": gf_rank(hx) == 39 and gf_rank(hz) == 120 and 240 - gf_rank(hx) - gf_rank(hz) == 81,
        "closure_ticks_are_12": len(closure_ticks) == 12,
        "active_trials_are_24": len(active_trials) == 24,
        "guard_trials_are_48": len(guard_trials) == 48,
        "total_trials_are_72": len(trials) == 72,
        "active_closure_cols_fixed": all(not t["moved"] for t in active_trials),
        "guard_closure_has_24_moved_value_trials": sum(1 for t in guard_trials if t["moved"]) == 24,
        "all_x_syndromes_equivariant": all(t["x_equiv"] for t in trials),
        "all_z_syndromes_equivariant": all(t["z_equiv"] for t in trials),
    }
    result = {
        "bt": 1449,
        "title": "Retwined closure decoder",
        "verified": all(checks.values()),
        "closure_source": "BT1448 fixed Szilassi hexagon closure map",
        "css_ranks": {"HX": gf_rank(hx), "HZ": gf_rank(hz), "k": 240 - gf_rank(hx) - gf_rank(hz)},
        "counts": {"closure_ticks": len(closure_ticks), "active_trials": len(active_trials), "guard_trials": len(guard_trials), "total_trials": len(trials)},
        "trial_samples": trials[:24],
        "interpretation": "The odd closure tick can be inserted into active closure coordinates and all 24 guard rail orientations while preserving X/Z syndrome equivariance under the retwined CSS frame rule.",
        "boundary": "This proves the finite decoder/frame compatibility of the closure tick; it does not yet prove an analog optical implementation of the physical Moebius helix.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1449, "verified": result["verified"], "trials": len(trials)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
