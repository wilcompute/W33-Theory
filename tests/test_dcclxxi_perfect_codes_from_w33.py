"""Part DCCLXXI -- Perfect codes (Hamming, Golay) from W(3,3) tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxxi_perfect_codes_from_w33 import (  # noqa: E402
    F_EIGEN,
    G_EIGEN,
    K,
    MU,
    OUT_PATH,
    Q,
    SPREAD_COUNT,
    V,
    binary_golay,
    binary_hamming_3,
    binary_hamming_4,
    build_bridge,
    steiner_systems,
    ternary_golay,
    ternary_hamming_4,
    write_bridge,
)


def test_ternary_hamming_n_eq_v():
    h = ternary_hamming_4()
    assert h["n"] == V == 40


def test_ternary_hamming_k_eq_spread_count():
    h = ternary_hamming_4()
    assert h["k"] == SPREAD_COUNT == 36 == math.comb(Q ** 2, 2)


def test_ternary_hamming_d_eq_q():
    h = ternary_hamming_4()
    assert h["d"] == Q == 3


def test_ternary_golay_G12_n_k_d():
    g = ternary_golay()
    assert g["G_12"]["n"] == K == 12
    assert g["G_12"]["k"] == math.factorial(Q) == 6
    assert g["G_12"]["d"] == math.factorial(Q) == 6


def test_ternary_golay_perfect():
    g = ternary_golay()
    assert g["perfect"] is True
    assert g["unique_perfect_ternary"] is True


def test_M_12_order():
    g = ternary_golay()
    assert g["M_12_order"] == 95040


def test_binary_hamming_3_n_k_d():
    h = binary_hamming_3()
    assert h["n"] == 7 == Q + (Q + 1)   # Heawood
    assert h["k"] == 4 == MU
    assert h["d"] == 3 == Q


def test_binary_hamming_4_n_k_d():
    h = binary_hamming_4()
    assert h["n"] == 15 == G_EIGEN
    assert h["k"] == 11 == K - 1
    assert h["d"] == 3 == Q


def test_binary_golay_G24_n_k_d():
    g = binary_golay()
    assert g["G_24"]["n"] == 24 == F_EIGEN
    assert g["G_24"]["k"] == 12 == K
    assert g["G_24"]["d"] == 8 == 2 ** Q


def test_binary_golay_perfect():
    g = binary_golay()
    assert g["perfect"] is True
    assert g["unique_perfect_binary"] is True


def test_M_24_order():
    g = binary_golay()
    assert g["M_24_order"] == 244823040


def test_steiner_S_5_6_12():
    s = steiner_systems()
    s_512 = next(r for r in s if r["name"] == "S(5, 6, 12)")
    assert s_512["transitivity"] == 5 == Q + 2
    assert s_512["block_size"] == 6 == math.factorial(Q)
    assert s_512["length"] == 12 == K


def test_steiner_S_5_8_24():
    s = steiner_systems()
    s_824 = next(r for r in s if r["name"] == "S(5, 8, 24)")
    assert s_824["transitivity"] == 5 == Q + 2
    assert s_824["block_size"] == 8 == 2 ** Q
    assert s_824["length"] == 24 == F_EIGEN


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Perfect-Codes" in b["theorem"]
    assert "Golay" in b["one_line"]


def test_honesty_boundary_explicit():
    b = build_bridge()
    boundary = b["honesty_boundary"].lower()
    assert "does not" in boundary


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
        "ternary_hamming_Ham_4_F_3",
        "ternary_golay",
        "binary_hamming_Ham_3_F_2",
        "binary_hamming_Ham_4_F_2",
        "binary_golay",
        "steiner_systems",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
