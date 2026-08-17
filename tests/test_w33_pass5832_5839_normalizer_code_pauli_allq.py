from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS5832_5839_NORMALIZER_CODE_PAULI_ALLQ.json"
PRODUCER = ROOT / "analysis" / "w33_pass5832_5839_normalizer_code_pauli_allq.py"


def test_pass5832_5839_producer_replays_frozen_certificate() -> None:
    expected = json.loads(CERT.read_text())
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True, capture_output=True, text=True)
    actual = json.loads(CERT.read_text())
    assert actual == expected


def test_pass5832_normalizer_and_pass5838_rook_are_same_1152() -> None:
    d = json.loads(CERT.read_text())
    n = d["pass_5832_full_normalizer"]
    r = d["pass_5838_unit_cayley_rook_graph"]
    assert n["full_S16_normalizer_order"] == 1152
    assert n["normalizer_quotient"] == "C2"
    assert r["full_automorphism_order"] == 1152
    assert r["equals_affine_normalizer_from_pass5832"] is True


def test_pass5833_code_and_pass5839_puncture_close_objectwise() -> None:
    d = json.loads(CERT.read_text())
    c = d["pass_5833_code_snf_interface"]
    s = d["pass_5839_simplex_line_puncture"]
    assert c["reye_binary_code"] == [12, 4, 6]
    assert c["weight_enumerator"] == {"0": 1, "6": 12, "8": 3}
    assert c["minimum_weight_words_equal_heavy_six_sets"] is True
    assert c["saturated_R_mod2_nullity"] == 4
    assert c["saturated_R_2adic_cokernel_valuation"] == 6
    assert s["punctured_code_equal_reye_kernel_objectwise"] is True


def test_pass5834_pauli_bridge_is_object_level_but_scoped() -> None:
    d = json.loads(CERT.read_text())
    p = d["pass_5834_two_qubit_object_isometry"]
    assert p["number_of_linear_quadratic_isometries"] == 72
    assert p["rank_one_maps_exactly_to_C7_C15"] is True
    assert p["units_map_exactly_to_C1_C6"] is True
    assert p["all_105_polar_commutation_pairs_preserved"] is True
    assert p["rank_one_grid_rows_and_columns_commute"] is True
    assert "does not identify" in p["interpretation"]


def test_pass5835_anchor_census_and_pass5837_bent_identity() -> None:
    d = json.loads(CERT.read_text())
    a = d["pass_5835_all_field_matrix_fourier_radon"]["prime_anchor_exact_replays"]
    assert a["2"]["rank_label_counts"] == {"0": 1, "1": 9, "2": 6}
    assert a["3"]["rank_label_counts"] == {"0": 1, "1": 32, "2": 48}
    assert a["5"]["rank_label_counts"] == {"0": 1, "1": 144, "2": 480}
    assert a["7"]["rank_label_counts"] == {"0": 1, "1": 384, "2": 2016}
    b = d["pass_5837_determinant_bent_chirp"]
    assert b["is_bent"] is True and b["is_self_dual"] is True
    assert b["walsh_distribution"] == {"+4": 10, "-4": 6}
