"""Tests for Part CCLIII — Casimir Effect Bridge."""

import math
import pytest

from PART_CCLIII_CASIMIR_EFFECT_BRIDGE import (
    Q, V, K, LAM, MU, M_NEG, LAP_MID, EDGES, AUT_ORDER,
    casimir_force_denom, casimir_force_dist_exp,
    casimir_energy_denom, casimir_energy_denom_aut, casimir_energy_dist_exp,
    casimir_energy_exp_form2,
    zeta_neg1_denom, zeta_neg1_num,
    zeta_neg3_denom, zeta_neg3_num,
    casimir_polarizations, mode_cutoff,
    bekenstein_entropy, casimir_bk_link,
    spacetime_dim, plate_dim,
    string_normal_order_denom, d_bosonic, d_superstring,
    casimir_6_factorial,
    checks, Verified,
)


def test_verified():
    assert Verified


def test_all_checks():
    failed = [lbl for lbl, v in checks if not v]
    assert failed == [], f"Failed checks: {failed}"


class TestCasimirForce:
    def test_force_denom_equals_edges(self):
        assert casimir_force_denom == EDGES == 240

    def test_force_dist_exp_equals_mu(self):
        assert casimir_force_dist_exp == MU == 4


class TestCasimirEnergy:
    def test_energy_denom_is_720(self):
        assert casimir_energy_denom == 720

    def test_energy_denom_is_factorial_6(self):
        assert casimir_energy_denom == math.factorial(6)

    def test_energy_denom_aut_form(self):
        assert casimir_energy_denom_aut == AUT_ORDER // (K * Q * LAM)

    def test_both_energy_forms_agree(self):
        assert casimir_energy_denom == casimir_energy_denom_aut

    def test_energy_dist_exp_equals_q(self):
        assert casimir_energy_dist_exp == Q == 3

    def test_energy_exp_form2_equals_q(self):
        assert casimir_energy_exp_form2 == Q

    def test_6_factorial_source(self):
        assert casimir_6_factorial == K // LAM == 6


class TestZeta:
    def test_zeta_neg1_denom(self):
        assert zeta_neg1_denom == K == 12

    def test_zeta_neg1_num(self):
        assert zeta_neg1_num == -1

    def test_zeta_neg3_denom(self):
        assert zeta_neg3_denom == EDGES // LAM == 120

    def test_zeta_neg3_num(self):
        assert zeta_neg3_num == 1


class TestPolarizations:
    def test_casimir_polarizations(self):
        assert casimir_polarizations == LAM == 2

    def test_mode_cutoff(self):
        assert mode_cutoff == K == 12


class TestBekenstein:
    def test_bekenstein_entropy(self):
        assert bekenstein_entropy == EDGES // MU == 60

    def test_casimir_bk_link(self):
        assert casimir_bk_link == bekenstein_entropy == 60

    def test_link_formula(self):
        assert casimir_bk_link == zeta_neg3_denom // LAM


class TestDimensions:
    def test_spacetime_dim(self):
        assert spacetime_dim == MU == 4

    def test_plate_dim(self):
        assert plate_dim == Q == 3

    def test_mu_minus_1_equals_q(self):
        assert MU - 1 == Q


class TestStringTheory:
    def test_normal_order_denom(self):
        assert string_normal_order_denom == K + M_NEG == 24

    def test_d_bosonic(self):
        assert d_bosonic == 26

    def test_d_superstring(self):
        assert d_superstring == LAP_MID == 10
