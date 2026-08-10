#!/usr/bin/env python3
"""Focused direct test for BT859 Bell-compass parabolic routing."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_bt859_bell_compass_parabolic_router() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "analysis/bt859_bell_compass_parabolic_router.py")],
        cwd=ROOT,
        check=True,
    )
    data = json.loads(
        (ROOT / "data/bt859_bell_compass_parabolic_router.json").read_text(encoding="utf-8")
    )
    assert all(data["checks"].values())
    assert data["gap"]["line_projective_orbits"] == [162, 162, 324, 648]
    assert data["gap"]["line_full_orbits"] == [324, 324, 648]
    assert data["gap"]["point_projective_orbits"] == [648, 648]
    assert data["gap"]["point_full_orbits"] == [648, 648]
    assert data["kraft_sum"] == "1"
    assert {
        row["word"] for row in data["prefix_decoder"].values()
    } == {"0", "10", "110", "111"}
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    assert "Bell--compass parabolic router" in paper
    assert "162_L+162_R+324+648" in paper
    assert "BT857 and BT859" in docs
    assert "address sheet" in docs


if __name__ == "__main__":
    test_bt859_bell_compass_parabolic_router()
    print("BT859 Bell-compass parabolic router test passed")
