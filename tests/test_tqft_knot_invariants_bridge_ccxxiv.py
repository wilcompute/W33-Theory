"""
Regression tests for Part CCXXIV: Topological QFT and Knot Invariants from W(3,3).

All tests import and validate the CCXXIV TQFT bridge.
SRG(40,12,2,4) with |Aut|=51840=|W(E6)|. Zero free parameters.
"""

import pytest
import sys
import json
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "exploration"))
from PART_CCXXIV_TQFT_KNOT_INVARIANTS_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, XI_POS, XI_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    results, checks, verified,
    state_space_logQ, state_space_log2,
    half_K, Z_proxy, Z_log_K,
    k_WRT,
    k_CS, k_CS_mod_Q,
    t_real, t_imag,
    top_charge,
    euler_graph, genus_proxy,
    link, reduced_link,
    kauffman_num, kauffman_div,
    surgery_index, lens_check,
)


class TestBridgeMetadata:
    def test_part_label(self):
        assert results["Part"] == "CCXXIV"

    def test_verified(self):
        assert verified is True
        assert results["Verified"] is True

    def test_zero_free_parameters(self):
        assert results["FreeParameters"] == 0

    def test_all_checks_pass(self):
        assert all(c["pass"] for c in checks)

    def test_check_count(self):
        assert len(checks) == 25


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_M_LAM(self):
        assert M_LAM == 27

    def test_EDGES(self):
        assert EDGES == 240

    def test_AUT_ORDER(self):
        assert AUT_ORDER == 51840


class TestTQFTStateSpace:
    """Bridge 1: TQFT state space = Q^V."""

    def test_state_space_logQ(self):
        assert state_space_logQ == V
        assert state_space_logQ == 40

    def test_state_space_log2(self):
        assert state_space_log2 == pytest.approx(V * math.log2(Q), abs=0.05)

    def test_log2_value(self):
        assert state_space_log2 == pytest.approx(63.4, abs=0.1)

    def test_state_space_log2_positive(self):
        assert state_space_log2 > 0


class TestPartitionFunction:
    """Bridge 2: Partition function proxy K^(K/2)."""

    def test_half_K(self):
        assert half_K == 6

    def test_half_K_formula(self):
        assert half_K == K // 2

    def test_Z_proxy(self):
        assert Z_proxy == K ** (K // 2)
        assert Z_proxy == 12 ** 6

    def test_Z_proxy_value(self):
        assert Z_proxy == 2985984

    def test_Z_log_K(self):
        assert Z_log_K == half_K
        assert Z_log_K == 6


class TestWRTInvariant:
    """Bridge 3: Witten-Reshetikhin-Turaev invariant level."""

    def test_k_WRT(self):
        assert k_WRT == AUT_ORDER // V
        assert k_WRT == 1296

    def test_k_WRT_is_power_of_6(self):
        assert k_WRT == 6 ** 4

    def test_k_WRT_is_square(self):
        assert k_WRT == 36 ** 2

    def test_k_WRT_positive(self):
        assert k_WRT > 0


class TestChernSimonsLevel:
    """Bridge 4: Chern-Simons level."""

    def test_k_CS(self):
        assert k_CS == K * (K - 1) // 2
        assert k_CS == 66

    def test_k_CS_mod_Q(self):
        assert k_CS_mod_Q == 0

    def test_k_CS_divisible_by_Q(self):
        assert k_CS % Q == 0

    def test_k_CS_positive(self):
        assert k_CS > 0


class TestJonesPolynomial:
    """Bridge 5: Jones polynomial root at t = exp(2πi/d)."""

    def test_t_real(self):
        # cos(2π/4) = cos(π/2) = 0
        assert t_real == pytest.approx(0.0, abs=1e-4)

    def test_t_imag(self):
        # sin(2π/4) = sin(π/2) = 1
        assert t_imag == pytest.approx(1.0, abs=1e-4)

    def test_unit_circle(self):
        assert t_real ** 2 + t_imag ** 2 == pytest.approx(1.0, abs=1e-6)

    def test_root_of_unity_order_d(self):
        # t^d = (e^(2πi/d))^d = e^(2πi) = 1; check real^2+imag^2 = 1
        import cmath
        t = complex(t_real, t_imag)
        assert abs(t ** MU - 1) < 1e-10


class TestTopologicalCharge:
    """Bridge 6: Topological charge."""

    def test_top_charge(self):
        assert top_charge == AUT_ORDER // K
        assert top_charge == 4320

    def test_top_charge_factorization(self):
        # 4320 = 6 * 720
        assert top_charge == 6 * 720

    def test_top_charge_positive(self):
        assert top_charge > 0

    def test_top_charge_divisible_by_K(self):
        assert AUT_ORDER % K == 0


class TestEulerCharacteristic:
    """Bridge 7: Euler characteristic and genus proxy."""

    def test_euler_graph(self):
        assert euler_graph == V - EDGES
        assert euler_graph == -200

    def test_euler_graph_negative(self):
        assert euler_graph < 0

    def test_genus_proxy(self):
        assert genus_proxy == (2 - euler_graph) // 2
        assert genus_proxy == 101

    def test_genus_positive(self):
        assert genus_proxy > 0


class TestLinkingNumber:
    """Bridge 8: Linking number proxy."""

    def test_link_zero(self):
        assert link == 0

    def test_link_formula(self):
        assert link == (LAM * V) // EDGES

    def test_reduced_link(self):
        assert reduced_link == 1

    def test_reduced_link_formula(self):
        assert reduced_link == EDGES // (V * (K // 2))


class TestKauffmanBracket:
    """Bridge 9: Kauffman bracket numerator proxy."""

    def test_kauffman_num(self):
        assert kauffman_num == Q ** K - 1
        assert kauffman_num == 531440

    def test_kauffman_divisibility(self):
        assert kauffman_div == 0

    def test_kauffman_div_formula(self):
        assert kauffman_num % (Q - 1) == 0

    def test_kauffman_positive(self):
        assert kauffman_num > 0


class TestSurgeryFormula:
    """Bridge 10: Dehn surgery formula index."""

    def test_surgery_index(self):
        assert surgery_index == M_LAM * MU // K
        assert surgery_index == 9

    def test_surgery_index_is_Q_squared(self):
        assert surgery_index == Q ** 2

    def test_lens_check(self):
        assert lens_check == M_LAM
        assert lens_check == 27

    def test_lens_check_formula(self):
        assert lens_check == surgery_index * K // MU


class TestJSONExport:
    def test_json_file_exists(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXIV_tqft_knot_invariants_results.json"
        assert json_file.exists()

    def test_json_content(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXIV_tqft_knot_invariants_results.json"
        with open(json_file) as f:
            data = json.load(f)
        assert data["Part"] == "CCXXIV"
        assert data["Verified"] is True
        assert len(data["Checks"]) == 25

    def test_json_bridges(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXIV_tqft_knot_invariants_results.json"
        with open(json_file) as f:
            data = json.load(f)
        bridges = data["Bridges"]
        assert "1_state_space_logQ" in bridges
        assert "3_k_WRT" in bridges
        assert "10_surgery_index" in bridges
