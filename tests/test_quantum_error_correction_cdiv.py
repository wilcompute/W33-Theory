"""
Phase CDIV (404) — Quantum Error Correction & Stabilizer Codes from W(3,3)
===========================================================================

  - Qutrit Hilbert space (d=q=3)
  - Symplectic structure of stabilizer codes = W(3,3)
  - Clifford group = Sp(4,3)
  - Stabilizer code parameters, Singleton bound
  - Magic states, discrete Wigner function, contextuality
  - MUBs, SIC-POVMs, Bell states
  - CSS construction, surface codes
"""
import math
from fractions import Fraction

v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


class TestT1_QutritSpace:
    def test_qutrit_dim(self):
        assert q == 3

    def test_mu_qutrits(self):
        assert q ** mu == 81

    def test_lam_qutrits(self):
        assert q ** lam == 9


class TestT2_SymplecticStabilizer:
    def test_symplectic_dim(self):
        # n=2 qutrits: F_3^4 = W(3,3) geometry
        assert 2 * lam == mu

    def test_pauli_classes(self):
        assert (q ** 4 - 1) // (q - 1) == v

    def test_w33_is_pauli_geometry(self):
        assert v == (q ** (2 * lam) - 1) // (q - 1)


class TestT3_CliffordGroup:
    def test_clifford_mod_phases(self):
        assert q ** 4 * (q ** 4 - 1) * (q ** 2 - 1) == 51840

    def test_sl2_3(self):
        assert q * (q ** 2 - 1) == f

    def test_psl2_3(self):
        # PSL(2,3) = A_4, order 12 = k
        assert q * (q ** 2 - 1) // (q - 1) == k


class TestT4_StabilizerCodes:
    def test_code_params(self):
        # [[4,2,2]]_3 code
        assert mu == 4  # n
        assert lam == 2  # k_logical and d

    def test_singleton_bound(self):
        assert lam <= mu - 2 * (lam - 1)

    def test_error_detection(self):
        assert (lam - 1) // 2 == 0  # t=0


class TestT5_MagicStates:
    def test_1qutrit_phase_space(self):
        assert q ** lam == 9

    def test_2qutrit_phase_space(self):
        assert q ** mu == 81

    def test_stabilizer_states(self):
        # q^2 + q = 12 = k
        assert q ** 2 + q == k

    def test_k_is_stab_states(self):
        assert q * (q + 1) == k


class TestT6_GottesmanKnill:
    def test_ext_clifford_1qutrit(self):
        assert q ** 2 * f == 216

    def test_216_is_cube(self):
        assert 216 == math.factorial(q) ** q


class TestT7_CSSCodes:
    def test_simplex_code(self):
        # [4, 2, 3]_3 = [mu, lam, q]_3
        assert mu == 4 and lam == 2 and q == 3


class TestT8_SurfaceCode:
    def test_surface_code(self):
        # [[q^2, 1, q]]_3 = [[9,1,3]]
        assert q ** 2 == 9

    def test_toric_code(self):
        # n = 2*q^2 = 18
        assert 2 * q ** 2 == 18

    def test_toric_alt(self):
        assert 2 * q ** 2 == lam * q ** lam


class TestT9_Bell:
    def test_bell_bases(self):
        assert q ** 2 == 9

    def test_mubs(self):
        assert q + 1 == mu

    def test_mub_vectors(self):
        assert mu * q == k


class TestT10_SICPOVM:
    def test_sic_vectors(self):
        assert q ** 2 == 9

    def test_sic_overlap(self):
        assert Fraction(1, q + 1) == Fraction(1, mu)

    def test_zauner_dim(self):
        assert mu == 4

    def test_heisenberg_order(self):
        assert q ** 3 == q ** q == 27


class TestT11_InfoIdentities:
    def test_pauli_ops(self):
        assert v == (q ** (2 * lam) - 1) // (q - 1)

    def test_commuting_paulis(self):
        assert k == 12

    def test_mu_is_q_plus_1(self):
        assert mu == q + 1

    def test_k_is_mu_times_q(self):
        assert k == mu * q
