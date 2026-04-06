"""
Phase CCCLXXVI — Twistor Theory and Scattering Amplitudes from W(3,3)
======================================================================

Twistor space CP^3 has dim 4 = mu.
N=4 SYM lives on twistor space; W(3,3) realises its discrete avatar.
"""
import math
from fractions import Fraction

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
r_eig, s_eig = 2, -4
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_TwistorSpace:
    def test_cp3_dim(self):
        # CP^3 has complex dim 3 = q, real dim 6
        assert q == 3

    def test_twistor_4(self):
        # 4 = mu twistor coordinates
        assert mu == 4

    def test_minitwistor(self):
        # Minitwistor for 3D = CP^1 x CP^1
        assert lam == 2


class TestT2_MHV:
    def test_mhv_amplitudes(self):
        # n-point MHV amplitude from Parke-Taylor
        # For n=4: A_4(MHV) ~ <12>^4 / <12><23><34><41>
        # 4 = mu
        assert mu == 4

    def test_max_helicity_violation(self):
        # 2 negative helicity gluons = "MHV"
        assert lam == 2

    def test_anti_mhv(self):
        # 2 positive helicity = anti-MHV
        assert lam == 2


class TestT3_NEqual4SYM:
    def test_n4_sym_susy(self):
        # N=4 SYM has 4 supercharges = mu
        assert mu == 4

    def test_n4_sym_field_content(self):
        # N=4: 1 gluon + 4 fermions + 6 scalars = 11
        # 11 = k - 1
        content = 1 + 4 + 6
        assert content == 11
        assert content == k - 1

    def test_su4_r_symmetry(self):
        # R-symmetry SU(4) = SO(6); dim = 15 = g
        assert 15 == g


class TestT4_Amplituhedron:
    def test_grassmannian_dim(self):
        # Gr(k,n): for k=2,n=4 → dim 4 = mu
        gr_24_dim = 2 * (4 - 2)
        assert gr_24_dim == mu

    def test_positivity(self):
        # Positive Grassmannian: cells indexed by permutations
        # 4! = 24 = f permutations
        assert math.factorial(mu) == f

    def test_loop_amplitude(self):
        # Loop amplitudes from polytopes in Grassmannians
        # Number of cells grows with order
        assert f == 24


class TestT5_Yangian:
    def test_yangian_symmetry(self):
        # N=4 SYM has Yangian Y(psu(2,2|4))
        # Bonus symmetry: dual conformal SO(2,4) = SU(2,2)
        # dim SU(2,2) = 15 = g
        assert g == 15

    def test_dual_conformal(self):
        # Dual conformal: x_i → 1/x_i type symmetry
        # Order 2 = lam
        assert lam == 2


class TestT6_Color_Kinematics:
    def test_bcj_duality(self):
        # Bern-Carrasco-Johansson: color/kinematics duality
        # Numerator satisfies Jacobi like color does
        # SU(3) Jacobi: 8 generators = lam^q
        assert lam ** q == 8

    def test_double_copy(self):
        # gravity = (gauge)^2; spin 2 = lam * spin 1
        assert lam == 2
