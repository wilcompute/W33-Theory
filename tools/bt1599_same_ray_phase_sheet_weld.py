#!/usr/bin/env python3
"""BT1599: weld unused same-ray Witting apertures to BT1365 phase sheets."""
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

OUT = ROOT / "data" / "bt1599_same_ray_phase_sheet_weld.json"
MD = ROOT / "analysis" / "BT1599_same_ray_phase_sheet_weld.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    control = load_json("data/bt1598_witting_accepted_control_rail.json")
    delayed = load_json("data/bt1410_witting_delayed_query_frame_compiler.json")
    phase = load_json("data/bt1365_qutrit_phase_sheet_alignment.json")

    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    ray_to_bases, _pair_to_bases = memberships(tetrads)
    selected_basis_by_ray = {
        int(ray): basis for ray, basis in control["same_ray_basis_matching"].items()
    }
    rows = []
    ray_hist: Counter[int] = Counter()
    phase_hist: Counter[int] = Counter()
    basis_hist: Counter[int] = Counter()
    sheet_hist: Counter[int] = Counter()
    for ray in range(40):
        unselected_bases = [
            basis for basis in ray_to_bases[ray] if basis != selected_basis_by_ray[ray]
        ]
        for surplus_phase, basis in enumerate(unselected_bases):
            selector_sheet = surplus_phase * 40 + ray
            rows.append(
                {
                    "ray": ray,
                    "surplus_phase": surplus_phase,
                    "unselected_basis": basis,
                    "selected_control_basis": selected_basis_by_ray[ray],
                    "selector_sheet": selector_sheet,
                    "selector_sheet_formula": "surplus_phase*40 + ray",
                    "tetrad": list(tetrads[basis]),
                    "role": "same-ray contextual audit aperture, not logical control frame",
                }
            )
            ray_hist[ray] += 1
            phase_hist[surplus_phase] += 1
            basis_hist[basis] += 1
            sheet_hist[selector_sheet] += 1

    checks = {
        "control_verified": control["verified"] is True,
        "delayed_query_verified": delayed["verified"] is True,
        "phase_alignment_verified": phase["verified"] is True,
        "surplus_rows_120": len(rows)
        == delayed["basis_local_frame_table"]["same_ray_extra_context_options"]
        == 120,
        "each_ray_has_three_surplus_contexts": sorted(ray_hist.values()) == [3] * 40,
        "three_phase_sheets_each_cover_40_rays": dict(sorted(phase_hist.items()))
        == {0: 40, 1: 40, 2: 40},
        "each_witting_basis_has_three_surplus_contexts": sorted(basis_hist.values())
        == [3] * 40,
        "selector_sheets_are_0_to_119": sorted(sheet_hist) == list(range(120))
        and sorted(sheet_hist.values()) == [1] * 120,
        "matches_bt1365_identity": phase["alignment"]["identity"]
        == "3 local tomotope sheets * 40 W33 lines = 120 selector phase sheets",
        "selected_and_surplus_recover_four_bases_per_ray": all(
            len(
                {
                    selected_basis_by_ray[ray],
                    *[row["unselected_basis"] for row in rows if row["ray"] == ray],
                }
            )
            == 4
            for ray in range(40)
        ),
    }
    result = {
        "bt": 1599,
        "title": "Same-ray Witting surplus to phase-sheet weld",
        "verified": all(checks.values()),
        "source_packets": {
            "accepted_control_rail": "data/bt1598_witting_accepted_control_rail.json",
            "delayed_query_frames": "data/bt1410_witting_delayed_query_frame_compiler.json",
            "phase_alignment": "data/bt1365_qutrit_phase_sheet_alignment.json",
        },
        "identity": {
            "basis_surplus": "160 same-ray basis-local apertures - 40 selected controls = 120 surplus audits",
            "phase_sheets": phase["alignment"]["identity"],
            "weld": "surplus same-ray contexts = 3 phases * 40 Witting rays",
        },
        "counts": {
            "surplus_contexts": len(rows),
            "rays": len(ray_hist),
            "phases": len(phase_hist),
            "selector_sheets": len(sheet_hist),
        },
        "histograms": {
            "ray": dict(sorted(ray_hist.items())),
            "phase": dict(sorted(phase_hist.items())),
            "basis": dict(sorted(basis_hist.items())),
        },
        "phase_rows": rows[:18] + rows[-18:],
        "interpretation": (
            "BT1599 explains the 120 records that remain after BT1598 chooses one "
            "same-ray control basis per ray. They are not discarded: they are exactly "
            "the BT1365 3-by-40 selector phase sheets."
        ),
        "honesty_boundary": (
            "This is a finite incidence weld. It does not choose a calibrated global "
            "phase gauge or measure phase noise."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1599 Same-Ray Phase-Sheet Weld\n\n"
        "BT1599 identifies the `120` same-ray basis-local surplus records with the "
        "BT1365 selector phase sheets:\n\n"
        "```text\n"
        "160 same-ray basis-local apertures - 40 selected same-ray controls = 120\n"
        "120 = 3 local tomotope sheets * 40 W33/Witting lines\n"
        "```\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1599,
                "verified": result["verified"],
                "surplus_contexts": len(rows),
                "selector_sheets": len(sheet_hist),
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
