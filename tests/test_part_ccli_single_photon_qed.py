"""Tests for Part CCLI — Single Photon QED Bridge."""

import pytest

from PART_CCLI_SINGLE_PHOTON_QED_BRIDGE import (
    Q, V, K, LAM, MU, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    photon_spin, photon_helicity_states, photon_magnetic_numbers,
    clifford_dim, dirac_components, gamma_basis_bivectors,
    lorentz_rank, lorentz_vector_dim, lorentz_adj_dim,
    a_components, physical_dof,
    lepton_families, quark_colors, quark_generations,
    ward_identity, photon_mass_exp,
    weyl_spinor_dim, dirac_from_weyl, schwinger_denom,
    u1_rank, u1_dim, u1_generators,
    checks, Verified,
)


def test_verified():
    assert Verified


def test_all_checks():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


class TestSpin:
    def test_photon_spin(self):
        assert photon_spin == 1

    def test_photon_helicity_states(self):
        assert photon_helicity_states == LAM == 2

    def test_photon_magnetic_numbers(self):
        assert photon_magnetic_numbers == Q == 3

    def test_magnetic_matches_2j_plus_1(self):
        assert photon_magnetic_numbers == 2 * photon_spin + 1


class TestDiracAlgebra:
    def test_clifford_dim(self):
        assert clifford_dim == LAP_TOP == 16

    def test_clifford_power_form(self):
        assert clifford_dim == LAM ** MU   # 2^4 = 16

    def test_dirac_components(self):
        assert dirac_components == MU == 4

    def test_gamma_bivectors(self):
        assert gamma_basis_bivectors == K // LAM == 6


class TestLorentz:
    def test_lorentz_rank(self):
        assert lorentz_rank == LAM == 2

    def test_lorentz_vector_dim(self):
        assert lorentz_vector_dim == MU == 4

    def test_lorentz_adj_dim(self):
        assert lorentz_adj_dim == K // LAM == 6


class TestGaugeField:
    def test_a_components(self):
        assert a_components == MU == 4

    def test_physical_dof(self):
        assert physical_dof == LAM == 2

    def test_physical_dof_reduction(self):
        # A_mu (4) minus longitudinal (1) minus gauge (1) = 2 = LAM
        assert a_components - 2 * (LAM // LAM) == LAM

    def test_ward_identity(self):
        assert ward_identity == 0

    def test_photon_mass_exp(self):
        assert photon_mass_exp == V + K + LAM == 54


class TestSM:
    def test_lepton_families(self):
        assert lepton_families == Q == 3

    def test_quark_colors(self):
        assert quark_colors == Q == 3

    def test_quark_generations(self):
        assert quark_generations == Q == 3

    def test_weyl_spinor_dim(self):
        assert weyl_spinor_dim == LAM == 2

    def test_dirac_from_weyl(self):
        assert dirac_from_weyl == MU == 4

    def test_schwinger_denom(self):
        assert schwinger_denom == LAM == 2

    def test_u1_rank(self):
        assert u1_rank == 1

    def test_u1_dim(self):
        assert u1_dim == 1

    def test_u1_generators(self):
        assert u1_generators == 1
