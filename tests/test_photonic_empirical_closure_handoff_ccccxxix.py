"""Regression tests for PART CCCCXXIX photonic empirical closure handoff."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXXIX_PHOTONIC_EMPIRICAL_CLOSURE_HANDOFF.py"
RESULTS_PATH = ROOT / "PART_CCCCXXIX_photonic_empirical_closure_handoff_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("photonic_empirical_closure_handoff_ccccxxix", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_photonic_empirical_handoff_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 35
    assert all(check["passed"] for check in results["checks"])


def test_source_streams_reconcile_numbering_tracks():
    streams = build_results()["source_streams"]
    assert streams == {
        "photonic_curved": "CCCCXXVIII",
        "mass_mixing_surface": "CCCXXVII",
        "empirical_audit": "CCCXXXI",
        "gut_planck": "CCCXXXII",
        "light_quarks": "CCCXXXIII",
    }


def test_shared_atoms_are_the_common_w33_language():
    atoms = build_results()["shared_w33_atoms"]
    assert atoms == {
        "q": 3,
        "lambda": 2,
        "mu": 4,
        "v": 40,
        "Phi3": 13,
        "Phi4": 10,
        "Phi6": 7,
        "alpha_inv": 137,
        "H0": 70,
    }


def test_photonic_curved_exact_layer_stays_locked():
    layer = build_results()["photonic_curved_exact_layer"]
    assert layer["c6"] == "12480"
    assert layer["cEH"] == "320"
    assert layer["a2"] == "2240"
    assert layer["x"] == "3/13"
    assert layer["df2_spectrum"] == {"0": 82, "4": 320, "10": 48, "16": 30}
    assert layer["protected_code"] == "[[82320,81,>=81]]"
    assert layer["h1_logical"] == 81


def test_empirical_mass_sheet_includes_mixing_light_quarks_and_gut_planck():
    sheet = build_results()["empirical_mass_sheet"]
    assert sheet["surface_observables"] == [
        "lambda_H_MSbar_MZ",
        "wolf_lambda",
        "wolf_A",
        "wolf_rhobar",
        "wolf_etabar",
        "top_yukawa_pole",
    ]
    assert sheet["reduced_chi2"] < 0.34
    assert sheet["max_abs_z"] <= 1.0 + 1e-12
    assert sheet["light_quark_yukawas"] == {
        "y_d": "70/137^3",
        "y_u": "32/137^3",
        "y_u_over_y_d": "16/35",
    }
    assert sheet["gut_planck"] == {"alpha_GUT_inverse": 24, "M_Pl_over_M_GUT": 114}


def test_derived_links_are_exact_cross_stream_identities():
    links = build_results()["derived_links"]
    assert links["rank39_lock"] == "39"
    assert links["rank39_as_q_phi3"] == 39
    assert links["topological_ratio"] == "7"
    assert links["topological_ratio_as_phi6"] == 7
    assert links["weinberg_x"] == "3/13"
    assert links["weinberg_denominator_phi3"] == 13
    assert links["alpha_inv"] == 137
    assert links["alpha_inv_cubed"] == 2571353
    assert links["hubble_fixed_point_h0"] == 70
    assert links["down_yukawa_numerator"] == 70
    assert links["gut_planck_ratio"] == 114
    assert links["gut_alpha_inverse"] == 24


def test_theorem_and_boundary_are_bounded():
    results = build_results()
    theorem = results["theorem"]
    assert "c6/cEH=39=q*Phi3" in theorem
    assert "a2/cEH=7=Phi6" in theorem
    assert "x=q/Phi3=3/13" in theorem
    assert "alpha_inv=137" in theorem
    assert "H0=Phi6*Phi4=70" in theorem
    assert "compatibility handoff" in results["honesty_boundary"]
    assert "does not prove the smooth Einstein-Hilbert spectral action limit" in results["honesty_boundary"]
    assert all(value == "open" for value in results["open_boundaries"].values())


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXXIX"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["source_streams"] == live["source_streams"]
    assert artifact["shared_w33_atoms"] == live["shared_w33_atoms"]
    assert artifact["photonic_curved_exact_layer"] == live["photonic_curved_exact_layer"]
    assert artifact["empirical_mass_sheet"] == live["empirical_mass_sheet"]


def test_docs_index_exposes_photonic_empirical_handoff():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Photonic Empirical Closure Handoff" in text
    assert "PART_CCCCXXIX_PHOTONIC_EMPIRICAL_CLOSURE_HANDOFF.md" in text
    assert "CCCXXXIII" in text
    assert "137<sup>3</sup>" in text
    assert "70/137<sup>3</sup>" in text
    assert "32/137<sup>3</sup>" in text
    assert "24/114" in text
    assert "compatibility handoff" in text
