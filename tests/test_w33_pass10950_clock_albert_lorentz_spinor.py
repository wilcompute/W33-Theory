import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10950_clock_albert_lorentz_spinor.py"
CERT = ROOT / "data/w33_pass10950_clock_albert_lorentz_spinor.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True,
                   capture_output=True, text=True, timeout=900)
    assert load()["status"] == (
        "PASS_CLOCK_ALBERT_F4_E6M26_SO19_WEYL_SPINOR_AND_MATTER_PARITY_AS_PEIRCE_SYMMETRY")


def test_compact_f4_and_e6m26():
    s = load()["structure"]
    assert s["Der_dimension"] == 52 and s["Der_is_derivation_failures"] == 0
    assert s["Der_trace_form_inertia"] == [0, 52, 0]
    assert s["str0_dimension"] == 78 and s["str0_trace_form_inertia"] == [26, 52, 0]
    assert s["generating_identity_[D,L_x]=L_(Dx)_failures"] == 0


def test_so19_and_weyl_spinor():
    lo = load()["lorentz"]
    assert lo["Der_c_dimension"] == 36 and lo["Der_c_trace_inertia"] == [0, 36, 0]
    assert lo["lorentz_algebra_dimension"] == 45
    assert lo["A0_determinant_inertia"] == [1, 9, 0]
    assert lo["determinant_invariance_failures"] == 0
    assert lo["faithful_image_dimension_in_gl(A0)"] == 45
    assert lo["spinor_module_dimension"] == 16 and lo["spinor_commutant_dimension"] == 1


def test_three_plus_one_complex_spinor():
    t = load()["three_plus_one"]
    assert t["subalgebra_dimension"] == 21
    assert t["commutant_on_16_dimension"] == 2
    assert t["commutant_contains_complex_structure"] is True


def test_matter_parity_is_peirce_symmetry_and_two_pi_rotation():
    m = load()["matter_parity"]
    assert m["coordinate_idempotents_reproducing_Qpsi_spectrum_and_triad_patterns"] == 27
    assert all(m["peirce_symmetry_U_(2c-e)"].values())
    assert m["two_pi_rotation_equals_U_s_max_error"] < 1e-8


def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(encoding="utf-8")
    assert docs.count('id="pass10950-clock-albert-lorentz-spinor"') == 1
    assert tail.count("PASS10950_CLOCK_ALBERT_LORENTZ_SPINOR_INSERT}%") == 1
