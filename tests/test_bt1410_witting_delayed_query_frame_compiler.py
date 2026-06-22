#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool() -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "bt1410_witting_delayed_query_frame_compiler.py"),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_result() -> dict:
    return json.loads(
        (ROOT / "data" / "bt1410_witting_delayed_query_frame_compiler.json").read_text(
            encoding="utf-8"
        )
    )


def test_bt1410_compiler_runs_true() -> None:
    out = run_tool()
    assert out == {
        "basis_local_records": 640,
        "bt": 1410,
        "off_diagonal_data_records": 480,
        "same_ray_witness_records": 160,
        "verified": True,
    }

    data = load_result()
    assert data["verified"] is True
    assert all(data["checks"].values())


def test_bt1410_logical_and_physical_tables() -> None:
    data = load_result()

    assert data["logical_pair_table"] == {
        "accept_rate": "13/40",
        "accepted_ordered_pairs": 520,
        "mode_histogram": {
            "COMPATIBLE_UNIQUE_BASIS": 480,
            "INCOMPATIBLE_RETRY_SHADOW": 1080,
            "SAME_RAY_FOUR_BASIS_APERTURE": 40,
        },
        "records": 1600,
        "reject_rate": "27/40",
        "rejected_ordered_pairs": 1080,
    }
    assert data["basis_local_frame_table"] == {
        "basis_tile_histogram": {"16": 40},
        "factorization": "40 tetrads * 4 Alice query slots * 4 Bob query slots",
        "mode_histogram": {
            "DIAGONAL_WITNESS_APERTURE": 160,
            "OFF_DIAGONAL_DATA_HANDSHAKE": 480,
        },
        "reading": (
            "The physical table is larger than the logical accepted-pair "
            "table only because same-ray queries are contextual apertures: "
            "each ray lives in four bases."
        ),
        "records": 640,
        "same_ray_extra_context_options": 120,
    }


def test_bt1410_sample_compilations_and_handoff() -> None:
    data = load_result()

    distinct = data["sample_compilations"]["distinct_compatible"]
    assert distinct["mode"] == "COMPATIBLE_UNIQUE_BASIS"
    assert len(distinct["basis_options"]) == 1
    assert distinct["selected_basis"] == distinct["basis_options"][0]
    assert distinct["alice_query_slot"] != distinct["bob_query_slot"]

    same = data["sample_compilations"]["same_ray"]
    assert same["mode"] == "SAME_RAY_FOUR_BASIS_APERTURE"
    assert len(same["basis_options"]) == 4
    assert same["aperture_selector_domain"] == [0, 1, 2, 3]
    assert same["selected_basis_if_selector_is_0"] == same["basis_options"][0]
    assert len(same["query_slot_in_each_basis"]) == 4

    handoff = data["holonet_transaction"]
    assert handoff["bt1407_frame_ticks"] == 72
    assert handoff["basis_local_table_factorization"] == "40*4*4=640"
    assert handoff["outcome_slot_residue_domain"] == [0, 1, 2, 3]
    assert "mirror_slot mod 4" in handoff["bt1374_address_rule"]


def test_bt1410_publication_anchors() -> None:
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )

    assert "BT1410: Witting delayed-query frame compiler" in docs
    assert "BT1410_witting_delayed_query_frame_compiler.md" in docs
    assert "BT1410 Witting delayed-query frame compiler" in holonet
    assert "40$ tetrads times $4$ Alice slots times $4$ Bob slots" in holonet
    assert "160\\ \\text{diagonal witness records}" in holonet
    assert "480\\ \\text{off-diagonal data records}" in holonet
    assert "the Witting desk is now a packet admission ROM" in holonet


if __name__ == "__main__":
    test_bt1410_compiler_runs_true()
    test_bt1410_logical_and_physical_tables()
    test_bt1410_sample_compilations_and_handoff()
    test_bt1410_publication_anchors()
    print("BT1410 focused tests passed")
