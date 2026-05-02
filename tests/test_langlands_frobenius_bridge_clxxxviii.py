"""
Regression tests for Part CLXXXVIII — Langlands–Frobenius Bridge.

Run with:  pytest tests/test_langlands_frobenius_bridge_clxxxviii.py -v
"""

import json
import math
from pathlib import Path

import pytest

from PART_CLXXXVIII_LANGLANDS_FROBENIUS_BRIDGE import (
    ALPHA_INV,
    BETA_0,
    BETA_1,
    GALOIS_ORDER,
    PHI3,
    PHI6,
    PHI12,
    Q,
    Q2,
    Q3,
    Q4,
    eisenstein_norm,
    frobenius_class,
    full_norm,
    galois_orbit,
    gaussian_norm,
    gaussian_shadow,
    is_prime,
    langlands_frobenius_bridge_audit,
    search_unified_elements,
    _z12_power,
    z12_mul,
)

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def audit():
    return langlands_frobenius_bridge_audit()


# ---------------------------------------------------------------------------
# 1. W(3,3) atom constants
# ---------------------------------------------------------------------------

def test_q_equals_3():
    assert Q == 3

def test_phi6_equals_7():
    assert PHI6 == 7

def test_phi3_equals_13():
    assert PHI3 == 13

def test_phi12_equals_73():
    assert PHI12 == 73

def test_alpha_inv_equals_137():
    assert ALPHA_INV == 137

def test_beta0_equals_phi6():
    assert BETA_0 == PHI6  # both == 7

def test_beta1_equals_phi3():
    assert BETA_1 == PHI3  # both == 13

def test_galois_order_equals_4():
    assert GALOIS_ORDER == 4


# ---------------------------------------------------------------------------
# 2. Frobenius classification
# ---------------------------------------------------------------------------

def test_137_is_gaussian_sheet_only():
    assert frobenius_class(137) == "gaussian_sheet_only"

def test_7_is_eisenstein_sheet_only():
    assert frobenius_class(7) == "eisenstein_sheet_only"

def test_13_splits_completely():
    assert frobenius_class(13) == "splits_completely"

def test_2_is_ramified():
    assert frobenius_class(2) == "ramified"

def test_3_is_ramified():
    assert frobenius_class(3) == "ramified"

def test_11_is_inert_both():
    assert frobenius_class(11) == "inert_both"

def test_5_is_gaussian_sheet_only():
    assert frobenius_class(5) == "gaussian_sheet_only"

def test_19_is_eisenstein_sheet_only():
    assert frobenius_class(19) == "eisenstein_sheet_only"

def test_37_splits_completely():
    assert frobenius_class(37) == "splits_completely"


# ---------------------------------------------------------------------------
# 3. Modular residue checks
# ---------------------------------------------------------------------------

def test_137_mod_12():
    assert 137 % 12 == 5

def test_137_mod_4():
    assert 137 % 4 == 1     # splits in Z[i]

def test_137_mod_3():
    assert 137 % 3 == 2     # inert in Z[omega]

def test_7_mod_12():
    assert 7 % 12 == 7

def test_7_mod_4():
    assert 7 % 4 == 3       # inert in Z[i]

def test_7_mod_3():
    assert 7 % 3 == 1       # splits in Z[omega]

def test_13_mod_12():
    assert 13 % 12 == 1

def test_13_mod_4():
    assert 13 % 4 == 1      # splits in Z[i]

def test_13_mod_3():
    assert 13 % 3 == 1      # splits in Z[omega]


# ---------------------------------------------------------------------------
# 4. Gaussian and Eisenstein norms of canonical elements
# ---------------------------------------------------------------------------

def test_canon_g13_gaussian_norm():
    assert gaussian_norm((4, 6, 2, 1)) == 137

def test_canon_g13_eisenstein_norm():
    assert eisenstein_norm((4, 6, 2, 1)) == 13

def test_canon_g7_gaussian_norm():
    assert gaussian_norm((6, 3, 4, 0)) == 137

def test_canon_g7_eisenstein_norm():
    assert eisenstein_norm((6, 3, 4, 0)) == 7

def test_canon_g13_full_norm():
    assert full_norm((4, 6, 2, 1)) == 709 ** 2

def test_unit_element_gaussian_norm_1():
    assert gaussian_norm((1, 0, 0, 0)) == 1

def test_zero_element_gaussian_norm_0():
    assert gaussian_norm((0, 0, 0, 0)) == 0


# ---------------------------------------------------------------------------
# 5. Gaussian sum-of-squares for 137
# ---------------------------------------------------------------------------

def test_137_is_sum_of_two_squares():
    assert 4 ** 2 + 11 ** 2 == 137

def test_137_gaussian_shadow_modulus():
    """|π_i(canonical element)| rounds to sqrt(137)."""
    v = gaussian_shadow((4, 6, 2, 1))
    assert round(v.real ** 2 + v.imag ** 2) == 137


# ---------------------------------------------------------------------------
# 6. Z[ζ₁₂] ring arithmetic
# ---------------------------------------------------------------------------

def test_z12_mul_identity():
    identity = (1, 0, 0, 0)
    u = (2, 3, -1, 4)
    assert z12_mul(u, identity) == u

def test_z12_power_0():
    assert _z12_power(0) == (1, 0, 0, 0)

def test_z12_power_1():
    assert _z12_power(1) == (0, 1, 0, 0)

def test_z12_power_4_equals_z2_minus_1():
    # ζ¹² = ζ² - 1  from Φ₁₂ relation
    assert _z12_power(4) == (-1, 0, 1, 0)

def test_z12_power_12_is_identity():
    # ζ₁₂¹² = 1
    assert _z12_power(12) == (1, 0, 0, 0)

def test_galois_orbit_length():
    orbit = galois_orbit((4, 6, 2, 1))
    assert len(orbit) == 4


# ---------------------------------------------------------------------------
# 7. Unified element search
# ---------------------------------------------------------------------------

def test_unified_search_finds_elements():
    results = search_unified_elements(bound=6)
    assert len(results) > 0

def test_unified_search_count_equals_20():
    results = search_unified_elements(bound=6)
    assert len(results) == 20

def test_unified_all_have_gaussian_norm_137():
    results = search_unified_elements(bound=6)
    assert all(r["gaussian_norm"] == 137 for r in results)

def test_unified_all_have_eisenstein_norm_in_targets():
    results = search_unified_elements(bound=6)
    assert all(r["eisenstein_norm"] in {7, 13} for r in results)

def test_unified_12_have_eisenstein_7():
    results = search_unified_elements(bound=6)
    assert sum(1 for r in results if r["eisenstein_norm"] == 7) == 12

def test_unified_8_have_eisenstein_13():
    results = search_unified_elements(bound=6)
    assert sum(1 for r in results if r["eisenstein_norm"] == 13) == 8


# ---------------------------------------------------------------------------
# 8. Audit result structure
# ---------------------------------------------------------------------------

def test_audit_status_pass(audit):
    assert audit["status"] == "PASS"

def test_audit_frobenius_check_count(audit):
    assert audit["frobenius_check_count"] == 9

def test_audit_all_frobenius_pass(audit):
    assert audit["all_frobenius_pass"] is True

def test_audit_ring_check_count(audit):
    assert audit["ring_check_count"] == 23

def test_audit_all_ring_checks_pass(audit):
    assert audit["all_ring_checks_pass"] is True

def test_audit_unified_count(audit):
    assert audit["unified_count"] == 20

def test_audit_unified_found(audit):
    assert audit["unified_found"] is True

def test_audit_unified_with_e7(audit):
    assert audit["unified_with_eisenstein_7"] == 12

def test_audit_unified_with_e13(audit):
    assert audit["unified_with_eisenstein_13"] == 8

def test_audit_theorem_present(audit):
    assert "theorem_clxxxviii" in audit

def test_audit_theorem_phi6_equals_beta0(audit):
    assert audit["theorem_clxxxviii"]["phi6_equals_beta0"] is True

def test_audit_theorem_phi3_equals_beta1(audit):
    assert audit["theorem_clxxxviii"]["phi3_equals_beta1"] is True

def test_audit_w33_atoms_present(audit):
    atoms = audit["w33_atoms"]
    assert atoms["Q"] == 3
    assert atoms["PHI6"] == 7
    assert atoms["PHI3"] == 13
    assert atoms["ALPHA_INV"] == 137
    assert atoms["GALOIS_ORDER"] == 4


# ---------------------------------------------------------------------------
# 9. Results JSON file
# ---------------------------------------------------------------------------

def test_results_json_exists():
    p = ROOT / "PART_CLXXXVIII_langlands_frobenius_results.json"
    assert p.exists()

def test_results_json_valid():
    p = ROOT / "PART_CLXXXVIII_langlands_frobenius_results.json"
    with p.open() as fh:
        data = json.load(fh)
    assert data["status"] == "PASS"
    assert data["unified_count"] == 20
