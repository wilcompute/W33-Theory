"""
Regression tests for Part CCXXVI: Loop Quantum Gravity and Spin Networks from W(3,3).

Validates the CCXXVI LQG spin-networks bridge. SRG(40,12,2,4) with |Aut|=51840=|W(E6)|.
Zero free parameters.
"""

import pytest
import sys
import json
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "exploration"))
from PART_CCXXVI_LQG_SPIN_NETWORKS_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, XI_POS, XI_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    results, checks, verified,
    j_max_num, j_max_den, j_max, hilbert_edge,
    gamma_num, gamma_den, j_sq_plus_j,
    area_proxy_num, area_proxy_den, area_proxy,
    vol_int, vol_mod_K, half_K,
    CG_channels, vertex_amplitude, vertex_amp_mod_V,
    entropy_int, half_EDGES,
    gamma_red_num, gamma_red_den,
    V_SN, E_SN, E_SN_mod_K, Q_sq,
    D_kin_proxy,
    holonomy_trace, K_half,
    theta_nets, theta_check,
)


class TestBridgeMetadata:
    def test_part_label(self):
        assert results["Part"] == "CCXXVI"

    def test_verified(self):
        assert verified is True
        assert results["Verified"] is True

    def test_zero_free_parameters(self):
        assert results["FreeParameters"] == 0

    def test_all_checks_pass(self):
        assert all(c["pass"] for c in checks)

    def test_check_count(self):
        assert len(checks) == 27


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


class TestSpinNetworkVertex:
    """Bridge 1: Spin j_max and Hilbert space edge dimension."""

    def test_j_max_numerator(self):
        assert j_max_num == K - 2
        assert j_max_num == 10

    def test_j_max_denominator(self):
        assert j_max_den == 2

    def test_j_max_value(self):
        assert j_max == 5

    def test_hilbert_edge_value(self):
        assert hilbert_edge == 11

    def test_hilbert_edge_is_2j_plus_1(self):
        assert hilbert_edge == 2 * j_max + 1

    def test_hilbert_edge_equals_LAP_MID_plus_1(self):
        assert hilbert_edge == LAP_MID + 1


class TestAreaEigenvalue:
    """Bridge 2: LQG area eigenvalue proxy."""

    def test_gamma_numerator(self):
        assert gamma_num == LAM
        assert gamma_num == 2

    def test_gamma_denominator(self):
        assert gamma_den == K
        assert gamma_den == 12

    def test_j_sq_plus_j(self):
        assert j_sq_plus_j == j_max * (j_max + 1)
        assert j_sq_plus_j == 30

    def test_area_proxy_numerator(self):
        assert area_proxy_num == 8 * gamma_num * j_sq_plus_j
        assert area_proxy_num == 480

    def test_area_proxy_denominator(self):
        assert area_proxy_den == K
        assert area_proxy_den == 12

    def test_area_proxy_equals_V(self):
        assert area_proxy == V
        assert area_proxy == 40


class TestVolumeEigenvalue:
    """Bridge 3: LQG volume eigenvalue proxy."""

    def test_vol_int(self):
        assert vol_int == j_sq_plus_j * j_max
        assert vol_int == 150

    def test_vol_mod_K(self):
        assert vol_mod_K == 150 % K
        assert vol_mod_K == 6

    def test_half_K(self):
        assert half_K == K // LAM
        assert half_K == 6

    def test_vol_mod_K_equals_half_K(self):
        assert vol_mod_K == half_K


class TestSpinFoamAmplitude:
    """Bridge 4: Clebsch-Gordan channels and vertex amplitude."""

    def test_CG_channels(self):
        assert CG_channels == 2 * j_max + 1
        assert CG_channels == 11

    def test_vertex_amplitude(self):
        assert vertex_amplitude == CG_channels ** 2
        assert vertex_amplitude == 121

    def test_vertex_amp_mod_V(self):
        assert vertex_amp_mod_V == vertex_amplitude % V
        assert vertex_amp_mod_V == 1


class TestBekensteinEntropy:
    """Bridge 5: Bekenstein-Hawking entropy proxy."""

    def test_entropy_int(self):
        assert entropy_int == Q * area_proxy
        assert entropy_int == 120

    def test_half_EDGES(self):
        assert half_EDGES == EDGES // 2
        assert half_EDGES == 120

    def test_entropy_equals_half_EDGES(self):
        assert entropy_int == half_EDGES


class TestImmirziParameter:
    """Bridge 6: Barbero-Immirzi parameter proxy γ = 1/6."""

    def test_gamma_reduced_num(self):
        assert gamma_red_num == 1

    def test_gamma_reduced_den(self):
        assert gamma_red_den == 6

    def test_gamma_fraction(self):
        assert gamma_red_num / gamma_red_den == pytest.approx(1 / 6, abs=1e-9)

    def test_gamma_den_equals_6_times_num(self):
        assert gamma_red_den == 6 * gamma_red_num


class TestSpinNetworkGraph:
    """Bridge 7: Spin-network graph edge count."""

    def test_V_SN(self):
        assert V_SN == LAP_MID
        assert V_SN == 10

    def test_E_SN(self):
        assert E_SN == V_SN * (V_SN - 1) // 2
        assert E_SN == 45

    def test_E_SN_mod_K(self):
        assert E_SN_mod_K == E_SN % K
        assert E_SN_mod_K == 9

    def test_Q_sq(self):
        assert Q_sq == Q ** 2
        assert Q_sq == 9

    def test_E_SN_mod_K_equals_Q_sq(self):
        assert E_SN_mod_K == Q_sq


class TestKinematicHilbert:
    """Bridge 8: Kinematic Hilbert space dimension proxy."""

    def test_D_kin_proxy(self):
        assert D_kin_proxy == CG_channels % V
        assert D_kin_proxy == 11

    def test_D_kin_proxy_equals_LAP_MID_plus_1(self):
        assert D_kin_proxy == LAP_MID + 1


class TestHolonomy:
    """Bridge 9: Loop holonomy trace."""

    def test_holonomy_trace(self):
        assert holonomy_trace == LAM * Q
        assert holonomy_trace == 6

    def test_K_half(self):
        assert K_half == K // 2
        assert K_half == 6

    def test_holonomy_trace_equals_K_half(self):
        assert holonomy_trace == K_half


class TestHamiltonianTheta:
    """Bridge 10: LQG Hamiltonian constraint theta-network count."""

    def test_theta_nets(self):
        assert theta_nets == M_LAM // Q
        assert theta_nets == 9

    def test_theta_check(self):
        assert theta_check == Q ** 2
        assert theta_check == 9

    def test_theta_nets_equals_Q_sq(self):
        assert theta_nets == theta_check


class TestJSONExport:
    def test_json_file_exists(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXVI_lqg_spin_networks_results.json"
        assert json_file.exists()

    def test_json_content(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXVI_lqg_spin_networks_results.json"
        with open(json_file) as f:
            data = json.load(f)
        assert data["Part"] == "CCXXVI"
        assert data["Verified"] is True
        assert len(data["Checks"]) == 27

    def test_json_bridges(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXVI_lqg_spin_networks_results.json"
        with open(json_file) as f:
            data = json.load(f)
        bridges = data["Bridges"]
        assert "1_j_max" in bridges
        assert "5_entropy" in bridges
        assert "10_theta" in bridges
