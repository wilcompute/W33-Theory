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


def test_bt1403_hesse_port_eraser_lift_runs_true() -> None:
    out = run_tool("tools/bt1403_hesse_port_eraser_lift.py")
    assert out["bt"] == 1403
    assert out["verified"] is True
    assert out["sic_outcomes"] == 9
    assert out["preview_pdf_built"] is True

    data = json.loads(
        (ROOT / "data" / "bt1403_hesse_port_eraser_lift.json").read_text(
            encoding="utf-8"
        )
    )
    assert data["verified"] is True
    assert (
        data["eraser_lift"]["factorization"] == "9 = 3 route branches * 3 phase labels"
    )
    assert len(data["eraser_lift"]["grid"]) == 9
    assert data["eraser_lift"]["grid"][0]["pauli_correction"] == "X^0 Z^0"
    assert data["eraser_lift"]["grid"][-1]["pauli_correction"] == "X^2 Z^2"
    assert data["preview_pdf"]["path"] == "photonic_holonet_BT1403_preview.pdf"
    assert data["preview_pdf"]["bytes"] > 100_000


def test_bt1403_manuscript_and_docs_anchors() -> None:
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )
    single_photon = " ".join(
        (ROOT / "single_photon_universal_computation.tex")
        .read_text(encoding="utf-8")
        .split()
    )
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())

    assert "BT1403 eraser-lift port" in holonet
    assert "Hesse port is not a second computer" in holonet
    assert (
        "nine Hesse outcomes are exactly 3 route branches times 3 phase labels"
        in holonet
    )
    assert "BT1403 eraser-lift port" in single_photon
    assert "non-Clifford port is a lift of the eraser measurement" in single_photon
    assert "BT1403: Hesse port as eraser lift" in docs


def test_bt1403_preview_pdf_has_distinct_name() -> None:
    pdf = ROOT / "photonic_holonet_BT1403_preview.pdf"
    assert pdf.exists()
    assert pdf.name != "photonic_holonet.pdf"
    assert pdf.stat().st_size > 100_000


if __name__ == "__main__":
    test_bt1403_hesse_port_eraser_lift_runs_true()
    test_bt1403_manuscript_and_docs_anchors()
    test_bt1403_preview_pdf_has_distinct_name()
    print("BT1403 focused tests passed")
