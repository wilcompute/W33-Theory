import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10956_albert_spin8_halfspin_normalizer.py"
CERT = ROOT / "data/w33_pass10956_albert_spin8_halfspin_normalizer.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run(
        [sys.executable, str(PRODUCER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert load()["status"] == "PASS_ALBERT_SPIN8_HALFSPIN_NORMALIZER_BRIDGE"
def test_spin8_stabilizer_and_branching():
    s = load()["spin8_stabilizer"]
    assert s["dimension"] == 28
    assert s["restriction_commutant_dimension"] == 2
    assert s["halfspin_plus_dimension"] == 8
    assert s["halfspin_minus_dimension"] == 8
    assert s["plus_commutant_dimension"] == 1
    assert s["minus_commutant_dimension"] == 1
    assert s["cross_intertwiner_dimension"] == 0
    assert s["branching"] == "16 -> 8_s + 8_c under Spin(8)"


def test_exact_chirality_involution():
    c = load()["chirality_involution"]
    assert c["square"] == "+I16"
    assert c["trace"] == 0
    assert c["eigenvalue_multiplicities"] == {"+1": 8, "-1": 8}
    assert c["commutes_with_all_spin8_generators"] is True
def test_spin9_halfturn_swaps_halfspin_modules_and_squares_to_parity():
    h = load()["spin9_normalizer_halfturn"]
    assert h["axis_flip_error"] < 1e-8
    assert h["chirality_conjugation_to_minus_error"] < 1e-8
    assert h["plus_to_minus_projector_error"] < 1e-8
    assert h["minus_to_plus_projector_error"] < 1e-8
    assert h["square_equals_full_2pi_error"] < 1e-8
    assert h["two_pi_equals_minus_I16_error"] < 1e-8
    assert h["fourth_power_identity_error"] < 1e-8


def test_pass10955_weld_is_explicitly_bounded():
    w = load()["pass10955_weld"]
    assert "exchange 8_s <-> 8_c" in w["finite_D4_outer_action"]
    assert "same Spin(8) half-spin transposition" in w["albert_realization"]
    assert "no homomorphism/intertwiner" in w["not_yet_proved"]
def test_matter_parity_chain_preserves_power_mismatch_firewall():
    m = load()["matter_parity_chain"]
    assert m["halfturn_squared"] == "-I on the Peirce 16"
    assert "2pi Spin(9)" in m["pass10950"]
    assert "g^4=-I" in m["pass10951"]
    assert "powers differ" in m["firewall"]


def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10956-albert-spin8-halfspin"') == 1
    assert tail.count("PASS10956_ALBERT_SPIN8_HALFSPIN_NORMALIZER_INSERT}%") == 1
