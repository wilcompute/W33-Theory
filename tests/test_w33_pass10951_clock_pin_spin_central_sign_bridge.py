import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10951_clock_pin_spin_central_sign_bridge.py"
CERT = ROOT / "data/w33_pass10951_clock_pin_spin_central_sign_bridge.json"


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
    assert load()["status"] == "PASS_CLOCK_PIN_SPIN_CENTRAL_SIGN_BRIDGE"
def test_two_c2s_are_distinct():
    d = load()["two_C2s"]
    assert d["independent_not_conflated"] is True
    assert d["pin_component_character"]["kernel"] == "SL(2,3)"
    assert d["central_spin_sign"]["determinant"] == 1
    assert d["central_spin_sign"]["projective_action"] == "identity"


def test_order_eight_clock_lift():
    c = load()["clock_power_ladder"]
    assert c["g_order"] == 8
    assert c["projective_period"] == 4
    assert c["spin_lift_period"] == 8
    assert c["g_fourth"] == "-I2"
    assert c["g_eighth"] == "+I2"


def test_binary_tetrahedral_spin_certificate():
    b = load()["binary_tetrahedral_certificate"]
    assert b["Q8_size"] == 8
    assert b["quaternion_group_size"] == 24
    assert b["full_24_squared_homomorphism_check"] is True
    assert b["center_maps_to_quaternion_minus_one"] is True
def test_schur_cover_boundary():
    g = load()["groups"]
    assert g["GL2_3_order"] == 48
    assert g["SL2_3_order"] == 24
    assert g["schur_cover_type"] == "2^+ S4 = GL(2,3)"
    assert g["det_minus_coset_order_spectrum"] == {"2": 12, "8": 12}


def test_matter_parity_central_weld():
    m = load()["matter_parity_weld"]
    assert m["pass10950_spin9_2pi_equals_peirce_symmetry"] is True
    assert m["pass10950_numerical_error"] < 1e-8
    assert "No action of the full determinant-minus-one" in m["not_claimed"]


def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10951-clock-pin-spin"') == 1
    assert tail.count("PASS10951_CLOCK_PIN_SPIN_CENTRAL_SIGN_BRIDGE_INSERT}%") == 1
