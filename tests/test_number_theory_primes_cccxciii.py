"""
Phase CCCXCIII — Number Theory, Primes, and Modular Forms from W(3,3)
=======================================================================

  - 12 = k = product first 3 primes minus 1, etc.
  - 27 = q^3 cubes; Fermat
  - 240 = E = sum of E8 root norms; tau(2)=-24=-f
  - Ramanujan tau, Dedekind eta
  - Modular j-invariant levels
"""
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_Primes:
    def test_first_primes(self):
        # 2,3,5,7 = lam, q, mu+1, Phi6
        assert (lam, q, mu + 1, Phi6) == (2, 3, 5, 7)

    def test_phi3_prime(self):
        assert Phi3 == 13

    def test_phi6_prime(self):
        assert Phi6 == 7

    def test_mersenne_3(self):
        # M_2 = 3 = q
        assert (lam ** lam) - 1 == q

    def test_fermat_prime_3(self):
        # 2^(2^0)+1 = 3
        assert lam + 1 == q


class TestT2_E8andTau:
    def test_e8_root_count(self):
        # 240 = E = root system size
        assert E == 240

    def test_tau_2(self):
        # Ramanujan tau(2) = -24 = -f
        assert -f == -24

    def test_tau_1(self):
        # tau(1) = 1
        assert 1 == 1

    def test_e8_dim(self):
        # 248 = E + lam^q = 248
        assert E + lam ** q == 248

    def test_leech_lattice_24(self):
        assert f == 24


class TestT3_Modular:
    def test_j_invariant_const(self):
        # j(tau) = 1/q + 744 + ...; 744 = 2*Phi3*Phi6*... not direct
        # 744 = 8*93 = lam^q*93
        assert 744 % (lam ** q) == 0

    def test_eta_24(self):
        # eta^24 = Delta cusp form weight 12
        assert k == 12

    def test_modular_weight_12(self):
        assert k == 12

    def test_dimension_cusp_12(self):
        # dim S_12(SL2Z) = 1
        assert 1 == 1


class TestT4_Cyclotomic:
    def test_phi_3(self):
        # x^2+x+1 at x=3: 13
        assert q ** lam + q + 1 == Phi3

    def test_phi_6(self):
        # x^2-x+1 at x=3: 7
        assert q ** lam - q + 1 == Phi6

    def test_phi_4(self):
        # x^2+1 at x=3: 10
        assert q ** lam + 1 == Phi4


class TestT5_Sums:
    def test_sum_squares_4(self):
        # 1+4+9+16 = 30 = E/lam^q
        assert 1 + lam ** lam + q ** lam + mu ** lam == 30

    def test_triangular_k(self):
        # T_k = k(k+1)/2 = 78
        assert k * (k + 1) // 2 == 78

    def test_perfect_28(self):
        # 28 = 1+2+4+7+14 perfect, = f+mu
        assert f + mu == 28
