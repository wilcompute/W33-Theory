"""Part DCCLIX -- 24-cell / D_4 triality tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclix_24cell_d4_triality import (  # noqa: E402
    CELL_24,
    E_W33,
    F_EIGEN,
    K,
    OUT_PATH,
    Q,
    build_bridge,
    cell_24_w33_table,
    d4_triality_data,
    f_vector_total,
    polytope_chain_24_600_E8,
    write_bridge,
)


def test_24_cell_V_is_24():
    assert CELL_24["V"] == 24 == F_EIGEN


def test_24_cell_E_is_96():
    assert CELL_24["E"] == 96


def test_24_cell_F_eq_E_self_dual():
    assert CELL_24["E"] == CELL_24["F"] == 96


def test_24_cell_C_eq_V_self_dual():
    assert CELL_24["V"] == CELL_24["C"] == 24


def test_24_cell_E_eq_4_times_f():
    assert CELL_24["E"] == 4 * F_EIGEN == 96


def test_24_cell_E_eq_rank_E8_times_k():
    assert CELL_24["E"] == 8 * K == 96


def test_f_vector_sum_is_240():
    f = f_vector_total()
    assert f["sum"] == 240


def test_f_vector_sum_equals_E_W33():
    f = f_vector_total()
    assert f["eq_E_W33"] is True
    assert f["sum"] == E_W33 == 240


def test_f_vector_sum_equals_E8_roots():
    f = f_vector_total()
    assert f["eq_E_8_roots"] is True


def test_D_4_root_count_is_24():
    t = d4_triality_data()
    assert t["D_4_root_count"] == 24 == F_EIGEN
    assert t["D_4_root_count_eq_24_cell_V"] is True


def test_W_D_4_order_is_192():
    t = d4_triality_data()
    assert t["W_D_4_order"] == 192


def test_Out_D_4_is_S_3():
    t = d4_triality_data()
    assert t["Out_D_4_order"] == 6 == math.factorial(Q)


def test_W_F_4_eq_W_D_4_times_Out():
    t = d4_triality_data()
    assert t["W_F_4_eq_W_D4_times_Out_D4"] is True
    assert t["W_F_4_order"] == 192 * 6 == 1152


def test_polytope_chain_3_steps():
    chain = polytope_chain_24_600_E8()
    assert len(chain) == 3


def test_chain_vertex_counts_are_f_5f_10f():
    chain = polytope_chain_24_600_E8()
    assert [r["key_count"] for r in chain] == [24, 120, 240]
    assert 24 == F_EIGEN
    assert 120 == 5 * F_EIGEN
    assert 240 == 10 * F_EIGEN


def test_24_cell_w33_table_has_4_slots():
    table = cell_24_w33_table()
    assert len(table) == 4
    slots = [r["slot"] for r in table]
    assert slots == ["V", "E", "F", "C"]


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "24-cell" in b["theorem"]
    assert "240" in b["one_line"]


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
        "24_cell_data",
        "24_cell_w33_table",
        "f_vector_total_identity",
        "D_4_triality_data",
        "polytope_chain",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
