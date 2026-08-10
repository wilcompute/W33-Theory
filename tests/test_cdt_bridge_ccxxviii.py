"""
Regression tests for Part CCXXVIII: Causal Dynamical Triangulation from W(3,3).

Covers all 28 bridge checks across 13 test classes.
"""

import json
import math
import pathlib
import pytest

from PART_CCXXVIII_CDT_BRIDGE import (
    # SRG constants (via re-export)
    Q, V, K, LAM, MU, M_LAM, M_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    # Bridge 1
    dim_CDT, n_simplex_verts,
    # Bridge 2
    chi_S4, chi_S2, chi_sum,
    # Bridge 3
    d_s_UV, d_s_IR, delta_d_s,
    # Bridge 4
    regge_links, regge_check,
    # Bridge 5
    N_slices, slice_vol, slice_dS,
    # Bridge 6
    vol4_proxy, vol4_per_slice,
    # Bridge 7
    l_Pl_num, l_Pl_den, l_Pl_red_num, l_Pl_red_den,
    # Bridge 8
    Lambda_cdt,
    # Bridge 9
    G_N_proxy, G_N_times_MU,
    # Bridge 10
    S_dS_proxy, S_dS_Q_check,
    # Verification flag
    Verified,
)

ROOT = pathlib.Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
class TestBridgeMetadata:
    def test_verified_true(self):
        assert Verified is True

    def test_checks_total(self):
        from PART_CCXXVIII_CDT_BRIDGE import checks
        assert len(checks) == 28

    def test_all_checks_pass(self):
        from PART_CCXXVIII_CDT_BRIDGE import checks
        failed = [lbl for lbl, v in checks if not v]
        assert failed == [], f"Failed checks: {failed}"

    def test_json_exists(self):
        assert (ROOT / "PART_CCXXVIII_cdt_results.json").exists()

    def test_json_verified(self):
        data = json.loads((ROOT / "PART_CCXXVIII_cdt_results.json").read_text(encoding="utf-8"))
        assert data["Verified"] is True


# ---------------------------------------------------------------------------
# SRG parameters
# ---------------------------------------------------------------------------
class TestSRGParameters:
    def test_Q(self):   assert Q == 3
    def test_V(self):   assert V == 40
    def test_K(self):   assert K == 12
    def test_LAM(self): assert LAM == 2
    def test_MU(self):  assert MU == 4
    def test_M_LAM(self): assert M_LAM == 27
    def test_M_NEG(self): assert M_NEG == 12
    def test_LAP_MID(self): assert LAP_MID == 10
    def test_EDGES(self): assert EDGES == 240


# ---------------------------------------------------------------------------
# Bridge 1: Simplex geometry
# ---------------------------------------------------------------------------
class TestSimplexGeometry:
    def test_dim_CDT_equals_MU(self):
        assert dim_CDT == MU

    def test_dim_CDT_is_4(self):
        assert dim_CDT == 4

    def test_n_simplex_verts_equals_MU_plus_1(self):
        assert n_simplex_verts == MU + 1

    def test_n_simplex_verts_is_5(self):
        assert n_simplex_verts == 5


# ---------------------------------------------------------------------------
# Bridge 2: Euler characteristics
# ---------------------------------------------------------------------------
class TestEulerCharacteristic:
    def test_chi_S4_equals_LAM(self):
        assert chi_S4 == LAM

    def test_chi_S2_equals_LAM(self):
        assert chi_S2 == LAM

    def test_chi_sum_equals_MU(self):
        assert chi_sum == MU

    def test_chi_sum_is_4(self):
        assert chi_sum == 4


# ---------------------------------------------------------------------------
# Bridge 3: Spectral dimension
# ---------------------------------------------------------------------------
class TestSpectralDimension:
    def test_d_s_UV_equals_LAM(self):
        assert d_s_UV == LAM

    def test_d_s_IR_equals_MU(self):
        assert d_s_IR == MU

    def test_delta_d_s_equals_LAM(self):
        assert delta_d_s == LAM

    def test_delta_d_s_is_2(self):
        assert delta_d_s == 2

    def test_delta_d_s_equals_d_s_IR_minus_d_s_UV(self):
        assert delta_d_s == d_s_IR - d_s_UV


# ---------------------------------------------------------------------------
# Bridge 4: Regge links
# ---------------------------------------------------------------------------
class TestReggeLinks:
    def test_regge_links_equals_EDGES_div_K(self):
        assert regge_links == EDGES // K

    def test_regge_links_equals_V_div_2(self):
        assert regge_links == V // 2

    def test_regge_links_is_20(self):
        assert regge_links == 20

    def test_regge_check_equals_V(self):
        assert regge_check == V

    def test_regge_check_is_40(self):
        assert regge_check == 40


# ---------------------------------------------------------------------------
# Bridge 5: CDT foliation
# ---------------------------------------------------------------------------
class TestFoliation:
    def test_N_slices_equals_Q(self):
        assert N_slices == Q

    def test_N_slices_is_3(self):
        assert N_slices == 3

    def test_slice_vol_is_30(self):
        assert slice_vol == 30

    def test_slice_vol_equals_N_slices_times_LAP_MID(self):
        assert slice_vol == N_slices * LAP_MID

    def test_slice_dS_equals_slice_vol(self):
        assert slice_dS == slice_vol


# ---------------------------------------------------------------------------
# Bridge 6: 4-volume
# ---------------------------------------------------------------------------
class TestFourVolume:
    def test_vol4_proxy_equals_V_times_K(self):
        assert vol4_proxy == V * K

    def test_vol4_proxy_is_480(self):
        assert vol4_proxy == 480

    def test_vol4_proxy_equals_2_times_EDGES(self):
        assert vol4_proxy == 2 * EDGES

    def test_vol4_per_slice_equals_MU_times_K(self):
        assert vol4_per_slice == MU * K

    def test_vol4_per_slice_is_48(self):
        assert vol4_per_slice == 48


# ---------------------------------------------------------------------------
# Bridge 7: Planck length
# ---------------------------------------------------------------------------
class TestPlanckLength:
    def test_l_Pl_num_equals_LAM(self):
        assert l_Pl_num == LAM

    def test_l_Pl_den_equals_MU(self):
        assert l_Pl_den == MU

    def test_l_Pl_red_num_is_1(self):
        assert l_Pl_red_num == 1

    def test_l_Pl_red_den_is_2(self):
        assert l_Pl_red_den == 2

    def test_l_Pl_reduced_fraction(self):
        assert l_Pl_red_den == 2 * l_Pl_red_num


# ---------------------------------------------------------------------------
# Bridge 8: Cosmological constant
# ---------------------------------------------------------------------------
class TestCosmologicalConstant:
    def test_Lambda_cdt_equals_MLAM_div_K(self):
        assert Lambda_cdt == M_LAM // K

    def test_Lambda_cdt_equals_LAM(self):
        assert Lambda_cdt == LAM

    def test_Lambda_cdt_is_2(self):
        assert Lambda_cdt == 2


# ---------------------------------------------------------------------------
# Bridge 9: Newton constant
# ---------------------------------------------------------------------------
class TestNewtonConstant:
    def test_G_N_proxy_equals_K_div_MU(self):
        assert G_N_proxy == K // MU

    def test_G_N_proxy_equals_Q(self):
        assert G_N_proxy == Q

    def test_G_N_proxy_is_3(self):
        assert G_N_proxy == 3

    def test_G_N_times_MU_equals_K(self):
        assert G_N_times_MU == K


# ---------------------------------------------------------------------------
# Bridge 10: De Sitter entropy
# ---------------------------------------------------------------------------
class TestDeSitterEntropy:
    def test_S_dS_proxy_equals_EDGES_div_8(self):
        assert S_dS_proxy == EDGES // (MU * LAM)

    def test_S_dS_Q_check_equals_Q_times_LAP_MID(self):
        assert S_dS_Q_check == Q * LAP_MID

    def test_S_dS_proxy_equals_S_dS_Q_check(self):
        assert S_dS_proxy == S_dS_Q_check

    def test_S_dS_proxy_is_30(self):
        assert S_dS_proxy == 30


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------
class TestJSONExport:
    def _data(self):
        return json.loads((ROOT / "PART_CCXXVIII_cdt_results.json").read_text(encoding="utf-8"))

    def test_json_part(self):
        assert self._data()["Part"] == "CCXXVIII"

    def test_json_checks_passed(self):
        assert self._data()["checks_passed"] == 28

    def test_json_bridges_keys(self):
        keys = set(self._data()["bridges"].keys())
        expected = {
            "1_simplex_geometry", "2_euler_characteristic",
            "3_spectral_dimension", "4_regge_links",
            "5_foliation", "6_4volume", "7_planck_length",
            "8_cosm_constant", "9_newton_constant", "10_desitter_entropy",
        }
        assert keys == expected
