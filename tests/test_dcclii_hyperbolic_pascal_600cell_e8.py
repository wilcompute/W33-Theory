"""Part DCCLII -- Hyperbolic Pascal / 600-cell / E_8 tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclii_hyperbolic_pascal_600cell_e8 import (  # noqa: E402
    CELL_600,
    E_W33,
    G_EIGEN,
    HPS_LEVELS,
    K,
    MU,
    OUT_PATH,
    PHI3,
    PHI4,
    PHI6,
    Q,
    QP1,
    V,
    build_bridge,
    cell_600_w33_divisions,
    e8_as_two_600_cells,
    fibonacci,
    hps_dictionary,
    pascal_row,
    polytope_tower,
    row_4_polytope_reading,
    row_7_palindrome,
    write_bridge,
)


def test_hps_levels_first_six():
    assert HPS_LEVELS == [1, 4, 10, 26, 89, 534]


def test_hps_level_1_eq_mu():
    assert HPS_LEVELS[1] == MU == QP1 == 4


def test_hps_level_2_eq_phi_4():
    assert HPS_LEVELS[2] == PHI4 == 10


def test_hps_level_3_eq_2_phi_3():
    assert HPS_LEVELS[3] == 2 * PHI3 == 26


def test_hps_level_3_eq_d_bosonic():
    # D_bosonic from DCCXXVI = 26
    assert HPS_LEVELS[3] == 26


def test_hps_level_4_eq_fibonacci_11():
    assert HPS_LEVELS[4] == fibonacci(11) == 89


def test_hps_fibonacci_index_eq_k_minus_one():
    assert 11 == K - 1


def test_600_cell_V_is_5_factorial():
    assert CELL_600["V"] == math.factorial(5) == 120


def test_600_cell_E_is_6_factorial():
    assert CELL_600["E"] == math.factorial(6) == 720


def test_600_cell_V_over_q_is_w33_v():
    assert CELL_600["V"] // Q == V == 40


def test_600_cell_E_over_q_is_w33_E():
    assert CELL_600["E"] // Q == E_W33 == 240


def test_600_cell_C_over_v_is_g():
    assert CELL_600["C"] // V == G_EIGEN == 15


def test_e8_is_two_600_cells():
    info = e8_as_two_600_cells()
    assert info["match"] is True
    assert info["E_8_root_count"] == 240
    assert info["two_600_cells"] == 240


def test_pascal_row_4_tetrahedron():
    row = pascal_row(MU)
    assert row == [1, 4, 6, 4, 1]
    assert row[2] == math.factorial(Q) == 6  # central = q!


def test_pascal_row_4_eval_at_phi_4_is_11_to_4():
    r = row_4_polytope_reading()
    assert r["matches_k_minus_one_to_mu"] is True
    assert r["evaluated_at_Phi_4"] == 11 ** 4 == 14641


def test_pascal_row_7_palindrome():
    row = pascal_row(PHI6)
    assert row == [1, 7, 21, 35, 35, 21, 7, 1]
    assert row == row[::-1]


def test_pascal_row_7_eval_at_phi_4_is_11_to_phi_6():
    r = row_7_palindrome()
    assert r["matches_k_minus_one_to_Phi_6"] is True
    assert r["evaluated_at_Phi_4"] == 11 ** PHI6 == 11 ** 7


def test_csaszar_szilassi_pairs_in_row_7():
    """Palindrome pairs C(7,k) = C(7, 7-k)."""
    r = row_7_palindrome()
    pairs = r["palindrome_pairs"]
    for a, b in pairs:
        assert a == b


def test_polytope_tower_has_9_polytopes():
    t = polytope_tower()
    assert len(t) == 9


def test_polytope_tower_includes_600_cell():
    t = polytope_tower()
    found = [p for p in t if "600-cell" in p["polytope"]]
    assert len(found) == 1
    assert found[0]["f_vector"] == [120, 720, 1200, 600]


def test_600_cell_divisions():
    divs = cell_600_w33_divisions()
    assert len(divs) >= 5


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_hps_dictionary_has_6_entries():
    d = hps_dictionary()
    assert len(d) == 6


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Hyperbolic Pascal" in b["theorem"]
    assert "HPS" in b["one_line"]


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
        "hyperbolic_pascal_simplex",
        "600_cell_w33_divisions",
        "600_cell_factorial_form",
        "e8_as_two_600_cells",
        "pascal_row_4_tetrahedron",
        "pascal_row_7_csaszar_szilassi_palindrome",
        "polytope_tower_at_q_3",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
