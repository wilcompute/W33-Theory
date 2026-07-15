"""Focused live-GAP tests for the Pass 338--342 breakthrough packet."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = {
    338: ROOT / "analysis" / "w33_pass338_selector_frame_240.g",
    339: ROOT / "analysis" / "w33_pass339_extraspecial_clifford_spin_bridge.g",
    340: ROOT / "analysis" / "w33_pass340_halfspin_discriminant_module.g",
    341: ROOT / "analysis" / "w33_pass341_selector_extension_cohomology.g",
    342: ROOT / "analysis" / "w33_pass342_global_lattice_reconciliation.g",
}
CERTIFICATES = {
    number: next((ROOT / "data").glob(f"w33_pass{number}_*.json"))
    for number in SCRIPTS
}


@lru_cache(maxsize=None)
def _certificate(number: int) -> dict:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Passes 338--342"
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


def test_pass338_builds_the_principal_selector_frame_240_cover() -> None:
    cert = _certificate(338)
    frame = cert["selector_frame"]
    signed = cert["signed_E8_comparison"]
    assert cert["check_count"] == 17
    assert frame["orders_G_K_N"] == [51_840, 1_296, 216]
    assert frame["deck"] == "S3"
    assert frame["subdegrees"] == [1] * 6 + [27] * 6 + [72]
    assert frame["inner_subdegrees"] == [1] * 6 + [27] * 6 + [36, 36]
    assert frame["block_sizes"] == {"2": 3, "3": 1, "6": 1}
    assert signed["order"] == 103_680
    assert signed["forty_hexad_base"] == "p40a, not p40b"
    assert signed["equivalent_to_selector_frame"] is False
    assert cert["refinement_twist"]["integral_orbits"] == [3, 3]
    assert cert["refinement_twist"]["sign_twisted_orbit"] == [6]


def test_pass339_builds_the_extraspecial_clifford_carrier() -> None:
    cert = _certificate(339)
    extra = cert["extraspecial_group"]
    h10 = cert["H10_orthogonal_action"]
    assert cert["check_count"] == 14
    assert extra["order"] == 2_048
    assert extra["structure"] == "2_+^(1+10)"
    assert extra["square_one_elements"] == 1_056
    assert extra["trace_distribution"] == [[-32, 1], [0, 2_046], [32, 1]]
    assert extra["unique_nonlinear_degree"] == 32
    assert h10 == {
        "image": "U4(2)",
        "order": 25_920,
        "dimension": 10,
        "type": "plus",
        "invariant_refinements": 2,
        "zeros_per_refinement": 528,
    }
    assert "projective Clifford lift" in cert["bridge"]["scope"]


def test_pass340_names_the_three_adic_discriminant_module() -> None:
    cert = _certificate(340)
    module = cert["module"]
    assert cert["check_count"] == 15
    assert module["dimension"] == 16
    assert module["decomposition"] == [1, 5, 10]
    assert module["submodule_dimensions"] == [0, 1, 5, 6, 10, 11, 15, 16]
    assert module["endomorphism_algebra"] == "F3^3"
    assert module["self_dual"] and module["plus_equals_minus"]
    assert cert["Eisenstein_action"]["plus"] == "identity"
    assert cert["Eisenstein_action"]["minus"] == "identity"
    assert cert["spin16_separation"]["U4(2)_irreducible_16_exists"] is False
    assert cert["spin16_separation"]["center_action"] == "-I16"


def test_pass341_separates_restriction_classes_and_kills_yoneda_product() -> None:
    cert = _certificate(341)
    assert cert["check_count"] == 19
    assert cert["dimensions"] == {
        "H2_PGSp": 2,
        "H2_PSp": 1,
        "H2_line_stabilizer": 2,
        "H2_A": 1,
        "H2_selector_kernel": 3,
    }
    assert "one-dimensional signed-E8 span" in cert["restriction_verdict"]
    assert cert["Yoneda"]["inner_H1_trivial_8_radical"] == [0, 2, 2]
    assert cert["Yoneda"]["full_H1_trivial_8_radical"] == [1, 1, 2]
    assert cert["Yoneda"]["connecting_map"] == "zero"
    assert cert["Yoneda"]["product_in_H2"].startswith("zero")


def test_pass342_globalizes_the_local_complex_without_forcing_kirschmer() -> None:
    cert = _certificate(342)
    assert cert["check_count"] == 12
    assert cert["local_nodes"] == ["L", "R", "L1", "L2", "L3"]
    assert cert["omega_permutation"] == [1, 2, 5, 3, 4]
    assert cert["outer_reflection_permutation"] == [1, 2, 3, 5, 4]
    assert "L and R remain separately stable" in cert["compression"]
    assert "do not equate" in cert["Kirschmer_reconciliation"]["verdict"]


def test_packet_is_visible_on_shared_theory_surfaces() -> None:
    synthesis = " ".join(
        (ROOT / "PASS338_342_SELECTOR_CLIFFORD_COHOMOLOGY_SYNTHESIS.md")
        .read_text(encoding="utf-8")
        .split()
    )
    paper = " ".join((ROOT / "w33_paper.tex").read_text(encoding="utf-8").split())
    selection = " ".join(
        (ROOT / "analysis" / "THE_SELECTION_LAYER.md")
        .read_text(encoding="utf-8")
        .split()
    )
    index = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    for surface in (synthesis, paper, selection, index):
        assert "Pass 338" in surface or "Passes 338--342" in surface
        assert "Pass 342" in surface or "Passes 338--342" in surface
    assert "principal `S3`" in synthesis
    assert "Yoneda product" in paper
    assert "1 + 5 + 10" in selection
    assert "pass341-selector-extension-cohomology" in index
