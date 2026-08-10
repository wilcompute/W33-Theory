#!/usr/bin/env python3
"""Focused direct test for BT867 cache/transport extension boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_bt867_cache_split_transport_nonsplit_boundary() -> None:
    subprocess.run(
        [sys.executable,
         str(ROOT / "analysis/bt867_cache_split_transport_nonsplit_boundary.py")],
        cwd=ROOT,
        check=True,
    )
    data = json.loads(
        (ROOT / "data/bt867_cache_split_transport_nonsplit_boundary.json").read_text(encoding="utf-8")
    )
    assert all(data["checks"].values())
    assert data["parabolic"]["cache_gsets"] == ["H/C4", "H/C4"]
    assert data["shared_81_base"]["base_gset"] == "H/N_H(C4) = H/D8"
    assert data["shared_81_base"]["base_size"] == 81
    assert data["cache_union_commutant"]["group"] == "D8"
    assert data["cache_union_commutant"]["formula"] == (
        "324 = 81 x 4 = 81 x 2_deck x 2_cache"
    )
    assert data["f3_operator_boundary"]["cache_difference_relation"] == (
        "(D-I)^2 = D-I (rank 1)"
    )
    assert data["f3_operator_boundary"]["transport_shift_relation"] == (
        "N^2 = 0 (rank 1)"
    )

    note = (
        ROOT / "analysis/BT867_cache_split_transport_nonsplit_boundary.md"
    ).read_text(encoding="utf-8")
    assert "Cache Addressing Is Split; Transport Memory Is Not" in note
    paper = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    assert "The cache/transport extension boundary" in paper
    assert "324=81\\times4" in paper
    assert "BT867: cache addressing is split" in docs
    assert "H/C<sub>4</sub>" in docs


if __name__ == "__main__":
    test_bt867_cache_split_transport_nonsplit_boundary()
    print("BT867 cache/transport boundary test passed")
