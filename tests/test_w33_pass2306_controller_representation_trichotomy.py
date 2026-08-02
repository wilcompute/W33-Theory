"""GAP-owned regression for the Pass-2306 controller trichotomy."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")
SCRIPT = ROOT / "analysis" / "w33_pass2306_controller_representation_trichotomy.g"
CERTIFICATE = ROOT / "data" / "w33_pass2306_controller_representation_trichotomy.json"


@pytest.fixture(scope="module")
def pass2306() -> tuple[str, dict]:
    assert GAP is not None, "GAP is required for Pass 2306"
    result = subprocess.run(
        [GAP, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    return result.stdout, json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_gap_witness_passes(pass2306: tuple[str, dict]) -> None:
    output, certificate = pass2306
    assert "Pass2306 status=PASS" in output
    assert "minimal_faithful_Q_degree=4" in output
    assert "common_inverter_nullity=0" in output
    assert "finite_A2B_order=6 arithmetic_R2U_order=infinity" in output
    assert certificate["status"] == "PASS"
    assert len(certificate["checks"]) == 19
    assert all(certificate["checks"].values())


def test_three_controller_objects_are_not_conflated(pass2306: tuple[str, dict]) -> None:
    _, certificate = pass2306
    abstract = certificate["abstract_controller"]
    canonical = certificate["canonical_single_J_quotient"]
    arithmetic = certificate["overlapping_arithmetic_carrier"]

    assert abstract["order"] == 48
    assert abstract["minimal_faithful_rational_degree"] == 4
    assert abstract["natural_character_irreducibles"] == [10, 12]
    assert canonical == {
        "map": "(a,b,e) -> (3a+2b mod 12,e)",
        "image": "C12:C2",
        "image_order": 24,
        "kernel": [[0, 0, 0], [2, 3, 0]],
        "fiber_size": 2,
    }
    assert arithmetic["dimension"] == 3
    assert arithmetic["generators_commute"] is False
    assert arithmetic["commutator_order"] == 4
    assert arithmetic["common_inverter_equation_rank"] == 9
    assert arithmetic["common_inverter_nullity"] == 0


def test_same_syntactic_word_changes_dynamical_type(pass2306: tuple[str, dict]) -> None:
    _, certificate = pass2306
    finite = certificate["abstract_controller"]["matched_word"]
    arithmetic = certificate["overlapping_arithmetic_carrier"]

    assert finite["word"] == "A4^2 B6"
    assert finite["order"] == 6
    assert finite["spectral_radius"] == 1
    assert finite["factorization"] == "(t+1)^2(t^2-t+1)"
    assert arithmetic["golden_word"] == "R4^2 U6"
    assert arithmetic["golden_word_order"] == "infinity"
    assert arithmetic["golden_word_spectral_radius"] == "phi"
    assert arithmetic["golden_word_factorization"] == "(t+1)(t^2-t-1)"


def test_publication_surfaces_state_the_boundary() -> None:
    report = (ROOT / "PASS2306_CONTROLLER_REPRESENTATION_TRICHOTOMY.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    for text in (report, readme, index):
        assert "minimal faithful rational degree" in text
        assert "common inverter" in text
        assert "arithmetic" in text
    assert "not a selected physical observable" in report
