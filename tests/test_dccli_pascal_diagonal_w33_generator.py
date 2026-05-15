"""Part DCCLI -- Pascal diagonal W(3,3) generator tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccli_pascal_diagonal_w33_generator import (  # noqa: E402
    K,
    OUT_PATH,
    Q,
    T,
    V,
    build_bridge,
    exceptional_coxeter_ladder,
    exceptional_coxeter_sum_identities,
    fibonacci,
    seventh_overdetermination,
    triangular_dictionary,
    write_bridge,
)


def test_T_3_is_q_factorial():
    assert T(3) == math.factorial(Q) == 6


def test_T_5_is_g_eigen_mult():
    assert T(5) == 15


def test_T_6_is_csaszar_edges():
    assert T(6) == 21


def test_T_8_is_spread_count():
    assert T(8) == math.comb(Q ** 2, 2) == 36


def test_T_9_is_antiline_count():
    assert T(9) == math.comb(Q ** 2 + 1, 2) == 45


def test_T_11_is_C_k_2():
    assert T(11) == math.comb(K, 2) == 66


def test_T_12_is_dim_E6():
    assert T(12) == 78


def test_T_15_is_V_600cell():
    assert T(15) == 120 == math.factorial(5)


def test_121_is_v_plus_q4():
    assert 121 == V + Q ** 4


def test_121_is_k_minus_one_squared():
    assert 121 == (K - 1) ** 2


def test_seventh_overdetermination_at_q_3():
    r = seventh_overdetermination(3)
    assert r["vanishes"] is True
    assert r["gap"] == 0


def test_seventh_overdetermination_fails_for_q_neq_3():
    for q in (2, 4, 5):
        r = seventh_overdetermination(q)
        assert r["vanishes"] is False


def test_h_G2_is_q_factorial():
    ladder = exceptional_coxeter_ladder()
    h_G2 = next(r for r in ladder if r["algebra"] == "G_2")["h"]
    assert h_G2 == math.factorial(Q) == 6


def test_h_F4_is_k():
    ladder = exceptional_coxeter_ladder()
    h_F4 = next(r for r in ladder if r["algebra"] == "F_4")["h"]
    assert h_F4 == K == 12


def test_h_E6_equals_h_F4():
    ladder = exceptional_coxeter_ladder()
    h_E6 = next(r for r in ladder if r["algebra"] == "E_6")["h"]
    h_F4 = next(r for r in ladder if r["algebra"] == "F_4")["h"]
    assert h_E6 == h_F4 == K == 12


def test_h_E7_is_3_q_factorial():
    ladder = exceptional_coxeter_ladder()
    h_E7 = next(r for r in ladder if r["algebra"] == "E_7")["h"]
    assert h_E7 == 3 * math.factorial(Q) == 18


def test_h_E8_is_5_q_factorial():
    ladder = exceptional_coxeter_ladder()
    h_E8 = next(r for r in ladder if r["algebra"] == "E_8")["h"]
    assert h_E8 == 5 * math.factorial(Q) == 30


def test_fibonacci_multipliers_are_1_2_2_3_5():
    ladder = exceptional_coxeter_ladder()
    mults = [r["fibonacci_value"] for r in ladder]
    assert mults == [1, 2, 2, 3, 5]


def test_fibonacci_sum_eq_k_minus_one():
    # Distinct multipliers are 1, 2, 3, 5
    assert 1 + 2 + 3 + 5 == K - 1 == 11


def test_G2_E6_E7_E8_sum_eq_C_k_2():
    s = exceptional_coxeter_sum_identities()
    assert s["G2_E6_E7_E8_eq_C_k_2"] is True


def test_all_five_coxeter_sum_eq_dim_E6():
    s = exceptional_coxeter_sum_identities()
    assert s["all_five_eq_dim_E6"] is True


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_triangular_dictionary_has_15_entries():
    assert len(triangular_dictionary()) == 15


def test_fibonacci_function():
    assert fibonacci(1) == 1
    assert fibonacci(3) == 2
    assert fibonacci(4) == 3
    assert fibonacci(5) == 5


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Pascal Second Diagonal Theorem" in b["theorem"]
    assert "Pascal" in b["one_line"]


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
        "triangular_dictionary",
        "exceptional_coxeter_ladder",
        "exceptional_coxeter_sum_identities",
        "seventh_overdetermination_q_3",
        "seventh_overdetermination_scan",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
