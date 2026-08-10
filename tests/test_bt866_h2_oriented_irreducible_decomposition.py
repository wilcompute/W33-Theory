#!/usr/bin/env python3
"""Focused direct test for BT866 oriented H2 decomposition."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_bt866_h2_oriented_irreducible_decomposition() -> None:
    subprocess.run(
        [sys.executable,
         str(ROOT / "analysis/bt866_h2_oriented_irreducible_decomposition.py")],
        cwd=ROOT,
        check=True,
    )
    data = json.loads(
        (ROOT / "data/bt866_h2_oriented_irreducible_decomposition.json").read_text(encoding="utf-8")
    )
    assert all(data["checks"].values())
    assert data["plain_line_module"]["decomposition_degrees"] == [1, 15, 24]
    assert data["oriented_h2_module"]["decomposition_degrees"] == [5, 5, 30]
    assert data["oriented_h2_module"]["constituent_fields"] == [
        "CF(3)", "CF(3)", "Rationals"
    ]
    assert data["outer_weyl_extension"]["degree_10_extensions_found"] == [10]
    assert data["outer_weyl_extension"]["degree_30_extensions_found"] == [30, 30]
    assert data["homology_dictionary"]["euler_dimension"] == "1 - 81 + 40 = -40"

    note = (
        ROOT / "analysis/BT866_h2_oriented_irreducible_decomposition.md"
    ).read_text(encoding="utf-8")
    assert "5_{\\omega}+5_{\\omega^2}+30" in note
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    assert "The oriented timetable spectrum" in paper
    assert "1-81+(5+5+30)=-40=-v" in paper
    assert "BT866: the oriented timetable carrier" in docs
    assert "5<sub>&omega;</sub>" in docs


if __name__ == "__main__":
    test_bt866_h2_oriented_irreducible_decomposition()
    print("BT866 oriented H2 decomposition test passed")
