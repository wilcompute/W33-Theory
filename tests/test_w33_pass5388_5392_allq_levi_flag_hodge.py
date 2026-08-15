from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_pass5388_5392_allq_levi_flag_hodge.py"
FROZEN = ROOT / "data/PART_W33_PASS5388_5392_ALLQ_LEVI_FLAG_HODGE.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass5388_allq_levi", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_anchor_formulas_and_q3_specialization():
    m = load_module()
    for q in [2, 3, 4, 5, 7, 8, 9, 11, 13]:
        row = m.theorem_row(q)
        assert row["distance_shells"] == [1, 2*q, 2*q*q, 2*q**3, q**4]
        assert row["levi_cycle_rank"] == q**4
        assert row["terminal_P_row"] == ["1", "-2", "2", "-2", "1"]
        assert row["terminal_Q_column"] == [str(q**4), str(-q**3), str(q**2), str(-q), "1"]
    q3 = m.theorem_row(3)
    assert q3["flags_linegraph_vertices"] == 160
    assert q3["distance_shells"] == [1, 6, 18, 54, 81]
    assert q3["terminal_Q_column"] == ["81", "-27", "9", "-3", "1"]


def test_frozen_certificate_load_bearing_claims():
    data = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert data["status"] == "THEOREM_ALGEBRAIC_AND_GRAPH_THEORETIC"
    assert data["distance_theorem"]["intersection_array"] == "{2q,q,q,q ; 1,1,1,2}"
    assert data["hodge_bridge"]["cycle_dimension"] == "q^4"
    assert data["hodge_bridge"]["terminal_first_eigenmatrix_row"] == ["1", "-2", "2", "-2", "1"]
    assert data["hodge_bridge"]["terminal_second_eigenmatrix_column"] == ["q^4", "-q^3", "q^2", "-q", "1"]
    assert data["w33_specialization"]["projector_numerator"] == [81, -27, 9, -3, 1]


def test_characteristic_polynomial_factorization_for_many_q():
    m = load_module()
    for q in range(2, 40):
        assert m.quotient_charpoly(q) == m.expected_charpoly(q)
