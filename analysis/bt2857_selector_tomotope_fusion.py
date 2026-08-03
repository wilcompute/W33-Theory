#!/usr/bin/env python3
from __future__ import annotations

from bt2854_2860_common import *

def pass2857() -> dict:
    faces = ("0111", "1011", "1101", "1110")
    channels = ("011", "101", "110")
    phases = tuple(product((0, 1), repeat=3))
    tokens = []
    tetra_words = []
    hemi_words = []
    for f, face in enumerate(faces):
        for c, channel in enumerate(channels):
            sheet_id = 3 * f + c
            for phase in phases:
                parity = sum(phase) & 1
                if parity == 0:
                    cell_type = "T"
                    cell_index = tuple(p for p in phases if sum(p) % 2 == 0).index(phase)
                    tetra_words.append(phase)
                else:
                    cell_type = "H"
                    cell_index = minority_coordinate(phase)
                    hemi_words.append(phase)
                tokens.append({
                    "face": face,
                    "channel": channel,
                    "sheet_id": sheet_id,
                    "phase": "".join(map(str, phase)),
                    "cell_type": cell_type,
                    "cell_index": cell_index,
                })
    checks = {
        "four_faces": len(faces) == 4,
        "three_channels": len(channels) == 3,
        "twelve_sheet_ids": {t["sheet_id"] for t in tokens} == set(range(12)),
        "eight_phases_per_sheet": all(sum(t["sheet_id"] == i for t in tokens) == 8 for i in range(12)),
        "ninety_six_control_tokens": len(tokens) == 96,
        "all_control_tokens_unique": len({(t["face"], t["channel"], t["phase"]) for t in tokens}) == 96,
        "even_phase_is_tetra": all(t["cell_type"] == "T" for t in tokens if sum(map(int, t["phase"])) % 2 == 0),
        "odd_phase_is_hemi": all(t["cell_type"] == "H" for t in tokens if sum(map(int, t["phase"])) % 2 == 1),
        "all_four_tetra_cells_reached_per_sheet": all({t["cell_index"] for t in tokens if t["sheet_id"] == i and t["cell_type"] == "T"} == set(range(4)) for i in range(12)),
        "all_four_hemi_cells_reached_per_sheet": all({t["cell_index"] for t in tokens if t["sheet_id"] == i and t["cell_type"] == "H"} == set(range(4)) for i in range(12)),
        "token_count_equals_tomotope_aut_order": len(tokens) == 96,
    }
    assert all(checks.values())
    return {
        "schema": "w33.pass2857.selector_tomotope_fusion.v1",
        "status": "COMPLETE_EXACT_RTL",
        "control_word": "face[1:0] + matching[1:0] + phase[2:0]",
        "valid_control_states": 96,
        "mapping_sha256": sha(tokens),
        "sample_tokens": tokens[:12],
        "hardware": "rtl/w33_pass2857_selector_tomotope_fusion.sv",
        "checks": checks,
        "check_count": len(checks),
        "reading": "One seven-bit typed control word simultaneously selects one of the twelve exact Type-A sheets and one of the eight parity-coded tomotope cells.",
        "boundary": "The equality 12*8=96 is implemented as an exact bijection of control labels. It is not promoted as a regular action of Aut(tomotope) on these tokens without an additional group law/intertwiner.",
    }
