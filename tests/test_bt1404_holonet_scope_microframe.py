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


def test_bt1404_scope_microframe_runs_true() -> None:
    out = run_tool("tools/bt1404_holonet_scope_microframe.py")
    assert out["bt"] == 1404
    assert out["verified"] is True
    assert out["scope_ticks"] == 72
    assert out["html"] == "docs/bt1404_holonet_scope.html"

    data = json.loads(
        (ROOT / "data" / "bt1404_holonet_scope_microframe.json").read_text(
            encoding="utf-8"
        )
    )
    assert data["verified"] is True
    assert data["scope_identity"] == (
        "9 Hesse outcomes * 8 packet ticks = 72 ticks = one microframe"
    )
    assert data["timing"]["hesse_outcomes"] == 9
    assert data["timing"]["word_ticks"] == 8
    assert data["timing"]["microframe_ticks"] == 72
    assert data["timing"]["microframes_per_clifford_window"] == 720

    frames = data["frames"]
    assert [frame["h"] for frame in frames] == list(range(9))
    assert {len(frame["packet_word"]) for frame in frames} == {8}
    assert sorted(
        tick["microframe_tick"] for frame in frames for tick in frame["packet_word"]
    ) == list(range(72))
    assert {frame["pauli_correction"] for frame in frames} >= {
        "X^0 Z^0",
        "X^1 Z^1",
        "X^2 Z^2",
    }
    assert all(frame["t_frame_bit"] == frame["h"] % 2 for frame in frames)


def test_bt1404_html_scope_surface() -> None:
    html = (ROOT / "docs" / "bt1404_holonet_scope.html").read_text(encoding="utf-8")
    assert "BT1404 Holonet Scope" in html
    assert "9 Hesse outcomes x 8 packet ticks = 72 ticks" in html
    assert "scope-data" in html
    assert "Hesse Outcome Grid" in html
    assert "8-Tick Return Word" in html
    assert "docs/bt1404_holonet_scope.html" in html


def test_bt1404_publication_anchors() -> None:
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )
    single_photon = " ".join(
        (ROOT / "single_photon_universal_computation.tex")
        .read_text(encoding="utf-8")
        .split()
    )
    assert "BT1404: holonet scope microframe" in docs
    assert "bt1404_holonet_scope.html" in docs
    assert "BT1404 holonet scope" in holonet
    assert "9 Hesse outcomes times 8 packet ticks" in holonet
    assert "BT1404 Holonet Scope" in single_photon


if __name__ == "__main__":
    test_bt1404_scope_microframe_runs_true()
    test_bt1404_html_scope_surface()
    test_bt1404_publication_anchors()
    print("BT1404 focused tests passed")
