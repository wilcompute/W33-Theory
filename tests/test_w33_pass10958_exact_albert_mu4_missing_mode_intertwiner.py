import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10958_exact_albert_mu4_missing_mode_intertwiner.py"
CERT = ROOT / "data/w33_pass10958_exact_albert_mu4_missing_mode_intertwiner.json"
INT = ROOT / "data/w33_pass10958_mu4_intertwiner_matrix.json"


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
    assert load()["status"] == "PASS_EXACT_ALBERT_MU4_MISSING_MODE_INTERTWINER"
def test_exact_halfturn_has_mu4_spectrum():
    x = load()["exact_albert_halfturn"]
    assert x["formula"] == "U=R/2 over Q"
    assert x["R_squared"] == "-4I16"
    assert x["U_squared"] == "-I16"
    assert x["U_fourth"] == "+I16"
    assert x["minimal_polynomial"] == "x^2+1"
    assert x["characteristic_polynomial"] == "(x^2+1)^8"
    assert x["plus_i_eigenspace_dimension"] == 8
    assert x["minus_i_eigenspace_dimension"] == 8


def test_missing_two_mode_module_is_exactly_embedded():
    c = load()["carrier_intertwiner"]
    assert c["field"] == "Q(i)"
    assert c["two_mode_embedding_rank"] == 2
    assert c["full_change_of_basis_rank"] == 16
    assert all(c["exact_relations"].values())
    assert "8 copies" in c["module_isomorphism"]
def test_chirality_pairs_plus_and_minus_i_modes():
    x = load()["chirality_exchange_reading"]
    assert x["exact_anticommutation"] == "U Chi = - Chi U"
    assert "+i Albert eigenvector" in x["paired_basis"]
    assert x["plus_i_intersection_with_chirality_plus"] == 0
    assert x["plus_i_intersection_with_chirality_minus"] == 0
    assert x["minus_i_intersection_with_chirality_plus"] == 0
    assert x["minus_i_intersection_with_chirality_minus"] == 0
    assert "not chirality eigenstates" in x["conclusion"]


def test_matter_parity_square_relation_is_shared():
    m = load()["matter_parity"]
    assert m["Albert_relation"] == "U^2=-I16"
    assert m["missing_module_relation"] == "A2^2=-I2"
    assert "2pi Spin(9)" in m["pass10950_reading"]
def test_pass10957_is_upgraded_from_phase_to_carrier():
    p = load()["pass10957_cover_converter"]
    assert p["mu4_square_roots"] == ["+i", "-i"]
    assert "explicit Q(i) carrier embedding" in p["new_upgrade"]
    assert "not the full GL(2,3)" in p["remaining_gap"]


def test_intertwiner_certificate_has_expected_shape():
    d = json.loads(INT.read_text(encoding="utf-8"))
    assert d["field"] == "Q(i)"
    assert len(d["two_column_embedding_W2"]) == 16
    assert all(len(row) == 2 for row in d["two_column_embedding_W2"])
    assert len(d["full_change_of_basis_W"]) == 16
    assert all(len(row) == 16 for row in d["full_change_of_basis_W"])
    assert "U W2 = W2 A2" in d["relations"]
def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10958-albert-mu4-intertwiner"') == 1
    assert tail.count(
        "PASS10958_EXACT_ALBERT_MU4_MISSING_MODE_INTERTWINER_INSERT}%"
    ) == 1
