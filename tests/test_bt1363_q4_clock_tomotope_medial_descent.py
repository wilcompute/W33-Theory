#!/usr/bin/env python3
"""Regression tests for BT1363 Q4 clock descent."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script() -> None:
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "analysis" / "bt1363_q4_clock_tomotope_medial_descent.py"),
        ],
        cwd=ROOT,
        check=True,
    )


def load_result() -> dict:
    with (ROOT / "data" / "bt1363_q4_clock_tomotope_medial_descent.json").open() as f:
        return json.load(f)


def test_bt1363_descended_clock_counts() -> None:
    run_script()
    data = load_result()
    assert data["verified"] is True
    assert data["q4_source"] == {
        "faces": 24,
        "edges": 32,
        "face_edge_incidences": 96,
    }
    assert (
        data["tomotope_reye_quotient"]["tomotope_edge_labels_from_q4_face_pairs"] == 12
    )
    assert (
        data["tomotope_reye_quotient"]["tomotope_face_labels_from_q4_edge_pairs"] == 16
    )
    assert data["tomotope_reye_quotient"]["middle_blocks"] == 48
    assert data["tomotope_reye_quotient"]["lift_multiplicity_profile"] == {"2": 48}


def test_bt1363_clock_descends_as_c2cubed_c4() -> None:
    run_script()
    data = load_result()
    clock = data["descended_clock"]
    assert clock["bt1362_stabilizer_order"] == 64
    assert len(clock["antipodal_kernel_elements"]) == 2
    assert clock["quotient_group_order"] == 32
    assert clock["structure"] == "(C2^4/<1111>) : C4 = C2^3 : C4"
    assert clock["tomotope_edge_orbit_profile"] == [4, 8]
    assert clock["tomotope_face_orbit_profile"] == [16]
    assert clock["middle_block_orbit_profile"] == [16, 16, 16]


def test_bt1363_ternary_sheets_hit_all_face_labels_once() -> None:
    run_script()
    data = load_result()
    sheets = data["descended_clock"]["ternary_sheets"]
    assert len(sheets) == 3
    assert all(sheet["middle_blocks"] == 16 for sheet in sheets)
    assert all(sheet["tomotope_face_labels_hit"] == 16 for sheet in sheets)
    assert all(
        sheet["face_projection_multiplicity_profile"] == {"1": 16} for sheet in sheets
    )
    assert sorted(sheet["tomotope_edge_labels_hit"] for sheet in sheets) == [4, 8, 8]


def test_bt1363_pure_c4_gives_twelve_four_tick_cycles() -> None:
    run_script()
    data = load_result()
    c4 = data["pure_c4_clock"]
    assert c4["order"] == 4
    assert c4["tomotope_edge_orbit_profile"] == [2, 2, 4, 4]
    assert c4["tomotope_face_orbit_profile"] == [4, 4, 4, 4]
    assert c4["middle_block_orbit_profile"] == [4] * 12


def test_bt1363_docs_index_card_present() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "BT1363: the Q4 clock descends to the tomotope medial layer" in text
    assert "BT1363_q4_clock_tomotope_medial_descent.md" in text
    assert "C2<sup>3</sup> : C4" in text
    assert "48=3&times;16=12&times;4" in text


if __name__ == "__main__":
    test_bt1363_descended_clock_counts()
    test_bt1363_clock_descends_as_c2cubed_c4()
    test_bt1363_ternary_sheets_hit_all_face_labels_once()
    test_bt1363_pure_c4_gives_twelve_four_tick_cycles()
    test_bt1363_docs_index_card_present()
    print("BT1363 focused tests passed")
