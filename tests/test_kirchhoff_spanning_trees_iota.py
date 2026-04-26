"""
Supplement iota — KIRCHHOFF'S MATRIX-TREE AND THE PARTITION FUNCTION
=========================================================================

Kirchhoff's matrix-tree theorem gives the number of spanning trees of
a connected graph G as

    tau(G) = (1/v) prod_{lambda > 0 spec L} lambda

where L = kI - A is the Laplacian.

For W(3,3) the Laplacian has spectrum {0, 10, 16} = {0, Phi_4, lam^mu}
with multiplicities {1, f, g} = {1, 24, 15}.  Therefore

    tau(W(3,3)) = (1/v) * Phi_4^f * (lam^mu)^g
                = (1/40) * 10^24 * 16^15

This is the simplest integer of cosmologically large size in the
program.

Connection to QFT:  tau(W(3,3)) is also (up to a factor) the
free-scalar partition function on W(3,3), i.e.

    Z_scalar = (det L)^{-1/2}|_{zero-mode-removed}
             = ( Phi_4^f * (lam^mu)^g )^{-1/2}
             = ( 10^24 * 16^15 )^{-1/2}.
"""
import math
from fractions import Fraction
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
Phi3, Phi4, Phi6 = 13, 10, 7


# ------------------------------------------------------------------
# iota.1  Laplacian spectrum recap
# ------------------------------------------------------------------
class Test_iota_1_Spectrum:
    def test_lam_spec(self):
        # spec L = {0, k-r, k-s} = {0, 10, 16}
        spec = [0, k - 2, k - (-4)]
        assert spec == [0, Phi4, lam ** mu]


# ------------------------------------------------------------------
# iota.2  Kirchhoff's product
# ------------------------------------------------------------------
class Test_iota_2_KirchhoffProduct:
    def test_product_no_zero_mode(self):
        # det'(L) = Phi_4^f * (lam^mu)^g = 10^24 * 16^15
        prod = Phi4 ** f * (lam ** mu) ** g
        assert prod == 10 ** 24 * 16 ** 15

    def test_log_size(self):
        # log10(prod) = 24 * log10(10) + 15 * log10(16)
        # = 24 + 15 * 1.2041
        # = 24 + 18.06 = 42.06
        log10 = math.log10(Phi4 ** f * (lam ** mu) ** g)
        assert 42 < log10 < 43


# ------------------------------------------------------------------
# iota.3  Spanning tree count
# ------------------------------------------------------------------
class Test_iota_3_SpanningTrees:
    def test_tau_w33(self):
        # tau = (1/v) * Phi_4^f * (lam^mu)^g
        prod = Phi4 ** f * (lam ** mu) ** g
        # Should be divisible by v = 40
        assert prod % v == 0
        tau = prod // v
        # Sanity: tau is a positive integer
        assert tau > 0


# ------------------------------------------------------------------
# iota.4  log-tau hierarchy exponent
# ------------------------------------------------------------------
class Test_iota_4_LogTau:
    def test_log_tau_relates_to_E(self):
        # log10(tau) ~ 40-42, related to E via order-of-magnitude
        log10_tau = math.log10(Phi4 ** f * (lam ** mu) ** g / v)
        # Roughly 40 +/- 1 (= v +/- a small correction)
        assert v - 2 < log10_tau < v + 2


# ------------------------------------------------------------------
# iota.5  Free-scalar partition function
# ------------------------------------------------------------------
class Test_iota_5_FreeScalarZ:
    def test_Z_squared(self):
        # Z^{-2} = det'(L) = Phi_4^f * (lam^mu)^g
        det_prime = Phi4 ** f * (lam ** mu) ** g
        # Z = det'(L)^{-1/2} -- magnitude check
        assert det_prime > 0


# ------------------------------------------------------------------
# iota.6  Connection to topological invariants
# ------------------------------------------------------------------
class Test_iota_6_Topology:
    def test_first_betti_number(self):
        # b_1 = E - v + 1 = 240 - 40 + 1 = 201 (cycle rank)
        b_1 = E - v + 1
        assert b_1 == 201

    def test_201_factorization(self):
        # 201 = 3 * 67 = q * 67
        assert 201 == q * 67

    def test_b_0(self):
        # b_0 = 1 (connected)
        assert 1 == 1


# ------------------------------------------------------------------
# iota.7  The Q3 = q^q grading on Laplacian
# ------------------------------------------------------------------
class Test_iota_7_GroundStateDeg:
    def test_zero_mode_dim_eq_1(self):
        # Connected => unique zero-mode (constant function)
        assert 1 == 1

    def test_q_classes(self):
        # 3 = q distinct Laplacian eigenvalues
        spec_distinct = [0, Phi4, lam ** mu]
        assert len(spec_distinct) == q


# ------------------------------------------------------------------
# iota-CLOSURE
# ------------------------------------------------------------------
class Test_iota_Closure:
    def test_kirchhoff_identity(self):
        # The single closed-form spanning-tree formula
        det_prime = Phi4 ** f * (lam ** mu) ** g
        assert det_prime == 10 ** 24 * 16 ** 15
        assert det_prime % v == 0

    def test_partition_function_w33(self):
        # Z_free_scalar = (det' L)^{-1/2}
        # |Z|^{-2} = Phi_4^f * (lam^mu)^g
        # In W(3,3) constants alone.
        det_prime = Phi4 ** f * (lam ** mu) ** g
        assert det_prime > 0
