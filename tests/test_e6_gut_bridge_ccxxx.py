"""
Tests for Part CCXXX: E₆ Exceptional Lie Algebra and Grand Unification from W(3,3).

Covers all 34 bridge checks plus JSON export integrity.
"""

import json
import os
import pytest

Q = 3; V = 40; K = 12; LAM = 2; MU = 4
M_LAM = 27; M_NEG = 12; LAP_MID = 10; LAP_TOP = 16
EDGES = 240; AUT_ORDER = 51840


class TestBridgeMetadata:
    def test_import(self):
        from PART_CCXXX_E6_GUT_BRIDGE import Verified
        assert Verified is True

    def test_all_checks_pass(self):
        from PART_CCXXX_E6_GUT_BRIDGE import passed, checks
        assert passed == len(checks)

    def test_checks_count(self):
        from PART_CCXXX_E6_GUT_BRIDGE import checks
        assert len(checks) == 34

    def test_no_failures(self):
        from PART_CCXXX_E6_GUT_BRIDGE import failed
        assert failed == []


class TestSRGParameters:
    def test_Q(self):
        from PART_CCXXX_E6_GUT_BRIDGE import Q as q; assert q == 3
    def test_V(self):
        from PART_CCXXX_E6_GUT_BRIDGE import V as v; assert v == 40
    def test_K(self):
        from PART_CCXXX_E6_GUT_BRIDGE import K as k; assert k == 12
    def test_LAM(self):
        from PART_CCXXX_E6_GUT_BRIDGE import LAM as lam; assert lam == 2
    def test_MU(self):
        from PART_CCXXX_E6_GUT_BRIDGE import MU as mu; assert mu == 4
    def test_M_LAM(self):
        from PART_CCXXX_E6_GUT_BRIDGE import M_LAM as ml; assert ml == 27
    def test_LAP_MID(self):
        from PART_CCXXX_E6_GUT_BRIDGE import LAP_MID as lm; assert lm == 10
    def test_LAP_TOP(self):
        from PART_CCXXX_E6_GUT_BRIDGE import LAP_TOP as lt; assert lt == 16
    def test_EDGES(self):
        from PART_CCXXX_E6_GUT_BRIDGE import EDGES as e; assert e == 240
    def test_AUT_ORDER(self):
        from PART_CCXXX_E6_GUT_BRIDGE import AUT_ORDER as ao; assert ao == 51840


class TestWeylGroup:
    """Bridge 1: |W(E₆)| = AUT_ORDER = 51840."""

    def test_weyl_E6_equals_AUT_ORDER(self):
        from PART_CCXXX_E6_GUT_BRIDGE import weyl_E6
        assert weyl_E6 == AUT_ORDER

    def test_weyl_E6_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import weyl_E6
        assert weyl_E6 == 51840

    def test_weyl_E6_is_aut_order(self):
        from PART_CCXXX_E6_GUT_BRIDGE import weyl_E6, weyl_E6_anchor
        assert weyl_E6 == weyl_E6_anchor


class TestE6Rank:
    """Bridge 2: rank(E₆) = K//2 = 6."""

    def test_rank_E6_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import rank_E6
        assert rank_E6 == 6

    def test_rank_E6_equals_K_half(self):
        from PART_CCXXX_E6_GUT_BRIDGE import rank_E6
        assert rank_E6 == K // 2

    def test_two_rank_E6_equals_K(self):
        from PART_CCXXX_E6_GUT_BRIDGE import two_rank_E6
        assert two_rank_E6 == K

    def test_rank_E6_sq_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import rank_E6_sq
        assert rank_E6_sq == 36

    def test_rank_E6_sq_equals_QK(self):
        from PART_CCXXX_E6_GUT_BRIDGE import rank_E6_sq
        assert rank_E6_sq == Q * K


class TestSO10Decomposition:
    """Bridge 3: 27 of E₆ = 16 + 10 + 1 under SO(10)."""

    def test_dim_27_equals_M_LAM(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_27
        assert dim_27 == M_LAM

    def test_dim_27_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_27
        assert dim_27 == 27

    def test_decomp_parts(self):
        from PART_CCXXX_E6_GUT_BRIDGE import so10_decomp_16, so10_decomp_10, so10_decomp_1
        assert so10_decomp_16 == LAP_TOP
        assert so10_decomp_10 == LAP_MID
        assert so10_decomp_1 == 1

    def test_decomp_sum_equals_27(self):
        from PART_CCXXX_E6_GUT_BRIDGE import decomp_sum
        assert decomp_sum == 27

    def test_decomp_sum_equals_dim_27(self):
        from PART_CCXXX_E6_GUT_BRIDGE import decomp_sum, dim_27
        assert decomp_sum == dim_27

    def test_decomp_sum_equals_M_LAM(self):
        from PART_CCXXX_E6_GUT_BRIDGE import decomp_sum
        assert decomp_sum == M_LAM


class TestSO10Structure:
    """Bridge 4: SO(10) representations and rank."""

    def test_rank_SO10_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import rank_SO10
        assert rank_SO10 == 5

    def test_rank_SO10_equals_LAPMID_div_LAM(self):
        from PART_CCXXX_E6_GUT_BRIDGE import rank_SO10
        assert rank_SO10 == LAP_MID // LAM

    def test_dim_spinor_equals_LAPTOP(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_spinor_SO10
        assert dim_spinor_SO10 == LAP_TOP

    def test_dim_spinor_equals_MU_sq(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_spinor_SO10, dim_spinor_check
        assert dim_spinor_SO10 == dim_spinor_check
        assert dim_spinor_check == MU ** 2

    def test_dim_vector_equals_LAPMID(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_vector_SO10
        assert dim_vector_SO10 == LAP_MID


class TestE6Adjoint:
    """Bridge 5: dim(E₆) = 78 via two SRG formulas."""

    def test_d_bos_precursor_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import d_bos_precursor
        assert d_bos_precursor == 26

    def test_d_bos_precursor_equals_MLAM_minus_1(self):
        from PART_CCXXX_E6_GUT_BRIDGE import d_bos_precursor
        assert d_bos_precursor == M_LAM - 1

    def test_dim_E6_adj_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_E6_adj
        assert dim_E6_adj == 78

    def test_dim_E6_alt_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_E6_alt
        assert dim_E6_alt == 78

    def test_dim_E6_both_equal(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_E6_adj, dim_E6_alt
        assert dim_E6_adj == dim_E6_alt

    def test_dim_E6_adj_formula(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_E6_adj, d_bos_precursor
        assert dim_E6_adj == Q * d_bos_precursor


class TestE8Adjoint:
    """Bridge 6: dim(E₈) = 248 = EDGES + 2·MU."""

    def test_dim_E8_adj_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_E8_adj
        assert dim_E8_adj == 248

    def test_dim_E8_adj_formula(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_E8_adj
        assert dim_E8_adj == EDGES + 2 * MU

    def test_dim_E8_residue_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_E8_residue
        assert dim_E8_residue == 8

    def test_dim_E8_residue_equals_2MU(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_E8_residue
        assert dim_E8_residue == 2 * MU


class TestSO10Adjoint:
    """Bridge 7: dim(SO(10)) = 45 via two SRG formulas."""

    def test_dim_SO10_adj_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_SO10_adj
        assert dim_SO10_adj == 45

    def test_dim_SO10_alt_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_SO10_alt
        assert dim_SO10_alt == 45

    def test_dim_SO10_both_equal(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_SO10_adj, dim_SO10_alt
        assert dim_SO10_adj == dim_SO10_alt

    def test_dim_SO10_n_formula(self):
        from PART_CCXXX_E6_GUT_BRIDGE import dim_SO10_adj
        # n=10=LAP_MID: dim(SO(n)) = n(n-1)/2
        assert dim_SO10_adj == LAP_MID * (LAP_MID - 1) // 2


class TestK3Euler:
    """Bridge 8: χ(K3) = 24 = K·λ."""

    def test_chi_K3_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import chi_K3
        assert chi_K3 == 24

    def test_chi_K3_formula(self):
        from PART_CCXXX_E6_GUT_BRIDGE import chi_K3
        assert chi_K3 == K * LAM

    def test_chi_K3_over_MU_equals_rank_E6(self):
        from PART_CCXXX_E6_GUT_BRIDGE import chi_K3_over_MU, rank_E6
        assert chi_K3_over_MU == rank_E6

    def test_chi_K3_over_MU_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import chi_K3_over_MU
        assert chi_K3_over_MU == 6


class TestBosonicString:
    """Bridge 9: bosonic string critical dimension d_bos = 26."""

    def test_d_bos_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import d_bos
        assert d_bos == 26

    def test_d_bos_equals_MLAM_minus_1(self):
        from PART_CCXXX_E6_GUT_BRIDGE import d_bos
        assert d_bos == M_LAM - 1

    def test_d_bos_mod_K_equals_LAM(self):
        from PART_CCXXX_E6_GUT_BRIDGE import d_bos_mod_K
        assert d_bos_mod_K == LAM

    def test_d_bos_div_Q_equals_2MU(self):
        from PART_CCXXX_E6_GUT_BRIDGE import d_bos_div_Q
        assert d_bos_div_Q == 2 * MU


class TestE6RootSystem:
    """Bridge 10: E₆ root system — 36 positive roots, 72 total."""

    def test_n_pos_roots_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import n_pos_roots_E6
        assert n_pos_roots_E6 == 36

    def test_n_pos_roots_equals_QK(self):
        from PART_CCXXX_E6_GUT_BRIDGE import n_pos_roots_E6
        assert n_pos_roots_E6 == Q * K

    def test_n_pos_roots_equals_rank_sq(self):
        from PART_CCXXX_E6_GUT_BRIDGE import n_pos_roots_E6, rank_E6_sq
        assert n_pos_roots_E6 == rank_E6_sq

    def test_n_tot_roots_value(self):
        from PART_CCXXX_E6_GUT_BRIDGE import n_tot_roots_E6
        assert n_tot_roots_E6 == 72

    def test_n_tot_roots_equals_rank_K(self):
        from PART_CCXXX_E6_GUT_BRIDGE import n_tot_roots_E6, rank_E6
        assert n_tot_roots_E6 == rank_E6 * K

    def test_n_tot_roots_equals_2pos(self):
        from PART_CCXXX_E6_GUT_BRIDGE import n_pos_roots_E6, n_tot_roots_E6
        assert n_tot_roots_E6 == 2 * n_pos_roots_E6


class TestJSONExport:
    @pytest.fixture(scope="class")
    def data(self):
        path = os.path.join(os.path.dirname(__file__), "..", "PART_CCXXX_e6_gut_results.json")
        with open(path) as f:
            return json.load(f)

    def test_part_field(self, data):
        assert data["Part"] == "CCXXX"

    def test_verified_true(self, data):
        assert data["Verified"] is True

    def test_all_checks_in_json(self, data):
        assert data["checks_passed"] == data["checks_total"]

    def test_checks_count_in_json(self, data):
        assert data["checks_total"] == 34

    def test_all_individual_checks_true(self, data):
        for k, v in data["checks"].items():
            assert v is True, f"Check {k!r} failed in JSON"
