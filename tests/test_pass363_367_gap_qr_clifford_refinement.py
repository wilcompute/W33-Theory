"""Focused regressions for the GAP-owned Passes 363--367."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")


def _run_gap(basename: str, marker: str) -> dict:
    assert GAP is not None
    result = subprocess.run(
        [GAP, "-q", str(ROOT / "analysis" / f"{basename}.g")],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    assert marker in result.stdout
    return json.loads(
        (ROOT / "data" / f"{basename}.json").read_text(encoding="utf-8")
    )


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 363")
def test_pass363_builds_the_complete_real_clifford_character_diamond() -> None:
    cert = _run_gap(
        "w33_pass363_real_clifford_character_diamond",
        "Pass363 status=PASS",
    )
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 44 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert cert["ambient"] == {
        "group_order": 2304,
        "abelianization": "C2 x C2",
        "class_count": 29,
        "derived_orders": [2304, 576, 288, 32, 2, 1],
    }
    assert cert["kernel_orders"] == [1152, 1152, 1152]
    assert cert["kernel_class_counts"] == [25, 34, 19]
    assert cert["normalized_f4_shell"]["W(F4)_orbits"] == [24, 24]
    assert cert["normalized_f4_shell"]["2O_central_product_orbit"] == [48]
    assert cert["correction"] == {
        "GL(2,3)": "SmallGroup(48,29), 13 involutions",
        "binary_octahedral_2O": "SmallGroup(48,28), 1 involution",
        "isomorphic": False,
    }


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 364")
def test_pass364_realizes_the_e8_mod_2_graph_on_four_qr_blocks() -> None:
    cert = _run_gap(
        "w33_pass364_qr548_e8_phase_space",
        "Pass364 status=PASS",
    )
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 22 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert cert["code"] == {
        "parameters": "[[548,4,21]]",
        "stabilizer_rank": 544,
        "encoded_H_count": 4,
        "transversal_CNOT_count": 12,
    }
    assert cert["logical_group"] == {
        "group": "O+(8,2)",
        "order": 348364800,
        "index_in_Sp8_2": 136,
        "nonzero_orbits": [135, 120],
    }
    assert "SRG(255,126,61,63)" in cert["graphs"]["symplectic"]
    assert "SRG(135,70,37,35)" in cert["graphs"]["isotropic"]
    assert "SRG(120,63,30,36)" in cert["graphs"]["anisotropic"]


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 365")
def test_pass365_lifts_the_w33_spread_graph_to_three_qr_blocks() -> None:
    cert = _run_gap(
        "w33_pass365_qr411_e6_minus_polar_lift",
        "Pass365 status=PASS",
    )
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 25 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert cert["code"] == {
        "parameters": "[[411,3,21]]",
        "stabilizer_rank": 408,
        "full_encoded_label_group": "Sp(6,2), order 1451520",
    }
    assert cert["orthogonal_group"] == {
        "group": "O-(6,2)=W(E6)",
        "order": 51840,
        "derived": "PSp(4,3), order 25920",
        "vector_orbits": [1, 27, 36],
    }
    assert len(cert["spread_to_vector_index_map"]) == 36
    assert sorted(cert["spread_to_vector_index_map"]) == list(range(1, 37))
    assert cert["real_complex_split"] == {
        "shared_q_plus_nonsingular": 16,
        "phase_required": 20,
    }
    assert "Zbar_3" in cert["named_lift"]


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 366")
def test_pass366_builds_the_qr137m_refinement_tower() -> None:
    cert = _run_gap(
        "w33_pass366_qr137m_real_clifford_refinement_tower",
        "Pass366 status=PASS",
    )
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 17 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert [row["code"] for row in cert["verified_tower"]] == [
        "[[137,1,21]]",
        "[[274,2,21]]",
        "[[411,3,21]]",
        "[[548,4,21]]",
    ]
    assert [row["Sp_index"] for row in cert["verified_tower"]] == [3, 10, 36, 136]
    assert cert["refinement_counts_m1_to_m4"] == [
        [3, 1],
        [10, 6],
        [36, 28],
        [136, 120],
    ]
    assert cert["exceptional_boundaries"]["m3_plus"].endswith("not W(E6)")


@pytest.mark.skipif(GAP is None, reason="GAP is required for Pass 367")
def test_pass367_proves_the_universal_parity_pullback_is_nonsplit() -> None:
    cert = _run_gap(
        "w33_pass367_universal_c2_exchange_gate_pullback",
        "Pass367 status=PASS",
    )
    assert cert["status"] == "PASS"
    assert cert["check_count"] == 19 == len(cert["checks"])
    assert all(cert["checks"].values())
    assert [factor["split"] for factor in cert["factors"]] == [True, True, False, True]
    assert cert["even_kernel_order"] == 14420554127769600
    assert cert["pullback_order"] == 28841108255539200
    assert cert["odd_order_obstruction"] == {
        "QR_odd_orders": [8, 136],
        "minimum_pullback_odd_order": 8,
        "odd_involution_exists": False,
    }


def test_pass363_367_are_published_with_their_scope_boundaries() -> None:
    synthesis = (
        ROOT / "PASS363_367_QR_CLIFFORD_REFINEMENT_SYNTHESIS.md"
    ).read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    selection = (ROOT / "analysis" / "THE_SELECTION_LAYER.md").read_text(
        encoding="utf-8"
    )
    website = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    photonic = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    practical = (ROOT / "holonet_practical_implications.tex").read_text(
        encoding="utf-8"
    )
    results_index = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8")
    legacy_gl = (
        ROOT / "analysis" / "w33_BREAKTHROUGH_GL2_F3_irreps.py"
    ).read_text(encoding="utf-8")

    for surface in (synthesis, readme, paper, selection, website):
        assert "[[548,4,21]]" in surface
        assert "[[411,3,21]]" in surface
        assert "28,841,108,255,539,200" in surface.replace("{,}", ",")
    assert "spread-index to nonsingular-vector-index" in synthesis
    assert "no locality, transversality, or fault-tolerance" in synthesis
    assert "THE COMPLETE CHARACTER DIAMOND" in paper
    assert "UNIVERSAL PARITY PULLBACK" in paper
    assert "parity **grading**, but not dynamically as" in selection
    assert "SmallGroup(48,29)" in website
    assert "SmallGroup(48,28)" in website
    assert "a canonical fermion/chirality assignment" not in website
    assert "Exact resource boundary from the QR branch" in photonic
    assert "the QR witnesses do not establish $P=1$" in photonic
    assert "proposed integrated magic supply" in practical
    assert "not a proof of continuous fault-tolerant magic replenishment" in practical
    assert "| `[[411,3,21]]` |" in results_index
    assert "| `[[548,4,21]]` |" in results_index
    assert "GL(2, F_3) =~ 2.S_4" not in legacy_gl
    assert "binary octahedral group" not in legacy_gl
