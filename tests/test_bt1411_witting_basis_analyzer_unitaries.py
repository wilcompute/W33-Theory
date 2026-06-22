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
            str(ROOT / "tools" / "bt1411_witting_basis_analyzer_unitaries.py"),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_result() -> dict:
    return json.loads(
        (ROOT / "data" / "bt1411_witting_basis_analyzer_unitaries.json").read_text(
            encoding="utf-8"
        )
    )


def test_bt1411_analyzer_compiler_runs_true() -> None:
    out = run_tool()
    assert out == {
        "bt": 1411,
        "families": {
            "COMPUTATIONAL_DIRECT_RAILS": 1,
            "FOUR_THREE_RAIL_WITTING_ROWS": 27,
            "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER": 12,
        },
        "max_nonzero_entries": 12,
        "verified": True,
    }

    data = load_result()
    assert data["verified"] is True
    assert all(data["checks"].values())


def test_bt1411_unitary_and_sparse_histograms() -> None:
    data = load_result()

    assert data["histograms"]["optical_family"] == {
        "COMPUTATIONAL_DIRECT_RAILS": 1,
        "FOUR_THREE_RAIL_WITTING_ROWS": 27,
        "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER": 12,
    }
    assert data["histograms"]["support_profile"] == {
        "1,1,1,1": 1,
        "1,3,3,3": 12,
        "3,3,3,3": 27,
    }
    assert data["histograms"]["nonzero_entries"] == {"4": 1, "10": 12, "12": 27}
    assert data["error_bounds"]["max_unitarity_error"] < 1e-10
    assert data["error_bounds"]["max_slot_error"] < 1e-10


def test_bt1411_phase_alphabet_and_samples() -> None:
    data = load_result()

    assert set(data["histograms"]["entry_tokens"]) == {
        "0",
        "1",
        "1/sqrt3",
        "-1/sqrt3",
        "omega/sqrt3",
        "omega2/sqrt3",
        "-omega/sqrt3",
        "-omega2/sqrt3",
    }

    samples = data["sample_analyzers"]
    assert samples["basis_0_computational"]["optical_family"] == (
        "COMPUTATIONAL_DIRECT_RAILS"
    )
    assert samples["basis_0_computational"]["nonzero_entries"] == 4
    assert samples["basis_1_one_direct_rail"]["optical_family"] == (
        "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER"
    )
    assert samples["basis_1_one_direct_rail"]["nonzero_entries"] == 10
    assert samples["basis_13_contextual"]["optical_family"] == (
        "FOUR_THREE_RAIL_WITTING_ROWS"
    )
    assert samples["basis_13_contextual"]["nonzero_entries"] == 12


def test_bt1411_hardware_interface_and_publication_anchors() -> None:
    data = load_result()
    handoff = data["hardware_interface"]
    assert handoff["detector_slots"] == [0, 1, 2, 3]
    assert "mirror_slot mod 4" in handoff["bt1374_slot_rule"]
    assert handoff["bt1410_basis_local_records"] == 640

    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )

    assert "BT1411: Witting basis analyzer unitaries" in docs
    assert "BT1411_witting_basis_analyzer_unitaries.md" in docs
    assert "BT1411 Witting basis analyzer unitaries" in holonet
    assert "one computational direct-rail analyzer" in holonet
    assert "twelve one-direct-rail plus complement-tritter analyzers" in holonet
    assert "twenty-seven four-three-rail contextual analyzers" in holonet


if __name__ == "__main__":
    test_bt1411_analyzer_compiler_runs_true()
    test_bt1411_unitary_and_sparse_histograms()
    test_bt1411_phase_alphabet_and_samples()
    test_bt1411_hardware_interface_and_publication_anchors()
    print("BT1411 focused tests passed")
