"""Part DCCXXVII -- E_8 Cartan as tomotope tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxvii_e8_cartan_as_tomotope import (  # noqa: E402
    CODEC,
    HEAWOOD,
    OUT_PATH,
    Q,
    QP1,
    TOMOTOPE_F_VECTOR,
    build_bridge,
    cartan_invariants,
    e8_cartan_matrix,
    exceptional_coxeter_table,
    q3_reading_of_cartan_entries,
    tomotope_to_cartan_mapping,
    write_bridge,
)


def test_e8_cartan_is_8x8():
    A = e8_cartan_matrix()
    assert A.shape == (8, 8)


def test_diagonal_all_two():
    A = e8_cartan_matrix()
    for i in range(8):
        assert A[i, i] == 2


def test_off_diagonal_only_zero_or_minus_one():
    A = e8_cartan_matrix()
    vals = {int(A[i, j]) for i in range(8) for j in range(8) if i != j}
    assert vals == {0, -1}


def test_rank_8():
    inv = cartan_invariants(e8_cartan_matrix())
    assert inv["rank"] == 8


def test_trace_16():
    inv = cartan_invariants(e8_cartan_matrix())
    assert inv["trace"] == 16
    assert inv["trace"] == (Q + 1) ** 2 == 16


def test_trace_equals_tomotope_F():
    inv = cartan_invariants(e8_cartan_matrix())
    assert inv["trace"] == TOMOTOPE_F_VECTOR[2] == 16


def test_rank_equals_tomotope_C():
    inv = cartan_invariants(e8_cartan_matrix())
    assert inv["rank"] == TOMOTOPE_F_VECTOR[3] == 8


def test_sum_all_entries_is_2():
    inv = cartan_invariants(e8_cartan_matrix())
    assert inv["sum_all_entries"] == 2


def test_determinant_1():
    inv = cartan_invariants(e8_cartan_matrix())
    assert inv["determinant"] == 1


def test_dynkin_edges_7_equals_heawood():
    inv = cartan_invariants(e8_cartan_matrix())
    assert inv["dynkin_edge_count"] == HEAWOOD == 7


def test_off_diagonal_minus_one_is_2_cos_2pi_q():
    val = 2 * math.cos(2 * math.pi / Q)
    assert math.isclose(val, -1, abs_tol=1e-10)


def test_q3_reading_diagonal_value():
    r = q3_reading_of_cartan_entries()
    assert r["diagonal_value"] == 2
    assert r["off_diagonal_value"] == -1
    assert math.isclose(r["off_diagonal_evaluation_at_q_3"], -1, abs_tol=1e-10)


def test_tomotope_mapping_F_and_C_match():
    rows = tomotope_to_cartan_mapping()
    f_row = next(r for r in rows if r["tomotope_slot"] == "F")
    c_row = next(r for r in rows if r["tomotope_slot"] == "C")
    assert f_row["matches"] is True
    assert c_row["matches"] is True


def test_E6_coxeter_is_codec():
    tab = exceptional_coxeter_table()
    e6 = tab[0]
    assert e6["coxeter_number"] == CODEC == 12
    assert e6["rank"] == 6 == math.factorial(Q)


def test_E7_rank_is_heawood():
    tab = exceptional_coxeter_table()
    e7 = tab[1]
    assert e7["rank"] == HEAWOOD == 7


def test_E8_dim_is_240_plus_8():
    tab = exceptional_coxeter_table()
    e8 = tab[2]
    assert e8["dim"] == 240 + 8 == 248
    assert e8["num_roots"] == 240


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_eigenvalues_positive():
    """Cartan matrix of a Lie algebra is positive-definite (positive eigenvalues)."""
    A = e8_cartan_matrix()
    eigs = np.linalg.eigvalsh(A)
    for e in eigs:
        assert e > 0


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Cartan-Tomotope Theorem" in b["theorem"]
    assert "16" in b["one_line"]


def test_honesty_boundary_explicit():
    b = build_bridge()
    boundary = b["honesty_boundary"].lower()
    assert "structural" in boundary or "does not" in boundary


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "cartan_matrix",
        "cartan_invariants",
        "q3_reading",
        "tomotope_to_cartan_mapping",
        "exceptional_coxeter_table",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
