#!/usr/bin/env python3
"""BT1598: compile accepted Witting ordered pairs into the control rail."""
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

OUT = ROOT / "data" / "bt1598_witting_accepted_control_rail.json"
MD = ROOT / "analysis" / "BT1598_witting_accepted_control_rail.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def slot_in_basis(tetrad: tuple[int, int, int, int], ray: int) -> int:
    return list(tetrad).index(ray)


def balanced_same_ray_basis_matching(
    ray_to_bases: list[list[int]], tetrads: list[tuple[int, int, int, int]]
) -> dict[int, int]:
    options = {
        ray: [(basis, slot_in_basis(tetrads[basis], ray)) for basis in bases]
        for ray, bases in enumerate(ray_to_bases)
    }
    assignment: dict[int, int] = {}
    used_bases: set[int] = set()
    slot_quota = [10, 10, 10, 10]

    def assign() -> bool:
        if len(assignment) == len(ray_to_bases):
            return slot_quota == [0, 0, 0, 0]
        remaining = [ray for ray in range(len(ray_to_bases)) if ray not in assignment]
        ray = min(
            remaining,
            key=lambda candidate: sum(
                1
                for basis, slot in options[candidate]
                if basis not in used_bases and slot_quota[slot] > 0
            ),
        )
        available = [
            (basis, slot)
            for basis, slot in options[ray]
            if basis not in used_bases and slot_quota[slot] > 0
        ]
        available.sort(key=lambda item: -slot_quota[item[1]])
        for basis, slot in available:
            assignment[ray] = basis
            used_bases.add(basis)
            slot_quota[slot] -= 1
            still_possible = True
            for other in remaining:
                if other == ray:
                    continue
                if not any(
                    basis_2 not in used_bases and slot_quota[slot_2] > 0
                    for basis_2, slot_2 in options[other]
                ):
                    still_possible = False
                    break
            if still_possible and assign():
                return True
            slot_quota[slot] += 1
            used_bases.remove(basis)
            del assignment[ray]
        return False

    if not assign():
        raise RuntimeError("no balanced same-ray basis matching found")
    return dict(sorted(assignment.items()))


def main() -> None:
    witting = load_json("data/bt1408_witting_contextual_communication_bridge.json")
    delayed = load_json("data/bt1410_witting_delayed_query_frame_compiler.json")
    transaction = load_json("data/bt1597_universal_transaction_object.json")
    analyzers = load_json("data/bt1411_witting_basis_analyzer_unitaries.json")

    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    ray_to_bases, pair_to_bases = memberships(tetrads)
    same_matching = balanced_same_ray_basis_matching(ray_to_bases, tetrads)
    analyzer_by_basis = {row["basis_id"]: row for row in analyzers["all_analyzers"]}

    rows = []
    mode_hist: Counter[str] = Counter()
    source_hist: Counter[int] = Counter()
    target_hist: Counter[int] = Counter()
    basis_hist: Counter[int] = Counter()
    slot_hist: Counter[int] = Counter()
    optical_family_hist: Counter[str] = Counter()
    for source_ray in range(40):
        for target_ray in range(40):
            common_bases = pair_to_bases.get((source_ray, target_ray), [])
            if not common_bases:
                continue
            if source_ray == target_ray:
                selected_basis = same_matching[source_ray]
                mode = "SAME_RAY_MATCHED_CONTROL_APERTURE"
            else:
                selected_basis = common_bases[0]
                mode = "COMPATIBLE_UNIQUE_BASIS_CONTROL"
            tetrad = tetrads[selected_basis]
            alice_slot = slot_in_basis(tetrad, source_ray)
            bob_slot = slot_in_basis(tetrad, target_ray)
            analyzer = analyzer_by_basis[selected_basis]
            frame_index = len(rows)
            tomotope_block = selected_basis
            tomotope_flag = 4 * tomotope_block + bob_slot
            rows.append(
                {
                    "control_frame": frame_index,
                    "source_ray": source_ray,
                    "target_ray": target_ray,
                    "selected_basis": selected_basis,
                    "basis_options": common_bases,
                    "alice_slot": alice_slot,
                    "bob_slot": bob_slot,
                    "detector_slot": bob_slot,
                    "mirror_slot_mod_4": bob_slot,
                    "tomotope_block": tomotope_block,
                    "tomotope_flag": tomotope_flag,
                    "optical_family": analyzer["optical_family"],
                    "mode": mode,
                    "frame_start_tick": frame_index * 72,
                    "frame_end_tick": frame_index * 72 + 71,
                    "handoff": "Witting analyzer slot -> detector slot -> mirror_slot mod 4 -> Q6/tomotope flag",
                }
            )
            mode_hist[mode] += 1
            source_hist[source_ray] += 1
            target_hist[target_ray] += 1
            basis_hist[selected_basis] += 1
            slot_hist[bob_slot] += 1
            optical_family_hist[analyzer["optical_family"]] += 1

    same_basis_hist = Counter(same_matching.values())
    checks = {
        "witting_verified": witting["verified"] is True,
        "delayed_query_verified": delayed["verified"] is True,
        "transaction_object_verified": transaction["verified"] is True,
        "analyzers_verified": analyzers["verified"] is True,
        "perfect_same_ray_matching": len(same_matching) == 40
        and len(set(same_matching.values())) == 40,
        "accepted_control_frames_520": len(rows) == 520,
        "mode_histogram_is_480_plus_40": dict(sorted(mode_hist.items()))
        == {
            "COMPATIBLE_UNIQUE_BASIS_CONTROL": 480,
            "SAME_RAY_MATCHED_CONTROL_APERTURE": 40,
        },
        "each_source_has_13_control_frames": sorted(source_hist.values()) == [13] * 40,
        "each_target_has_13_control_frames": sorted(target_hist.values()) == [13] * 40,
        "each_basis_has_13_control_frames": sorted(basis_hist.values()) == [13] * 40,
        "same_matching_uses_each_basis_once": sorted(same_basis_hist.values())
        == [1] * 40,
        "detector_slots_balanced": dict(sorted(slot_hist.items()))
        == {0: 130, 1: 130, 2: 130, 3: 130},
        "tomotope_flags_stay_in_first_40_blocks": min(
            row["tomotope_flag"] for row in rows
        )
        == 0
        and max(row["tomotope_flag"] for row in rows) == 159,
        "control_tick_budget": len(rows) * 72
        == transaction["ticks"]["accepted_control"]
        == 37440,
        "basis_as_tomotope_block_has_eight_slack_blocks": 48 - len(set(basis_hist))
        == 8,
    }
    result = {
        "bt": 1598,
        "title": "Accepted Witting control rail compiler",
        "verified": all(checks.values()),
        "source_packets": {
            "witting_bridge": "data/bt1408_witting_contextual_communication_bridge.json",
            "delayed_query_frames": "data/bt1410_witting_delayed_query_frame_compiler.json",
            "witting_analyzers": "data/bt1411_witting_basis_analyzer_unitaries.json",
            "transaction_object": "data/bt1597_universal_transaction_object.json",
        },
        "control_identity": {
            "logical": "40 same-ray controls + 480 compatible controls = 520 accepted frames",
            "basis_local": "40 Witting bases * 13 controls per basis = 520",
            "ticks": "520 accepted frames * 72 ticks = 37440",
            "address_rule": "tomotope_flag = 4*selected_basis + detector_slot",
        },
        "counts": {
            "control_frames": len(rows),
            "ticks": len(rows) * 72,
            "witting_bases_used": len(basis_hist),
            "tomotope_blocks_used": len(set(row["tomotope_block"] for row in rows)),
            "tomotope_blocks_slack": 8,
        },
        "histograms": {
            "mode": dict(sorted(mode_hist.items())),
            "source": dict(sorted(source_hist.items())),
            "target": dict(sorted(target_hist.items())),
            "basis": dict(sorted(basis_hist.items())),
            "detector_slot": dict(sorted(slot_hist.items())),
            "optical_family": dict(sorted(optical_family_hist.items())),
        },
        "same_ray_basis_matching": dict(sorted(same_matching.items())),
        "control_rows_sample": rows[:20] + rows[-20:],
        "interpretation": (
            "BT1598 compiles the accepted 13/40 Witting rail into actual control "
            "frames. A perfect same-ray matching selects one witness basis per ray, "
            "so each of the 40 Witting bases carries exactly 13 accepted controls."
        ),
        "honesty_boundary": (
            "This is a finite control-frame compiler. It does not prove cryptographic "
            "security, detector efficiency, or optical loss tolerance."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1598 Accepted Witting Control Rail\n\n"
        "BT1598 compiles the `520` accepted Witting ordered pairs into concrete "
        "control frames.  A perfect same-ray basis matching selects one same-ray "
        "aperture per Witting basis, so the accepted rail factors as "
        "`40 bases * 13 control frames = 520`, with `520*72=37440` ticks.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1598,
                "verified": result["verified"],
                "control_frames": len(rows),
                "ticks": len(rows) * 72,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
