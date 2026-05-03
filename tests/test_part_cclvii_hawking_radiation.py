"""Tests for Part CCLVII: Hawking Radiation — W(3,3) Bridge."""
import pytest
from PART_CCLVII_HAWKING_RADIATION_BRIDGE import (
    schwarzschild_dim,
    kruskal_regions,
    penrose_diagram_corners,
    bh_no_hair_params,
    btz_spacetime_dim,
    bekenstein_entropy_denom,
    bekenstein_entropy,
    entropy_area_exponent,
    horizon_S2_dim,
    bekenstein_bound_2_factor,
    hawking_temp_spectral_gap,
    hawking_planck_power,
    hawking_photon_spin,
    evaporation_rate_exponent,
    unruh_temp_2_factor,
    near_horizon_rindler_coords,
    rindler_Z2_order,
    page_time_exponent,
    page_turnover,
    information_paradox_bits,
    w33_edges_lap_link,
    aut_entropy_link,
    lap_top_link,
    m_neg_link,
    ads_bulk_dim,
    string_dim,
    greybody_min_l,
    planck_length_exp_denom,
    checks,
    Verified,
)

Q, V, K, LAM, MU = 3, 40, 12, 2, 4
M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER = 27, 12, 10, 16, 240, 51840


class TestAllChecks:
    def test_all_checks_pass(self):
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"

    def test_verified(self):
        assert Verified is True


class TestSchwarzschildGeometry:
    def test_schwarzschild_dim(self):
        # 4D Schwarzschild: spacetime dimension = MU=4
        assert schwarzschild_dim == MU

    def test_kruskal_regions(self):
        # Kruskal maximal extension: MU=4 distinct regions
        assert kruskal_regions == MU

    def test_penrose_diagram_corners(self):
        # Penrose diagram: MU=4 boundary corners
        assert penrose_diagram_corners == MU

    def test_bh_no_hair_params(self):
        # No-hair: Q=3 parameters (mass, charge, spin)
        assert bh_no_hair_params == Q

    def test_btz_spacetime_dim(self):
        # BTZ black hole: 2+1 = Q=3 dimensions
        assert btz_spacetime_dim == Q


class TestBekensteinHawkingEntropy:
    def test_bekenstein_entropy_denom(self):
        # S_BH = A / (4 l_P^2): denominator = MU=4
        assert bekenstein_entropy_denom == MU

    def test_bekenstein_entropy(self):
        # EDGES//MU = 240//4 = 60 = V*Q//LAM = 40*3//2
        assert bekenstein_entropy == 60
        assert bekenstein_entropy == EDGES // MU
        assert bekenstein_entropy == V * Q // LAM

    def test_entropy_area_exponent(self):
        # Area ~ r^2: exponent = LAM=2
        assert entropy_area_exponent == LAM

    def test_horizon_S2_dim(self):
        # Event horizon S^2: dimension = LAM=2
        assert horizon_S2_dim == LAM

    def test_bekenstein_bound_2_factor(self):
        # Bekenstein bound: S <= 2*pi*R*E; leading 2 = LAM
        assert bekenstein_bound_2_factor == LAM


class TestHawkingTemperature:
    def test_hawking_temp_spectral_gap(self):
        # W(3,3) spectral gap encodes T_H scale = LAP_MID=10
        assert hawking_temp_spectral_gap == LAP_MID

    def test_hawking_planck_power(self):
        # Planck spectrum ~ omega^3: power = Q=3
        assert hawking_planck_power == Q

    def test_hawking_photon_spin(self):
        # Hawking radiation: spin-1 photons
        assert hawking_photon_spin == 1

    def test_evaporation_rate_exponent(self):
        # dM/dt ~ -1/M^2: exponent = LAM=2
        assert evaporation_rate_exponent == LAM


class TestUnruhEffect:
    def test_unruh_temp_2_factor(self):
        # T_U = hbar*a / (2*pi*k_B*c): factor 2 = LAM
        assert unruh_temp_2_factor == LAM

    def test_near_horizon_rindler_coords(self):
        # Rindler: 2 relevant coordinates (t, rho) = LAM=2
        assert near_horizon_rindler_coords == LAM

    def test_rindler_Z2_order(self):
        # Rindler wedge Z_2 time-reversal: order = LAM=2
        assert rindler_Z2_order == LAM


class TestPageCurve:
    def test_page_time_exponent(self):
        # Page time ~ M^3: exponent = Q=3
        assert page_time_exponent == Q

    def test_page_turnover(self):
        # Half entropy emitted = bekenstein_entropy = 60
        # Also: V + LAP_MID + LAP_MID = 40+10+10 = 60
        assert page_turnover == 60
        assert page_turnover == V + LAP_MID + LAP_MID
        assert page_turnover == bekenstein_entropy

    def test_information_paradox_bits(self):
        # Total information = EDGES=240
        assert information_paradox_bits == EDGES


class TestW33SpectralEncoding:
    def test_w33_edges_lap_link(self):
        # EDGES // (K * LAM) = 240 // 24 = 10 = LAP_MID
        assert w33_edges_lap_link == LAP_MID
        assert EDGES // (K * LAM) == LAP_MID

    def test_aut_entropy_link(self):
        # AUT_ORDER // (EDGES * LAM) = 51840 // 480 = 108 = M_LAM * MU
        assert aut_entropy_link == M_LAM * MU
        assert aut_entropy_link == 108

    def test_lap_top_link(self):
        # LAP_TOP = K + MU = 12 + 4 = 16
        assert lap_top_link == LAP_TOP
        assert lap_top_link == K + MU

    def test_m_neg_link(self):
        # M_NEG = LAP_MID + LAM = 10 + 2 = 12
        assert m_neg_link == M_NEG
        assert m_neg_link == LAP_MID + LAM


class TestAdsCFT:
    def test_ads_bulk_dim(self):
        # AdS/CFT type IIB on AdS5 x S5: bulk dim = LAP_MID=10
        assert ads_bulk_dim == LAP_MID

    def test_string_dim(self):
        # String theory: LAP_MID=10 dimensions
        assert string_dim == LAP_MID

    def test_greybody_min_l(self):
        # s-wave dominates Hawking emission: min l = 0
        assert greybody_min_l == 0

    def test_planck_length_exp_denom(self):
        # l_P = (hbar G / c^3)^(1/2): exponent denom = LAM=2
        assert planck_length_exp_denom == LAM
