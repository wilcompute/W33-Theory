"""Focused regression for the GAP-owned Pass 377 binary-switch header clock."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 377")
def test_pass377_constructs_the_binary_q3_switch_header_clock() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass377_binary_q3_switch_header.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass377 status=PASS" in result.stdout

    certificate = json.loads(
        (ROOT / "data" / "w33_pass377_binary_q3_switch_header.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 13 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["source_model"] == {
        "address_labels": 40,
        "binary_q3_blocks": 5,
        "q3_coordinates": 3,
        "depth_residues": 3,
        "directed_one_axis_toggles": 360,
    }
    assert certificate["header_map"] == {
        "formula": "flag=4*((16*depth+3*source+target) mod 48)+(target mod 4)",
        "flag_bus": 192,
        "image_size": 48,
        "axis_supports": [24, 12, 12],
        "axis_fibers": [5, 10, 10],
        "combined_fiber_profile": {"5": 24, "10": 24},
    }
    assert certificate["clock"] == {
        "depth_step": "flag -> flag+64 mod 192",
        "group": "C3",
        "free_flag_cycles": 16,
        "axis_cycle_profile": [8, 4, 4],
        "identity": "48=16*3",
    }
    assert certificate["search_signature"] == "360/48/24/12/12/5/10/16x3"
    assert "does not identify a binary Q3 toggle with a Q6 edge traversal" in certificate[
        "scope"
    ]


def test_pass377_public_surfaces_keep_the_header_not_intertwiner_boundary() -> None:
    synthesis = (ROOT / "PASS377_BINARY_Q3_SWITCH_HEADER.md").read_text(
        encoding="utf-8"
    )
    for surface in (
        synthesis,
        (ROOT / "README.md").read_text(encoding="utf-8"),
        (ROOT / "docs" / "index.html").read_text(encoding="utf-8"),
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8"),
    ):
        assert "Pass 377" in surface or "Pass~377" in surface
        assert "48" in surface
        assert "C3" in surface or "C_3" in surface
        assert "Q6" in surface

    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `360/48/24/12/12/5/10/16x3` |" in index
