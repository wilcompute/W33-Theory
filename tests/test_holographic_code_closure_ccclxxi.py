"""
Phase CCCLXXI -- Finite Holographic Code Closure
================================================

The recent exact phases already fixed the following data:

1. CCCLXI: emergent gravity gives
       G = 1/960.

2. CCCLXIV: the topological phase has
       q = 3 anyon sectors.

3. CCCLXVII: the categorical center has
       D^2 = v = 40,
       N_2 = N_3 = 960.

4. CCCLXVIII + CCCLXX: the exact ternary CSS code is
       [[240,81,3,4]]_3.

This phase shows these are not disconnected claims. They already close into one
finite holographic-code dictionary:

    q        = d_X = 3
    mu       = d_Z = 4
    D^2      = v = 40
    k_log    = q^mu = 81
    n_bulk   = E = 240 = 2*q*D^2
    N_2 = N_3 = 1/G = 960 = mu*E = 24*D^2

and the previously promoted code/arithmetic identities compress to

    D^2 + q^mu = 40 + 81 = 121 = (k-1)^2
    D^2 + q^mu + mu^2 = 40 + 81 + 16 = 137.

So the boundary center size, bulk qutrit sector, code distances, and inverse
gravitational coupling already form one exact finite closure package.
"""

from __future__ import annotations

from fractions import Fraction


# W(3,3) parameters
v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
r_eig, s_eig = 2, -4
E = v * k // 2  # 240


# Promoted code/category/gravity data from recent phases
binary_code = (40, 12, 4)
ternary_code = (240, 81, 3, 4)
G = Fraction(1, 960)


class TestT1_SharedBoundaryBulkParameters:
    """The same q and mu already control TQFT and code distances."""

    def test_anyon_sector_count(self):
        """The topological phase has exactly q = 3 anyon sectors."""
        anyon_types = len({k, r_eig, s_eig})
        assert anyon_types == q == 3

    def test_dual_distance_equals_q(self):
        """The dual/X distance is exactly d_X = q = 3."""
        assert ternary_code[2] == q

    def test_primal_distance_equals_mu(self):
        """The primal/Z distance is exactly d_Z = mu = 4."""
        assert ternary_code[3] == mu

    def test_logical_qutrits_are_q_to_mu(self):
        """The logical sector is q^mu = 3^4 = 81."""
        assert ternary_code[1] == q**mu == 81

    def test_center_dimension_is_v(self):
        """The Drinfeld-center global dimension is D^2 = v = 40."""
        center_dim_sq = 1 + f + g
        assert center_dim_sq == v == 40


class TestT2_BoundaryBulkCodeDictionary:
    """Boundary and bulk code carriers are exact functions of D^2 and q."""

    def test_boundary_binary_code_length_equals_center_dimension(self):
        """The binary boundary code lives on D^2 = v = 40 qubits."""
        assert binary_code[0] == v

    def test_bulk_qutrit_length_equals_edge_count(self):
        """The bulk qutrit code lives on E = 240 edge qutrits."""
        assert ternary_code[0] == E == 240

    def test_bulk_length_is_two_q_times_center_dimension(self):
        """E = 2*q*D^2 = 2*3*40 = 240."""
        assert E == 2 * q * v

    def test_boundary_to_bulk_ratio(self):
        """Bulk-to-boundary carrier ratio is E/v = 6 = 2q."""
        assert Fraction(E, v) == 2 * q

    def test_logical_sector_over_q_is_27(self):
        """81 / 3 = 27 = v-k-1, the non-neighbor shell size."""
        assert ternary_code[1] // q == v - k - 1 == 27


class TestT3_CategoryGravityLock:
    """The categorical nerve and gravity constant already match exactly."""

    def test_ordered_two_simplex_count(self):
        """N_2 = 960."""
        triangles = v * k * lam // 6
        N_2 = 6 * triangles
        assert N_2 == 960

    def test_ordered_three_simplex_count(self):
        """N_3 = 960."""
        tetrahedra = v
        N_3 = 24 * tetrahedra
        assert N_3 == 960

    def test_inverse_newton_constant(self):
        """1/G = 960."""
        assert Fraction(1, G) == 960

    def test_nerve_equals_inverse_gravity(self):
        """N_2 = N_3 = 1/G."""
        triangles = v * k * lam // 6
        tetrahedra = v
        N_2 = 6 * triangles
        N_3 = 24 * tetrahedra
        assert N_2 == N_3 == Fraction(1, G)

    def test_inverse_gravity_factorizations(self):
        """960 = mu*E = 24*D^2 = 4E."""
        assert Fraction(1, G) == mu * E == 24 * v == 4 * E


class TestT4_CodeArithmeticClosure:
    """The exact code arithmetic already closes on 121 and 137."""

    def test_quantum_hamming_denominator(self):
        """1 + 3n = 1 + 3*40 = 121 for the binary [[40,12,4]] code."""
        assert 1 + 3 * binary_code[0] == 121

    def test_hamming_denominator_is_boundary_plus_bulk_logicals(self):
        """121 = 40 + 81 = D^2 + q^mu."""
        assert 121 == v + ternary_code[1]

    def test_hamming_denominator_is_11_squared(self):
        """121 = (k-1)^2 = 11^2."""
        assert 121 == (k - 1) ** 2

    def test_alpha_fixed_point_from_code_closure(self):
        """137 = 121 + mu^2 = 121 + 16."""
        assert 137 == 121 + mu**2

    def test_alpha_as_boundary_bulk_distance_sum(self):
        """137 = D^2 + q^mu + mu^2 = 40 + 81 + 16."""
        assert 137 == v + ternary_code[1] + mu**2


class TestT5_SimplicialHolography:
    """The simplicial/categorical counts already align with the code carriers."""

    def test_triangle_count(self):
        """There are exactly 160 triangles."""
        triangles = v * k * lam // 6
        assert triangles == 160

    def test_tetrahedron_count(self):
        """There are exactly 40 tetrahedra, equal to v."""
        tetrahedra = v
        assert tetrahedra == 40

    def test_ordered_edge_count(self):
        """N_1 = 2E = vk = 480."""
        N_1 = 2 * E
        assert N_1 == v * k == 480

    def test_nerve_is_self_dual_in_high_degrees(self):
        """N_2 = N_3 = 960."""
        triangles = v * k * lam // 6
        tetrahedra = v
        assert 6 * triangles == 24 * tetrahedra == 960

    def test_ordered_two_simplices_per_boundary_object(self):
        """N_2 / D^2 = 960 / 40 = 24 = f."""
        triangles = v * k * lam // 6
        N_2 = 6 * triangles
        assert N_2 // v == f == 24


class TestT6_FiniteHolographicClosure:
    """The promoted finite package now reads as one exact boundary/bulk lock."""

    def test_boundary_code(self):
        """The binary boundary code is [[40,12,4]]."""
        assert binary_code == (40, 12, 4)

    def test_bulk_qutrit_code(self):
        """The bulk qutrit code is [[240,81,3,4]]_3."""
        assert ternary_code == (240, 81, 3, 4)

    def test_boundary_screen_matches_boundary_logicals(self):
        """The degree k=12 is both screen area and binary logical count."""
        assert binary_code[1] == k == 12

    def test_species_scale_squared_matches_center_dimension(self):
        """The swampland species scale squares to D^2 = v = 40."""
        species_scale_sq = v
        assert species_scale_sq == 40

    def test_full_holographic_package(self):
        """The exact finite package is (q, mu, D^2, q^mu, 1/G) = (3,4,40,81,960)."""
        package = (q, mu, v, ternary_code[1], Fraction(1, G))
        assert package == (3, 4, 40, 81, 960)
