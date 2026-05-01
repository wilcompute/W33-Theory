"""Regression tests for the five conflict-clearance resolutions."""

import pytest
from fractions import Fraction
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.w33_conflict_clearance_audit import w33_conflict_clearance_audit

Q, LAMBDA, MU, K, V, F = 3, 2, 4, 12, 40, 24
E = V * K // 2  # 240
PHI3 = Q**2 + Q + 1  # 13
PHI6 = Q**2 - Q + 1  # 7
X = Fraction(Q, PHI3)


@pytest.fixture(scope="module")
def report():
    return w33_conflict_clearance_audit()


def test_all_conflicts_cleared(report):
    assert report["all_cleared"] is True


def test_conflict_count_drops_to_zero(report):
    assert report["conflict_count_after_clearance"] == 0


# 1. Omega_Lambda
def test_omega_cosmo_table_promoted(report):
    r = report["resolutions"]["1_omega_lambda"]
    assert r["pass"] is True
    assert r["promoted_claim"] == "Omega_Lambda = (v+1)/60 = 41/60"


def test_omega_cosmo_within_one_sigma(report):
    r = report["resolutions"]["1_omega_lambda"]
    assert r["pdg_sigma"] < 1.0


# 2. Cabibbo tan vs sin
def test_cabibbo_tan_reading_closer(report):
    r = report["resolutions"]["2_cabibbo_tan_vs_sin"]
    assert r["pass"] is True


def test_cabibbo_legacy_retired(report):
    r = report["resolutions"]["2_cabibbo_tan_vs_sin"]
    assert r["legacy_shorthand_retired"] is True


def test_cabibbo_sin2_exact_fraction():
    # sin^2(arctan(3/13)) = 9/(9 + 169) = 9/178
    sin2 = Fraction(Q**2, Q**2 + PHI3**2)
    assert sin2 == Fraction(9, 178)


# 3. PMNS theta_12
def test_pmns_promoted_value_is_mu_over_phi3(report):
    r = report["resolutions"]["3_pmns_theta12"]
    assert r["on_mu_phi3_surface"] is True
    assert r["pass"] is True


def test_pmns_legacy_retired(report):
    r = report["resolutions"]["3_pmns_theta12"]
    assert r["legacy_3_over_10_retired"] is True


# 4. SO(32) label
def test_so32_three_identities_all_496(report):
    r = report["resolutions"]["4_so32_label"]
    ids = r["correct_identities"]
    assert ids["2E_plus_16"] == 496
    assert ids["2_dim_E8"] == 496
    assert ids["SO32_adjoint"] == 496
    assert r["pass"] is True


# 5. Alpha rounding
def test_alpha_exact_fraction_is_closer_to_codata(report):
    r = report["resolutions"]["5_alpha_rounding"]
    assert r["pass"] is True
    assert r["err_exact"] < r["err_superseded"]
