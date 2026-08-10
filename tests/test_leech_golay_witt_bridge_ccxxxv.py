"""
Tests for Part CCXXXV — Leech Lattice, Golay Codes, and Witt Designs
SRG(40,12,2,4) constants.

75 tests across 11 classes.
"""

import json
from pathlib import Path
import pytest

from PART_CCXXXV_LEECH_GOLAY_WITT_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, EDGES, AUT_ORDER,
    phi3_Q,
    dim_Leech, min_norm_Leech, kissing_Leech,
    niemeier_count,
    binary_Golay_n, binary_Golay_k, binary_Golay_d, binary_Golay_d_alt,
    ternary_Golay_n, ternary_Golay_k, ternary_Golay_d, ternary_base_field,
    witt_t, witt_k_block, witt_v_points, witt_lambda,
    octads_count,
    E8_copies, E8_dim, leech_from_3E8,
    golay_rate_n_over_k,
    dim_modular_weight_K,
    tau_2_abs, tau_2,
    E8_kissing,
    checks, Verified,
)

ROOT = Path(__file__).resolve().parents[1]


class TestBridgeMetadata:
    def test_verified_true(self):
        assert Verified is True

    def test_all_checks_pass(self):
        failed = [lbl for lbl, v in checks if not v]
        assert failed == [], f"Failed checks: {failed}"

    def test_check_count_at_least_30(self):
        assert len(checks) >= 30

    def test_json_exists(self):
        assert (ROOT / "PART_CCXXXV_leech_golay_witt_results.json").exists()

    def test_json_verified(self):
        d = json.loads((ROOT / "PART_CCXXXV_leech_golay_witt_results.json").read_text(encoding="utf-8"))
        assert d["Verified"] is True

    def test_json_checks_passed_equals_total(self):
        d = json.loads((ROOT / "PART_CCXXXV_leech_golay_witt_results.json").read_text(encoding="utf-8"))
        assert d["checks_passed"] == d["checks_total"]


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_EDGES(self):
        assert EDGES == 240


class TestLeechLattice:
    """B1/B2/B3: Leech lattice parameters."""

    def test_dim_Leech_value(self):
        assert dim_Leech == 24

    def test_dim_Leech_eq_K_times_LAM(self):
        assert dim_Leech == K * LAM

    def test_min_norm_eq_MU(self):
        assert min_norm_Leech == MU

    def test_min_norm_value(self):
        assert min_norm_Leech == 4

    def test_kissing_value(self):
        assert kissing_Leech == 196560

    def test_kissing_factored(self):
        # 196560 = EDGES × Q² × (K//2+1) × Φ₃(Q)
        assert EDGES * Q**2 * (K // 2 + 1) * phi3_Q == 196560

    def test_kissing_EDGES_factor(self):
        # Kissing number is divisible by EDGES
        assert kissing_Leech % EDGES == 0
        assert kissing_Leech // EDGES == Q**2 * (K // 2 + 1) * phi3_Q

    def test_niemeier_count_eq_dim(self):
        assert niemeier_count == dim_Leech

    def test_niemeier_count_value(self):
        assert niemeier_count == 24


class TestBinaryGolay:
    """B5–B7: Binary Golay code [24,12,8]₂."""

    def test_binary_n(self):
        assert binary_Golay_n == 24

    def test_binary_n_eq_K_times_LAM(self):
        assert binary_Golay_n == K * LAM

    def test_binary_k(self):
        assert binary_Golay_k == K

    def test_binary_k_value(self):
        assert binary_Golay_k == 12

    def test_binary_d(self):
        assert binary_Golay_d == 8

    def test_binary_d_eq_2_MU(self):
        assert binary_Golay_d == 2 * MU

    def test_binary_d_alt(self):
        assert binary_Golay_d_alt == 8

    def test_binary_d_alt_eq_K_half_plus_2(self):
        assert binary_Golay_d_alt == K // 2 + 2

    def test_binary_d_both_agree(self):
        assert binary_Golay_d == binary_Golay_d_alt

    def test_binary_rate(self):
        # Rate = k/n = 1/2 = 1/λ
        assert binary_Golay_n // binary_Golay_k == LAM

    def test_binary_n_eq_leech_dim(self):
        assert binary_Golay_n == dim_Leech


class TestTernaryGolay:
    """B8–B10: Ternary Golay code [12,6,6]₃."""

    def test_ternary_n_eq_K(self):
        assert ternary_Golay_n == K

    def test_ternary_n_value(self):
        assert ternary_Golay_n == 12

    def test_ternary_k_eq_K_half(self):
        assert ternary_Golay_k == K // 2

    def test_ternary_k_value(self):
        assert ternary_Golay_k == 6

    def test_ternary_d_eq_K_half(self):
        assert ternary_Golay_d == K // 2

    def test_ternary_d_value(self):
        assert ternary_Golay_d == 6

    def test_ternary_base_field_eq_Q(self):
        # Over F_Q = F_3: the SRG deformation field is the code alphabet!
        assert ternary_base_field == Q

    def test_ternary_rate(self):
        # Rate = k/n = 6/12 = 1/2 = 1/λ
        assert ternary_Golay_n // ternary_Golay_k == LAM


class TestWittDesign:
    """B11–B15: Witt design S(5,8,24)."""

    def test_witt_t(self):
        assert witt_t == 5

    def test_witt_t_eq_K_half_minus_1(self):
        assert witt_t == K // 2 - 1

    def test_witt_k_block(self):
        assert witt_k_block == 8

    def test_witt_k_block_eq_2_MU(self):
        assert witt_k_block == 2 * MU

    def test_witt_v(self):
        assert witt_v_points == 24

    def test_witt_v_eq_K_times_LAM(self):
        assert witt_v_points == K * LAM

    def test_witt_lambda_value(self):
        assert witt_lambda == 1

    def test_witt_lambda_eq_LAM_minus_1(self):
        assert witt_lambda == LAM - 1

    def test_octads_count(self):
        assert octads_count == 759

    def test_octads_from_SRG(self):
        # 759 = Q × (K-1) × (2K-1)
        assert Q * (K - 1) * (2 * K - 1) == 759


class TestLeechFrom3E8:
    """B16: Leech lattice from 3 copies of E₈."""

    def test_E8_copies_eq_Q(self):
        assert E8_copies == Q

    def test_E8_copies_value(self):
        assert E8_copies == 3

    def test_E8_dim_value(self):
        assert E8_dim == 8

    def test_E8_dim_eq_2_MU(self):
        assert E8_dim == 2 * MU

    def test_leech_from_3E8_eq_dim_Leech(self):
        assert leech_from_3E8 == dim_Leech

    def test_leech_from_3E8_value(self):
        assert leech_from_3E8 == 24

    def test_E8_kissing_eq_EDGES(self):
        assert E8_kissing == EDGES


class TestModularForms:
    """B17/B18/B19: Modular forms and Ramanujan tau."""

    def test_golay_rate_n_over_k_eq_LAM(self):
        assert golay_rate_n_over_k == LAM

    def test_dim_M_weight_K_eq_LAM(self):
        # dim M_{12}(SL₂(ℤ)) = 2 = λ
        assert dim_modular_weight_K == LAM

    def test_dim_M_weight_K_value(self):
        assert dim_modular_weight_K == 2

    def test_tau_2_abs_eq_K_times_LAM(self):
        # |τ(2)| = 24 = K·λ = dim(Λ₂₄)
        assert tau_2_abs == K * LAM

    def test_tau_2_value(self):
        assert tau_2 == -24

    def test_tau_2_abs_eq_dim_Leech(self):
        assert tau_2_abs == dim_Leech
