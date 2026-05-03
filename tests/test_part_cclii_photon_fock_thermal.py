"""Tests for Part CCLII — Photon Fock Space and Thermal Statistics Bridge."""

import pytest

from PART_CCLII_PHOTON_FOCK_THERMAL_BRIDGE import (
    Q, V, K, LAM, MU, LAP_MID, EDGES,
    photon_spin_integer, be_pole_order,
    stefan_boltzmann_exp, planck_integrand_power,
    photon_number_exp, photon_number_integrand_power,
    mode_polarizations, momentum_space_dim,
    zero_point_denom,
    universe_photon_exp,
    zeta_arg_number, zeta_arg_energy,
    wien_floor, wien_ceil,
    fock_vacuum_dim, noon_modes,
    coherent_mean_photon,
    checks, Verified,
)


def test_verified():
    assert Verified


def test_all_checks():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


class TestBoseEinstein:
    def test_photon_spin_integer(self):
        assert photon_spin_integer == 1

    def test_be_pole_order(self):
        assert be_pole_order == 1


class TestThermal:
    def test_stefan_boltzmann_exp(self):
        assert stefan_boltzmann_exp == MU == 4

    def test_planck_integrand_power(self):
        assert planck_integrand_power == Q == 3

    def test_planck_integrand_matches_mu_minus_1(self):
        assert planck_integrand_power == MU - 1

    def test_photon_number_exp(self):
        assert photon_number_exp == Q == 3

    def test_photon_number_integrand_power(self):
        assert photon_number_integrand_power == LAM == 2


class TestModes:
    def test_mode_polarizations(self):
        assert mode_polarizations == LAM == 2

    def test_momentum_space_dim(self):
        assert momentum_space_dim == Q == 3

    def test_zero_point_denom(self):
        assert zero_point_denom == LAM == 2


class TestZeta:
    def test_zeta_arg_number(self):
        assert zeta_arg_number == Q == 3

    def test_zeta_arg_energy(self):
        assert zeta_arg_energy == MU == 4


class TestWien:
    def test_wien_floor(self):
        assert wien_floor == LAM == 2

    def test_wien_ceil(self):
        assert wien_ceil == Q == 3


class TestFock:
    def test_fock_vacuum_dim(self):
        assert fock_vacuum_dim == 1

    def test_noon_modes(self):
        assert noon_modes == LAM == 2

    def test_coherent_mean_photon(self):
        assert coherent_mean_photon == 1

    def test_universe_photon_exp(self):
        assert universe_photon_exp == LAM * MU * (K - 1) == 88
