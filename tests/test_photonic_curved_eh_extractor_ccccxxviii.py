"""Regression tests for PART CCCCXXVIII photonic curved EH extractor."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXXVIII_PHOTONIC_CURVED_EH_EXTRACTOR.py"
RESULTS_PATH = ROOT / "PART_CCCCXXVIII_photonic_curved_eh_extractor_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("photonic_curved_eh_extractor_ccccxxviii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_photonic_curved_eh_extractor_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 63
    assert all(check["passed"] for check in results["checks"])


def test_coefficient_package_locks_eh_and_weinberg_roundtrip():
    package = build_results()["coefficient_package"]
    assert package["discrete_eh"] == "12480"
    assert package["continuum_eh"] == "320"
    assert package["rank39_normalization"] == "12480 / 39 = 320"
    assert package["topological_a2"] == "2240"
    assert package["topological_ratio"] == "7"
    assert package["discrete_to_continuum_ratio"] == "39"
    assert package["master_variable"] == "3/13"
    assert package["weinberg_roundtrip"] == "9"


def test_extractor_stack_is_projector_residue_and_three_sample_curved_tower():
    stack = build_results()["extractor_stack"]
    assert stack["projector_polynomial"] == "x^3 - 127x^2 + 846x - 720"
    assert stack["shift_projectors"] == {
        "P_120": "((E-6)(E-1))/13566",
        "P_6": "-((E-120)(E-1))/570",
        "P_1": "((E-120)(E-6))/595",
    }
    assert stack["residue_generating_function"] == "A/(1 - 120 z) + B/(1 - 6 z) + C/(1 - z)"
    assert "39 * 6^r" in stack["continuum_formula"]
    assert stack["curved_sample_count"] == 6
    assert stack["curved_sample_seeds"] == ["CP2_9", "K3_16"]


def test_finite_roundtrip_recovers_full_internal_spectral_package():
    finite = build_results()["finite_roundtrip"]
    assert finite["chain_dimensions"] == {"c0": 40, "c1": 240, "c2": 160, "c3": 40}
    assert finite["boundary_ranks"] == {"rank_d1": 39, "rank_d2": 120, "rank_d3": 40}
    assert finite["betti_numbers"] == {"b0": 1, "b1": 81, "b2": 0, "b3": 0}
    assert finite["df2_spectrum"] == {"0": 82, "4": 320, "10": 48, "16": 30}
    assert finite["seeley_dewitt_moments"] == {"a0_f": 480, "a2_f": 2240, "a4_f": 17600}


def test_inverse_rosetta_recovers_w33_and_promoted_projective_shell():
    inverse = build_results()["inverse_rosetta"]
    assert inverse["q"] == 3
    assert inverse["phi3"] == "13"
    assert inverse["phi6"] == "7"
    assert inverse["srg"] == {"v": 40, "k": 12, "lambda": 2, "mu": 4}
    assert inverse["spectrum"] == {"k": 12, "r": 2, "s": -4}


def test_protected_photonic_handoff_remains_the_runtime_boundary():
    handoff = build_results()["protected_photonic_handoff"]
    assert handoff["source_part"] == "CCCCXXVII"
    assert handoff["active_code"] == "[[82320,81,>=81]]"
    assert handoff["h1_logical"] == 81
    assert handoff["selector_trits"] == 40
    assert handoff["edge_carrier"] == 240
    assert handoff["curved_seeds"]["CP2_9"]["harmonic_total"] == 3
    assert handoff["curved_seeds"]["K3_16"]["harmonic_total"] == 24
    assert handoff["logical_harmonic_channels"]["CP2_9_total"] == 243
    assert handoff["logical_harmonic_channels"]["K3_16_total"] == 1944


def test_theorem_and_boundary_state_exact_claim_without_overclaiming():
    results = build_results()
    theorem = results["theorem"]
    assert "three successive refinement samples" in theorem
    assert "c6=12480" in theorem
    assert "rank-39 normalization gives cEH=320" in theorem
    assert "D_F^2={0^82,4^320,10^48,16^30}" in theorem
    assert "SRG(40,12,2,4)" in theorem
    assert "x=3/13" in theorem
    assert "exact coefficient-extractor and roundtrip theorem" in results["honesty_boundary"]
    assert "not the final Einstein-Hilbert spectral-action asymptotic theorem" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXXVIII"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["coefficient_package"] == live["coefficient_package"]
    assert artifact["extractor_stack"] == live["extractor_stack"]
    assert artifact["finite_roundtrip"] == live["finite_roundtrip"]
    assert artifact["inverse_rosetta"] == live["inverse_rosetta"]


def test_docs_index_exposes_photonic_curved_eh_extractor():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Photonic Curved Einstein-Hilbert Extractor" in text
    assert "PART_CCCCXXVIII_PHOTONIC_CURVED_EH_EXTRACTOR.md" in text
    assert "12480" in text
    assert "320" in text
    assert "2240" in text
    assert "3/13" in text
    assert "SRG(40,12,2,4)" in text
    assert "not yet the final Einstein-Hilbert asymptotic theorem" in text


def test_single_photon_paper_records_curved_handoff_and_extractor():
    text = (ROOT / "single_photon_universal_computation.tex").read_text(encoding="utf-8")
    assert "\\subsection{Curved Product Handoff}" in text
    assert "\\Delta_{\\mathrm{ext}}\\otimes 1 + 1\\otimes D_F^2" in text
    assert "81\\cdot 3=243" in text
    assert "81\\cdot 24=1944" in text
    assert "\\subsection{Curved Coefficient Extractor}" in text
    assert "c_6=12480" in text
    assert "c_{\\mathrm{EH}}=320" in text
    assert "a_2=2240" in text
    assert "D_F^2=\\{0^{82},4^{320},10^{48},16^{30}\\}" in text
    assert "x=\\sin^2\\theta_W=\\frac{3}{13}" in text
    assert "smooth spectral-action limit" in text
