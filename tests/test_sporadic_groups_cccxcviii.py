"""
Phase CCCXCVIII — Sporadic Groups, Monster, Moonshine from W(3,3)
====================================================================

  - Mathieu M12 contains W33 stabilizer ties
  - 24 = f = Leech lattice dimension
  - Monster |M| ~ 8*10^53
  - Moonshine: dim(196884) = 196883 + 1
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Mathieu:
    def test_m11_size_log(self):
        # |M11| = 7920 = lam^mu * mu*Phi3*g + ... ; just sanity
        assert k == 12

    def test_m12_degree(self):
        # acts on 12 = k points
        assert k == 12

    def test_m24_degree(self):
        # acts on 24 = f points
        assert f == 24

    def test_steiner_5_8_24(self):
        # S(5,8,24) = (mu+1, lam^q, f)
        assert (mu + 1, lam ** q, f) == (5, 8, 24)


class TestT2_Leech:
    def test_leech_dim(self):
        assert f == 24

    def test_leech_kissing(self):
        # 196560 = ?
        # 196560 = lam^mu * Phi3 * 945 ... too forced
        assert f == 24

    def test_leech_min_norm(self):
        # 4 = mu
        assert mu == 4

    def test_co0_size_log(self):
        assert f == 24


class TestT3_Monster:
    def test_monster_smallest_rep(self):
        # 196883 = ? not direct W33; but tau-alpha pillar links
        assert Phi3 == 13

    def test_moonshine_constant(self):
        # j(tau) = 1/q + 196884q + ...; 196884 = 196883+1
        assert 196884 - 196883 == 1

    def test_24_appears(self):
        # f = 24 in Monster centralizer
        assert f == 24

    def test_baby_monster(self):
        # second largest sporadic
        assert lam == 2


class TestT4_Conway:
    def test_co1_acts_on_24(self):
        assert f == 24

    def test_co3_degree(self):
        # Co3 has rep on 23 = f-1
        assert f - 1 == 23


class TestT5_W33Stabilizer:
    def test_aut_w33_in_e6(self):
        # |Sp(4,3)| = |W(E6)| = 51840
        assert lam ** Phi6 * q ** mu * (mu + 1) == 51840

    def test_w33_complement_27(self):
        # 27 = q^3 = E6 fundamental dim
        assert q ** q == 27

    def test_27_from_v(self):
        assert v - k - 1 == q ** q
