"""
Phase V46 — Exact mass-sector closure after the light-quark repair
==================================================================

Starting packet:
    m_c/m_t = 1/136
    m_u/m_c = 1/(v*g) = 1/600
    m_b/m_t = 1/(v+lam) = 1/42
    m_s/m_b = q/136 = 3/136
    m_d/m_s = 1/((q+lam)*mu) = 1/20

Exact closure identities:
    (m_s/m_b)/(m_c/m_t) = q
    (m_u/m_c)/(m_d/m_s) = 1/(v-Phi_4) = 1/30
    m_s/m_c = 1/(2*Phi_6) = 1/14
    m_u/m_d = Phi_6/g = 7/15
    (m_s/m_c)(m_u/m_d) = 1/(v-Phi_4) = 1/30
"""

from fractions import Fraction as Fr

v, k, lam, mu = 40, 12, 2, 4
q = 3
g = 15
Phi4, Phi6 = 10, 7
alpha_inv = 137


class TestV46MassSectorPacket:
    def test_primary_ratios(self):
        assert Fr(1, alpha_inv - 1) == Fr(1, 136)   # m_c/m_t
        assert Fr(1, v * g) == Fr(1, 600)           # m_u/m_c
        assert Fr(1, v + lam) == Fr(1, 42)          # m_b/m_t
        assert Fr(q, alpha_inv - 1) == Fr(3, 136)   # m_s/m_b
        assert Fr(1, (q + lam) * mu) == Fr(1, 20)   # m_d/m_s


class TestV46MassSectorClosure:
    def test_strange_charm_bridge(self):
        ms_mb = Fr(q, alpha_inv - 1)
        mc_mt = Fr(1, alpha_inv - 1)
        assert ms_mb / mc_mt == q

    def test_light_ud_bridge(self):
        mu_mc = Fr(1, v * g)
        md_ms = Fr(1, (q + lam) * mu)
        assert mu_mc / md_ms == Fr(1, v - Phi4)
        assert mu_mc / md_ms == Fr(1, 30)

    def test_ms_over_mc(self):
        ms_mb = Fr(q, alpha_inv - 1)
        mb_mt = Fr(1, v + lam)
        mc_mt = Fr(1, alpha_inv - 1)
        ms_mc = ms_mb * mb_mt / mc_mt
        assert ms_mc == Fr(1, 2 * Phi6)
        assert ms_mc == Fr(1, 14)

    def test_mu_over_md(self):
        mu_mc = Fr(1, v * g)
        mc_mt = Fr(1, alpha_inv - 1)
        md_ms = Fr(1, (q + lam) * mu)
        ms_mb = Fr(q, alpha_inv - 1)
        mb_mt = Fr(1, v + lam)

        mu_md = (mu_mc * mc_mt) / (md_ms * ms_mb * mb_mt)
        assert mu_md == Fr(Phi6, g)
        assert mu_md == Fr(7, 15)

    def test_product_closure(self):
        ms_mc = Fr(1, 14)
        mu_md = Fr(7, 15)
        assert ms_mc * mu_md == Fr(1, v - Phi4)
        assert ms_mc * mu_md == Fr(1, 30)
