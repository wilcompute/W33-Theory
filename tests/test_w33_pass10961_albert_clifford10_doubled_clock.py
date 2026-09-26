import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10961_albert_clifford10_doubled_clock.py"
CERT = ROOT / "data/w33_pass10961_albert_clifford10_doubled_clock.json"
MATS = ROOT / "data/w33_pass10961_albert_clifford9_gammas.json"


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
    assert load()["status"] == (
        "PASS_ALBERT_CL9_CL10_AND_CLOCK_GRADE_OBSTRUCTION"
    )


def test_albert_cl9_is_exact():
    x = load()["albert_cl9"]
    assert x["spatial_dimension"] == 9
    assert x["peirce_spinor_dimension"] == 16
    assert x["spatial_gram"] == "2 I9"
    assert x["gamma_count"] == 9
    assert x["clifford_relation"] == (
        "{gamma_i,gamma_j}=2 delta_ij I16"
    )
    assert x["bivector_span_dimension"] == 36


def test_doubled_cl10_has_expected_dimensions():
    x = load()["doubled_cl10"]
    assert x["carrier_dimension"] == 32
    assert x["vector_span_dimension"] == 10
    assert x["bivector_span_dimension"] == 45
    assert x["vector_plus_mixed_span_dimension"] == 19
    assert "Gamma_10=diag(I16,-I16)" in x["construction"]


def test_halfturn_is_exact_pi_rotation():
    x = load()["spin9_halfturn"]
    assert x["C9_orthogonal"] is True
    assert x["C9_determinant"] == 1
    assert x["C9_trace"] == 5
    assert x["C9_spectrum"] == {"+1": 7, "-1": 2}


def test_one_tick_is_clifford_vector_normalizer_obstruction():
    g = load()["doubled_clock_generator"]
    assert g["G_squared"] == "i Gamma_10"
    assert g["G_fourth"] == "-I32"
    assert g["G_eighth"] == "+I32"
    assert g["Gamma10_fixed"] is True
    assert "mixed bivectors" in g["one_tick_target_grade"]
    assert g["vector_span_plus_image_rank"] == 19

    o = load()["clifford_normalizer_obstruction"]
    assert o["full_C8_normalizes_vector_space"] is False
    assert o["intersection_dimension_with_one_tick_image"] == 1
    assert o["intersection"] == "span{Gamma_10}"
    assert o["two_ticks_normalize_vector_space"] is True
    assert o["two_tick_operator"] == "G^2=i Gamma_10"
    assert o["two_tick_O10_determinant"] == -1


def test_frozen_gamma_matrix_certificate():
    d = json.loads(MATS.read_text(encoding="utf-8"))
    assert d["field"] == "Q"
    assert len(d["gamma9"]) == 9
    assert all(len(M) == 16 for M in d["gamma9"])
    assert all(len(row) == 16 for M in d["gamma9"] for row in M)
    assert len(d["halfturn_vector_action_C9"]) == 9
    assert len(d["sha256"]) == 64


def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10961-albert-clifford10"') == 1
    assert tail.count(
        "PASS10961_ALBERT_CLIFFORD10_DOUBLED_CLOCK_INSERT}%"
    ) == 1
