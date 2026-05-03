"""
Tests for Part CCXXIX: Non-commutative Geometry and Spectral Triples from W(3,3).

Covers all 29 bridge checks and JSON export integrity.
"""

import json
import math
import os
import pytest

# SRG parameters (directly from PART_CCXVIII)
Q = 3
V = 40
K = 12
LAM = 2
MU = 4
M_LAM = 27
M_NEG = 12
LAP_MID = 10
LAP_TOP = 16
EDGES = 240
AUT_ORDER = 51840


class TestBridgeMetadata:
    """Bridge module loads and reports verified status."""

    def test_import(self):
        from PART_CCXXIX_NCG_BRIDGE import Verified
        assert Verified is True

    def test_checks_passed(self):
        from PART_CCXXIX_NCG_BRIDGE import passed, checks
        assert passed == len(checks)

    def test_verified_true(self):
        from PART_CCXXIX_NCG_BRIDGE import Verified
        assert Verified

    def test_checks_count(self):
        from PART_CCXXIX_NCG_BRIDGE import checks
        assert len(checks) == 29

    def test_no_failed_checks(self):
        from PART_CCXXIX_NCG_BRIDGE import failed
        assert failed == []


class TestSRGParameters:
    """Validate immutable SRG(40,12,2,4) constants are unchanged."""

    def test_Q(self):
        from PART_CCXXIX_NCG_BRIDGE import Q as q
        assert q == 3

    def test_V(self):
        from PART_CCXXIX_NCG_BRIDGE import V as v
        assert v == 40

    def test_K(self):
        from PART_CCXXIX_NCG_BRIDGE import K as k
        assert k == 12

    def test_LAM(self):
        from PART_CCXXIX_NCG_BRIDGE import LAM as lam
        assert lam == 2

    def test_MU(self):
        from PART_CCXXIX_NCG_BRIDGE import MU as mu
        assert mu == 4

    def test_LAP_MID(self):
        from PART_CCXXIX_NCG_BRIDGE import LAP_MID as lm
        assert lm == 10

    def test_LAP_TOP(self):
        from PART_CCXXIX_NCG_BRIDGE import LAP_TOP as lt
        assert lt == 16

    def test_EDGES(self):
        from PART_CCXXIX_NCG_BRIDGE import EDGES as e
        assert e == 240

    def test_AUT_ORDER(self):
        from PART_CCXXIX_NCG_BRIDGE import AUT_ORDER as ao
        assert ao == 51840


class TestKODimension:
    """Bridge 1: KO-dimension of the SM spectral triple."""

    def test_KO_dim_value(self):
        from PART_CCXXIX_NCG_BRIDGE import KO_dim
        assert KO_dim == 6

    def test_KO_dim_equals_K_half(self):
        from PART_CCXXIX_NCG_BRIDGE import KO_dim
        assert KO_dim == K // 2

    def test_KO_dim_mod8(self):
        from PART_CCXXIX_NCG_BRIDGE import KO_dim_mod8
        assert KO_dim_mod8 == 6

    def test_KO_dim_mod8_in_Z8(self):
        from PART_CCXXIX_NCG_BRIDGE import KO_dim_mod8
        assert 0 <= KO_dim_mod8 < 8

    def test_KO_plus_spacetime_equals_LAPMID(self):
        from PART_CCXXIX_NCG_BRIDGE import KO_plus_spacetime
        assert KO_plus_spacetime == LAP_MID

    def test_KO_plus_spacetime_value(self):
        from PART_CCXXIX_NCG_BRIDGE import KO_plus_spacetime
        assert KO_plus_spacetime == 10


class TestFermionicGenerations:
    """Bridge 2: Three fermionic generations from Q."""

    def test_n_gen_equals_Q(self):
        from PART_CCXXIX_NCG_BRIDGE import n_gen
        assert n_gen == Q

    def test_n_gen_value(self):
        from PART_CCXXIX_NCG_BRIDGE import n_gen
        assert n_gen == 3

    def test_Q_sq(self):
        from PART_CCXXIX_NCG_BRIDGE import Q_sq
        assert Q_sq == 9

    def test_n_gen_K_product(self):
        from PART_CCXXIX_NCG_BRIDGE import n_gen_K_product
        assert n_gen_K_product == 36

    def test_n_gen_K_equals_MU_Qsq(self):
        from PART_CCXXIX_NCG_BRIDGE import n_gen_K_product, Q_sq
        assert n_gen_K_product == MU * Q_sq


class TestGaugeRank:
    """Bridge 3: SM gauge group rank = MU = 4."""

    def test_SM_rank_equals_MU(self):
        from PART_CCXXIX_NCG_BRIDGE import SM_rank
        assert SM_rank == MU

    def test_SM_rank_value(self):
        from PART_CCXXIX_NCG_BRIDGE import SM_rank
        assert SM_rank == 4

    def test_SM_rank_sq_equals_LAPTOP(self):
        from PART_CCXXIX_NCG_BRIDGE import SM_rank_sq
        assert SM_rank_sq == LAP_TOP

    def test_SM_rank_sq_value(self):
        from PART_CCXXIX_NCG_BRIDGE import SM_rank_sq
        assert SM_rank_sq == 16

    def test_SM_rank_sq_equals_MU2(self):
        from PART_CCXXIX_NCG_BRIDGE import SM_rank_sq
        assert SM_rank_sq == MU ** 2


class TestSpectralTripleDimension:
    """Bridge 4: NCG spectral triple dimension structure."""

    def test_d_spec_equals_MU(self):
        from PART_CCXXIX_NCG_BRIDGE import d_spec
        assert d_spec == MU

    def test_d_KO_equals_K_half(self):
        from PART_CCXXIX_NCG_BRIDGE import d_KO
        assert d_KO == K // 2

    def test_d_sum_equals_LAPMID(self):
        from PART_CCXXIX_NCG_BRIDGE import d_sum
        assert d_sum == LAP_MID

    def test_d_sum_value(self):
        from PART_CCXXIX_NCG_BRIDGE import d_sum
        assert d_sum == 10

    def test_d_KO_plus_d_spec(self):
        from PART_CCXXIX_NCG_BRIDGE import d_spec, d_KO, d_sum
        assert d_spec + d_KO == d_sum


class TestDiracZeroModes:
    """Bridge 5: Dirac operator zero-mode count via index theorem proxy."""

    def test_KL_prod(self):
        from PART_CCXXIX_NCG_BRIDGE import KL_prod
        assert KL_prod == 24

    def test_KL_prod_equals_K_times_LAM(self):
        from PART_CCXXIX_NCG_BRIDGE import KL_prod
        assert KL_prod == K * LAM

    def test_zero_modes_proxy_value(self):
        from PART_CCXXIX_NCG_BRIDGE import zero_modes_proxy
        assert zero_modes_proxy == 16

    def test_zero_modes_proxy_equals_V_mod_KL(self):
        from PART_CCXXIX_NCG_BRIDGE import zero_modes_proxy, KL_prod
        assert zero_modes_proxy == V % KL_prod

    def test_zero_modes_proxy_equals_LAPTOP(self):
        from PART_CCXXIX_NCG_BRIDGE import zero_modes_proxy
        assert zero_modes_proxy == LAP_TOP


class TestHeatKernel:
    """Bridge 6: Seeley-DeWitt heat-kernel coefficients."""

    def test_a_0_equals_V(self):
        from PART_CCXXIX_NCG_BRIDGE import a_0
        assert a_0 == V

    def test_a_2_equals_K(self):
        from PART_CCXXIX_NCG_BRIDGE import a_2
        assert a_2 == K

    def test_a_4_equals_LAM(self):
        from PART_CCXXIX_NCG_BRIDGE import a_4
        assert a_4 == LAM

    def test_a4_times_a2_equals_KL_prod(self):
        from PART_CCXXIX_NCG_BRIDGE import a_4_times_a_2, KL_prod
        assert a_4_times_a_2 == KL_prod

    def test_a4_times_a2_value(self):
        from PART_CCXXIX_NCG_BRIDGE import a_4_times_a_2
        assert a_4_times_a_2 == 24

    def test_a0_minus_a4a2_equals_LAPTOP(self):
        from PART_CCXXIX_NCG_BRIDGE import a_0_minus_a4a2
        assert a_0_minus_a4a2 == LAP_TOP

    def test_a0_minus_a4a2_value(self):
        from PART_CCXXIX_NCG_BRIDGE import a_0_minus_a4a2
        assert a_0_minus_a4a2 == 16


class TestSpectralAction:
    """Bridge 7: Spectral action bosonic term count."""

    def test_spec_act_proxy_equals_EDGES_div_KL(self):
        from PART_CCXXIX_NCG_BRIDGE import spec_act_proxy, KL_prod
        assert spec_act_proxy == EDGES // KL_prod

    def test_spec_act_proxy_equals_LAPMID(self):
        from PART_CCXXIX_NCG_BRIDGE import spec_act_proxy
        assert spec_act_proxy == LAP_MID

    def test_spec_act_proxy_value(self):
        from PART_CCXXIX_NCG_BRIDGE import spec_act_proxy
        assert spec_act_proxy == 10

    def test_spec_act_cross_equals_V_half(self):
        from PART_CCXXIX_NCG_BRIDGE import spec_act_cross
        assert spec_act_cross == V // 2

    def test_spec_act_cross_value(self):
        from PART_CCXXIX_NCG_BRIDGE import spec_act_cross
        assert spec_act_cross == 20


class TestHochschildCohomology:
    """Bridge 8: Hochschild cohomology dimension of the SM finite algebra."""

    def test_hh_dim_equals_LAPTOP(self):
        from PART_CCXXIX_NCG_BRIDGE import hh_dim
        assert hh_dim == LAP_TOP

    def test_hh_dim_equals_MU2(self):
        from PART_CCXXIX_NCG_BRIDGE import hh_dim
        assert hh_dim == MU ** 2

    def test_hh_dim_value(self):
        from PART_CCXXIX_NCG_BRIDGE import hh_dim
        assert hh_dim == 16


class TestMoyalDeformation:
    """Bridge 9: Moyal deformation parameter θ."""

    def test_theta_proxy_equals_MU_div_LAM(self):
        from PART_CCXXIX_NCG_BRIDGE import theta_proxy
        assert theta_proxy == MU // LAM

    def test_theta_proxy_equals_LAM(self):
        from PART_CCXXIX_NCG_BRIDGE import theta_proxy
        assert theta_proxy == LAM

    def test_theta_proxy_value(self):
        from PART_CCXXIX_NCG_BRIDGE import theta_proxy
        assert theta_proxy == 2

    def test_theta_scaling_equals_KL_prod(self):
        from PART_CCXXIX_NCG_BRIDGE import theta_scaling, KL_prod
        assert theta_scaling == KL_prod

    def test_theta_scaling_value(self):
        from PART_CCXXIX_NCG_BRIDGE import theta_scaling
        assert theta_scaling == 24


class TestSpectralZeta:
    """Bridge 10: Spectral zeta function residues."""

    def test_z_0_equals_V_div_MU(self):
        from PART_CCXXIX_NCG_BRIDGE import z_0
        assert z_0 == V // MU

    def test_z_0_equals_LAPMID(self):
        from PART_CCXXIX_NCG_BRIDGE import z_0
        assert z_0 == LAP_MID

    def test_z_0_value(self):
        from PART_CCXXIX_NCG_BRIDGE import z_0
        assert z_0 == 10

    def test_z_1_equals_K_div_Q(self):
        from PART_CCXXIX_NCG_BRIDGE import z_1
        assert z_1 == K // Q

    def test_z_1_equals_MU(self):
        from PART_CCXXIX_NCG_BRIDGE import z_1
        assert z_1 == MU

    def test_z_1_value(self):
        from PART_CCXXIX_NCG_BRIDGE import z_1
        assert z_1 == 4

    def test_z_product_equals_V(self):
        from PART_CCXXIX_NCG_BRIDGE import z_product
        assert z_product == V

    def test_z_product_value(self):
        from PART_CCXXIX_NCG_BRIDGE import z_product
        assert z_product == 40


class TestJSONExport:
    """JSON output integrity."""

    @pytest.fixture(scope="class")
    def result_data(self):
        path = os.path.join(os.path.dirname(__file__), "..", "PART_CCXXIX_ncg_results.json")
        with open(path) as f:
            return json.load(f)

    def test_part_field(self, result_data):
        assert result_data["Part"] == "CCXXIX"

    def test_verified_true(self, result_data):
        assert result_data["Verified"] is True

    def test_all_checks_passed(self, result_data):
        assert result_data["checks_passed"] == result_data["checks_total"]

    def test_checks_count(self, result_data):
        assert result_data["checks_total"] == 29

    def test_all_individual_checks_true(self, result_data):
        for key, val in result_data["checks"].items():
            assert val is True, f"Check {key!r} not True in JSON"
