"""Regression tests for the GAP-owned Pass 540 certificate."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass540_symplectic_separator_chainring.g"
CERTIFICATE = ROOT / "data" / "w33_pass540_symplectic_separator_chainring.json"
GAP = shutil.which("gap")
pytestmark = pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 540")


@lru_cache(maxsize=1)
def _certificate() -> dict:
    """Run GAP once; Python only checks and parses its deterministic output."""

    assert GAP is not None, "GAP is required for the Pass 540 certificate"
    before = CERTIFICATE.read_bytes()
    result = subprocess.run(
        [GAP, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert "Pass 540: PASS (53/53)" in result.stdout
    assert CERTIFICATE.read_bytes() == before
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_q3_merge_is_the_two_d4_chiralities() -> None:
    cert = _certificate()
    q3 = cert["q3"]
    assert cert["status"] == "PASS"
    assert q3["group_order"] == 24
    assert q3["orbit_count"] == 7
    assert q3["full_support_orbit_representatives"] == [
        [1, 1, 1, 1],
        [1, 1, 1, 2],
    ]
    assert q3["coordinate_products"] == [1, 2]
    assert q3["orientation_kappa"] == 1
    assert q3["reoriented_first_pair_kappa"] == 2
    assert q3["reoriented_first_orbit_coordinate_product"] == 2
    assert q3["moore_dickson_scalar"] == 1
    assert q3["lex_ordered_six_bracket_scalar"] == 1
    assert q3["full_support_orbits_by_product"] == [[0, 0], [1, 1], [2, 1]]
    assert q3["stabiliser_sizes"] == [3, 3]
    assert q3["projective_permutation_image_order"] == 12
    assert q3["shared_characteristic_polynomial"] == "x_1^3-36*x_1-81"


def test_q5_full_support_burnside_and_further_genuine_collision() -> None:
    q5 = _certificate()["q5"]
    assert q5["all_full_support_sections"] == 16_777_216
    assert q5["all_full_support_orbits_exact"] == 139_904
    assert q5["full_support_orbits_by_coordinate_product"] == [
        [0, 0],
        [1, 34_976],
        [2, 34_976],
        [3, 34_976],
        [4, 34_976],
    ]
    assert q5["full_support_orbits_sampled"] == 3_000
    assert q5["distinct_charpolys"] == 2_966
    assert q5["sample_orbit_merges"] == 34
    assert q5["zero_offset_GL_equivalent_merge_classes"] == 33
    assert q5["shift_required_affine_equivalent_merge_classes"] == 0
    assert q5["affine_inequivalent_merge_classes"] == 1

    merge = q5["affine_inequivalent_merge"]
    assert merge["same_affine_pair_as_pass456"] is False
    assert merge["outside_eight_explicit_pre540_affine_pairs"] is True
    assert merge["mechanism"] == "sheet coincidence (Pass 481 mechanism)"
    assert merge["section_a"] == [1, 1, 2, 2, 2, 3, 3, 2, 3, 2, 3, 2]
    assert merge["section_b"] == [1, 1, 2, 2, 3, 3, 3, 3, 2, 3, 2, 2]
    assert merge["feature_a"][0] == 4
    assert merge["feature_b"][0] == 1
    assert (
        merge["nonneighbor_common_neighbor_profiles"][0]
        != merge["nonneighbor_common_neighbor_profiles"][1]
    )
    assert merge["nonneighbor_common_neighbor_profiles"] == [
        [[0, 6], [2, 10], [3, 16], [4, 24], [5, 20], [6, 14], [7, 8], [8, 2]],
        [[0, 4], [2, 14], [3, 16], [4, 24], [5, 20], [6, 10], [7, 8], [8, 4]],
    ]
    assert merge["nonunit_smith_invariant_factors"] == [
        [[5, 16], [25, 5], [125, 13], [2_028_949_923_625, 10]],
        [[5, 16], [25, 5], [125, 13], [2_028_949_923_625, 10]],
    ]
    assert merge["faithful_degree10_rational_factor"] == (
        "x_1^10-120*x_1^8-90*x_1^7+4795*x_1^6+6317*x_1^5"
        "-69675*x_1^4-108795*x_1^3+277460*x_1^2+383845*x_1+34441"
    )


def test_z9_signed_burnside_and_shell_refinement_are_exact() -> None:
    z9 = _certificate()["z9_burnside"]
    assert z9["group"] == "SL(2,Z/9Z)"
    assert z9["group_order"] == 648
    assert z9["antipodal_pairs"] == 40
    assert z9["sections"] == "147808829414345923316083210206383297601"
    assert z9["orbits"] == "228100045392509153077600971330057241"
    assert z9["full_support_orbits"] == ("2051277771273019233341050472890368")
    assert z9["deep_shell_orbits"] == 301
    assert z9["primitive_deep_joint_cycle_profile"] == [
        [0, 0, 405],
        [6, 2, 72],
        [8, 2, 72],
        [12, 2, 72],
        [12, 4, 18],
        [18, 4, 8],
        [36, 4, 1],
    ]


def test_all_gap_checks_pass_and_boundaries_are_explicit() -> None:
    cert = _certificate()
    assert len(cert["checks"]) == 53
    assert all(cert["checks"].values())
    assert "q5 full-support Burnside count are exhaustive" in cert["boundary"]
    assert "Only the q5 spectral search" in cert["boundary"]
    assert "139,904 full-support orbits" in cert["q5"]["boundary"]
    assert "does not estimate the full image cardinality" in cert["q5"]["boundary"]
