"""
Part CCXLII — L∞ Bracket Mass Hierarchy Closure
Regression tests for exploration/PART_CCXLII_LINFINITY_BRACKET_BRIDGE.py

Closes the OPEN problem in docs/STATUS_AND_GAPS.md:
  "L∞ Bracket Formalism Completion"
"""

import json
from fractions import Fraction
from pathlib import Path

from PART_CCXLII_LINFINITY_BRACKET_BRIDGE import (
    Q, V, K, LAM, MU, EDGES,
    Phi3, Phi4, Phi6,
    depth1_denom_form1, depth1_denom_form2, depth1_denom, ratio_c_over_t,
    depth2_num, depth2_denom, ratio_u_over_t,
    depth2_factor_1, depth2_factor_2, depth2_factor_3, depth2_factor_4, depth2_factor_5,
    pred_u_over_t, pred_c_over_t, obs_u_over_t, obs_c_over_t, rel_err_u, rel_err_c,
    chain_mt_over_mu, closure_mt_over_mu, closure_mt_over_mu_floor, truncation_factor,
    depths, num_depths, num_depth2_factors,
    checks, Verified,
)

ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------
# Master gate
# ------------------------------------------------------------------
def test_verified_true():
    assert Verified is True


def test_all_bridge_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == []


def test_bridge_check_count():
    assert len(checks) == 29


# ------------------------------------------------------------------
# SRG anchors
# ------------------------------------------------------------------
def test_srg_constants():
    assert (Q, V, K, LAM, MU, EDGES) == (3, 40, 12, 2, 4, 240)


# ------------------------------------------------------------------
# Cyclotomic values
# ------------------------------------------------------------------
def test_cyclotomics():
    assert Phi3 == 13
    assert Phi4 == 10
    assert Phi6 == 7


# ------------------------------------------------------------------
# Depth-1 closure (m_c / m_t)
# ------------------------------------------------------------------
def test_depth1_form1():
    assert depth1_denom_form1 == 136


def test_depth1_form2():
    assert depth1_denom_form2 == 136


def test_depth1_forms_equal():
    assert depth1_denom_form1 == depth1_denom_form2 == depth1_denom


def test_depth1_ratio_exact():
    assert ratio_c_over_t.numerator == 1
    assert ratio_c_over_t.denominator == 136


# ------------------------------------------------------------------
# Depth-2 closure (m_u / m_t)
# ------------------------------------------------------------------
def test_depth2_numerator():
    assert depth2_num == 39


def test_depth2_factors():
    assert [depth2_factor_1, depth2_factor_2, depth2_factor_3,
            depth2_factor_4, depth2_factor_5] == [512, 5, 7, 11, 17]


def test_depth2_denominator():
    assert depth2_denom == 3_351_040


def test_depth2_ratio_exact():
    assert ratio_u_over_t.numerator == 39
    assert ratio_u_over_t.denominator == 3_351_040


def test_depth2_factor_count_mu_plus_one():
    assert num_depth2_factors == MU + 1 == 5


# ------------------------------------------------------------------
# Observational proximity
# ------------------------------------------------------------------
def test_relerr_charm_subpercent():
    assert rel_err_c < 0.01


def test_relerr_up_within_ten_percent():
    assert rel_err_u < 0.10


def test_pred_obs_ordering_up():
    assert pred_u_over_t < obs_u_over_t


def test_pred_obs_ordering_charm():
    assert pred_c_over_t > obs_c_over_t


# ------------------------------------------------------------------
# Supplement-R vs CCXLII depth-bracket closure
# ------------------------------------------------------------------
def test_chain_value_from_supplement_r():
    assert chain_mt_over_mu == 63_960


def test_closure_fraction_exact():
    assert closure_mt_over_mu.numerator == 3_351_040
    assert closure_mt_over_mu.denominator == 39


def test_closure_floor():
    assert closure_mt_over_mu_floor == 85_924


def test_truncation_factor_gt_one():
    assert truncation_factor > 1.0


# ------------------------------------------------------------------
# L∞ depth bookkeeping
# ------------------------------------------------------------------
def test_depths_are_three():
    assert depths == [0, 1, 2]
    assert num_depths == Q == 3


# ------------------------------------------------------------------
# JSON output
# ------------------------------------------------------------------
def test_json_exists():
    assert (ROOT / "PART_CCXLII_linfinity_bracket_results.json").exists()


def test_json_verified_true():
    data = json.loads(
        (ROOT / "PART_CCXLII_linfinity_bracket_results.json").read_text(encoding="utf-8")
    )
    assert data["Verified"] is True


def test_json_checks_count():
    data = json.loads(
        (ROOT / "PART_CCXLII_linfinity_bracket_results.json").read_text(encoding="utf-8")
    )
    assert data["checks_passed"] == data["checks_total"] == 29


def test_json_depth2_denominator():
    data = json.loads(
        (ROOT / "PART_CCXLII_linfinity_bracket_results.json").read_text(encoding="utf-8")
    )
    assert data["depth2"]["denominator"] == 3_351_040
