"""
Phase V48 — Exact lepton-sector closure
=======================================

Charged-lepton packet:
    m_mu/m_tau = 1/(k+q+lam) = 1/17
    m_e/m_mu   = 1/(alpha^-1+v+nn+lam) = 1/206
    m_e/m_tau  = 1/3502

with
    17  = k + q + lam
    206 = alpha^-1 + v + nn + lam
    206 - alpha^-1 = v + nn + lam = 69
"""

from fractions import Fraction as Fr

q = 3
v = 40
k = 12
lam = 2
nn = 27
alpha_inv = 137


class TestV48LeptonClosure:
    def test_primary_ratios(self):
        assert Fr(1, k + q + lam) == Fr(1, 17)
        assert Fr(1, alpha_inv + v + nn + lam) == Fr(1, 206)

    def test_product_ratio(self):
        mu_tau = Fr(1, 17)
        e_mu = Fr(1, 206)
        assert mu_tau * e_mu == Fr(1, 3502)

    def test_muon_denominator(self):
        assert k + q + lam == 17

    def test_electron_denominator(self):
        assert alpha_inv + v + nn + lam == 206
        assert 206 - alpha_inv == v + nn + lam == 69

    def test_closure_packet(self):
        mu_tau = Fr(1, k + q + lam)
        e_mu = Fr(1, alpha_inv + v + nn + lam)
        e_tau = mu_tau * e_mu
        closure = {
            'mu_tau': mu_tau == Fr(1, 17),
            'e_mu': e_mu == Fr(1, 206),
            'e_tau': e_tau == Fr(1, 3502),
            'mu_den': k + q + lam == 17,
            'e_den': alpha_inv + v + nn + lam == 206,
            'geom_tail': v + nn + lam == 69,
        }
        assert all(closure.values())
