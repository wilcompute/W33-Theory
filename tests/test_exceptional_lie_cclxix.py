"""
Tests for Part CCLXIX — Exceptional Lie Algebras and the W(3,3) Arithmetic Atlas.

Covers all 38 bridge identities plus JSON output validation.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import the bridge module
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BRIDGE = importlib.import_module(
    "exploration.PART_CCLXIX_EXCEPTIONAL_LIE_BRIDGE"
)

# ---------------------------------------------------------------------------
# Section 1: G₂
# ---------------------------------------------------------------------------

def test_B01_dim_G2_eq_LAM_times_Phi6():
    assert BRIDGE.G2["dim"] == BRIDGE.LAM * BRIDGE.PHI6


def test_B02_rank_G2_eq_LAM():
    assert BRIDGE.G2["rank"] == BRIDGE.LAM


def test_B03_h_G2_eq_LAM_times_Q():
    assert BRIDGE.G2["h"] == BRIDGE.LAM * BRIDGE.Q


def test_B04_hv_G2_eq_MU():
    assert BRIDGE.G2["hv"] == BRIDGE.MU


def test_B05_roots_G2_eq_K():
    assert BRIDGE.G2["roots"] == BRIDGE.K


def test_B06_h_plus_hv_G2_eq_LAP_MID():
    assert BRIDGE.G2["h"] + BRIDGE.G2["hv"] == BRIDGE.LAP_MID


# ---------------------------------------------------------------------------
# Section 2: F₄
# ---------------------------------------------------------------------------

def test_B07_dim_F4_eq_V_plus_LAP_MID_plus_LAM():
    assert BRIDGE.F4["dim"] == BRIDGE.V + BRIDGE.LAP_MID + BRIDGE.LAM


def test_B07b_dim_F4_eq_MU_times_Phi3():
    assert BRIDGE.F4["dim"] == BRIDGE.MU * BRIDGE.PHI3


def test_B08_rank_F4_eq_MU():
    assert BRIDGE.F4["rank"] == BRIDGE.MU


def test_B09_h_F4_eq_K():
    assert BRIDGE.F4["h"] == BRIDGE.K


def test_B10_hv_F4_eq_Q_squared():
    assert BRIDGE.F4["hv"] == BRIDGE.Q ** 2


def test_B11_roots_F4_eq_MU_times_K():
    assert BRIDGE.F4["roots"] == BRIDGE.MU * BRIDGE.K


def test_B12_hv_G2_plus_hv_F4_eq_Phi3():
    assert BRIDGE.G2["hv"] + BRIDGE.F4["hv"] == BRIDGE.PHI3


# ---------------------------------------------------------------------------
# Section 3: E₆
# ---------------------------------------------------------------------------

def test_B13_dim_E6_eq_LAM_Q_Phi3():
    assert BRIDGE.E6["dim"] == BRIDGE.LAM * BRIDGE.Q * BRIDGE.PHI3


def test_B14_rank_E6_eq_LAM_times_Q():
    assert BRIDGE.E6["rank"] == BRIDGE.LAM * BRIDGE.Q


def test_B15_h_E6_eq_K():
    assert BRIDGE.E6["h"] == BRIDGE.K


def test_B16_hv_E6_eq_K():
    assert BRIDGE.E6["hv"] == BRIDGE.K


def test_B17_roots_E6_eq_K_LAM_Q():
    assert BRIDGE.E6["roots"] == BRIDGE.K * BRIDGE.LAM * BRIDGE.Q


def test_B18_W_order_E6_eq_AUT_ORDER():
    assert BRIDGE.E6["W_order"] == BRIDGE.AUT_ORDER


# ---------------------------------------------------------------------------
# Section 4: E₇
# ---------------------------------------------------------------------------

def test_B19_dim_E7_eq_VQ_plus_Phi3():
    assert BRIDGE.E7["dim"] == BRIDGE.V * BRIDGE.Q + BRIDGE.PHI3


def test_B20_rank_E7_eq_Phi6():
    assert BRIDGE.E7["rank"] == BRIDGE.PHI6


def test_B21_h_E7_eq_K_plus_MU_plus_LAM():
    assert BRIDGE.E7["h"] == BRIDGE.K + BRIDGE.MU + BRIDGE.LAM


def test_B22_roots_E7_eq_LAM_Q2_Phi6():
    assert BRIDGE.E7["roots"] == BRIDGE.LAM * BRIDGE.Q**2 * BRIDGE.PHI6


def test_B23_dim_E7_plus_rank_E7_eq_LAP_MID_times_dim_G2():
    assert BRIDGE.E7["dim"] + BRIDGE.E7["rank"] == BRIDGE.LAP_MID * BRIDGE.G2["dim"]


def test_B24_hv_E7_eq_K_plus_MU_plus_LAM():
    assert BRIDGE.E7["hv"] == BRIDGE.K + BRIDGE.MU + BRIDGE.LAM


# ---------------------------------------------------------------------------
# Section 5: E₈
# ---------------------------------------------------------------------------

def test_B25_roots_E8_eq_EDGES():
    assert BRIDGE.E8["roots"] == BRIDGE.EDGES


def test_B26_dim_E8_eq_EDGES_plus_2MU():
    assert BRIDGE.E8["dim"] == BRIDGE.EDGES + 2 * BRIDGE.MU


def test_B27_rank_E8_eq_2MU():
    assert BRIDGE.E8["rank"] == 2 * BRIDGE.MU


def test_B28_h_E8_eq_LAP_MID_times_Q():
    assert BRIDGE.E8["h"] == BRIDGE.LAP_MID * BRIDGE.Q


def test_B29_dim_E8_div_rank_E8_eq_V_minus_Q2():
    assert BRIDGE.E8["dim"] // BRIDGE.E8["rank"] == BRIDGE.V - BRIDGE.Q**2


def test_B30_roots_plus_rank_E8_eq_dim_E8():
    assert BRIDGE.E8["roots"] + BRIDGE.E8["rank"] == BRIDGE.E8["dim"]


# ---------------------------------------------------------------------------
# Section 6: Coxeter number sums
# ---------------------------------------------------------------------------

def test_B31_sum_h_all_5_eq_dim_E6():
    total_h = (BRIDGE.G2["h"] + BRIDGE.F4["h"] + BRIDGE.E6["h"]
               + BRIDGE.E7["h"] + BRIDGE.E8["h"])
    assert total_h == BRIDGE.E6["dim"]


def test_B32_sum_h_eq_LAM_Q_Phi3():
    total_h = (BRIDGE.G2["h"] + BRIDGE.F4["h"] + BRIDGE.E6["h"]
               + BRIDGE.E7["h"] + BRIDGE.E8["h"])
    assert total_h == BRIDGE.LAM * BRIDGE.Q * BRIDGE.PHI3


def test_B33_h_E_series_eq_VQ_over_2():
    assert (BRIDGE.E6["h"] + BRIDGE.E7["h"] + BRIDGE.E8["h"]
            == BRIDGE.V * BRIDGE.Q // 2)


def test_B34_rank_E_series_eq_K_plus_Q_plus_MU_plus_LAM():
    rank_sum = BRIDGE.E6["rank"] + BRIDGE.E7["rank"] + BRIDGE.E8["rank"]
    assert rank_sum == BRIDGE.K + BRIDGE.Q + BRIDGE.MU + BRIDGE.LAM


def test_B35_h_F4_eq_h_E6_eq_K():
    assert BRIDGE.F4["h"] == BRIDGE.E6["h"] == BRIDGE.K


# ---------------------------------------------------------------------------
# Section 7: j-invariant and Moonshine
# ---------------------------------------------------------------------------

def test_B36_j_i_eq_K_cubed():
    assert BRIDGE.J_I == BRIDGE.K ** 3


def test_B37_AUT_ORDER_eq_j_i_times_h_E8():
    assert BRIDGE.AUT_ORDER == BRIDGE.J_I * BRIDGE.E8["h"]


def test_B38_744_eq_V_minus_Q2_times_2K():
    assert BRIDGE.J_CONST == (BRIDGE.V - BRIDGE.Q**2) * (2 * BRIDGE.K)


# ---------------------------------------------------------------------------
# Cross-cutting: numerical values
# ---------------------------------------------------------------------------

def test_sum_h_value_is_78():
    total_h = (BRIDGE.G2["h"] + BRIDGE.F4["h"] + BRIDGE.E6["h"]
               + BRIDGE.E7["h"] + BRIDGE.E8["h"])
    assert total_h == 78


def test_dim_E6_is_78():
    assert BRIDGE.E6["dim"] == 78


def test_j_i_value_is_1728():
    assert BRIDGE.J_I == 1728


def test_moonshine_constant_is_744():
    assert BRIDGE.J_CONST == 744


def test_AUT_ORDER_value():
    assert BRIDGE.AUT_ORDER == 51_840


# ---------------------------------------------------------------------------
# Aggregate checks
# ---------------------------------------------------------------------------

def test_all_38_bridge_checks_pass():
    failed = [lbl for lbl, v in BRIDGE.checks if not v]
    assert failed == [], f"Failed checks: {failed}"


def test_checks_count_is_38():
    assert len(BRIDGE.checks) == 38


def test_verified_flag_is_true():
    assert BRIDGE.VERIFIED is True


# ---------------------------------------------------------------------------
# JSON output validation
# ---------------------------------------------------------------------------

JSON_PATH = ROOT / "PART_CCLXIX_exceptional_lie_results.json"


def test_json_file_exists():
    assert JSON_PATH.exists(), f"Missing {JSON_PATH.name}"


def test_json_verified_true():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["verified"] is True


def test_json_checks_passed_38():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["checks_passed"] == 38
    assert data["checks_total"] == 38


def test_json_j_i_eq_K_cubed():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["j_invariant"]["j_i"] == 1728
    assert data["j_invariant"]["j_i_eq_K_cubed"] is True


def test_json_W_E6_eq_AUT_ORDER():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["E6"]["W_order"] == 51840
    assert data["E6"]["W_order_eq_AUT_ORDER"] is True


def test_json_E8_roots_eq_EDGES():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["E8"]["roots"] == 240
    assert data["E8"]["roots_eq_EDGES"] is True


def test_json_sum_h_eq_dim_E6():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["coxeter_sums"]["sum_h_all_5"] == 78
    assert data["coxeter_sums"]["sum_h_eq_dim_E6"] is True
