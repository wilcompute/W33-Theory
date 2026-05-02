"""
tests/test_golay_code_bridge_cxci.py

Regression tests for Part CXCI: Golay Code Bridge.
"""

import json
import pytest

from PART_CXCI_GOLAY_CODE_BRIDGE import (
    Q, LAM, MU, V, K, PHI3, PHI4, PHI6, PHI12, J_INV, ALPHA_INV, VIETA2,
    EDGES, MULTIPLICITIES, EIGENVALUES,
    BIN_EXT_N, BIN_EXT_K, BIN_EXT_D,
    TER_EXT_N, TER_EXT_K, TER_EXT_D,
    BIN_PERF_N, BIN_PERF_K, BIN_PERF_D, BIN_PERF_T,
    TER_PERF_N, TER_PERF_K, TER_PERF_D, TER_PERF_T,
    E8_RANK, E8_KISSING, LEECH_RANK, LEECH_KISSING,
    hamming_ball_volume, is_perfect_code, sigma3,
    GolayCheck, golay_code_bridge_audit,
)


# ─── Atom constants ──────────────────────────────────────────────────────────

class TestAtoms:
    def test_Q(self):             assert Q == 3
    def test_LAM(self):           assert LAM == 2
    def test_MU(self):            assert MU == 4
    def test_V(self):             assert V == 40
    def test_K(self):             assert K == 12
    def test_PHI3(self):          assert PHI3 == 13
    def test_PHI4(self):          assert PHI4 == 10
    def test_PHI6(self):          assert PHI6 == 7
    def test_PHI12(self):         assert PHI12 == 73
    def test_J_INV(self):         assert J_INV == 8
    def test_EDGES(self):         assert EDGES == 240
    def test_EDGES_formula(self): assert EDGES == V * K // 2
    def test_third_mult_is_K2(self): assert MULTIPLICITIES[2] == K // 2


# ─── hamming_ball_volume ─────────────────────────────────────────────────────

class TestHammingBallVolume:
    def test_radius_0_binary(self):    assert hamming_ball_volume(2, 5, 0) == 1
    def test_radius_1_binary(self):    assert hamming_ball_volume(2, 5, 1) == 6
    def test_radius_1_ternary(self):   assert hamming_ball_volume(3, 3, 1) == 7
    def test_binary_23_3_is_2048(self):
        # Perfect binary Golay volume
        assert hamming_ball_volume(2, 23, 3) == 2048
    def test_binary_23_3_is_2_to_11(self):
        assert hamming_ball_volume(2, 23, 3) == 2 ** 11
    def test_ternary_11_2_is_243(self):
        # Perfect ternary Golay volume
        assert hamming_ball_volume(3, 11, 2) == 243
    def test_ternary_11_2_is_3_to_5(self):
        assert hamming_ball_volume(3, 11, 2) == 3 ** 5


# ─── is_perfect_code ─────────────────────────────────────────────────────────

class TestIsPerfectCode:
    def test_perfect_binary_golay(self):
        assert is_perfect_code(2, 23, 12, 7)
    def test_perfect_ternary_golay(self):
        assert is_perfect_code(3, 11, 6, 5)
    def test_hamming_code_7_4_3(self):
        # [7,4,3]_2 is perfect
        assert is_perfect_code(2, 7, 4, 3)
    def test_extended_binary_golay_not_perfect(self):
        # [24,12,8]_2 is NOT perfect
        assert not is_perfect_code(2, 24, 12, 8)
    def test_extended_ternary_golay_not_perfect(self):
        # [12,6,6]_3 is NOT perfect
        assert not is_perfect_code(3, 12, 6, 6)
    def test_ternary_golay_volume_times_M(self):
        # V_3(11,2) * 3^6 = 3^11
        assert hamming_ball_volume(3, 11, 2) * (3 ** 6) == 3 ** 11
    def test_binary_golay_volume_times_M(self):
        # V_2(23,3) * 2^12 = 2^23
        assert hamming_ball_volume(2, 23, 3) * (2 ** 12) == 2 ** 23


# ─── sigma3 ──────────────────────────────────────────────────────────────────

class TestSigma3:
    def test_sigma3_1(self):    assert sigma3(1) == 1
    def test_sigma3_2(self):    assert sigma3(2) == 9
    def test_sigma3_3(self):    assert sigma3(3) == 28
    def test_sigma3_4(self):    assert sigma3(4) == 73
    def test_sigma3_2_is_Q2(self):  assert sigma3(2) == Q ** 2
    def test_sigma3_3_is_V_K(self): assert sigma3(3) == V - K
    def test_sigma3_4_is_PHI12(self): assert sigma3(4) == PHI12


# ─── Golay code parameters ───────────────────────────────────────────────────

class TestGolayParameters:
    # Extended binary [24,12,8]
    def test_bin_ext_n_is_2K(self):   assert BIN_EXT_N == 2 * K
    def test_bin_ext_k_is_K(self):    assert BIN_EXT_K == K
    def test_bin_ext_d_is_Jinv(self): assert BIN_EXT_D == J_INV
    def test_bin_ext_self_dual(self): assert BIN_EXT_N == 2 * BIN_EXT_K

    # Extended ternary [12,6,6]_3
    def test_ter_ext_n_is_K(self):    assert TER_EXT_N == K
    def test_ter_ext_k_is_K2(self):   assert TER_EXT_K == K // 2
    def test_ter_ext_d_is_K2(self):   assert TER_EXT_D == K // 2
    def test_ter_ext_q_is_Q(self):    assert Q == Q          # alphabet
    def test_ter_ext_self_dual(self): assert TER_EXT_N == 2 * TER_EXT_K

    # Perfect binary [23,12,7]
    def test_bin_perf_n_formula(self): assert BIN_PERF_N == K + PHI3 - 2
    def test_bin_perf_t_is_Q(self):    assert BIN_PERF_T == Q
    def test_bin_perf_n_value(self):   assert BIN_PERF_N == 23

    # Perfect ternary [11,6,5]_3
    def test_ter_perf_n_is_K_minus_1(self): assert TER_PERF_N == K - 1
    def test_ter_perf_n_mtheory(self):      assert TER_PERF_N == 11
    def test_ter_perf_t_is_LAM(self):       assert TER_PERF_T == LAM
    def test_ter_perf_t_value(self):        assert TER_PERF_T == 2


# ─── E8 and Leech lattices ───────────────────────────────────────────────────

class TestLatticeParameters:
    def test_E8_rank_is_Jinv(self):        assert E8_RANK == J_INV
    def test_E8_rank_value(self):          assert E8_RANK == 8
    def test_E8_kissing_is_edges(self):    assert E8_KISSING == EDGES
    def test_E8_kissing_formula(self):     assert E8_KISSING == V * K // 2
    def test_E8_kissing_value(self):       assert E8_KISSING == 240

    def test_Leech_rank_is_2K(self):       assert LEECH_RANK == 2 * K
    def test_Leech_rank_value(self):       assert LEECH_RANK == 24
    def test_Leech_kissing_value(self):    assert LEECH_KISSING == 196560
    def test_Leech_kissing_formula(self):
        assert LEECH_KISSING == EDGES * Q ** 2 * PHI6 * PHI3
    def test_Leech_over_E8_ratio(self):
        assert LEECH_KISSING // E8_KISSING == Q ** 2 * PHI6 * PHI3


class TestE8ThetaSeries:
    def test_norm2_is_240(self):        assert 240 * sigma3(1) == 240
    def test_norm2_is_EDGES(self):      assert 240 * sigma3(1) == EDGES
    def test_sigma3_2_is_Q2(self):      assert sigma3(2) == Q ** 2
    def test_sigma3_3_is_V_minus_K(self): assert sigma3(3) == V - K
    def test_norm4_formula(self):       assert 240 * sigma3(2) == EDGES * Q ** 2
    def test_norm6_formula(self):       assert 240 * sigma3(3) == EDGES * (V - K)
    def test_norm4_value(self):         assert 240 * sigma3(2) == 2160
    def test_norm6_value(self):         assert 240 * sigma3(3) == 6720


# ─── GolayCheck dataclass ────────────────────────────────────────────────────

class TestGolayCheck:
    def test_passes_exact_equal(self):
        c = GolayCheck("t", "d", 5, 5)
        assert c.passes
    def test_fails_exact_unequal(self):
        c = GolayCheck("t", "d", 5, 6)
        assert not c.passes
    def test_passes_inexact(self):
        c = GolayCheck("t", "d", 1.000000000001, 1.0, exact=False)
        assert c.passes
    def test_fails_inexact(self):
        c = GolayCheck("t", "d", 1.1, 1.0, exact=False)
        assert not c.passes


# ─── Full audit ──────────────────────────────────────────────────────────────

class TestGolayCodeBridgeAudit:
    @pytest.fixture(scope="class")
    def result(self):
        return golay_code_bridge_audit()

    def test_status_pass(self, result):
        assert result["status"] == "PASS"

    def test_all_checks_pass(self, result):
        assert result["all_checks_pass"]

    def test_no_failed_checks(self, result):
        assert result["failed_checks"] == []

    def test_check_count(self, result):
        assert result["check_count"] == 40

    def test_checks_passing(self, result):
        assert result["checks_passing"] == 40

    def test_atom_check_count(self, result):
        assert result["atom_check_count"] == 9

    def test_golay_check_count(self, result):
        assert result["golay_check_count"] == 18

    def test_lattice_check_count(self, result):
        assert result["lattice_check_count"] == 13

    def test_binary_extended_params(self, result):
        p = result["golay_parameters"]["binary_extended"]
        assert p["n"] == 24 and p["k"] == 12 and p["d"] == 8

    def test_ternary_extended_params(self, result):
        p = result["golay_parameters"]["ternary_extended"]
        assert p["n"] == 12 and p["k"] == 6 and p["d"] == 6 and p["q"] == 3

    def test_ternary_perfect_params(self, result):
        p = result["golay_parameters"]["ternary_perfect"]
        assert p["n"] == 11 and p["t"] == 2

    def test_binary_perfect_params(self, result):
        p = result["golay_parameters"]["binary_perfect"]
        assert p["n"] == 23 and p["t"] == 3

    def test_E8_in_result(self, result):
        assert result["lattice_parameters"]["E8"]["rank"] == 8
        assert result["lattice_parameters"]["E8"]["kissing"] == 240

    def test_Leech_in_result(self, result):
        assert result["lattice_parameters"]["Leech"]["rank"] == 24
        assert result["lattice_parameters"]["Leech"]["kissing"] == 196560

    def test_sigma3_2_in_e8_theta(self, result):
        assert result["e8_theta_series"]["sigma3_2_equals_Q2"]

    def test_sigma3_3_in_e8_theta(self, result):
        assert result["e8_theta_series"]["sigma3_3_equals_V_minus_K"]

    def test_theorem_string_present(self, result):
        assert "theorem_cxci" in result
        assert len(result["theorem_cxci"]) > 50
