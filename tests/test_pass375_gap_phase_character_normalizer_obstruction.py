"""Focused regression for the GAP-owned Pass 375 normalizer obstruction."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 375")
def test_pass375_cuts_the_phase_normalizer_and_excludes_a_split_complement() -> None:
    result = subprocess.run(
        [
            GAP,
            "-q",
            str(
                ROOT
                / "analysis"
                / "w33_pass375_phase_character_normalizer_obstruction.g"
            ),
        ],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert "Pass375 status=PASS" in result.stdout
    assert "Syntax warning" not in result.stdout
    assert "Error," not in result.stdout

    certificate = json.loads(
        (
            ROOT
            / "data"
            / "w33_pass375_phase_character_normalizer_obstruction.json"
        ).read_text(encoding="utf-8")
    )
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == 29 == len(certificate["checks"])
    assert all(certificate["checks"].values())
    assert certificate["scalar_fibre"] == {
        "group": "D=C2_X x C2_Z=(F3*)^2",
        "order": 4,
        "phase_character": "chi(a,b)=ab",
        "phase_blocks": [[1, 2], [3, 4]],
        "Aut_D": "S3",
        "Aut_D_stabilizer_of_ker_chi": "C2",
    }
    assert certificate["abstract_extensions"] == {
        "D_semidirect_C3": "A4",
        "D_semidirect_S3": "S4",
        "D_direct_C3": "C6 x C2",
        "boundary": (
            "the order-three automorphism cycles all three nonzero character "
            "kernels and cannot preserve the owned chi partition"
        ),
    }
    assert certificate["phase_partition_normalizer"] == {
        "unrestricted": "S4",
        "partition_setwise": "D8",
        "order": 8,
        "deck_quotient": "C2",
        "contains_order_3": False,
    }
    assert certificate["actual_pass374_stabilizer"] == {
        "connected_projective_order": 2,
        "full_group": "W(E6)=PGSp(4,3)",
        "K": "C2 x C2",
        "K_order": 4,
        "normalizer_order": 32,
        "normalizer_structure": "(C2 x C2 x C2 x C2) : C2",
        "normalizer_quotient": "D8",
        "identification_boundary": (
            "the phase-sheet D8 and N_W(E6)(K)/K are isomorphic outputs on "
            "different objects; no intertwiner is claimed"
        ),
    }
    assert certificate["subgroup_class_count"] == 350
    obstruction = certificate["regular_complement_obstruction"]
    assert obstruction["split_group"] == "W(E6) x D"
    assert obstruction["split_order"] == 207360
    assert obstruction["point_stabilizer"] == "embedded K=C2 x C2"
    assert obstruction["coset_state_count"] == 51840
    assert obstruction["target_regular_order"] == 51840
    assert obstruction["forced_projection_kernel_order"] == 12960
    assert obstruction["W_E6_has_order_12960_subgroup"] is False
    assert obstruction["W_E6_has_order_6480_subgroup"] is False
    assert "ker(R->D)" in obstruction["proof"]
    assert "PSp(4,3) is simple" in obstruction["independent_reason"]

    pass374 = json.loads(
        (
            ROOT
            / "data"
            / "w33_pass374_minimal_pair_phase_sheet_obstruction.json"
        ).read_text(encoding="utf-8")
    )
    assert pass374["full_action"]["orbit_profile"] == [12960] * 4
    assert pass374["full_action"]["stabilizer"] == "C2 x C2"
    assert pass374["connected_action"]["stabilizer"] == "C2"
    assert pass374["deck_group"]["group"] == "C2_X x C2_Z"


def test_pass375_synthesis_preserves_object_ownership_boundaries() -> None:
    synthesis = (
        ROOT / "PASS375_W33_PHASE_CHARACTER_NORMALIZER_OBSTRUCTION.md"
    ).read_text(encoding="utf-8")

    for owner in ("BT571", "BT637", "BT644", "BT1480", "BT783", "Pass 214"):
        assert owner in synthesis
    for result in ("D_8", "12{,}960", "207{,}360", "51{,}840"):
        assert result in synthesis
    assert "no intertwiner is claimed" in synthesis.lower()
    assert "does not preserve" in synthesis
    assert "not a torsor" in synthesis


def test_pass375_is_published_on_all_requested_surfaces() -> None:
    surfaces = {
        "README": (ROOT / "README.md").read_text(encoding="utf-8"),
        "paper": (ROOT / "w33_paper.tex").read_text(encoding="utf-8"),
        "photonic": (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8"),
        "practical": (ROOT / "holonet_practical_implications.tex").read_text(
            encoding="utf-8"
        ),
        "website": (ROOT / "docs" / "index.html").read_text(encoding="utf-8"),
    }
    for name, surface in surfaces.items():
        assert "Pass 375" in surface or "Pass~375" in surface, name
        assert "D8" in surface or "D_8" in surface, name
        assert "regular" in surface.lower(), name

    index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    assert "| `207360` | `PASS375_W33_PHASE_CHARACTER_NORMALIZER_OBSTRUCTION.md` |" in index
