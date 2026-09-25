import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10957_mu4_schur_cover_converter.py"
CERT = ROOT / "data/w33_pass10957_mu4_schur_cover_converter.json"


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
    assert load()["status"] == "PASS_MU4_SCHUR_COVER_CONVERTER"
def test_plus_cover_is_objectwise_clock_gl23():
    p = load()["clock_plus_cover"]
    assert p["extension"] == "GL(2,3)=2^+S4"
    assert p["cocycle_identity_checks"] == 24 ** 3
    assert p["objectwise_GL2_3_homomorphism_checks"] == 48 ** 2
    assert p["involution_count"] == 13
    assert p["center_order"] == 2
    assert p["smallgroup_crosscheck"] == "[48,29]"


def test_parity_cup_square_gives_minus_cover_profile():
    m = load()["twisted_minus_cover"]
    assert "epsilon(s)epsilon(t)" in m["cocycle_formula"]
    assert m["difference_checks"] == 24 ** 2
    assert m["involution_count"] == 1
    assert m["center_order"] == 2
    assert m["smallgroup_repo_crosscheck"] == "[48,28]"
    assert m["order_spectrum"] == {
        "1": 1, "2": 1, "3": 8, "4": 18, "6": 8, "8": 12
    }
def test_mu4_cochain_converts_projective_cocycles():
    m = load()["mu4_converter"]
    assert m["all_pair_checks"] == 24 ** 2
    assert "i^epsilon" in m["cochains"]["plus"]
    assert "(-i)^epsilon" in m["cochains"]["minus"]
    assert "cohomologous" in m["cohomology_statement"]
    assert "remain nonisomorphic" in m["abstract_group_boundary"]


def test_missing_clock_modes_are_square_roots_of_sign_on_c4():
    c = load()["clock_C4_square_root"]
    assert c["projective_clock_order"] == 4
    assert c["permutation_parity_word"] == [0, 1, 0, 1]
    assert c["chi_plus_values"] == ["1", "i", "-1", "-i"]
    assert c["chi_minus_values"] == ["1", "-i", "-1", "i"]
    assert c["square_equals_sign_character"] is True
    assert c["pass10954_missing_C8_characters"] == [2, 6]
    assert c["pass10954_missing_phase_values"] == ["+i", "-i"]
def test_albert_bridge_keeps_matrix_intertwiner_open():
    a = load()["albert_cover_bridge"]
    assert "plus cover" in a["clock"]
    assert "squares to the central -1" in a["pass10956"]
    assert "epsilon cup epsilon" in a["resolution"]
    assert "no matrix intertwiner" in a["remaining_gap"]


def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10957-mu4-schur-cover"') == 1
    assert tail.count("PASS10957_MU4_SCHUR_COVER_CONVERTER_INSERT}%") == 1
