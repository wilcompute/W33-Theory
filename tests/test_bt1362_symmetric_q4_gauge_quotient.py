#!/usr/bin/env python3
"""Regression tests for BT1362 symmetric Q4 gauge quotient."""
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
            str(ROOT / "analysis" / "bt1362_symmetric_q4_gauge_quotient.py"),
        ],
        cwd=ROOT,
        check=True,
    )


def load_result() -> dict:
    with (ROOT / "data" / "bt1362_symmetric_q4_gauge_quotient.json").open() as f:
        return json.load(f)


def test_bt1362_symmetric_quotient_code_parameters() -> None:
    run_script()
    data = load_result()
    assert data["verified"] is True
    assert data["code"] == {
        "n": 32,
        "rank_hx": 15,
        "rank_hz": 13,
        "k": 4,
        "dx": 4,
        "dz": 4,
    }
    assert data["checks"]["quotient_avoids_weight_lt4_dual_obstructions"] is True


def test_bt1362_stabilizer_is_affine_cyclic_axis_clock() -> None:
    run_script()
    data = load_result()
    symmetry = data["symmetry"]
    assert symmetry["cube_automorphism_group_order"] == 384
    assert symmetry["generic_bt1341_active_stabilizer_size"] == 1
    assert symmetry["generic_bt1341_active_orbit_size"] == 384
    assert symmetry["symmetric_active_stabilizer_size"] == 64
    assert symmetry["symmetric_active_orbit_size"] == 6
    assert symmetry["hz_rowspace_stabilizer_size"] == 64
    assert symmetry["stabilizer_structure"] == "C2^4 : C4"
    assert symmetry["cyclic_axis_order_count"] == 6
    assert data["checks"]["orbit_stabilizer_384"] is True


def test_bt1362_stabilizer_elements_are_all_translations_times_c4() -> None:
    run_script()
    data = load_result()
    elements = data["symmetry"]["stabilizer_elements"]
    assert len(elements) == 64
    perms = {tuple(row["perm"]) for row in elements}
    flips_by_perm = {
        tuple(row["perm"]): sorted(
            r["flip"] for r in elements if r["perm"] == row["perm"]
        )
        for row in elements
    }
    assert perms == {
        (0, 1, 2, 3),
        (1, 2, 3, 0),
        (2, 3, 0, 1),
        (3, 0, 1, 2),
    }
    assert all(flips == list(range(16)) for flips in flips_by_perm.values())


def test_bt1362_docs_index_card_present() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "BT1362: the Q4 quotient can carry a cyclic axis clock" in text
    assert "BT1362_symmetric_q4_gauge_quotient.md" in text
    assert "C2<sup>4</sup> : C4" in text
    assert "[[32,4,4]]" in text


if __name__ == "__main__":
    test_bt1362_symmetric_quotient_code_parameters()
    test_bt1362_stabilizer_is_affine_cyclic_axis_clock()
    test_bt1362_stabilizer_elements_are_all_translations_times_c4()
    test_bt1362_docs_index_card_present()
    print("BT1362 focused tests passed")
