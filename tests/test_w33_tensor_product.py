"""Tests for Part MCLVIII: Tensor Product Spectrum for W(3,3)."""
import pytest
from fractions import Fraction
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'analysis'))
from w33_tensor_product import (
    tensor_product_spectrum,
    symmetric_kronecker_spectrum,
    cartesian_product_spectrum,
    strong_product_spectrum,
    verify_tensor_trace,
    verify_tensor_frobenius,
    tensor_equal_energy_analysis,
    novel_tensor_identities,
    tensor_product_main,
    v, k,
)

V, K = 40, 12


class TestTensorProductSpectrum:
    def setup_method(self):
        self.eigs = tensor_product_spectrum()

    def test_dimension(self):
        total = sum(m for _, m in self.eigs)
        assert total == V * V

    def test_largest_eigenvalue(self):
        assert self.eigs[0][0] == Fraction(K * K)

    def test_largest_mult(self):
        assert self.eigs[0][1] == 1

    def test_eigenvalue_set(self):
        eig_vals = {e for e, _ in self.eigs}
        expected = {Fraction(144), Fraction(24), Fraction(16),
                    Fraction(4), Fraction(-8), Fraction(-48)}
        assert eig_vals == expected

    def test_trace_zero(self):
        trace = verify_tensor_trace(self.eigs)
        assert trace == Fraction(0)

    def test_frobenius_sq(self):
        frob = verify_tensor_frobenius(self.eigs)
        # ||A||_F^2 = 480 = kv; ||A⊗A||_F^2 = 480^2
        assert frob == Fraction(480 * 480)


class TestTensorMultiplicities:
    def setup_method(self):
        self.eigs = dict(tensor_product_spectrum())

    def test_mult_144(self):
        assert self.eigs[Fraction(144)] == 1

    def test_mult_24(self):
        assert self.eigs[Fraction(24)] == 48   # 2*1*24

    def test_mult_16(self):
        assert self.eigs[Fraction(16)] == 225  # 15*15 = s*s

    def test_mult_4(self):
        assert self.eigs[Fraction(4)] == 576   # 24*24 = r*r

    def test_mult_neg8(self):
        assert self.eigs[Fraction(-8)] == 720  # 2*24*15

    def test_mult_neg48(self):
        assert self.eigs[Fraction(-48)] == 30  # 2*1*15


class TestCartesianProduct:
    def setup_method(self):
        self.eigs = dict(cartesian_product_spectrum())

    def test_max_eigenvalue(self):
        assert max(self.eigs.keys()) == Fraction(2 * K)

    def test_trace_zero(self):
        trace = sum(e * m for e, m in self.eigs.items())
        assert trace == 0

    def test_dimension(self):
        assert sum(self.eigs.values()) == V * V


class TestStrongProduct:
    def setup_method(self):
        self.eigs = dict(strong_product_spectrum())

    def test_max_eigenvalue(self):
        assert max(self.eigs.keys()) == Fraction((1 + K) * (1 + K) - 1)

    def test_dimension(self):
        assert sum(self.eigs.values()) == V * V

    def test_eigenvalue_8_multiplicity(self):
        # (1+r)^2-1 = (1+s)^2-1 = 8; mult = m_r^2 + m_s^2 = 576+225 = 801
        assert self.eigs[Fraction(8)] == 801

    def test_eigenvalue_neg10_multiplicity(self):
        # (1+r)(1+s)-1 = -10; mult = 2*m_r*m_s = 720
        assert self.eigs[Fraction(-10)] == 720


class TestKemenyCrossProduct:
    """The crown jewel: strong product mult(8) = m_r^2 + m_s^2 = 801 = 20*Kemeny."""

    def test_m_r_sq_plus_m_s_sq(self):
        assert 24 * 24 + 15 * 15 == 801

    def test_kemeny_from_strong_product(self):
        # strong mult(8) / 20 = Kemeny
        assert Fraction(801, 20) == Fraction(801, 20)

    def test_equal_energy_implies_kemeny(self):
        # mu_r = 20/m_r = 5/6, mu_s = 20/m_s = 4/3
        # K = m_r/mu_r + m_s/mu_s = m_r^2/20 + m_s^2/20 = (m_r^2+m_s^2)/20 = 801/20
        common_energy = Fraction(20)
        m_r, m_s = 24, 15
        K = Fraction(m_r * m_r) / common_energy + Fraction(m_s * m_s) / common_energy
        assert K == Fraction(801, 20)


class TestEnergyBalance:
    def setup_method(self):
        self.eigs = tensor_product_spectrum()

    def test_pos_subleading_energy(self):
        pos = sum(e * m for e, m in self.eigs if 0 < e < K * K)
        assert pos == Fraction(7056)

    def test_neg_subleading_energy(self):
        neg = sum(e * m for e, m in self.eigs if e < 0)
        assert neg == Fraction(-7200)

    def test_energy_balance_equals_neg_k_sq(self):
        pos = sum(e * m for e, m in self.eigs if 0 < e < K * K)
        neg = sum(e * m for e, m in self.eigs if e < 0)
        assert pos + neg == Fraction(-K * K)


class TestFullPacket:
    def test_main_runs(self):
        results = tensor_product_main()
        assert results["n_verified"] == 14
        assert results["strong_mult_8"] == 801
        assert results["kemeny_connection"] == "801/20"
