#!/usr/bin/env python3
"""
BT830 - Two-phase holonet commit clock.

BT828 compiles fast reversible routes.  BT827 gives the durable tomotope clock
T(g)=4(7^g-1).  BT830 proves the operating-system split:

    PREPARE: execute at most 8n reversible route moves.
    COMMIT: wait for the tomotope/Csaszar durable tick T(n).

T(n) is always divisible by 24 and 8, so it is aligned with the local runtime
stabilizer and the one-digit route window.  It is not always divisible by the
full 8n route epoch; the first desync is level 5.  That desync is a feature:
the commit layer is slower and cover-like, not a synonym for the fast route
layer.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def route_bound(level: int) -> int:
    return 8 * level


def commit_ticks(level: int) -> int:
    return 1 if level == 0 else 4 * (7**level - 1)


def level_row(level: int) -> dict:
    route = route_bound(level)
    commit = commit_ticks(level)
    return {
        "level": level,
        "route_bound": route,
        "commit_ticks": commit,
        "commit_minus_route": commit - route,
        "commit_divisible_by_24": commit % 24 == 0,
        "commit_divisible_by_8": commit % 8 == 0,
        "full_route_epoch_remainder": commit % route,
        "full_route_epoch_sync": commit % route == 0,
        "full_route_epochs": commit // route,
        "digit_windows": commit // 8,
    }


def main() -> None:
    bt828 = load_json("data/bt828_holonet_packet_compiler.json")
    rows = [level_row(level) for level in range(1, 25)]
    sample_program_rows = []
    for program in bt828["compiled_programs"]:
        level = program["level"]
        commit = commit_ticks(level)
        sample_program_rows.append({
            "program": program["program"],
            "level": level,
            "actual_reversible_moves": program["reversible_moves"],
            "route_bound": route_bound(level),
            "commit_ticks": commit,
            "prepare_fits_route_bound": program["reversible_moves"] <= route_bound(level),
            "prepare_fits_commit_phase": program["reversible_moves"] < commit,
            "commit_slack_after_actual_route": commit - program["reversible_moves"],
        })

    sync_levels = [row["level"] for row in rows if row["full_route_epoch_sync"]]
    desync_levels = [row["level"] for row in rows if not row["full_route_epoch_sync"]]
    checks = {
        "all_sample_programs_fit_prepare": all(row["prepare_fits_route_bound"] for row in sample_program_rows),
        "all_sample_programs_fit_commit": all(row["prepare_fits_commit_phase"] for row in sample_program_rows),
        "commit_dominates_route_bound": all(row["commit_ticks"] >= 3 * row["route_bound"] for row in rows),
        "commit_is_always_24_aligned": all(row["commit_divisible_by_24"] for row in rows),
        "commit_is_always_8_aligned": all(row["commit_divisible_by_8"] for row in rows),
        "first_desync_is_level_5": desync_levels[0] == 5,
        "first_four_levels_sync": sync_levels[:4] == [1, 2, 3, 4],
        "desync_remainders_are_guard_bands": all(0 < row["full_route_epoch_remainder"] < row["route_bound"] for row in rows if not row["full_route_epoch_sync"]),
        "level_one_commit_is_three_route_windows": rows[0]["full_route_epochs"] == 3,
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT830 check failed: {name}")

    out = {
        "theorem": "BT830 two-phase holonet commit clock",
        "protocol": {
            "prepare_phase": "execute the BT828 reversible packet route, bounded by 8n",
            "commit_phase": "commit only on the durable tomotope/Csaszar tick T(n)=4(7^n-1)",
            "separation": "route clock is fast and reversible; commit clock is slower, 24-aligned, and cover-like",
        },
        "levels_1_to_24": rows,
        "sync_levels_1_to_24": sync_levels,
        "desync_levels_1_to_24": desync_levels,
        "sample_program_commit_fit": sample_program_rows,
        "checks": checks,
    }
    path = ROOT / "data" / "bt830_two_phase_commit_clock.json"
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
