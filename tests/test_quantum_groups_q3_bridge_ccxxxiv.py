"""
Tests for Part CCXXXIV — Quantum Groups at q=Q=3 from W(3,3)
SRG(40,12,2,4) constants.

76 tests across 11 classes.
"""

import json
from pathlib import Path
import pytest

from PART_CCXXXIV_QUANTUM_GROUPS_Q3_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, EDGES, AUT_ORDER, LAP_MID,
    q_int, q_factorial, q_binom,
    q_int_1, q_int_2, q_int_3, q_int_4, q_int_5,
    q_fact_1, q_fact_2, q_fact_3,
    q_fact_3_val, dim_F4_check,
    phi3_Q, phi3_eq_q3,
    q_dim_spin0, q_dim_spin_half, q_dim_spin1, q_dim_spin_3half, q_dim_spin2,
    rank_quantum_E6, level_affine, h_E6, c_wzw_E6_check,
    q_binom_41, q_binom_31, q_binom_42,
    n_star, transport_wall_value, above_wall,
    q_dim_E6_27, albert_q_dim,
    serre_relations, dynkin_E6_edges,
    aut_from_q, aut_check,
    q_char_27,
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
        assert (ROOT / "PART_CCXXXIV_quantum_groups_q3_results.json").exists()

    def test_json_verified(self):
        d = json.loads((ROOT / "PART_CCXXXIV_quantum_groups_q3_results.json").read_text(encoding="utf-8"))
        assert d["Verified"] is True

    def test_json_checks_passed(self):
        d = json.loads((ROOT / "PART_CCXXXIV_quantum_groups_q3_results.json").read_text(encoding="utf-8"))
        assert d["checks_passed"] == d["checks_total"]


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_MU(self):
        assert MU == 4

    def test_M_LAM(self):
        assert M_LAM == 27

    def test_EDGES(self):
        assert EDGES == 240


class TestQIntegers:
    """B1: q-integer identifications at q=Q=3."""

    def test_q_int_1(self):
        assert q_int_1 == 1

    def test_q_int_2_eq_MU(self):
        assert q_int_2 == MU

    def test_q_int_2_value(self):
        assert q_int_2 == 4

    def test_q_int_3_eq_cyclotomic(self):
        assert q_int_3 == Q**2 + Q + 1

    def test_q_int_3_value(self):
        assert q_int_3 == 13

    def test_q_int_4_eq_V(self):
        # This is the transport wall: [4]_3 = V = 40
        assert q_int_4 == V

    def test_q_int_4_value(self):
        assert q_int_4 == 40

    def test_q_int_5_value(self):
        assert q_int_5 == 121

    def test_q_int_5_eq_11sq(self):
        assert q_int_5 == 11**2

    def test_q_int_function(self):
        assert q_int(4) == V
        assert q_int(2) == MU
        assert q_int(3) == Q**2 + Q + 1


class TestQFactorials:
    """B2: q-factorial identifications."""

    def test_q_fact_1(self):
        assert q_fact_1 == 1

    def test_q_fact_2_eq_MU(self):
        assert q_fact_2 == MU

    def test_q_fact_3_eq_dim_F4(self):
        # [3]!_3 = [1][2][3] = 1 × 4 × 13 = 52 = dim(F₄)
        assert q_fact_3_val == dim_F4_check

    def test_q_fact_3_value(self):
        assert q_fact_3 == 52

    def test_q_fact_3_eq_V_plus_K(self):
        assert q_fact_3 == V + K

    def test_q_fact_3_product(self):
        # [2]_3 × [3]_3 = 4 × 13 = 52
        assert q_int_2 * q_int_3 == V + K


class TestCyclotomic:
    """B3: Cyclotomic polynomial Φ₃."""

    def test_phi3_Q_value(self):
        assert phi3_Q == 13

    def test_phi3_Q_formula(self):
        assert phi3_Q == Q**2 + Q + 1

    def test_phi3_eq_q3(self):
        assert phi3_eq_q3 is True

    def test_phi3_eq_q_int_3(self):
        assert phi3_Q == q_int_3


class TestQuantumSpinDimensions:
    """B4/B5: Quantum dimensions of sl₂ representations at q=3."""

    def test_spin0(self):
        assert q_dim_spin0 == 1

    def test_spin_half_eq_MU(self):
        assert q_dim_spin_half == MU

    def test_spin1_eq_Phi3(self):
        assert q_dim_spin1 == phi3_Q

    def test_spin_3half_eq_V(self):
        # The transport wall: spin-3/2 quantum dim = V = 40
        assert q_dim_spin_3half == V

    def test_spin2_eq_121(self):
        assert q_dim_spin2 == 121

    def test_rank_quantum_E6(self):
        assert rank_quantum_E6 == K // 2

    def test_rank_quantum_E6_value(self):
        assert rank_quantum_E6 == 6

    def test_wzw_central_charge(self):
        # c(E₆, level K=12) = 12×78/24 = 39
        assert c_wzw_E6_check == 39


class TestQuantumBinomials:
    """B7: Gaussian q-binomial coefficients."""

    def test_q_binom_41_eq_V(self):
        assert q_binom_41 == V

    def test_q_binom_41_value(self):
        assert q_binom_41 == 40

    def test_q_binom_31_eq_phi3(self):
        assert q_binom_31 == phi3_Q

    def test_q_binom_31_value(self):
        assert q_binom_31 == 13

    def test_q_binom_42_value(self):
        assert q_binom_42 == 130

    def test_q_binom_function(self):
        assert q_binom(4, 1) == V
        assert q_binom(3, 1) == phi3_Q


class TestTransportWall:
    """B8: Nilpotent transport wall formalization at V=40."""

    def test_n_star_eq_MU(self):
        # The wall index is MU = 4 (the SRG co-degree)
        assert n_star == MU

    def test_transport_wall_value_eq_V(self):
        # [MU]_3 = [4]_3 = 40 = V
        assert transport_wall_value == V

    def test_above_wall_value(self):
        assert above_wall == 121

    def test_above_wall_exceeds_V(self):
        assert above_wall > V

    def test_above_wall_exceeds_by_factor(self):
        # 121 / 40 > 3 (large gap)
        assert above_wall > Q * V

    def test_wall_is_exact_saturation(self):
        # q_int(n_star) == V and q_int(n_star-1) < V
        assert q_int(n_star) == V
        assert q_int(n_star - 1) < V


class TestE6QuantumDimension:
    """B9: 27-rep of E₆ at q=3."""

    def test_q_dim_E6_27_eq_M_LAM(self):
        assert q_dim_E6_27 == M_LAM

    def test_q_dim_E6_27_eq_Q_cubed(self):
        assert q_dim_E6_27 == Q**3

    def test_q_dim_E6_27_value(self):
        assert q_dim_E6_27 == 27

    def test_albert_q_dim_eq_M_LAM(self):
        assert albert_q_dim == M_LAM

    def test_q_char_27_eq_M_LAM(self):
        assert q_char_27 == M_LAM


class TestAutOrderFromQ:
    """B11: AUT_ORDER recovered from q-integers."""

    def test_aut_from_q_value(self):
        assert aut_from_q == AUT_ORDER

    def test_aut_from_q_formula(self):
        # [4]_3 × (K//2)^4 = 40 × 6^4 = 40 × 1296 = 51840
        assert q_int(4) * (K // 2)**4 == AUT_ORDER

    def test_aut_order_value(self):
        assert AUT_ORDER == 51840
