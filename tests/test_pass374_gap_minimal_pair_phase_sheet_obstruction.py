"""Focused regression for the GAP-owned Pass 374 phase-sheet obstruction."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 374")
def test_pass374_classifies_the_natural_action_and_refutes_a_weyl_torsor() -> None:
    result = subprocess.run(
        [
            GAP,
            "-q",
            str(ROOT / "analysis" / "w33_pass374_minimal_pair_phase_sheet_obstruction.g"),
        ],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert "Pass374 status=PASS" in result.stdout

    certificate = json.loads(
        (
            ROOT
            / "data"
            / "w33_pass374_minimal_pair_phase_sheet_obstruction.json"
        ).read_text(encoding="utf-8")
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 22 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["pairing_space"] == {
        "X_min_vectors": 320,
        "Z_min_vectors": 3240,
        "nonzero_pairs": 51840,
        "phase_counts": {"1": 25920, "2": 25920},
    }
    assert certificate["connected_action"] == {
        "group": "PSp(4,3)",
        "order": 25920,
        "orbit_profile": [12960, 12960, 12960, 12960],
        "stabilizer": "C2",
    }
    assert certificate["group_identification_owner"] == {
        "file": "w33_pass125_two_we6_embeddings.py",
        "result": (
            "the multiplier-2 projective similitude extends PSp(4,3) to "
            "PGSp(4,3) isomorphic to W(E6)"
        ),
        "boundary": (
            "Pass 374 reuses this constructed identification; it does not infer "
            "an isomorphism from order 51840 alone."
        ),
    }
    assert certificate["phase_cover_owners"] == {
        "files": [
            "analysis/bt571_phase_double_cover_algebra.py",
            "analysis/bt637_phase_deck_ij_scalar_lift.py",
            "analysis/bt644_phase_character_commutative_diagram.py",
        ],
        "owned_result": (
            "four F3-star x F3-star lifts over each of 12960 projective "
            "incidences, split 25920+25920 with scalar sign deck involutions"
        ),
        "new_gap": (
            "the orbit and stabilizer classification of the natural signed-chain "
            "PSp(4,3) and PGSp(4,3) actions"
        ),
    }
    assert certificate["full_action"] == {
        "group": "PGSp(4,3)=PSp(4,3):2=W(E6)",
        "order": 51840,
        "orbit_profile": [12960, 12960, 12960, 12960],
        "stabilizer": "C2 x C2",
        "coset_model": "four disjoint copies of W(E6)/(C2 x C2)",
    }
    assert certificate["deck_group"]["group"] == "C2_X x C2_Z"
    assert "not a torsor theorem" in certificate["correction"]
    assert "additional non-geometric phase transport" in certificate["boundary"]

    projective = json.loads(
        (ROOT / "data" / "w33_visible_pair_orbit_weyl_torsor.json").read_text(
            encoding="utf-8"
        )
    )
    assert projective["theorem_name"] == (
        "Visible Pair Projective Orbit and Weyl-Count Lift Theorem"
    )
    assert projective["scalar_action_boundary"] == {
        "owner": "analysis/w33_pass374_minimal_pair_phase_sheet_obstruction.g",
        "full_orbit_profile": [12960, 12960, 12960, 12960],
        "full_stabilizer": "C2 x C2",
        "conclusion": (
            "51840=|W(E6)| is a cardinality identity here, "
            "not a regular-action theorem."
        ),
    }


def test_pass374_is_published_as_an_action_theorem_not_a_reclaimed_cover() -> None:
    synthesis = (
        ROOT / "PASS373_374_W33_BOUNDARY_MLUT_PHASE_SHEET_SYNTHESIS.md"
    ).read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    website = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    for surface in (synthesis, readme, paper, website):
        assert "BT571" in surface
        assert "12960" in surface or "12,960" in surface
        assert "C2" in surface or "C_2" in surface
    assert "unbuilt scalar lift" not in synthesis
    assert "[12960,12960,12960,12960]" in synthesis

    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `[12960,12960,12960,12960]` |" in index
