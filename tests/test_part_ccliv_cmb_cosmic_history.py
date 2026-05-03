"""Tests for Part CCLIV — CMB Photons and Cosmic History Bridge."""

import pytest

from PART_CCLIV_CMB_COSMIC_HISTORY_BRIDGE import (
    Q, V, K, LAM, MU, LAP_MID, EDGES,
    Phi6,
    universe_photon_exp, healpix_base, photon_baryon_exp, recombination_z_exp,
    inflation_efolds, S_BH, bbn_np_denom, bbn_np_num,
    cmb_dipole_l, cmb_quadrupole_l,
    cmb_energy_exp, cmb_number_exp,
    bao_half_oscillation, bao_full_oscillation,
    horizon_exponent_factor, spectral_distortion_exp, entropy_photon_ratio_order,
    checks, Verified,
)


def test_verified():
    assert Verified


def test_all_checks():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


class TestPhotonCount:
    def test_universe_photon_exp(self):
        assert universe_photon_exp == 88

    def test_universe_photon_formula(self):
        assert universe_photon_exp == LAM * MU * (K - 1)


class TestCMBStructure:
    def test_healpix_base(self):
        assert healpix_base == K == 12

    def test_photon_baryon_exp(self):
        assert photon_baryon_exp == LAP_MID == 10

    def test_recombination_z_exp(self):
        assert recombination_z_exp == Q == 3

    def test_dipole_l(self):
        assert cmb_dipole_l == 1

    def test_quadrupole_l(self):
        assert cmb_quadrupole_l == LAM == 2


class TestInflation:
    def test_efolds(self):
        assert inflation_efolds == 60

    def test_efolds_formula(self):
        assert inflation_efolds == EDGES // MU

    def test_efolds_equals_sbh(self):
        assert inflation_efolds == S_BH


class TestBBN:
    def test_np_denom(self):
        assert bbn_np_denom == Phi6 == 7

    def test_np_num(self):
        assert bbn_np_num == 1

    def test_phi6_cyclotomic(self):
        assert Phi6 == Q**2 - Q + 1


class TestTemperatureScalings:
    def test_energy_exp(self):
        assert cmb_energy_exp == MU == 4

    def test_number_exp(self):
        assert cmb_number_exp == Q == 3


class TestBAO:
    def test_half_oscillation(self):
        assert bao_half_oscillation == 1

    def test_full_oscillation(self):
        assert bao_full_oscillation == LAM == 2


class TestMisc:
    def test_horizon_factor(self):
        assert horizon_exponent_factor == LAM == 2

    def test_spectral_distortion_exp(self):
        assert spectral_distortion_exp == LAP_MID // LAM == 5

    def test_entropy_ratio_order(self):
        assert entropy_photon_ratio_order == Q == 3
