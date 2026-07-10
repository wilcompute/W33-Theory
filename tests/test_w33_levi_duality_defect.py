"""Regression tests for the Levi duality-defect / incidence-Dirac theorem."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_levi_duality_defect.py"
SPEC = importlib.util.spec_from_file_location("w33_levi_duality_defect", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def result() -> dict:
    return MOD.analyze()


def test_full_certificate_passes() -> None:
    data = result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())


def test_characteristic_zero_partner_spectrum_and_defect() -> None:
    data = result()
    c0 = data["characteristic_zero"]
    geometry = data["geometry"]
    assert c0["incidence_gram_spectrum"] == {"0": 15, "6": 24, "16": 1}
    assert c0["dirac_spectrum"] == {
        "-4": 1,
        "-sqrt(6)": 24,
        "0": 30,
        "+sqrt(6)": 24,
        "+4": 1,
    }
    assert c0["point_zero_modes"] == c0["line_zero_modes"] == 15
    assert c0["witten_index"] == 0
    assert geometry["point_line_graphs_isomorphic"] is False
    assert geometry["alpha_point_graph"] == 7
    assert geometry["alpha_line_graph"] == 10


def test_characteristic_two_quartic_nilpotent_filtration() -> None:
    data = result()["characteristic_two"]
    assert data["dirac_power_ranks"] == {"1": 50, "2": 26, "3": 2, "4": 0}
    assert data["dirac_kernel_filtration"] == {"1": 30, "2": 54, "3": 78, "4": 80}
    assert data["dirac_jordan_blocks"] == {"1": 6, "3": 22, "4": 2}


def test_half_homologies_recover_dual_glue_ranks() -> None:
    data = result()["characteristic_two"]
    assert data["point_half_rank"] == 16
    assert data["line_half_rank"] == 10
    assert data["point_half_homology_dimension"] == 8
    assert data["line_half_homology_dimension"] == 20
    assert data["homology_dimension_sum"] == 28
    assert data["induced_point_to_line_homology_rank"] == 0
    assert data["induced_line_to_point_homology_rank"] == 0
