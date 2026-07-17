"""Focused regression for the GAP-owned Pass 379 Q6 geometry boundary."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 379")
def test_pass379_proves_the_header_clock_is_not_a_q6_edge_symmetry() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass379_header_q6_geometry_boundary.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Pass379 status=PASS" in result.stdout
    assert "q6_adjacent=960 preserved=146" in result.stdout.replace("\n", "")

    certificate = json.loads(
        (ROOT / "data" / "w33_pass379_header_q6_geometry_boundary.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 11 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["header_clock"] == {
        "shift": "flag -> flag+64 mod 192",
        "group": "C3",
        "full_bus_cycles": 64,
        "pass377_subclock": "48=16*3",
    }
    assert certificate["q6_adjacency"] == {
        "adjacent_edge_pairs": 960,
        "preserved_by_header_shift": 146,
        "lost": 814,
        "false_positives": 814,
    }
    assert certificate["first_adjacency_failure"] == {
        "source_flags": [0, 8],
        "shifted_flags": [64, 72],
    }
    assert "not a Q6 line-graph automorphism" in certificate["conclusion"]
    assert certificate["search_signature"] == "192/64x3/960/geometry-boundary"


def test_pass379_witness_remains_pinned_to_the_live_bt1371_address_table() -> None:
    table = json.loads(
        (
            ROOT / "data" / "bt1371_q6_tomotope_explicit_orbit_address_table.json"
        ).read_text(encoding="utf-8")
    )["address_table"]
    by_flag = {row["tomotope_flag"]: row for row in table}
    assert {
        flag: (by_flag[flag]["q6_endpoint_a"], by_flag[flag]["q6_endpoint_b"])
        for flag in (0, 8, 64, 72)
    } == {
        0: ("000000", "000001"),
        8: ("000001", "001001"),
        64: ("011111", "111111"),
        72: ("010101", "010111"),
    }


def test_pass379_public_surfaces_keep_the_geometry_boundary_searchable() -> None:
    synthesis = (ROOT / "PASS379_HEADER_Q6_GEOMETRY_BOUNDARY.md").read_text(
        encoding="utf-8"
    )
    assert "960" in synthesis
    assert "146" in synthesis
    assert "not a Q6 geometry operation" in synthesis

    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `192/64x3/960/geometry-boundary` |" in index
