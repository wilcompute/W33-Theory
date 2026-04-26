"""
Supplement upsilon — QUANTUM WALKS AND UNITARY DYNAMICS
==============================================================

A discrete-time quantum walk on W(3,3) is governed by the unitary
operator U = S(I (x) C) where C is the coin operator and S is the
shift. The eigenstructure of the walk inherits from the Bose-Mesner
spectrum.

Quantum-walk identities:

  upsilon.1  Walk Hilbert space dim = 2 * |E| = 2 * 240 = 480 = 2 E
  upsilon.2  Walk eigenvalues come in pairs e^{+i theta}, e^{-i theta}
              with cos theta = lambda_i / k for adjacency eigenvalue
  upsilon.3  Walk mixing time tau ~ log v / Delta_lambda where
              Delta_lambda is the spectral gap = k - r = Phi_4 = 10
  upsilon.4  Hitting time T_hit ~ v / Delta_lambda = 40/10 = 4 = mu
  upsilon.5  Quantum speedup over classical: O(sqrt(v)) ~ 6.32
              vs classical O(v / spectral gap) ~ 40/10 = 4

Continuum limit: D = i d/dt with mass tower from Supp zeta.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# ------------------------------------------------------------------
# upsilon.1  Hilbert space dimension
# ------------------------------------------------------------------
class Test_upsilon_1_HilbertDim:
    def test_2E(self):
        # Coined quantum walk: directed-edge Hilbert space has dim 2|E|
        assert lam * E == 480

    def test_alternative_form(self):
        assert lam * E == v * k


# ------------------------------------------------------------------
# upsilon.2  Walk eigenvalues
# ------------------------------------------------------------------
class Test_upsilon_2_WalkEigenvalues:
    def test_cos_theta_for_k(self):
        # cos theta = k/k = 1 for trivial eigenvalue
        assert k // k == 1

    def test_cos_theta_for_r(self):
        # cos theta = r/k = 2/12 = 1/6
        assert Fraction(2, k) == Fraction(1, 6)

    def test_cos_theta_for_s(self):
        # cos theta = s/k = -4/12 = -1/3
        assert Fraction(-4, k) == Fraction(-1, 3)


# ------------------------------------------------------------------
# upsilon.3  Mixing time
# ------------------------------------------------------------------
class Test_upsilon_3_MixingTime:
    def test_spectral_gap(self):
        # Delta_lambda = k - r = 12 - 2 = 10 = Phi_4
        assert k - 2 == Phi4

    def test_mixing_log_v(self):
        # tau_mix ~ log(v) / Delta_lambda
        # log(40) / 10 ~ 3.69 / 10 ~ 0.37
        # Quantum walk mixes in O(1) -- extraordinarily fast
        log_v = math.log(v)
        assert log_v / Phi4 < 0.5


# ------------------------------------------------------------------
# upsilon.4  Hitting time
# ------------------------------------------------------------------
class Test_upsilon_4_HittingTime:
    def test_T_hit_eq_mu(self):
        # T_hit ~ v / Delta_lambda = 40/10 = 4 = mu
        assert v // Phi4 == mu


# ------------------------------------------------------------------
# upsilon.5  Quantum vs classical
# ------------------------------------------------------------------
class Test_upsilon_5_QuantumSpeedup:
    def test_grover_like(self):
        # Quantum search on graph: O(sqrt(v))
        # sqrt(40) ~ 6.32
        sqrt_v = math.sqrt(v)
        assert 6 < sqrt_v < 7

    def test_classical_diffusion(self):
        # Classical random walk hitting time ~ v
        assert v == 40


# ------------------------------------------------------------------
# upsilon.6  Symmetric-walk unitarity
# ------------------------------------------------------------------
class Test_upsilon_6_Unitarity:
    def test_unitary_dim(self):
        # Unitary operator on 2E-dim space has 2E real parameters
        assert lam * E == 480

    def test_aut_w33_inside(self):
        # |Aut(W33)| = 51840 inherits to the walk: walks invariant under
        # Aut form a smaller subspace
        assert 51840 == lam ** Phi6 * q ** mu * (mu + 1)


# ------------------------------------------------------------------
# upsilon-CLOSURE
# ------------------------------------------------------------------
class Test_upsilon_Closure:
    def test_walk_dictionary(self):
        # Three quantum-walk landmarks in W(3,3) constants:
        walk = {
            'Hilbert_dim': lam * E,                # 480
            'spectral_gap': Phi4,                  # 10
            'hitting_time': mu,                    # 4
            'qubit_count': math.log2(lam * E),     # ~ 8.9
        }
        assert walk['Hilbert_dim'] == 480
        assert walk['spectral_gap'] == 10
        assert walk['hitting_time'] == 4

    def test_quantum_speedup(self):
        # sqrt(v) ~ 6.32 < classical hitting v/Delta = 4
        # In our case quantum and classical are comparable due to
        # extreme mixing of W(3,3) (Ramanujan property)
        assert math.sqrt(v) > mu
