"""
Regression tests for Part CCXXVII: Holographic Entanglement Entropy and
Ryu-Takayanagi from W(3,3).

SRG(40,12,2,4) with |Aut| = 51840 = |W(E6)|. Zero free parameters.
"""

import pytest
import sys
import json
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "exploration"))
from PART_CCXXVII_HEE_RT_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, XI_POS, XI_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    results, checks, verified,
    n_A, n_B, n_AB_total, boundary_sym, product_AB,
    cut, cut_alt,
    page_entropy,
    renyi2, renyi2_quot,
    I_proxy, cut_rem,
    EW_size, EW_mod_K,
    code_dist,
    C_V_proxy,
    S_island,
    delta_S, S_rel,
)


class TestBridgeMetadata:
    def test_part_label(self):
        assert results["Part"] == "CCXXVII"

    def test_verified(self):
        assert verified is True
        assert results["Verified"] is True

    def test_zero_free_parameters(self):
        assert results["FreeParameters"] == 0

    def test_all_checks_pass(self):
        assert all(c["pass"] for c in checks)

    def test_check_count(self):
        assert len(checks) == 28


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

    def test_M_NEG(self):
        assert M_NEG == 12

    def test_EDGES(self):
        assert EDGES == 240

    def test_AUT_ORDER(self):
        assert AUT_ORDER == 51840


class TestRTBipartition:
    """Bridge 1: Ryu-Takayanagi bipartition of the SRG."""

    def test_n_A_equals_K(self):
        assert n_A == K
        assert n_A == 12

    def test_n_B_equals_M_LAM(self):
        assert n_B == M_LAM
        assert n_B == 27

    def test_total_n_AB(self):
        assert n_AB_total == V - 1
        assert n_AB_total == 39

    def test_boundary_sym(self):
        assert boundary_sym == (Q * K) // LAM
        assert boundary_sym == 18

    def test_product_AB_is_boundary_sym_sq(self):
        assert product_AB == boundary_sym ** 2
        assert product_AB == 324

    def test_product_AB_is_K_times_M_LAM(self):
        assert product_AB == K * M_LAM


class TestRTCutSize:
    """Bridge 2: Ryu-Takayanagi minimal surface cut."""

    def test_cut_from_A_side(self):
        assert cut == K * (K - LAM - 1)
        assert cut == 108

    def test_cut_from_B_side(self):
        assert cut_alt == MU * M_LAM
        assert cut_alt == 108

    def test_cut_both_sides_equal(self):
        assert cut == cut_alt


class TestPageEntropy:
    """Bridge 3: Page entropy (information-theoretic entropy bound)."""

    def test_page_entropy_equals_K(self):
        assert page_entropy == K
        assert page_entropy == 12

    def test_page_entropy_equals_M_NEG(self):
        assert page_entropy == M_NEG


class TestRenyiEntropy:
    """Bridge 4: Rényi-2 entropy proxy from K^2 mod V."""

    def test_renyi2_is_K_sq_mod_V(self):
        assert renyi2 == K ** 2 % V
        assert renyi2 == 24

    def test_renyi2_is_2K(self):
        assert renyi2 == 2 * K

    def test_renyi2_quotient_is_Q(self):
        assert renyi2_quot == K ** 2 // V
        assert renyi2_quot == Q
        assert renyi2_quot == 3

    def test_K_sq_identity(self):
        # K^2 = V*Q + 2*K  (pure arithmetic identity of W(3,3))
        assert K ** 2 == V * Q + 2 * K


class TestMutualInformation:
    """Bridge 5: Holographic mutual information proxy."""

    def test_I_proxy_is_cut_div_LAP_MID(self):
        assert I_proxy == cut // LAP_MID
        assert I_proxy == 10

    def test_I_proxy_is_LAP_MID(self):
        assert I_proxy == LAP_MID

    def test_cut_remainder(self):
        assert cut_rem == cut % LAP_MID
        assert cut_rem == 2 * MU
        assert cut_rem == 8


class TestEntanglementWedge:
    """Bridge 6: Entanglement wedge reconstruction."""

    def test_EW_size_is_M_LAM(self):
        assert EW_size == M_LAM
        assert EW_size == 27

    def test_EW_size_is_Q_cubed(self):
        assert EW_size == Q ** 3

    def test_EW_size_mod_K(self):
        assert EW_mod_K == EW_size % K
        assert EW_mod_K == Q
        assert EW_mod_K == 3


class TestQECCodeDistance:
    """Bridge 7: Holographic quantum error correction code distance."""

    def test_code_dist_formula(self):
        assert code_dist == LAP_MID - LAM
        assert code_dist == 8

    def test_code_dist_is_2MU(self):
        assert code_dist == 2 * MU


class TestHolographicComplexity:
    """Bridge 8: Holographic complexity — CV conjecture."""

    def test_C_V_proxy(self):
        assert C_V_proxy == V // MU
        assert C_V_proxy == 10

    def test_C_V_proxy_is_LAP_MID(self):
        assert C_V_proxy == LAP_MID

    def test_C_V_proxy_times_MU_is_V(self):
        assert C_V_proxy * MU == V


class TestIslandFormula:
    """Bridge 9: Island formula for Page curve (Penington/AMMZ)."""

    def test_S_island_is_cut_mod_LAP_TOP(self):
        assert S_island == cut % LAP_TOP
        assert S_island == 12

    def test_S_island_is_K(self):
        assert S_island == K


class TestRelativeEntropy:
    """Bridge 10: Relative entropy (Uhlmann-Araki) proxy."""

    def test_delta_S(self):
        assert delta_S == M_LAM - M_NEG
        assert delta_S == 15

    def test_S_rel_mod(self):
        assert S_rel == delta_S % K
        assert S_rel == 3

    def test_S_rel_is_Q(self):
        assert S_rel == Q


class TestJSONExport:
    def test_json_file_exists(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXVII_hee_rt_results.json"
        assert json_file.exists()

    def test_json_content(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXVII_hee_rt_results.json"
        with open(json_file) as f:
            data = json.load(f)
        assert data["Part"] == "CCXXVII"
        assert data["Verified"] is True
        assert len(data["Checks"]) == 28

    def test_json_bridges(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXVII_hee_rt_results.json"
        with open(json_file) as f:
            data = json.load(f)
        bridges = data["Bridges"]
        assert "1_bipartition" in bridges
        assert "5_mutual_info" in bridges
        assert "10_relative_entropy" in bridges
