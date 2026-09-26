import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p10976",
    ROOT / "analysis" / "w33_pass10976_first_order_clock_selection.py",
)
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)

CERT_PATH = ROOT / "data" / "w33_pass10976_first_order_clock_selection.json"
CERT = json.loads(CERT_PATH.read_text(encoding="utf-8"))


def test_certificate_replays_exactly():
    assert P.payload() == CERT


def test_exact_coexistence_and_jump():
    ph = CERT["exact_phase_structure"]
    assert ph["coexistence_alpha"] == "gamma^2/(12 beta)"
    assert ph["order_parameter_jump"] == "gamma/(2 sqrt(3) beta)"
    assert ph["barrier_height_at_coexistence"] == "gamma^4/(2304 beta^3)"
def test_spinodals_and_metastability():
    ph = CERT["exact_phase_structure"]
    assert ph["ordered_spinodal_alpha"] == "3 gamma^2/(32 beta)"
    assert ph["disordered_spinodal_alpha"] == "0"
    assert ph["coexistence_to_ordered_spinodal_gap"] == "gamma^2/(96 beta)"


def test_native_e6_normalization_is_inherited():
    n = CERT["native_E6_normalization"]
    assert n["gamma_eff"] == "2 g_E6 / 3"
    assert n["r_jump"] == "sqrt(3)*g_E6/(9*beta)"
    assert n["alpha_coexistence"] == "g_E6**2/(27*beta)"
    assert n["alpha_ordered_spinodal"] == "g_E6**2/(24*beta)"
    assert n["barrier_height"] == "g_E6**4/(11664*beta**3)"


def test_finite_group_breaking_has_no_goldstones():
    ph = CERT["exact_phase_structure"]
    assert ph["vacuum_multiplicity_below_transition"].startswith("4")
    assert ph["goldstone_modes"] == 0
    assert "finite group" in ph["reason_no_goldstones"]
