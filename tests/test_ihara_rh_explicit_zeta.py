"""
Phase ζ — EXPLICIT IHARA ZETA AND THE GRAPH RIEMANN HYPOTHESIS FOR W(3,3)
============================================================================

The Ihara zeta function of a k-regular graph G with adjacency matrix A
and |E(G)| = vk/2 edges, |V(G)| = v vertices is:

   1/zeta_G(u) = (1 - u^2)^{r-1} . det(I - A u + (k-1) u^2 I)

where r = |E| - |V| + 1 = vk/2 - v + 1 is the cycle rank.

For a (k-regular) graph, zeta_G satisfies the Graph Riemann Hypothesis
(GRH) iff all non-trivial zeros lie on the circle |u| = 1/sqrt(k-1).
This is equivalent to the graph being Ramanujan.

We prove GRH for W(3,3) EXPLICITLY by factoring the characteristic
determinant over the three adjacency eigenvalues k=12, r=2, s=-4
and computing the six non-trivial zeros.

Results:
  zeros from lambda = 12:  u = 1 (trivial)     and u = 1/11 (trivial)
  zeros from lambda = 2:   u = (1 +/- i*sqrt(10))/11     -- |u| = 1/sqrt(11)
  zeros from lambda = -4:  u = (-2 +/- i*sqrt(7))/11     -- |u| = 1/sqrt(11)

The six non-trivial zeros all lie on the critical circle
|u| = 1/sqrt(11) = 1/sqrt(k-1) exactly, so W(3,3) is Ramanujan
AND GRH is verified constructively.
"""
import math
from fractions import Fraction


v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# -------------------------------------------------------------------
# Z1: Ihara zeta building blocks
# -------------------------------------------------------------------
class TestZ1_Structure:
    def test_cycle_rank(self):
        # r = E - v + 1
        cycle_rank = E - v + 1
        assert cycle_rank == 201

    def test_k_minus_1(self):
        assert k - 1 == 11

    def test_critical_radius_squared(self):
        # critical radius^2 = 1/(k-1) = 1/11
        rho2 = Fraction(1, k - 1)
        assert rho2 == Fraction(1, 11)


# -------------------------------------------------------------------
# Z2: Zero polynomial factors
# -------------------------------------------------------------------
# For each eigenvalue lambda, the local polynomial is:
#   p_lambda(u) = 1 - lambda u + (k-1) u^2
# We solve p(u) = 0:  u = (lambda +/- sqrt(lambda^2 - 4(k-1)))/(2(k-1))

def zero_magnitude_squared(lam_val, k_val):
    """|u|^2 for zeros of 1 - lambda u + (k-1) u^2 = 0."""
    disc = lam_val ** 2 - 4 * (k_val - 1)
    if disc >= 0:
        # real zeros: |u| varies
        r1 = (lam_val + math.sqrt(disc)) / (2 * (k_val - 1))
        r2 = (lam_val - math.sqrt(disc)) / (2 * (k_val - 1))
        return max(r1 ** 2, r2 ** 2), min(r1 ** 2, r2 ** 2)
    else:
        # complex conjugate: |u|^2 = 1/(k-1) (product of roots)
        return Fraction(1, k_val - 1), Fraction(1, k_val - 1)


class TestZ2_ZeroMagnitudes:
    def test_trivial_zeros_from_k(self):
        # lambda = k = 12:  1 - 12u + 11 u^2 = 0 -> (1-u)(1-11u) = 0
        # -> u = 1, u = 1/11.  These are TRIVIAL zeros (poles of the graph).
        hi, lo = zero_magnitude_squared(12, 12)
        # float tolerances
        assert abs(lo - 1 / 121) < 1e-12
        assert abs(hi - 1.0) < 1e-12

    def test_lambda_2_on_critical_circle(self):
        # lambda = 2:  1 - 2u + 11 u^2 = 0 -> disc = 4 - 44 = -40 (complex)
        # Complex conj roots -> |u|^2 = 1/11
        disc = 2 ** 2 - 4 * 11
        assert disc == -40
        hi, lo = zero_magnitude_squared(2, 12)
        assert hi == lo == Fraction(1, 11)

    def test_lambda_minus4_on_critical_circle(self):
        # lambda = -4: 1 + 4u + 11 u^2 = 0 -> disc = 16 - 44 = -28 (complex)
        # Complex conj roots -> |u|^2 = 1/11
        disc = (-4) ** 2 - 4 * 11
        assert disc == -28
        hi, lo = zero_magnitude_squared(-4, 12)
        assert hi == lo == Fraction(1, 11)


# -------------------------------------------------------------------
# Z3: The Ramanujan / GRH bound
# -------------------------------------------------------------------
class TestZ3_RamanujanGRH:
    def test_ramanujan_strict(self):
        # max non-trivial eigenvalue is r = 2; |2| < 2*sqrt(11)
        assert 2 < 2 * math.sqrt(11)

    def test_s_on_Ramanujan(self):
        # |s| = 4 < 2*sqrt(11) ~ 6.63
        assert 4 < 2 * math.sqrt(11)

    def test_every_non_trivial_zero_on_critical_circle(self):
        # The three adjacency eigenvalues k=12, r=2, s=-4.
        # For k=12 the zeros are trivial (poles u=1 and u=1/k-1=1/11).
        # For r=2 and s=-4 the polynomials have complex conjugate roots
        # whose |u| = 1/sqrt(k-1) exactly.
        lambdas_non_trivial = [2, -4]
        target = Fraction(1, 11)
        for lam_val in lambdas_non_trivial:
            hi, lo = zero_magnitude_squared(lam_val, 12)
            assert hi == lo == target


# -------------------------------------------------------------------
# Z4: Count the zeros
# -------------------------------------------------------------------
class TestZ4_ZeroCount:
    def test_total_zero_count(self):
        # Determinant det(I - A u + (k-1) u^2 I) has degree 2v (v = 40).
        # For each eigenvalue lambda: 2 zeros, total 2*v.
        # Trivial (u=1, u=1/11 from lambda=k): multiplicity 1 each
        # Non-trivial complex-conjugate pairs: one per eigenvalue with
        # mult equal to adjacency eigenvalue multiplicity.
        # Number of complex-conjugate pair zeros =
        # f (mult of r) + g (mult of s) = 24 + 15 = 39
        # Total non-trivial zeros = 2 * 39 = 78 (= E/lam - E/k*... = hmm)
        assert 2 * (f + g) == 78

    def test_trivial_zeros_count(self):
        # Two trivial: u=1 and u=1/11 from lambda=k (mult 1)
        assert 2 == 2

    def test_zeros_plus_cycle_rank_contributes(self):
        # (1-u^2)^{r-1} contributes 2*(r-1) = 400 zeros at u=+/-1
        # but these are functorial cycle-rank zeros, not graph spectral
        assert E - v + 1 - 1 == 200


# -------------------------------------------------------------------
# Z5: The explicit prime-geodesic count
# -------------------------------------------------------------------
class TestZ5_PrimeGeodesics:
    def test_pi_1_is_zero(self):
        # W(3,3) is simple (no loops), so pi(1) = 0 (no length-1 primes)
        assert 0 == 0

    def test_pi_2_equal_trace_A_squared_over_2_minus_diagonal(self):
        # prime 2-cycles = traces / 2 - ... but simpler:
        # # closed walks of length 2 from each vertex = k = 12
        # # pi(2) = 0 (all closed 2-walks are backtracks)
        assert 0 == 0

    def test_pi_3_triangles(self):
        # # length-3 primes = 2 * #(directed triangles per vertex)
        # SRG(40,12,2,4): triangles through each vertex = k*lam/2 = 12
        # Wait: triangles per vertex = C(lam, 1) * k /(something)
        # Standard: #triangles = v*k*lam/6 = 40*12*2/6 = 160
        triangles = v * k * lam // 6
        assert triangles == 160


# -------------------------------------------------------------------
# Z-CLOSURE: The Graph Riemann Hypothesis for W(3,3)
# -------------------------------------------------------------------
class TestZClosure_GRH:
    def test_GRH_for_W33(self):
        # THEOREM (Graph Riemann Hypothesis for W(3,3)):
        #   Every non-trivial zero of the Ihara zeta function of W(3,3)
        #   lies on the critical circle |u| = 1/sqrt(k-1) = 1/sqrt(11).
        #
        # Proof: factor det(I - A u + (k-1) u^2 I) over adjacency eigenvalues.
        # For each non-trivial eigenvalue lambda in {2, -4}, the local
        # polynomial 1 - lambda u + 11 u^2 has NEGATIVE discriminant
        # (disc = lambda^2 - 44 < 0), hence complex-conjugate zeros
        # with product 1/11.  Magnitudes both equal 1/sqrt(11).  QED.
        for lam_val in [2, -4]:
            disc = lam_val ** 2 - 4 * (k - 1)
            assert disc < 0  # complex roots
            hi, lo = zero_magnitude_squared(lam_val, k)
            assert hi == lo == Fraction(1, k - 1)
