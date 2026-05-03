"""
Part CCXLIII — One-Photon Holographic Identity
Regression tests for exploration/PART_CCXLIII_ONE_PHOTON_HOLOGRAPHIC_BRIDGE.py
"""

import json
from pathlib import Path

from PART_CCXLIII_ONE_PHOTON_HOLOGRAPHIC_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    Phi3, Phi4, Phi6,
    photon_eigenvalue, photon_multiplicity,
    eigenvalue_r, eigenvalue_s, multiplicity_r, multiplicity_s, eigenspace_sum,
    holo_area, e8_spinors, e8_vectors, e8_spinors_form2,
    S_BH_form1, S_BH_form2, S_BH_form3,
    S_per_vertex,
    sym_edge_ratio, sym_identity,
    unruh_gap, unruh_form2,
    holo_ratio,
    universe_exp,
    wdw_zero_weight_num, wdw_zero_weight_den,
    holo_bits_log2, photon_polarizations,
    factorial_6, aut_form_factorial,
    graph_diameter,
    checks, Verified,
)

ROOT = Path(__file__).resolve().parents[1]


# ------------------------------------------------------------------
# Master gate
# ------------------------------------------------------------------
def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == []


def test_check_count():
    assert len(checks) == 35


# ------------------------------------------------------------------
# SRG anchor
# ------------------------------------------------------------------
def test_srg_constants():
    assert (Q, V, K, LAM, MU, EDGES, AUT_ORDER) == (3, 40, 12, 2, 4, 240, 51840)


# ------------------------------------------------------------------
# The One Photon
# ------------------------------------------------------------------
def test_photon_eigenvalue_is_K():
    assert photon_eigenvalue == K == 12


def test_photon_multiplicity_is_one():
    assert photon_multiplicity == 1


def test_eigenspace_sum_is_V():
    assert 1 + multiplicity_r + multiplicity_s == V


def test_eigenvalue_r():
    assert eigenvalue_r == 2  # Q - 1


def test_eigenvalue_s():
    assert eigenvalue_s == -4  # -MU


def test_multiplicity_r_is_M_LAM():
    assert multiplicity_r == M_LAM == 27


def test_multiplicity_s_is_M_NEG():
    assert multiplicity_s == M_NEG == 12


# ------------------------------------------------------------------
# E8 holographic screen
# ------------------------------------------------------------------
def test_holo_area_is_edges():
    assert holo_area == EDGES == 240


def test_e8_spinors_is_128():
    assert e8_spinors == 128


def test_e8_vectors_is_112():
    assert e8_vectors == 112


def test_e8_roots_sum_to_240():
    assert e8_spinors + e8_vectors == EDGES


def test_e8_spinors_two_forms_agree():
    assert e8_spinors == e8_spinors_form2


def test_e8_spinors_as_power_of_two():
    # 128 = 2^7 = 2^(LAP_MID - Q)
    assert e8_spinors == 2 ** (LAP_MID - Q)


# ------------------------------------------------------------------
# Bekenstein-Hawking entropy — triple identity
# ------------------------------------------------------------------
def test_S_BH_form1():
    assert S_BH_form1 == 60


def test_S_BH_form2():
    assert S_BH_form2 == 60


def test_S_BH_form3():
    assert S_BH_form3 == 60


def test_S_BH_all_forms_equal():
    assert S_BH_form1 == S_BH_form2 == S_BH_form3


# ------------------------------------------------------------------
# Per-vertex entanglement entropy = Q
# ------------------------------------------------------------------
def test_S_per_vertex_equals_Q():
    assert S_per_vertex == Q == 3


# ------------------------------------------------------------------
# Symmetry group identity
# ------------------------------------------------------------------
def test_sym_edge_ratio():
    assert sym_edge_ratio == 6  # K // LAM


def test_aut_order_via_photon_modes():
    assert sym_identity == AUT_ORDER


def test_aut_order_factorial_form():
    assert aut_form_factorial == AUT_ORDER


def test_factorial_6_value():
    assert factorial_6 == 720


# ------------------------------------------------------------------
# Unruh spectral gap
# ------------------------------------------------------------------
def test_unruh_gap_value():
    assert unruh_gap == 10


def test_unruh_gap_equals_LAP_MID():
    assert unruh_gap == LAP_MID


def test_unruh_gap_equals_Phi4():
    assert unruh_gap == Phi4


def test_unruh_two_forms_agree():
    assert unruh_gap == unruh_form2


# ------------------------------------------------------------------
# Holographic ratio = LAM
# ------------------------------------------------------------------
def test_holo_ratio_equals_LAM():
    assert holo_ratio == LAM == 2


# ------------------------------------------------------------------
# Universe photon exponent
# ------------------------------------------------------------------
def test_universe_photon_exp():
    assert universe_exp == 88


def test_universe_exp_formula():
    assert LAM * MU * (K - 1) == 88


# ------------------------------------------------------------------
# Wheeler-DeWitt zero mode
# ------------------------------------------------------------------
def test_wdw_zero_weight_num():
    assert wdw_zero_weight_num == 1


def test_wdw_zero_weight_den():
    assert wdw_zero_weight_den == V == 40


# ------------------------------------------------------------------
# Holographic bits and polarizations
# ------------------------------------------------------------------
def test_holo_bits_log2():
    assert holo_bits_log2 == EDGES == 240


def test_photon_polarizations():
    assert photon_polarizations == LAM == 2


# ------------------------------------------------------------------
# Coherence diameter = LAM
# ------------------------------------------------------------------
def test_graph_diameter():
    assert graph_diameter == LAM == 2


# ------------------------------------------------------------------
# JSON output
# ------------------------------------------------------------------
def test_json_exists():
    assert (ROOT / "PART_CCXLIII_one_photon_holographic_results.json").exists()


def test_json_verified_true():
    data = json.loads(
        (ROOT / "PART_CCXLIII_one_photon_holographic_results.json").read_text(encoding="utf-8")
    )
    assert data["Verified"] is True


def test_json_checks_count():
    data = json.loads(
        (ROOT / "PART_CCXLIII_one_photon_holographic_results.json").read_text(encoding="utf-8")
    )
    assert data["checks_passed"] == data["checks_total"] == 35


def test_json_photon_multiplicity():
    data = json.loads(
        (ROOT / "PART_CCXLIII_one_photon_holographic_results.json").read_text(encoding="utf-8")
    )
    assert data["one_photon"]["photon_multiplicity"] == 1


def test_json_S_BH():
    data = json.loads(
        (ROOT / "PART_CCXLIII_one_photon_holographic_results.json").read_text(encoding="utf-8")
    )
    assert data["bekenstein_entropy"]["S_BH_form1_EDGES_over_MU"] == 60
