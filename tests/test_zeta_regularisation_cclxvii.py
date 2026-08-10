"""
Tests for Part CCLXVII — Zeta Regularisation and the Tomotope Covering Tower.

Covers all 38 bridge identities plus JSON output validation.
"""

from __future__ import annotations

import importlib
import json
import sys
from fractions import Fraction
from math import factorial
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import the bridge module
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BRIDGE = importlib.import_module(
    "exploration.PART_CCLXVII_ZETA_REGULARISATION_BRIDGE"
)

# ---------------------------------------------------------------------------
# Section 1: ζ(-1) = -1/12 and W33 valency
# ---------------------------------------------------------------------------

def test_B01_zeta_neg1_is_neg1_over_12():
    assert BRIDGE.ZETA_NEG1 == Fraction(-1, 12)


def test_B02_zeta_neg1_denominator_eq_K():
    assert BRIDGE.ZETA_NEG1.denominator == BRIDGE.K


def test_B03_zeta_neg1_denominator_eq_TE():
    assert BRIDGE.ZETA_NEG1.denominator == BRIDGE.TE


def test_B04_B2_eq_one_sixth():
    assert BRIDGE.bernoulli(2) == Fraction(1, 6)


def test_B05_zeta_neg1_eq_neg_B2_over_2():
    assert BRIDGE.ZETA_NEG1 == -BRIDGE.bernoulli(2) / 2


# ---------------------------------------------------------------------------
# Section 2: Bosonic string critical dimension
# ---------------------------------------------------------------------------

def test_B06_D_bos_eq_26():
    assert BRIDGE.D_BOS == 26


def test_B07_D_bos_eq_M_LAM_minus1():
    assert BRIDGE.D_BOS == BRIDGE.M_LAM - 1


def test_B08_D_sup_eq_10():
    assert BRIDGE.D_SUP == 10


def test_B09_D_sup_eq_LAP_MID():
    assert BRIDGE.D_SUP == BRIDGE.LAP_MID


def test_B10_D_bos_minus_D_sup_eq_TF():
    assert BRIDGE.D_BOS - BRIDGE.D_SUP == BRIDGE.TF


def test_B11_D_bos_minus_D_sup_eq_LAP_TOP():
    assert BRIDGE.D_BOS - BRIDGE.D_SUP == BRIDGE.LAP_TOP


def test_B12_N_trans_bos_eq_2K():
    assert BRIDGE.N_TRANS_BOS == 2 * BRIDGE.K


def test_B13_N_trans_bos_eq_24():
    assert BRIDGE.N_TRANS_BOS == 24


def test_B14_casimir_bos_eq_neg2():
    assert BRIDGE.casimir_bos == -2


def test_B15_casimir_bos_eq_neg_LAM():
    assert BRIDGE.casimir_bos == -BRIDGE.LAM


def test_B16_N_trans_sup_eq_2_MU():
    assert BRIDGE.N_TRANS_SUP == 2 * BRIDGE.MU


def test_B17_N_trans_sup_eq_8():
    assert BRIDGE.N_TRANS_SUP == 8


# ---------------------------------------------------------------------------
# Section 3: Tomotope χ = 0 → infinite covering tower
# ---------------------------------------------------------------------------

def test_B18_chi_tomotope_eq_0():
    assert BRIDGE.chi_tomotope == 0


def test_B19_T_FLAGS_eq_TE_times_TF():
    assert BRIDGE.T_FLAGS == BRIDGE.TE * BRIDGE.TF


def test_B20_zeta_neg1_times_T_FLAGS_eq_neg_TF():
    assert BRIDGE.zeta_flags == -BRIDGE.TF


def test_B21_zeta_neg1_times_T_FLAGS_eq_neg_LAP_TOP():
    assert BRIDGE.zeta_flags == -BRIDGE.LAP_TOP


def test_B22_abs_zeta_neg1_times_K_eq_unity():
    assert abs(BRIDGE.ZETA_NEG1) * BRIDGE.K == 1


def test_B23_string_tachyon_numerator_eq_1():
    assert abs(BRIDGE.ZETA_NEG1.numerator) == 1


# ---------------------------------------------------------------------------
# Section 4: Euler-Maclaurin 3D-discrete ↔ 4D-continuous
# ---------------------------------------------------------------------------

def test_B24_EM_correction_eq_1over12():
    assert BRIDGE.EM_correction == Fraction(1, 12)


def test_B25_EM_correction_denominator_eq_K():
    assert BRIDGE.EM_correction.denominator == BRIDGE.K


def test_B26_EM_correction_denominator_eq_TE():
    assert BRIDGE.EM_correction.denominator == BRIDGE.TE


def test_B27_EM_correction_eq_neg_zeta_neg1():
    assert BRIDGE.EM_correction == -BRIDGE.ZETA_NEG1


def test_B28_discrete_sum_V_eq_820():
    assert BRIDGE.sum_V == 820


def test_B29_continuous_integral_V_eq_800():
    assert BRIDGE.int_V == 800


def test_B30_sum_minus_integral_eq_V_half():
    assert BRIDGE.sum_V - BRIDGE.int_V == BRIDGE.V // 2


# ---------------------------------------------------------------------------
# Section 5: Zeta values and W33 parameters
# ---------------------------------------------------------------------------

def test_B31_zeta_0_eq_neg_half():
    assert BRIDGE.ZETA_0 == Fraction(-1, 2)


def test_B32_neg_zeta_0_times_K_eq_LAM_Q():
    assert -BRIDGE.ZETA_0 * BRIDGE.K == BRIDGE.LAM * BRIDGE.Q


def test_B33_zeta_neg3_eq_1over120():
    assert BRIDGE.ZETA_NEG3 == Fraction(1, 120)


def test_B34_zeta_neg3_denominator_eq_V_Q():
    assert BRIDGE.ZETA_NEG3.denominator == BRIDGE.V * BRIDGE.Q


# ---------------------------------------------------------------------------
# Section 6: 3D-discrete → 4D-continuous dimension jump
# ---------------------------------------------------------------------------

def test_B35_PG33_point_count_eq_V():
    assert BRIDGE.points_PG33 == BRIDGE.V


def test_B36_TV_eq_Q_plus_1():
    assert BRIDGE.TV == BRIDGE.Q + 1


def test_B37_dim_jump_discrete_to_continuous():
    assert BRIDGE.dim_jump == 1


def test_B38_dim_jump_eq_LAM_minus_1():
    assert BRIDGE.dim_jump == BRIDGE.LAM - 1


# ---------------------------------------------------------------------------
# Aggregate: all 38 bridge checks pass
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

JSON_PATH = ROOT / "PART_CCLXVII_zeta_regularisation_results.json"


def test_json_file_exists():
    assert JSON_PATH.exists(), f"Missing {JSON_PATH.name}"


def test_json_verified_true():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["verified"] is True


def test_json_checks_passed_38():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["checks_passed"] == 38
    assert data["checks_total"] == 38


def test_json_zeta_neg1_value():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["zeta_values"]["zeta(-1)"] == "-1/12"


def test_json_bosonic_D_crit():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["bosonic_string"]["D_crit"] == 26


def test_json_tomotope_chi_zero():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["tomotope"]["chi"] == 0


def test_json_casimir_eq_neg_lam():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    assert data["bosonic_string"]["casimir_eq_neg_LAM"] is True
