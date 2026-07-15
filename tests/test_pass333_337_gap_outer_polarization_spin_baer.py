"""Focused live-GAP tests for the Pass 333--337 breakthrough packet."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = {
    333: ROOT / "analysis" / "w33_pass333_outer_s3_lift.g",
    334: ROOT / "analysis" / "w33_pass334_selector_leaf_bundle_obstruction.g",
    335: ROOT / "analysis" / "w33_pass335_complete_stable_lattice_complex.g",
    336: ROOT / "analysis" / "w33_pass336_integral_halfspin_lattices.g",
    337: ROOT / "analysis" / "w33_pass337_epsilon_e8_baer_separation.g",
}
CERTIFICATES = {
    number: next((ROOT / "data").glob(f"w33_pass{number}_*.json"))
    for number in SCRIPTS
}


@lru_cache(maxsize=None)
def _certificate(number: int) -> dict:
    """Run the owning GAP witness; Python only parses its certificate."""

    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Passes 333--337"
    result = subprocess.run(
        [gap, "-q", str(SCRIPTS[number])],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert "PASS" in result.stdout
    certificate = json.loads(CERTIFICATES[number].read_text(encoding="utf-8"))
    assert certificate["status"] == "PASS"
    assert certificate["check_count"] == len(certificate["checks"])
    assert all(certificate["checks"].values())
    return certificate


def test_pass333_outer_reflection_closes_the_integral_s3_lift() -> None:
    cert = _certificate(333)
    group = cert["group_ledger"]
    leaves = cert["lattice_leaf_ledger"]
    reflections = cert["reflection_family"]
    assert cert["check_count"] == 29
    assert group["inner_order"] == 25_920
    assert group["outer_order"] == 51_840
    assert group["omega_T_group"] == "S3, order 6"
    assert group["relation"] == "T^-1*omega*T=omega^-1"
    assert leaves["omega_permutation"] == [3, 1, 2]
    assert leaves["T_permutation"] == [1, 3, 2]
    assert leaves["T_leaf_map_determinants"] == [-1, -1, -1]
    assert len(reflections["unit_pairs"]) == 6
    assert sorted(reflections["leaf_permutations"]) == sorted(
        [[1, 3, 2], [1, 3, 2], [2, 1, 3], [2, 1, 3], [3, 2, 1], [3, 2, 1]]
    )


def test_pass334_selector_is_twisted_not_the_flat_leaf_product() -> None:
    cert = _certificate(334)
    actual = cert["actual_selector_bundle"]
    flat = cert["pass332_leaf_product"]
    holonomy = cert["overlap_and_holonomy"]
    assert cert["check_count"] == cert["passed_check_count"] == 20
    assert actual["indices_GK_KH_GH"] == [40, 3, 120]
    assert actual["orbits"] == [120]
    assert actual["fibre_action"] == "S3"
    assert actual["equivariant_deck_centralizer_order"] == 1
    assert flat["natural_product_orbits"] == [40, 40, 40]
    assert flat["psp_generator_leaf_actions"] == [[1, 2, 3], [1, 2, 3]]
    assert holonomy["selector_holonomy_order_profile"] == [
        [1, 11_070],
        [2, 29_160],
        [3, 19_440],
    ]
    assert holonomy["flat_product_holonomy_order_profile"] == [[1, 59_670]]


def test_pass335_complete_complex_has_symplectic_but_not_quadratic_lift() -> None:
    cert = _certificate(335)
    complex_ = cert["stable_lattice_complex"]
    polar = cert["symplectic_polar_lift"]
    obstruction = cert["quadratic_lattice_obstruction"]
    assert cert["check_count"] == 33
    assert complex_["homothety_class_count"] == 5
    assert complex_["index_two_skeleton"].startswith("K(2,3)")
    assert complex_["triangles"] == [
        ["L", "R", "L1"],
        ["L", "R", "L2"],
        ["L", "R", "L3"],
    ]
    assert polar["primitive_determinants"] == [1, 1, 1]
    assert polar["mod2_ranks"] == [10, 10, 10]
    assert polar["quadratic_refinements_per_leaf"] == 2
    assert "both plus type" in polar["refinement_types"]
    assert obstruction["H10_symmetric_determinants"] == [243, 243, 243]
    assert obstruction["rank10_even_plus_determinant_unit_mod8"] == 7
    assert obstruction["rational_symmetric_discriminant_unit_mod8"] == 3


def test_pass336_integral_halfspins_are_perfect_two_adic_duals() -> None:
    cert = _certificate(336)
    spin = cert["integral_halfspins"]
    pairing = cert["wedge_pairing"]
    boundary = cert["leaf_attachment_boundary"]
    assert cert["check_count"] == 22
    assert spin["ranks"] == [32, 32]
    assert spin["composition_factors_mod2"] == [[1, 4], [6, 2], [8, 2]]
    assert spin["Hom_mod2_dimension"] == 12
    assert 32 not in spin["Hom_mod2_rank_spectrum"]
    assert pairing["Smith_diagonal"] == [1] * 16 + [3] * 16
    assert pairing["determinant"] == 3**16
    assert pairing["rank_mod2"] == 32
    assert boundary["leaf_determinants"] == [243, 243, 243]
    assert boundary["odd_diagonal_weights_mod2"] == [5, 5, 5]


def test_pass337_epsilon_and_signed_e8_are_different_baer_classes() -> None:
    cert = _certificate(337)
    module = cert["H10_module_extension"]
    epsilon = cert["epsilon_group_extension"]
    signed = cert["signed_E8_group_extension"]
    assert cert["check_count"] == 20
    assert module["submodule_dimensions"] == [0, 1, 9, 10]
    assert "image=socle" in module["epsilon"]
    assert epsilon["order"] == signed["order"] == 103_680
    assert epsilon["derived_order"] == 25_920
    assert signed["derived_order"] == 51_840
    assert epsilon["abelian_invariants"] == [2, 2]
    assert signed["abelian_invariants"] == [2]
    assert epsilon["Baer_class"].startswith("zero/split")
    assert signed["Baer_class"].startswith("nonzero/nonsplit")
    assert cert["comparison"]["isomorphic"] is False


def test_packet_is_visible_on_all_shared_theory_surfaces() -> None:
    synthesis = " ".join(
        (ROOT / "PASS333_337_OUTER_POLARIZATION_SPIN_BAER_SYNTHESIS.md")
        .read_text(encoding="utf-8")
        .split()
    )
    paper = " ".join((ROOT / "w33_paper.tex").read_text(encoding="utf-8").split())
    selection = " ".join(
        (ROOT / "analysis" / "THE_SELECTION_LAYER.md")
        .read_text(encoding="utf-8")
        .split()
    )
    index = " ".join(
        (ROOT / "docs" / "index.html").read_text(encoding="utf-8").split()
    )
    for surface in (synthesis, paper, selection, index):
        assert "Pass 333" in surface or "Passes 333" in surface
        assert "Pass 337" in surface or "Passes 333--337" in surface
    assert "three triangles" in synthesis
    assert "symplectic polar lift" in selection
    assert "selector-leaf bundle" in paper
    assert "pass337-epsilon-e8-baer-separation" in index
