"""
Regression tests for Part CCXXV: Conformal Field Theory and OPE from W(3,3).

Validates the CCXXV CFT/OPE bridge. SRG(40,12,2,4) with |Aut|=51840=|W(E6)|.
Zero free parameters.
"""

import pytest
import sys
import json
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "exploration"))
from PART_CCXXV_CFT_OPE_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, XI_POS, XI_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    results, checks, verified,
    central_charge,
    h_pos_frac_num, h_pos_frac_den,
    h_neg_frac_num, h_neg_frac_den,
    ope_denom,
    kac_m, kac_n, kac_11_num, kac_11_denom,
    kac_21_frac_num, kac_21_frac_den,
    L0_eigenvalue,
    mm_p, mm_q,
    c_minimal_num, c_minimal_den,
    dim_S,
    N_fusion,
    c_UV_proxy, c_flow,
)


class TestBridgeMetadata:
    def test_part_label(self):
        assert results["Part"] == "CCXXV"

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


class TestCentralCharge:
    """Bridge 1: Central charge c = V - K - 1."""

    def test_central_charge_value(self):
        assert central_charge == 27

    def test_central_charge_formula(self):
        assert central_charge == V - K - 1

    def test_central_charge_equals_M_LAM(self):
        assert central_charge == M_LAM

    def test_central_charge_positive(self):
        assert central_charge > 0


class TestConformalWeights:
    """Bridge 2: Conformal weights from spectral eigenvalues."""

    def test_h_pos_numerator(self):
        assert h_pos_frac_num == 7

    def test_h_pos_denominator(self):
        assert h_pos_frac_den == 12

    def test_h_pos_fraction(self):
        # h_pos = 7/12 < 1
        assert h_pos_frac_num / h_pos_frac_den == pytest.approx(7 / 12, abs=1e-9)

    def test_h_neg_numerator(self):
        assert h_neg_frac_num == 2

    def test_h_neg_denominator(self):
        assert h_neg_frac_den == 3

    def test_h_neg_fraction(self):
        # h_neg = 2/3
        assert h_neg_frac_num / h_neg_frac_den == pytest.approx(2 / 3, abs=1e-9)

    def test_h_pos_less_than_h_neg(self):
        # 7/12 < 2/3 = 8/12
        assert h_pos_frac_num * h_neg_frac_den < h_neg_frac_num * h_pos_frac_den


class TestOPECoefficient:
    """Bridge 3: OPE coefficient denominator."""

    def test_ope_denom_value(self):
        assert ope_denom == 1296

    def test_ope_denom_formula(self):
        assert ope_denom == (K // LAM) ** MU

    def test_ope_denom_is_sixth_power(self):
        assert ope_denom == 6 ** 4

    def test_ope_denom_positive(self):
        assert ope_denom > 0


class TestKacTable:
    """Bridge 4: Kac table for (p,q) = (4,3) minimal model."""

    def test_kac_m(self):
        assert kac_m == MU
        assert kac_m == 4

    def test_kac_n(self):
        assert kac_n == Q
        assert kac_n == 3

    def test_kac_11_numerator_zero(self):
        assert kac_11_num == 0

    def test_kac_denom(self):
        assert kac_11_denom == 48

    def test_kac_denom_formula(self):
        assert kac_11_denom == 4 * kac_m * kac_n

    def test_kac_21_numerator(self):
        assert kac_21_frac_num == 1

    def test_kac_21_denominator(self):
        assert kac_21_frac_den == 2

    def test_kac_21_fraction(self):
        # h_{2,1} = 1/2
        assert kac_21_frac_num / kac_21_frac_den == pytest.approx(0.5, abs=1e-9)


class TestVirasoroL0:
    """Bridge 5: L0 eigenvalue = K."""

    def test_L0_eigenvalue(self):
        assert L0_eigenvalue == K
        assert L0_eigenvalue == 12

    def test_L0_positive(self):
        assert L0_eigenvalue > 0


class TestMinimalModel:
    """Bridge 6 & 7: M(p,q) minimal model."""

    def test_mm_p(self):
        assert mm_p == V // K
        assert mm_p == 3

    def test_mm_q(self):
        assert mm_q == K // MU
        assert mm_q == 3

    def test_mm_p_equals_Q(self):
        assert mm_p == Q

    def test_mm_q_equals_Q(self):
        assert mm_q == Q

    def test_mm_p_equals_mm_q(self):
        assert mm_p == mm_q

    def test_c_minimal_num(self):
        assert c_minimal_num == 9

    def test_c_minimal_den(self):
        assert c_minimal_den == 9

    def test_c_minimal_is_1(self):
        assert c_minimal_num // c_minimal_den == 1


class TestModularSMatrix:
    """Bridge 8: Modular S-matrix size."""

    def test_dim_S(self):
        assert dim_S == K + 1
        assert dim_S == 13

    def test_dim_S_positive(self):
        assert dim_S > 0


class TestFusionCoefficients:
    """Bridge 9: Verlinde fusion coefficients."""

    def test_N_fusion(self):
        assert N_fusion == M_NEG
        assert N_fusion == 12

    def test_N_fusion_equals_K(self):
        assert N_fusion == K


class TestCTheoremRGFlow:
    """Bridge 10: Zamolodchikov c-theorem and RG flow."""

    def test_c_UV_proxy(self):
        assert c_UV_proxy == K
        assert c_UV_proxy == 12

    def test_c_flow(self):
        assert c_flow == K - MU
        assert c_flow == 8

    def test_c_flow_formula(self):
        assert c_flow == 2 * MU

    def test_c_UV_greater_c_IR(self):
        c_IR = c_UV_proxy - c_flow
        assert c_UV_proxy > c_IR


class TestJSONExport:
    def test_json_file_exists(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXV_cft_ope_results.json"
        assert json_file.exists()

    def test_json_content(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXV_cft_ope_results.json"
        with open(json_file) as f:
            data = json.load(f)
        assert data["Part"] == "CCXXV"
        assert data["Verified"] is True
        assert len(data["Checks"]) == 28

    def test_json_bridges(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXV_cft_ope_results.json"
        with open(json_file) as f:
            data = json.load(f)
        bridges = data["Bridges"]
        assert "1_central_charge" in bridges
        assert "6_mm_p" in bridges
        assert "10_c_flow" in bridges
