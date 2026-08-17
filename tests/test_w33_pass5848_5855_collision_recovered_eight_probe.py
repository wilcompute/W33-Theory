from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS5848_5855_NORMALIZER_CODE_PAULI_ALLQ.json"
PRODUCER = ROOT / "analysis" / "w33_pass5848_5855_collision_recovered_eight_probe.py"


def test_corrected_producer_replays_frozen_certificate() -> None:
    expected = json.loads(CERT.read_text())
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True, capture_output=True, text=True)
    actual = json.loads(CERT.read_text())
    assert actual == expected
    assert actual["renumbered_from_contaminated_range"] == [5832, 5839]


def test_normalizer_and_rook_graph_are_same_1152() -> None:
    d = json.loads(CERT.read_text())
    n = d["pass_5848_full_normalizer"]
    r = d["pass_5854_unit_cayley_rook_graph"]
    assert n["full_S16_normalizer_order"] == 1152
    assert n["normalizer_quotient"] == "C2"
    assert r["full_automorphism_order"] == 1152
    assert r["equals_affine_normalizer_from_pass5848"] is True


def test_reye_heavy_code_and_simplex_puncture_close_objectwise() -> None:
    d = json.loads(CERT.read_text())
    c = d["pass_5849_code_snf_interface"]
    s = d["pass_5855_simplex_line_puncture"]
    assert c["reye_binary_code"] == [12, 4, 6]
    assert c["weight_enumerator"] == {"0": 1, "6": 12, "8": 3}
    assert c["minimum_weight_words_equal_heavy_six_sets"] is True
    assert c["saturated_R_mod2_nullity"] == 4
    assert c["saturated_R_2adic_cokernel_valuation"] == 6
    assert s["punctured_code_equal_reye_kernel_objectwise"] is True


def test_pauli_bridge_is_object_level_but_carrier_scoped() -> None:
    d = json.loads(CERT.read_text())
    p = d["pass_5850_two_qubit_object_isometry"]
    assert p["number_of_linear_quadratic_isometries"] == 72
    assert p["rank_one_maps_exactly_to_C7_C15"] is True
    assert p["units_map_exactly_to_C1_C6"] is True
    assert p["all_105_polar_commutation_pairs_preserved"] is True
    assert p["rank_one_grid_rows_and_columns_commute"] is True
    assert "does not identify" in p["interpretation"]


def test_all_field_anchors_and_bent_identity() -> None:
    d = json.loads(CERT.read_text())
    a = d["pass_5851_all_field_matrix_fourier_radon"]["prime_anchor_exact_replays"]
    assert a["2"]["rank_label_counts"] == {"0": 1, "1": 9, "2": 6}
    assert a["3"]["rank_label_counts"] == {"0": 1, "1": 32, "2": 48}
    assert a["5"]["rank_label_counts"] == {"0": 1, "1": 144, "2": 480}
    assert a["7"]["rank_label_counts"] == {"0": 1, "1": 384, "2": 2016}
    b = d["pass_5853_determinant_bent_chirp"]
    assert b["is_bent"] is True and b["is_self_dual"] is True
    assert b["walsh_distribution"] == {"+4": 10, "-4": 6}


def test_publication_packet_requires_corrected_namespace() -> None:
    d = json.loads(CERT.read_text())
    p = d["pass_5852_publication_front_doors"]
    tokens = {item[0] for item in p["cards_to_register_and_materialize"]}
    assert "pass-5848-5855-normalizer-code-pauli-allq" in tokens
    assert "pass-5832-5839-normalizer-code-pauli-allq" not in tokens
    assert p["stale_collision_card"] == "pass-5832-5839-normalizer-code-pauli-allq"
