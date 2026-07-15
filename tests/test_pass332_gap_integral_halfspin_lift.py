"""Focused parser tests for the GAP-owned Pass 332 certificate."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass332_integral_halfspin_lift.g"
CERTIFICATE = ROOT / "data" / "w33_pass332_integral_halfspin_lift.json"
SYNTHESIS = ROOT / "PASS331_332_WEIL_INTEGRAL_CHIRALITY_BRIDGE.md"
SELECTION_LAYER = ROOT / "analysis" / "THE_SELECTION_LAYER.md"
PAPER = ROOT / "w33_paper.tex"
INDEX = ROOT / "docs" / "index.html"


@lru_cache(maxsize=1)
def _certificate() -> dict:
    """Run GAP once; Python only parses the GAP-produced certificate."""

    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for the Pass 332 certificate"
    result = subprocess.run(
        [gap, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert "Pass332 status=PASS checks=" in result.stdout
    assert "39 output=data/w33_pass332_integral_halfspin_lift.json" in result.stdout
    return json.loads(CERTIFICATE.read_text(encoding="utf-8"))


def test_three_stable_lattice_classes_reduce_to_exact_h10() -> None:
    cert = _certificate()
    lift = cert["integral_lift"]
    assert cert["status"] == "PASS"
    assert lift["source"] == "Res_{Q(zeta3)/Q}(Atlas 5a)"
    assert lift["group_order"] == 25_920
    assert lift["base_mod2_submodule_dimensions"] == [0, 8, 9, 9, 9, 10]
    assert lift["invariant_nine_spaces"] == 3
    assert lift["neighbor_submodule_dimensions"] == [[0, 1, 9, 10]] * 3
    assert lift["Hom_dimensions_to_H10"] == [2, 2, 2]
    assert lift["Hom_rank_spectra"] == [[0, 1, 10]] * 3
    assert "invertible X exists for all three" in lift["intertwiner_equation"]


def test_eisenstein_scalar_is_the_singer_cycle_of_the_p1_star() -> None:
    lift = _certificate()["integral_lift"]
    assert lift["omega_neighbor_permutation"] == [3, 1, 2]
    assert "P1(F2)" in lift["stable_lattice_star"]
    assert "Singer 3-cycle" in lift["stable_lattice_star"]
    assert "stabilizes none" in lift["omega_reading"]


def test_halfspin_realization_and_form_boundary_are_explicit() -> None:
    cert = _certificate()
    forms = cert["forms"]
    spin = cert["halfspin"]
    assert forms["H10_isotropic_vectors"] == 528
    assert forms["primitive_form_determinant"] == 62_208
    assert forms["halved_neighbor_determinants"] == [243, 243, 243]
    assert forms["isometry_verdict"].startswith("NOT BUILT")
    assert spin["S_plus"].endswith("= 1+10a+5b")
    assert spin["S_minus"].endswith("= 5a+10b+1")
    assert "nonisomorphic complex-conjugate 16s" in spin["duality"]
    assert cert["outer_boundary"]["raw_conjugation_generator_membership"] == [
        True,
        False,
    ]
    assert "not constructed" in cert["outer_boundary"]["verdict"]
    assert cert["check_count"] == 39
    assert all(cert["checks"].values())


def test_characteristic_bridge_is_visible_with_its_boundaries() -> None:
    synthesis = " ".join(SYNTHESIS.read_text(encoding="utf-8").split())
    selection = " ".join(SELECTION_LAYER.read_text(encoding="utf-8").split())
    paper = " ".join(PAPER.read_text(encoding="utf-8").split())
    index = " ".join(INDEX.read_text(encoding="utf-8").split())

    assert "PASS 39/39" in synthesis
    assert "torsor of three integral polarizations" in selection
    assert "The Selection-Layer Characteristic Bridge" in paper
    assert "pass332-integral-h10-halfspin-realization" in index
    assert "extend the lift from PSp(4,3) to PGSp(4,3)" in synthesis
    assert "not yet PGSp-equivariant" in selection
    assert "rather than $\\mathrm{PGSp}(4,3)$-equivariant" in paper
    assert "not yet a PGSp" in index
