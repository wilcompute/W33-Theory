#!/usr/bin/env python3
"""BT1372: three-epoch lift of the 2160 scheduler to Steinberg basis labels."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1372_three_epoch_steinberg_basis_scheduler_lift.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_rows() -> list[dict[str, int]]:
    rows = []
    for epoch in range(3):
        for orbit in range(135):
            lane = orbit // 27
            matter_state = orbit % 27
            for face_slot in range(16):
                local_slot = lane * 16 + face_slot
                generation = (local_slot + matter_state + epoch) % 3
                basis_index = generation * 27 + matter_state
                global_slot = orbit * 16 + face_slot
                rows.append(
                    {
                        "epoch": epoch,
                        "global_slot": global_slot,
                        "phase_orbit": orbit,
                        "lane": lane,
                        "matter_state": matter_state,
                        "face_slot": face_slot,
                        "local_slot": local_slot,
                        "generation": generation,
                        "steinberg_basis_index": basis_index,
                    }
                )
    return rows


def build_result() -> dict[str, object]:
    bt1369 = load_json(
        ROOT / "data" / "bt1369_steinberg_generation_time_scheduler.json"
    )
    bt865 = load_json(ROOT / "data" / "bt865_dual_torsor_steinberg_compiler.json")
    rows = build_rows()

    single_epoch_basis_counts = Counter(
        row["steinberg_basis_index"] for row in rows if row["epoch"] == 0
    )
    three_epoch_basis_counts = Counter(row["steinberg_basis_index"] for row in rows)
    single_epoch_generation_counts = Counter(
        row["generation"] for row in rows if row["epoch"] == 0
    )
    three_epoch_generation_counts = Counter(row["generation"] for row in rows)
    per_matter_single = defaultdict(Counter)
    per_matter_three = defaultdict(Counter)
    commutation_failures = []
    for row in rows:
        if row["epoch"] == 0:
            per_matter_single[row["matter_state"]][row["generation"]] += 1
        per_matter_three[row["matter_state"]][row["generation"]] += 1
        if row["epoch"] < 2:
            next_generation = (
                row["local_slot"] + row["matter_state"] + row["epoch"] + 1
            ) % 3
            if next_generation != (row["generation"] + 1) % 3:
                commutation_failures.append(row)

    single_profiles = Counter(
        tuple(counter[g] for g in range(3)) for counter in per_matter_single.values()
    )
    three_profiles = Counter(
        tuple(counter[g] for g in range(3)) for counter in per_matter_three.values()
    )

    checks = {
        "one_epoch_has_2160_slots": len([row for row in rows if row["epoch"] == 0])
        == 2160,
        "three_epoch_cover_has_6480_slots": len(rows) == 6480,
        "single_epoch_cannot_be_uniform_on_81_basis": 2160 % 81 == 54,
        "single_epoch_is_globally_generation_balanced": dict(
            single_epoch_generation_counts
        )
        == {0: 720, 1: 720, 2: 720},
        "single_epoch_per_matter_has_27_27_26_profile": sorted(single_profiles)
        == [(26, 27, 27), (27, 26, 27), (27, 27, 26)],
        "three_epoch_is_uniform_on_81_basis": set(three_epoch_basis_counts.values())
        == {80}
        and len(three_epoch_basis_counts) == 81,
        "three_epoch_is_generation_balanced": dict(three_epoch_generation_counts)
        == {0: 2160, 1: 2160, 2: 2160},
        "three_epoch_per_matter_is_80_80_80": dict(three_profiles)
        == {(80, 80, 80): 27},
        "epoch_advance_commutes_with_generation_cycle": not commutation_failures,
        "bt865_basis_dimension_matches": bt865["chain_complex"]["dim_H1_mod3"] == 81,
        "bt1369_source_slots_match": bt1369["scheduler"]["total_slots"] == 2160,
    }

    return {
        "bt": 1372,
        "title": "Three-epoch Steinberg basis scheduler lift",
        "verified": all(checks.values()),
        "one_epoch_boundary": {
            "slots": 2160,
            "steinberg_basis_dim": 81,
            "division": "2160 = 81 * 26 + 54",
            "verdict": "one epoch cannot be uniform on the full 81-state Steinberg basis",
            "global_generation_counts": dict(
                sorted(single_epoch_generation_counts.items())
            ),
            "per_matter_generation_profiles": {
                str(k): v for k, v in sorted(single_profiles.items())
            },
        },
        "three_epoch_lift": {
            "slots": len(rows),
            "identity": "3 * 2160 = 6480 = 81 * 80",
            "basis_count_profile": {
                str(k): v
                for k, v in sorted(Counter(three_epoch_basis_counts.values()).items())
            },
            "generation_counts": dict(sorted(three_epoch_generation_counts.items())),
            "per_matter_generation_profiles": {
                str(k): v for k, v in sorted(three_profiles.items())
            },
            "rule": "generation = (local_slot + matter_state + epoch) mod 3",
            "rows_sample": rows[:24],
        },
        "interpretation": (
            "BT1369's scheduler is exactly a 27-matter-coordinate scheduler in "
            "one epoch.  The full 81-dimensional Steinberg basis needs the "
            "natural q=3 time cover: across three epochs, every basis label "
            "receives exactly 80 slots and epoch advance is the generation cycle."
        ),
        "boundary": (
            "This supplies explicit basis labels and counts.  It is not yet an "
            "operator on the concrete BT865 cycle-vector witnesses; that is the "
            "next linear-action test."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "identity": result["three_epoch_lift"]["identity"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
