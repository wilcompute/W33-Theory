#!/usr/bin/env python3
"""Bridge the BT367 selector phantom, BT982 E8 basis, and Holonet runtime.

This is an accounting certificate, not a new representation proof.  It verifies
that the existing machine-readable artifacts share a single runtime clock:

  * 120 selector sheets with self-support 108 give 120*108 = 12960 probes.
  * The frequency-bin lab packet assigns four runtime slots per probe, so
    12960*4 = 51840, the W(E6) / Holonet supercycle.
  * Doubling the 120 sheets by sign gives the 240 E8-root count, and each
    signed sheet/root gets 2*108 = 216 runtime slots, so 240*216 = 51840.

Boundary: this file does not construct a canonical sheet-to-E8-root bijection.
It records the exact quotient map that the next hardware/compiler layer can
try to refine.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_selector_e6_e8_runtime_bridge.json"


E8_CARTAN = [
    [2, 0, -1, 0, 0, 0, 0, 0],
    [0, 2, 0, -1, 0, 0, 0, 0],
    [-1, 0, 2, -1, 0, 0, 0, 0],
    [0, -1, -1, 2, -1, 0, 0, 0],
    [0, 0, 0, -1, 2, -1, 0, 0],
    [0, 0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, 0, -1, 2, -1],
    [0, 0, 0, 0, 0, 0, -1, 2],
]


def load_json(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def parse_gap_dims() -> list[int]:
    text = (ROOT / "data/bt360_120sheet_scheme_gap.txt").read_text(encoding="utf-8")
    match = re.search(r"gap_eigenspace_dims\s*:=\s*\[([^\]]+)\]", text)
    if not match:
        raise RuntimeError("could not find gap_eigenspace_dims")
    return sorted(int(part.strip()) for part in match.group(1).split(","))


def main() -> None:
    sheet_matrix = load_json("data/sheet_intersections.json")
    holonomy = load_json("data/w33_BREAKTHROUGH_367_holonomy_loops.json")
    e8 = load_json("data/bt982_explicit_integral_e8_basis.json")
    fabric = load_json("data/w33_holonet_firmware_fabric_profile.json")
    lab = load_json("data/w33_frequency_bin_lab_packet.json")
    compiler = load_json("data/w33_frequency_bin_hashimoto_compiler.json")

    sheet_count = len(sheet_matrix)
    row_lengths = sorted({len(row) for row in sheet_matrix})
    diagonal_values = [sheet_matrix[i][i] for i in range(sheet_count)]
    intersection_values = sorted({value for row in sheet_matrix for value in row})
    gap_dims = parse_gap_dims()

    mirror = fabric["mirror_fabric"]
    lab_summary = lab["schedule_summary"]

    we6_order = mirror["supercycle_slots"]
    line_count = 40
    phases_per_line = sheet_count // line_count
    sheet_support = diagonal_values[0]
    signed_sheet_count = 2 * sheet_count
    signed_sheet_slots = 2 * sheet_support
    sheets_per_mirror_atlas = sheet_count // mirror["mirror_atlases_per_supercycle"]
    signed_sheets_per_mirror_atlas = (
        signed_sheet_count // mirror["mirror_atlases_per_supercycle"]
    )
    probes_per_selector_sheet = sheet_support

    bridge_identities = {
        "selector_sheet_design": f"{line_count} lines * {phases_per_line} phases = {sheet_count}",
        "sheet_support_to_probe_clock": f"{sheet_count} sheets * {sheet_support} support = {lab_summary['supercycle_probe_rows']} probes",
        "probe_clock_to_runtime": f"{lab_summary['supercycle_probe_rows']} probes * {lab_summary['runtime_slots_per_probe']} slots = {we6_order}",
        "atlas_selector_budget": f"{sheets_per_mirror_atlas} sheets/atlas * {sheet_support} support * {lab_summary['runtime_slots_per_probe']} slots = {mirror['mirror_slots']}",
        "signed_e8_budget": f"{signed_sheet_count} signed sheets * {signed_sheet_slots} slots = {we6_order}",
        "mirror_runtime": fabric["layer_identities"]["runtime_supercycle"],
        "mirror_atlas": fabric["layer_identities"]["mirror_atlas"],
        "twisted_phase_phantom": f"{2 * holonomy['twisted_cycles_in_basis']} conflicts = 2 * {holonomy['twisted_cycles_in_basis']} twisted cycles",
    }

    checks = {
        "C1_sheet_matrix_is_120_square": sheet_count == 120 and row_lengths == [120],
        "C2_sheet_values_match_scheme_profile": intersection_values
        == [2, 4, 12, 54, 108],
        "C3_diagonal_support_is_uniform_108": diagonal_values == [108] * sheet_count,
        "C4_gap_irrep_dims_sum_to_120": gap_dims == [1, 15, 20, 24, 60]
        and sum(gap_dims) == sheet_count,
        "C5_holonomy_phantom_is_760": holonomy["twisted_cycles_in_basis"] == 380
        and 2 * holonomy["twisted_cycles_in_basis"] == 760,
        "C6_e8_basis_is_integral_cartan": e8["matches_standard_e8_cartan"] is True
        and e8["det_B"] in (-1, 1)
        and e8["final_gram_Bt_G_vertex_B"] == E8_CARTAN,
        "C7_e8_selector_winner_is_shared": e8["winner_minimizer"] == 2
        and e8["checks"]["T1_both_gauges_agree_minimizer_2"] is True,
        "C8_sheet_support_closes_probe_clock": sheet_count * sheet_support
        == lab_summary["supercycle_probe_rows"],
        "C9_probe_clock_closes_runtime": lab_summary["supercycle_probe_rows"]
        * lab_summary["runtime_slots_per_probe"]
        == we6_order,
        "C10_atlas_budget_is_five_sheets": sheets_per_mirror_atlas == 5
        and sheets_per_mirror_atlas
        * sheet_support
        * lab_summary["runtime_slots_per_probe"]
        == mirror["mirror_slots"],
        "C11_signed_sheet_budget_is_e8_root_budget": signed_sheet_count == 240
        and signed_sheet_slots == 216
        and signed_sheet_count * signed_sheet_slots == we6_order,
        "C12_frequency_lab_sources_are_verified": lab["verified"] is True
        and compiler["checks"]["phase_probe_budget_is_one_quarter_runtime_slots"]
        is True,
        "C13_firmware_supercycle_is_we6_order": mirror["mirror_atlases_per_supercycle"]
        == 24
        and mirror["mirror_slots"] == 2160
        and mirror["supercycle_slots"] == 51840,
    }

    result = {
        "theorem": "W33 selector E6/E8 runtime bridge",
        "verified": all(checks.values()),
        "breakthrough": (
            "The BT367 selector phantom, BT982 E8 basis, and frequency-bin "
            "Holonet lab packet share an exact support clock: 120 selector "
            "sheets have self-support 108, giving 12960 supercycle probes; "
            "the lab packet assigns four runtime slots per probe, giving "
            "51840 = |W(E6)|.  Signed sheets double to 240, matching the E8 "
            "root count, and each signed sheet/root owns 216 runtime slots."
        ),
        "source_certificates": [
            "data/sheet_intersections.json",
            "data/bt360_120sheet_scheme_gap.txt",
            "data/w33_BREAKTHROUGH_367_holonomy_loops.json",
            "data/bt982_explicit_integral_e8_basis.json",
            "data/w33_holonet_firmware_fabric_profile.json",
            "data/w33_frequency_bin_hashimoto_compiler.json",
            "data/w33_frequency_bin_lab_packet.json",
        ],
        "selector_e6_surface": {
            "line_count": line_count,
            "phases_per_line": phases_per_line,
            "sheet_count": sheet_count,
            "sheet_self_support": sheet_support,
            "intersection_values": intersection_values,
            "we6_irrep_dimensions": gap_dims,
            "twisted_cycles_in_basis": holonomy["twisted_cycles_in_basis"],
            "twisted_conflict_count": 2 * holonomy["twisted_cycles_in_basis"],
            "cycle_basis_size": holonomy["total_cycles_in_basis"],
        },
        "e8_surface": {
            "signed_sheet_count": signed_sheet_count,
            "e8_root_count_reading": "240 = 2 * 120 signed selector sheets",
            "winner_minimizer": e8["winner_minimizer"],
            "support_minimal_masks": e8["support_minimal_masks"],
            "basis_det": e8["det_B"],
            "cartan_match": e8["matches_standard_e8_cartan"],
            "vertex_subset": e8["vertex_subset"],
        },
        "runtime_surface": {
            "we6_order": we6_order,
            "mirror_atlases_per_supercycle": mirror["mirror_atlases_per_supercycle"],
            "mirror_slots": mirror["mirror_slots"],
            "packet_frames_per_supercycle": mirror["packet_frames_per_supercycle"],
            "frequency_probe_rows_per_atlas": lab_summary["rows"],
            "frequency_probe_rows_per_supercycle": lab_summary["supercycle_probe_rows"],
            "runtime_slots_per_probe": lab_summary["runtime_slots_per_probe"],
            "sheets_per_mirror_atlas_accounting": sheets_per_mirror_atlas,
            "signed_sheets_per_mirror_atlas_accounting": (
                signed_sheets_per_mirror_atlas
            ),
            "probes_per_selector_sheet_accounting": probes_per_selector_sheet,
            "runtime_slots_per_signed_sheet_accounting": signed_sheet_slots,
        },
        "bridge_identities": bridge_identities,
        "checks": checks,
        "claim_boundary": [
            "This is an executable accounting bridge, not a proof of a canonical sheet-to-root bijection.",
            "The E8 side is the BT982 vertex-gauge integral basis; a verbatim Z^40 split/double-cover lift remains outside this certificate.",
            "The 5 sheets per mirror atlas and 10 signed sheets per mirror atlas are exact quotient budgets, not yet a canonical atlas ordering.",
            "Frequency-bin counts, visibility, and phase-error measurements still require bench data.",
        ],
    }

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
