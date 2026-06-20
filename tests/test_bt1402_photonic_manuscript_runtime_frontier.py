#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(path: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def test_bt1402_manuscript_frontier_runs_true() -> None:
    out = run_tool("tools/bt1402_photonic_manuscript_runtime_frontier.py")
    assert out["bt"] == 1402
    assert out["verified"] is True
    assert out["baseline_gamma"] > 0.9
    assert out["maxsat_status"] == "witness_only"

    data = json.loads(
        (ROOT / "data" / "bt1402_photonic_manuscript_runtime_frontier.json").read_text(
            encoding="utf-8"
        )
    )
    assert data["verified"] is True
    assert (
        abs(data["frontier_contract"]["single_photon_demonstrator"]["V(F3)"] - 1 / 3)
        < 1e-12
    )
    assert (
        data["frontier_contract"]["quantum_eraser_readout"]["conditional_l1_coherence"]
        == 2.0
    )
    assert data["frontier_contract"]["hesse_sic_t_port"]["sic_outcomes"] == 9
    assert data["frontier_contract"]["s3_maxsat_boundary"]["computed_score"] == 210


def test_bt1402_manuscript_surfaces_have_expected_anchors() -> None:
    holonet = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    single_photon = (ROOT / "single_photon_universal_computation.tex").read_text(
        encoding="utf-8"
    )
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    holonet_norm = " ".join(holonet.split())
    single_photon_norm = " ".join(single_photon.split())

    assert "BT1402 runtime-frontier handoff" in holonet_norm
    assert "Hesse-SIC/T token has nine outcomes" in holonet_norm
    assert "MaxSAT frontier remains witness-only" in holonet_norm
    assert "BT1402 Runtime-Frontier Handoff" in single_photon_norm
    assert "route register is maximally mixed before the eraser" in single_photon_norm
    assert "Hesse-SIC/T port consumes one nine-outcome SIC token" in single_photon_norm
    assert "BT1402: manuscript runtime-frontier handoff" in docs


def test_bt1402_release_lock_includes_frontier_guard() -> None:
    runner = (ROOT / "tools" / "bt1389_run_runtime_frontier_release_lock.sh").read_text(
        encoding="utf-8"
    )
    assert "tools/bt1402_photonic_manuscript_runtime_frontier.py" in runner
    assert "tests/test_bt1402_photonic_manuscript_runtime_frontier.py" in runner
    assert "BT1402 runtime frontier release lock passed" in runner


if __name__ == "__main__":
    test_bt1402_manuscript_frontier_runs_true()
    test_bt1402_manuscript_surfaces_have_expected_anchors()
    test_bt1402_release_lock_includes_frontier_guard()
    print("BT1402 focused tests passed")
