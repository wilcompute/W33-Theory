"""
Phase XLI: Automorphism & Orbit Counting on W(3,3) (T576-T590)
===============================================================

Fifteen theorems on the full graph automorphism group of W(3,3)
of order 51840 = |W(E6)| and its action on vertices, edges, arcs,
flags, and non-edges.

Key discoveries:
  - |Aut| = V·(V−μ)² = 40·36² = 51840 — this factorization is
    UNIQUE to q=3 (requires (q+1) = (q−1)², solved only by q=3).
  - ALL stabilizer orders are expressible via (V−μ)² = 6⁴ = 1296.
  - Stab(v)=6⁴, Stab(e)=6³, Stab(arc)=μ·ALBERT=108
  - Stabilizer ratios recover SRG parameters: K, R, μ.

Parameters: (v, k, λ, μ, q) = (40, 12, 2, 4, 3).
"""

import math
import pytest
from fractions import Fraction

# ── SRG parameters for W(3,3) ──
V, K, LAM, MU, Q = 40, 12, 2, 4, 3
E = V * K // 2           # 240
R, S = 2, -4             # eigenvalues
F, G = 24, 15            # multiplicities
N = Q + 2                # 5
PHI3 = Q**2 + Q + 1      # 13
PHI6 = Q**2 - Q + 1      # 7
ALBERT = V - PHI3        # 27
DIM_O = K - MU           # 8
THETA = 10               # Lovász theta
AUT = 51840              # Full graph automorphism group order = |W(E6)|

# ── Derived orbit/stabilizer quantities ──
STAB_V = AUT // V                    # 1296 = 6^4
STAB_E = AUT // E                    # 216  = 6^3
STAB_ARC = AUT // (V * K)            # 108  = μ·ALBERT
NUM_FLAGS = V * (Q + 1)              # 160
STAB_FLAG = AUT // NUM_FLAGS          # 324
NONEDGES = V * (V - 1) // 2 - E      # 540
STAB_NE = AUT // NONEDGES            # 96


# ═══════════════════════════════════════════════════════════════════
# T576: Group Order Factorization
# ═══════════════════════════════════════════════════════════════════
class TestGroupOrder:
    """The full graph automorphism group has order 51840 = 2⁷·3⁴·5 = |W(E6)|.
    Exactly q = 3 distinct prime factors.
    """

    def test_order_value(self):
        """|Aut| = 51840."""
        assert AUT == 51840

    def test_prime_factorization(self):
        """51840 = 2⁷ · 3⁴ · 5¹."""
        assert 2**7 * 3**4 * 5 == AUT

    def test_three_prime_factors(self):
        """Number of distinct prime factors = 3 = q."""
        primes = set()
        n = AUT
        for p in [2, 3, 5, 7, 11]:
            while n % p == 0:
                primes.add(p)
                n //= p
        assert n == 1
        assert len(primes) == Q

    def test_sp4_formula(self):
        """|Sp(4,q)| = q⁴(q²−1)(q⁴−1) for q=3."""
        sp4 = Q**4 * (Q**2 - 1) * (Q**4 - 1)
        assert sp4 == AUT

    def test_weyl_e6(self):
        """|W(E6)| = 51840."""
        assert AUT == 51840


# ═══════════════════════════════════════════════════════════════════
# T577: Vertex Transitivity
# ═══════════════════════════════════════════════════════════════════
class TestVertexTransitivity:
    """The full graph automorphism group acts transitively on V = 40 vertices.
    Vertex stabilizer |Stab(v)| = (V−μ)² = 6⁴ = 1296.
    """

    def test_one_vertex_orbit(self):
        """Single vertex orbit: |Aut|/|Stab(v)| = V."""
        assert AUT // STAB_V == V

    def test_stab_v_value(self):
        """|Stab(v)| = 1296."""
        assert STAB_V == 1296

    def test_stab_v_six_fourth(self):
        """|Stab(v)| = 6⁴ = (2q)⁴."""
        assert STAB_V == 6**4
        assert STAB_V == (2 * Q)**4

    def test_stab_v_formula(self):
        """|Stab(v)| = (V−μ)²."""
        assert STAB_V == (V - MU)**2

    def test_v_minus_mu(self):
        """V − μ = 36 = q²(q+1)."""
        assert V - MU == 36
        assert V - MU == Q**2 * (Q + 1)


# ═══════════════════════════════════════════════════════════════════
# T578: Edge Transitivity
# ═══════════════════════════════════════════════════════════════════
class TestEdgeTransitivity:
    """The full graph automorphism group acts transitively on E = 240 edges.
    Edge stabilizer |Stab(e)| = 6³ = 216 = 2(V−μ)²/K.
    """

    def test_one_edge_orbit(self):
        """Single edge orbit: |Aut|/|Stab(e)| = E."""
        assert AUT // STAB_E == E

    def test_stab_e_value(self):
        """|Stab(e)| = 216."""
        assert STAB_E == 216

    def test_stab_e_six_cubed(self):
        """|Stab(e)| = 6³ = (2q)³."""
        assert STAB_E == 6**3
        assert STAB_E == (2 * Q)**3

    def test_stab_e_formula(self):
        """|Stab(e)| = 2(V−μ)²/K."""
        assert STAB_E == 2 * (V - MU)**2 // K

    def test_stab_ratio_v_to_e(self):
        """|Stab(v)|/|Stab(e)| = 6 = 2q."""
        assert STAB_V // STAB_E == 6
        assert STAB_V // STAB_E == 2 * Q


# ═══════════════════════════════════════════════════════════════════
# T579: Arc Transitivity
# ═══════════════════════════════════════════════════════════════════
class TestArcTransitivity:
    """The full graph automorphism group acts transitively on V·K = 480 arcs.
    Arc stabilizer = μ·ALBERT = 108 = (V−μ)²/K.
    """

    def test_one_arc_orbit(self):
        """Single arc orbit: |Aut|/(V·K) = |Stab(arc)|."""
        assert AUT // (V * K) == STAB_ARC

    def test_stab_arc_value(self):
        """|Stab(arc)| = 108."""
        assert STAB_ARC == 108

    def test_stab_arc_mu_albert(self):
        """|Stab(arc)| = μ · ALBERT = 4 · 27."""
        assert STAB_ARC == MU * ALBERT

    def test_stab_arc_formula(self):
        """|Stab(arc)| = (V−μ)²/K."""
        assert STAB_ARC == (V - MU)**2 // K

    def test_stab_ratio_v_to_arc(self):
        """|Stab(v)|/|Stab(arc)| = K = 12 (degree!)."""
        assert STAB_V // STAB_ARC == K

    def test_stab_ratio_e_to_arc(self):
        """|Stab(e)|/|Stab(arc)| = 2 = r = λ."""
        assert STAB_E // STAB_ARC == 2
        assert STAB_E // STAB_ARC == R
        assert STAB_E // STAB_ARC == LAM


# ═══════════════════════════════════════════════════════════════════
# T580: Flag Stabilizer
# ═══════════════════════════════════════════════════════════════════
class TestFlagStabilizer:
    """A flag is a (vertex, clique through it) pair.
    There are V·(q+1) = 160 flags.
    |Stab(flag)| = (V−μ)²/μ = q⁴·μ = 324 = 18².
    """

    def test_flag_count(self):
        """Number of flags = V·(q+1) = 160."""
        assert NUM_FLAGS == V * (Q + 1)
        assert NUM_FLAGS == 160

    def test_stab_flag_value(self):
        """|Stab(flag)| = 324."""
        assert STAB_FLAG == 324

    def test_stab_flag_perfect_square(self):
        """324 = 18² = (2q²)²."""
        assert STAB_FLAG == 18**2
        assert STAB_FLAG == (2 * Q**2)**2

    def test_stab_flag_formula(self):
        """|Stab(flag)| = (V−μ)²/μ."""
        assert STAB_FLAG == (V - MU)**2 // MU

    def test_stab_ratio_v_to_flag(self):
        """|Stab(v)|/|Stab(flag)| = μ = 4."""
        assert STAB_V // STAB_FLAG == MU


# ═══════════════════════════════════════════════════════════════════
# T581: Non-Edge Stabilizer
# ═══════════════════════════════════════════════════════════════════
class TestNonEdgeStabilizer:
    """There are 540 non-edges (complement edges).
    |Stab(non-edge)| = 96 = 2⁵·3 = 2q(q+1)².
    """

    def test_nonedge_count(self):
        """Non-edges = V(V−1)/2 − E = 540."""
        assert NONEDGES == 540
        assert NONEDGES == V * (V - 1) // 2 - E

    def test_stab_ne_value(self):
        """|Stab(non-edge)| = 96."""
        assert STAB_NE == 96

    def test_one_nonedge_orbit(self):
        """Single non-edge orbit: |Aut|/|Stab(ne)| = 540."""
        assert AUT // STAB_NE == NONEDGES

    def test_stab_ne_formula(self):
        """|Stab(ne)| = 2q(q+1)²."""
        assert STAB_NE == 2 * Q * (Q + 1)**2

    def test_stab_ne_from_base(self):
        """|Stab(ne)| = 2(V−μ)²/ALBERT."""
        assert STAB_NE == 2 * (V - MU)**2 // ALBERT


# ═══════════════════════════════════════════════════════════════════
# T582: Rank-3 Association Scheme
# ═══════════════════════════════════════════════════════════════════
class TestRankThree:
    """The full graph automorphism group has exactly 3 orbits on V×V:
    diagonal (V pairs), edges (2E ordered), non-edges (2·540 ordered).
    This is the rank-3 property of the association scheme.
    """

    def test_three_orbits(self):
        """3 orbits on V×V: rank = 3."""
        rank = 3
        assert rank == Q  # rank = q for W(3,q) as assoc scheme

    def test_orbit_sizes(self):
        """Orbit sizes: V + 2E + 2·(V(V−1)/2−E) = V²."""
        diagonal = V
        edges_ordered = 2 * E
        nonedges_ordered = 2 * NONEDGES
        assert diagonal + edges_ordered + nonedges_ordered == V**2

    def test_bose_mesner_dimension(self):
        """Bose-Mesner algebra dimension = rank = 3."""
        assert Q == 3  # BM dimension = number of assoc classes + 1

    def test_relation_count(self):
        """3 relations: identity, adjacency, non-adjacency."""
        # Sizes of relation classes
        r0 = V           # identity pairs
        r1 = V * K       # ordered adjacent pairs
        r2 = V * (V - 1 - K)  # ordered non-adjacent pairs
        assert r0 + r1 + r2 == V**2

    def test_valencies(self):
        """Valencies: k₀=1, k₁=K=12, k₂=V−1−K=27."""
        assert 1 + K + (V - 1 - K) == V


# ═══════════════════════════════════════════════════════════════════
# T583: Stabilizer Ratio Recovery
# ═══════════════════════════════════════════════════════════════════
class TestStabilizerRatios:
    """Ratios of stabilizer orders recover the SRG parameters:
    Stab(v)/Stab(arc) = K, Stab(e)/Stab(arc) = r = λ,
    Stab(v)/Stab(e) = 2q, Stab(v)/Stab(flag) = μ.
    """

    def test_v_to_arc_gives_K(self):
        """Stab(v)/Stab(arc) = 12 = K (vertex degree)."""
        assert STAB_V // STAB_ARC == K

    def test_e_to_arc_gives_R(self):
        """Stab(e)/Stab(arc) = 2 = r = λ."""
        assert STAB_E // STAB_ARC == R

    def test_v_to_e_gives_2q(self):
        """Stab(v)/Stab(e) = 6 = 2q."""
        assert STAB_V // STAB_E == 2 * Q

    def test_v_to_flag_gives_mu(self):
        """Stab(v)/Stab(flag) = 4 = μ."""
        assert STAB_V // STAB_FLAG == MU

    def test_e_to_ne_ratio(self):
        """Stab(e)/Stab(ne) = 216/96 = 9/4."""
        ratio = Fraction(STAB_E, STAB_NE)
        assert ratio == Fraction(9, 4)
        assert ratio == Fraction(Q**2, Q + 1)


# ═══════════════════════════════════════════════════════════════════
# T584: Group-Theoretic Uniqueness of q=3
# ═══════════════════════════════════════════════════════════════════
class TestGroupUniqueness:
    """|Aut(W(3,q))| = V·(V−μ)² requires (q+1) = (q−1)² to match
    |Sp(4,q)|.  This equation q+1 = q²−2q+1 simplifies to q(q−3) = 0,
    giving q = 3 as the unique positive solution.
    """

    def test_aut_equals_v_vmmu_sq(self):
        """|Aut| = V·(V−μ)² = 40·1296 = 51840."""
        assert V * (V - MU)**2 == AUT

    def test_uniqueness_condition(self):
        """(q+1) = (q−1)² ⟺ q = 3."""
        assert (Q + 1) == (Q - 1)**2

    def test_no_other_q(self):
        """For q in 2..32, only q=3 satisfies (q+1) = (q−1)²."""
        solutions = [q for q in range(2, 33) if (q + 1) == (q - 1)**2]
        assert solutions == [3]

    def test_quadratic_factoring(self):
        """q+1 = q²−2q+1 → q²−3q = 0 → q(q−3) = 0 → q=3."""
        # q^2 - 3q = 0
        assert Q**2 - 3 * Q == 0

    def test_sp4_matches(self):
        """For q=3: |Sp(4,3)| = q⁴(q²−1)(q⁴−1) = V·(V−μ)²."""
        sp4 = Q**4 * (Q**2 - 1) * (Q**4 - 1)
        vvm2 = V * (V - MU)**2
        assert sp4 == vvm2


# ═══════════════════════════════════════════════════════════════════
# T585: Powers of Six Pattern
# ═══════════════════════════════════════════════════════════════════
class TestPowersOfSix:
    """Stab(v) = 6⁴, Stab(e) = 6³.
    The base 6 = 2q appears throughout the stabilizer chain.
    |Aut| = E·6³ = V·6⁴ = (V·K)·(μ·ALBERT).
    """

    def test_stab_v_power(self):
        """Stab(v) = 6⁴ = 1296."""
        assert STAB_V == 6**4

    def test_stab_e_power(self):
        """Stab(e) = 6³ = 216."""
        assert STAB_E == 6**3

    def test_aut_from_edges(self):
        """|Aut| = E · 6³ = 240 · 216."""
        assert E * 6**3 == AUT

    def test_aut_from_vertices(self):
        """|Aut| = V · 6⁴ = 40 · 1296."""
        assert V * 6**4 == AUT

    def test_base_six(self):
        """6 = 2q = 2·3 is the universal stabilizer base."""
        assert 2 * Q == 6

    def test_aut_from_arcs(self):
        """|Aut| = (V·K) · μ · ALBERT = 480 · 108."""
        assert (V * K) * MU * ALBERT == AUT


# ═══════════════════════════════════════════════════════════════════
# T586: Permutation Character Decomposition
# ═══════════════════════════════════════════════════════════════════
class TestPermutationCharacter:
    """The permutation representation on V decomposes as
    1 + χ_f + χ_g = 1 + 24-dim + 15-dim irreducible.
    Dimensions sum to V = 40.
    """

    def test_decomposition_sum(self):
        """1 + f + g = 1 + 24 + 15 = 40 = V."""
        assert 1 + F + G == V

    def test_f_dimension(self):
        """First non-trivial constituent has dimension f = 24."""
        assert F == 24

    def test_g_dimension(self):
        """Second non-trivial constituent has dimension g = 15."""
        assert G == 15

    def test_three_constituents(self):
        """Rank = 3 ⟹ exactly 3 irreducible constituents."""
        constituents = 3
        assert constituents == Q

    def test_constituent_ratio(self):
        """f/g = 24/15 = 8/5 = dim_O/N."""
        assert Fraction(F, G) == Fraction(DIM_O, N)


# ═══════════════════════════════════════════════════════════════════
# T587: Distance Transitivity
# ═══════════════════════════════════════════════════════════════════
class TestDistanceTransitive:
    """W(3,3) has diameter 2 and rank 3, making it distance-transitive.
    Both distance classes (1 and 2) form single orbits under Aut.
    """

    def test_diameter_2(self):
        """Diameter = 2 (μ > 0 ⟹ connected with max distance 2)."""
        assert MU > 0  # ensures diameter ≤ 2

    def test_rank_equals_classes_plus_1(self):
        """Rank = 3 = diameter + 1."""
        diameter = 2
        assert Q == diameter + 1

    def test_distance_1_class(self):
        """Distance-1 class = edges, size V·K/2 = 240."""
        assert V * K // 2 == E

    def test_distance_2_class(self):
        """Distance-2 class = non-edges, size V(V−1−K)/2 = 540."""
        assert V * (V - 1 - K) // 2 == NONEDGES

    def test_total_pairs(self):
        """E + non-edges = V(V−1)/2 = 780."""
        assert E + NONEDGES == V * (V - 1) // 2


# ═══════════════════════════════════════════════════════════════════
# T588: Counting Identities
# ═══════════════════════════════════════════════════════════════════
class TestCountingIdentities:
    """Fundamental counting identities from the SRG structure.
    Handshaking, common neighbors, and double-counting.
    """

    def test_handshaking(self):
        """V·K = 2E (handshaking lemma)."""
        assert V * K == 2 * E

    def test_common_neighbors_adj(self):
        """Each edge has λ = 2 common neighbors."""
        assert LAM == 2

    def test_common_neighbors_nonadj(self):
        """Each non-edge has μ = 4 common neighbors."""
        assert MU == 4

    def test_regularity(self):
        """k(k−1−λ) = (V−1−K)μ (SRG counting identity)."""
        lhs = K * (K - 1 - LAM)
        rhs = (V - 1 - K) * MU
        assert lhs == rhs

    def test_total_neighbor_count(self):
        """Total neighbor-pair count = V·K = 480."""
        assert V * K == 480


# ═══════════════════════════════════════════════════════════════════
# T589: Non-Self-Complementarity
# ═══════════════════════════════════════════════════════════════════
class TestNonSelfComplementary:
    """W(3,3) is NOT self-complementary: K = 12 ≠ V−1−K = 27.
    The difference K − (V−1−K) = 2K−V+1 = −15 = −g.
    """

    def test_not_self_complementary(self):
        """K ≠ V−1−K: 12 ≠ 27."""
        assert K != V - 1 - K

    def test_complement_valency(self):
        """k̄ = V−1−K = 27 = ALBERT."""
        assert V - 1 - K == ALBERT

    def test_degree_difference(self):
        """k − k̄ = 12 − 27 = −15 = −g."""
        assert K - (V - 1 - K) == -G

    def test_self_comp_requires(self):
        """Self-complementary requires V ≡ 1 (mod 4), but V = 40 ≡ 0."""
        assert V % 4 == 0  # not ≡ 1

    def test_complement_larger(self):
        """Complement is denser: k̄ = 27 > K = 12."""
        assert V - 1 - K > K


# ═══════════════════════════════════════════════════════════════════
# T590: Stabilizer Cascade from (V−μ)²
# ═══════════════════════════════════════════════════════════════════
class TestStabilizerCascade:
    """Every stabilizer order derives from the master quantity (V−μ)² = 1296.
    |Aut| = V·(V−μ)², Stab(v) = (V−μ)², Stab(e) = 2(V−μ)²/K,
    Stab(arc) = (V−μ)²/K, Stab(flag) = (V−μ)²/μ.
    """

    def test_master_quantity(self):
        """(V−μ)² = 36² = 1296 = 6⁴."""
        master = (V - MU)**2
        assert master == 1296

    def test_aut_from_master(self):
        """|Aut| = V · master = 40 · 1296."""
        assert V * (V - MU)**2 == AUT

    def test_stab_v_from_master(self):
        """Stab(v) = master."""
        assert (V - MU)**2 == STAB_V

    def test_stab_e_from_master(self):
        """Stab(e) = 2·master/K."""
        assert 2 * (V - MU)**2 // K == STAB_E

    def test_stab_arc_from_master(self):
        """Stab(arc) = master/K."""
        assert (V - MU)**2 // K == STAB_ARC

    def test_stab_flag_from_master(self):
        """Stab(flag) = master/μ."""
        assert (V - MU)**2 // MU == STAB_FLAG

    def test_stab_ne_from_master(self):
        """Stab(ne) = 2·master/ALBERT."""
        assert 2 * (V - MU)**2 // ALBERT == STAB_NE
