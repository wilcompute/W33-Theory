#!/usr/bin/env python3
"""BT1600: compile all 1600 Witting ordered pairs into one transaction cycle."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bt1408_witting_contextual_communication_bridge import (
    construct_witting_40_rays,
    find_tetrads,
    memberships,
)

OUT = ROOT / "data" / "bt1600_full_witting_transaction_cycle.json"
MD = ROOT / "analysis" / "BT1600_full_witting_transaction_cycle.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    control = load_json("data/bt1598_witting_accepted_control_rail.json")
    phase_weld = load_json("data/bt1599_same_ray_phase_sheet_weld.json")
    fuel = load_json("data/bt1595_witting_matter_fuel_bijection.json")
    transaction = load_json("data/bt1597_universal_transaction_object.json")

    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    _ray_to_bases, pair_to_bases = memberships(tetrads)
    control_by_pair = {
        (row["source_ray"], row["target_ray"]): row
        for row in control["control_rows_sample"]
    }
    if len(control_by_pair) != control["counts"]["control_frames"]:
        # The JSON sample is intentionally truncated; rebuild compact control map
        control_by_pair = {}
        for source_ray in range(40):
            for target_ray in range(40):
                common_bases = pair_to_bases.get((source_ray, target_ray), [])
                if common_bases:
                    control_by_pair[(source_ray, target_ray)] = {
                        "common_bases": common_bases
                    }

    fuel_pairs = {tuple(row["witting_pair"]) for row in fuel["fuel_rows_sample"]}
    if len(fuel_pairs) != fuel["counts"]["fuel_segments"]:
        fuel_pairs = {
            (source, target)
            for source in range(40)
            for target in range(40)
            if not pair_to_bases.get((source, target), [])
        }

    rows = []
    rail_hist: Counter[str] = Counter()
    source_rail_hist: dict[int, Counter[str]] = {}
    for source_ray in range(40):
        for target_ray in range(40):
            pair = (source_ray, target_ray)
            frame_index = len(rows)
            if pair_to_bases.get(pair, []):
                rail = "ACCEPTED_CONTROL"
                payload = "Witting analyzer/mirror-slot control frame"
            else:
                rail = "CONTEXTUAL_FUEL"
                payload = "OAM/Hesse fuel frame"
            rows.append(
                {
                    "cycle_frame": frame_index,
                    "source_ray": source_ray,
                    "target_ray": target_ray,
                    "rail": rail,
                    "payload": payload,
                    "frame_start_tick": frame_index * 72,
                    "frame_end_tick": frame_index * 72 + 71,
                }
            )
            rail_hist[rail] += 1
            source_rail_hist.setdefault(source_ray, Counter())[rail] += 1

    checks = {
        "control_verified": control["verified"] is True,
        "phase_weld_verified": phase_weld["verified"] is True,
        "fuel_verified": fuel["verified"] is True,
        "transaction_object_verified": transaction["verified"] is True,
        "cycle_has_1600_frames": len(rows) == 1600,
        "rail_histogram_is_520_1080": dict(sorted(rail_hist.items()))
        == {"ACCEPTED_CONTROL": 520, "CONTEXTUAL_FUEL": 1080},
        "each_source_has_13_control_27_fuel": all(
            dict(hist) == {"ACCEPTED_CONTROL": 13, "CONTEXTUAL_FUEL": 27}
            for hist in source_rail_hist.values()
        ),
        "tick_budget_is_115200": len(rows) * 72
        == transaction["ticks"]["complete_cycle"]
        == 115200,
        "accepted_ticks_match_bt1598": rail_hist["ACCEPTED_CONTROL"] * 72
        == control["counts"]["ticks"]
        == 37440,
        "fuel_ticks_match_bt1595": rail_hist["CONTEXTUAL_FUEL"] * 72
        == fuel["counts"]["ticks"]
        == 77760,
        "phase_weld_is_sidecar_not_extra_cycle_frames": phase_weld["counts"][
            "surplus_contexts"
        ]
        == 120
        and len(rows) == 1600,
        "last_tick_is_115199": rows[-1]["frame_end_tick"] == 115199,
    }
    result = {
        "bt": 1600,
        "title": "Full Witting transaction cycle compiler",
        "verified": all(checks.values()),
        "source_packets": {
            "accepted_control": "data/bt1598_witting_accepted_control_rail.json",
            "same_ray_phase_weld": "data/bt1599_same_ray_phase_sheet_weld.json",
            "contextual_fuel": "data/bt1595_witting_matter_fuel_bijection.json",
            "transaction_object": "data/bt1597_universal_transaction_object.json",
        },
        "cycle_identity": {
            "frames": "40 source rays * 40 target rays = 1600 frames",
            "ticks": "1600 frames * 72 ticks = 115200",
            "rail_split": "520 accepted control frames + 1080 contextual fuel frames",
            "per_source": "13 accepted controls + 27 contextual fuel frames",
        },
        "counts": {
            "frames": len(rows),
            "ticks": len(rows) * 72,
            "accepted_control_frames": rail_hist["ACCEPTED_CONTROL"],
            "contextual_fuel_frames": rail_hist["CONTEXTUAL_FUEL"],
            "same_ray_phase_sidecar_records": phase_weld["counts"]["surplus_contexts"],
        },
        "rail_histogram": dict(sorted(rail_hist.items())),
        "source_rail_histogram": {
            source: dict(sorted(hist.items()))
            for source, hist in sorted(source_rail_hist.items())
        },
        "cycle_rows_sample": rows[:24] + rows[-24:],
        "interpretation": (
            "BT1600 compiles the entire Witting ordered-pair desk as one transaction "
            "cycle. Accepted pairs run on the Witting analyzer control rail; rejected "
            "pairs run on the OAM/Hesse fuel rail; the 120 same-ray phase records are "
            "a selector-sheet sidecar, not extra cycle frames."
        ),
        "honesty_boundary": (
            "This is a finite cycle compiler and rail partition. It does not prove "
            "hardware throughput, security, or fault-tolerant noise thresholds."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1600 Full Witting Transaction Cycle\n\n"
        "BT1600 compiles every Witting ordered pair into one `72`-tick frame:\n\n"
        "```text\n"
        "40 source rays * 40 target rays = 1600 frames\n"
        "1600 * 72 = 115200 ticks\n"
        "520 accepted control frames + 1080 contextual fuel frames\n"
        "```\n\n"
        "The `120` same-ray phase-sheet records from BT1599 are a selector sidecar, "
        "not extra cycle frames.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1600,
                "verified": result["verified"],
                "frames": len(rows),
                "ticks": len(rows) * 72,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
