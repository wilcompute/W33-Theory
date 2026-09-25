import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10953_minimal_doubled_pin_clock_visibility.py"
CERT = ROOT / "data/w33_pass10953_minimal_doubled_pin_clock_visibility.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run(
        [sys.executable, str(PRODUCER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert load()["status"] == "PASS_MINIMAL_DOUBLED_PIN_CLOCK_VISIBILITY_BRIDGE"
def test_six_dimensions_are_minimal():
    m = load()["minimal_linearization"]
    assert m["dimension"] == 6
    assert m["omega_central_eigenspace_dimension"] == 3
    assert m["omega_inverse_central_eigenspace_dimension"] == 3
    assert m["lower_bound"] == 6
    assert m["attained"] is True


def test_sector_bit_is_determinant_grading():
    s = load()["sector_grading"]
    assert s["Gamma_anticommutes_with_tick"] is True
    assert s["Gamma_commutes_with_Heisenberg_generators"] is True
    assert s["tick_inverts_Heisenberg_center"] is True
    for row in s["powers"]:
        assert row["sector_preserving"] == (row["power"] % 2 == 0)
        assert row["gamma_grading_error"] < 1e-8
def test_exact_z8_spectrum_and_visibility():
    z = load()["z8_spectrum"]
    assert z["eighth_root_exponents"] == [0, 1, 3, 4, 5, 7]
    assert z["missing_exponents"] == [2, 6]
    assert z["minimal_polynomial"] == "x^6 - x^4 + x^2 - 1"
    assert z["minimal_polynomial_matrix_residual"] < 1e-8
    assert z["trace_sequence"] == [
        [6.0, 0.0], [0.0, 0.0], [2.0, 0.0], [0.0, 0.0],
        [-2.0, 0.0], [0.0, 0.0], [2.0, 0.0], [0.0, 0.0],
    ]
    expected = [1, 0, 1/3, 0, 1/3, 0, 1/3, 0]
    assert all(abs(a-b) < 1e-11
               for a,b in zip(z["normalized_trace_visibility"], expected))
    assert z["six_dimensional_Bell_overlap_max_error"] < 1e-8
def test_physical_c4_has_qutrit_one_third_visibility():
    c = load()["physical_even_C4"]
    assert c["Fourier_class_conjugator_count"] == 4
    assert c["one_qutrit_lift_after_conjugacy"]["residual"] < 1e-8
    expected = [1, 1/3, 1/3, 1/3]
    assert all(abs(a-b) < 1e-11
               for a,b in zip(c["normalized_trace_visibility"], expected))
    assert "existing Bell-qutrit calibration" in c["reading"]


def test_hardware_boundary_is_explicit():
    p = load()["interferometric_prediction"]
    assert "existing qutrit Bell interferometer" in p["hardware_boundary"]
    assert "6D" in p["hardware_boundary"]
def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10953-minimal-pin-clock-visibility"') == 1
    assert tail.count(
        "PASS10953_MINIMAL_DOUBLED_PIN_CLOCK_VISIBILITY_INSERT}%"
    ) == 1
