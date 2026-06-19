#!/usr/bin/env python3
"""BT1365: align the BT1363 ternary sheets with the selector qutrit phases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1365_qutrit_phase_sheet_alignment.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_result() -> dict[str, object]:
    bt1363 = load_json(ROOT / "data" / "bt1363_q4_clock_tomotope_medial_descent.json")
    bt361 = load_json(
        ROOT / "data" / "w33_BREAKTHROUGH_361_selector_qutrit_phase_bundle.json"
    )

    local_sheets = bt1363["descended_clock"]["ternary_sheets"]
    selector_summary = bt361["summary"]
    selector_profiles = bt361["profiles"]
    local_phase_count = len(local_sheets)
    selector_phase_count = int(selector_summary["phase_fiber_size"])
    base_line_count = int(selector_summary["base_line_count"])
    selector_sheet_count = int(selector_summary["sheet_count"])

    phase_alignment_rows = []
    for phase, sheet in enumerate(local_sheets):
        phase_alignment_rows.append(
            {
                "phase": phase,
                "local_middle_blocks": sheet["middle_blocks"],
                "local_face_labels_hit": sheet["tomotope_face_labels_hit"],
                "selector_sheets_over_40_lines": base_line_count,
                "selector_sheet_range": [
                    phase * base_line_count,
                    (phase + 1) * base_line_count - 1,
                ],
            }
        )

    checks = {
        "local_sheets_match_qutrit_phase_count": local_phase_count
        == selector_phase_count
        == 3,
        "local_phase_sheets_hit_16_face_labels_once": all(
            sheet["tomotope_face_labels_hit"] == 16
            and sheet["face_projection_multiplicity_profile"] == {"1": 16}
            for sheet in local_sheets
        ),
        "selector_bundle_is_40_times_3": base_line_count * selector_phase_count
        == selector_sheet_count
        == 120,
        "same_line_selector_relation_is_k3": selector_profiles[
            "line_fiber_size_profile"
        ]
        == {"3": 40}
        and selector_profiles["r54_component_size_profile"] == {"3": 40},
        "skew_selector_matching_has_three_phase_pairs": bt361["bundle_law"][
            "skew_lines"
        ].startswith("one perfect matching of 3 phase pairs"),
        "phase_alignment_accounts_for_all_selector_sheets": sum(
            row["selector_sheets_over_40_lines"] for row in phase_alignment_rows
        )
        == 120,
        "phase_alignment_accounts_for_local_bus": sum(
            row["local_middle_blocks"] for row in phase_alignment_rows
        )
        == 48,
    }

    return {
        "bt": 1365,
        "title": "Qutrit phase sheet alignment",
        "verified": all(checks.values()),
        "local_bt1363_phase_bus": {
            "phase_count": local_phase_count,
            "middle_blocks": 48,
            "blocks_per_phase": [sheet["middle_blocks"] for sheet in local_sheets],
            "face_labels_per_phase": [
                sheet["tomotope_face_labels_hit"] for sheet in local_sheets
            ],
        },
        "selector_bt361_phase_bundle": {
            "base_lines": base_line_count,
            "phase_fiber_size": selector_phase_count,
            "selector_sheets": selector_sheet_count,
            "same_line_law": bt361["bundle_law"]["same_line"],
            "skew_line_law": bt361["bundle_law"]["skew_lines"],
        },
        "alignment": {
            "phase_rows": phase_alignment_rows,
            "identity": "3 local tomotope sheets * 40 W33 lines = 120 selector phase sheets",
        },
        "interpretation": (
            "The three BT1363 tomotope sheets have exactly the cardinality and "
            "local incidence behavior required to be the qutrit phase labels of "
            "the BT361 selector bundle.  Each local phase is a 16-face register; "
            "globalizing over 40 W33 lines gives the existing 120 selector sheets."
        ),
        "boundary": (
            "This aligns phase indices and incidence profiles.  It does not yet "
            "choose a global phase gauge for every W33 skew-line transport matching."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "identity": result["alignment"]["identity"],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
