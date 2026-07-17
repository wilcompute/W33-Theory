"""Focused regression for the GAP-owned Pass 376 marked D8 bridge."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 376")
def test_pass376_constructs_the_marked_d8_bridge_without_a_sheet_overread() -> None:
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / "w33_pass376_marked_d8_bridge.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert "Pass376 status=PASS" in result.stdout

    certificate = json.loads(
        (ROOT / "data" / "w33_pass376_marked_d8_bridge.json").read_text(
            encoding="utf-8"
        )
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 20 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["phase_side"] == {
        "group": "D8",
        "deck": "V4=(F3*)^2",
        "phase_kernel": "ker chi = Z(D8)",
        "quotient": "C2",
        "deck_conjugation_orbits": [1, 1, 2],
    }
    assert certificate["geometric_side"] == {
        "group": "N_W(E6)(K)/K",
        "group_order": 8,
        "deck": "C_N(K)/K",
        "deck_order": 4,
        "normalizer_order": 32,
        "quotient": "C2",
        "deck_conjugation_orbits": [1, 1, 2],
    }
    assert certificate["marked_bridge"] == {
        "exists": True,
        "maps_phase_deck_to_geometric_deck": True,
        "maps_center_to_center": True,
        "marked_isomorphism_count": 4,
        "ambiguity_group": "C2 x C2",
    }
    assert certificate["search_signature"] == "32/8/4/2/1/1/2/4"
    assert "does not identify scalar sheets with geometric states" in certificate[
        "prior_boundary"
    ]
    assert "no preferred scalar-sheet-to-state map" in certificate["scope"]


def test_pass376_synthesis_and_public_surfaces_keep_the_fourfold_boundary() -> None:
    synthesis = (ROOT / "PASS376_MARKED_D8_BRIDGE.md").read_text(encoding="utf-8")
    for surface in (
        synthesis,
        (ROOT / "README.md").read_text(encoding="utf-8"),
        (ROOT / "w33_paper.tex").read_text(encoding="utf-8"),
        (ROOT / "docs" / "index.html").read_text(encoding="utf-8"),
    ):
        assert "Pass 376" in surface or "Pass~376" in surface
        assert (
            "C_N(K)/K" in surface
            or "C_{N}(K)/K" in surface
            or "C<sub>N</sub>(K)/K" in surface
        )
        assert "four" in surface.lower()

    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `32/8/4/2/1/1/2/4` |" in index
