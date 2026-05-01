import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from w33_rg_phi6_polar_pipeline import (  # noqa: E402
    MODEL_NAME,
    MU,
    PHI3,
    PHI6,
    PDG_ALPHA_S_MZ,
    selected_alpha_s_gut,
    selected_delta_gut,
    selected_k3_bare,
    selected_k3_effective,
    selected_phi6_polar_report,
    selected_tau_gut,
    w33_phi6_polar_alpha_s_mz,
)


def test_selected_k3_bare_is_24_over_13():
    assert selected_k3_bare() == 24 / PHI3


def test_selected_tau_is_phi6_polar_log():
    assert abs(selected_tau_gut() - math.log(math.sqrt(MU / PHI6))) < 1e-15
    assert selected_tau_gut() < 0


def test_selected_delta_is_subpercent_negative():
    delta = selected_delta_gut()
    assert -0.002 < delta < 0


def test_selected_effective_k3_matches_cxliii_value():
    assert abs(selected_k3_effective() - 1.849448291286928) < 1e-12


def test_selected_alpha_s_gut_is_finite_and_physical():
    a = selected_alpha_s_gut()
    assert 0.02 < a < 0.03


def test_selected_pipeline_recovers_pdg_alpha_s_mz():
    result = w33_phi6_polar_alpha_s_mz(verbose=False)
    assert result["status"] == "ok"
    assert result["model"] == MODEL_NAME
    assert abs(result["alpha_s_mz"] - PDG_ALPHA_S_MZ) < 1e-5
    assert result["sigma"] < 0.01


def test_report_contains_selected_branch_metadata():
    report = selected_phi6_polar_report()
    assert report["selected_branch"]["model"] == MODEL_NAME
    assert report["selected_branch"]["k3_bare"] == "24/13"
    assert "Phi6" in report["selected_branch"]["selection_principle"]
