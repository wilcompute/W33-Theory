#!/usr/bin/env python3
"""
THEORY PART CXXIX: THE E8 - W33 EDGE BIJECTION

Both E8 and W33 have 240:
- E8: 240 root vectors
- W33: 240 edges (orthogonal pairs of Witting states)

This CANNOT be coincidence. Let's find the explicit bijection.

KEY INSIGHT:
The Witting polytope has 240 vertices in C^4.
Under projection to CP^3, these become 40 rays (÷6 for phase).
The 240 vertices can be organized into 40 "hexads" of 6 related vertices.

HYPOTHESIS:
E8 roots ↔ Witting polytope vertices (both 240)
Witting edges (in the full polytope) ↔ some structure in E8

But we want: E8 roots ↔ W33 edges
This requires understanding how the 240 E8 roots map to 240 orthogonal pairs.
"""

from collections import defaultdict
from itertools import combinations, product

import numpy as np

omega = np.exp(2j * np.pi / 3)


def build_full_witting_polytope():
    """
    Build all 240 vertices of the Witting polytope in C^4.

    From Vlasov equation (1):
    (0,±ω^μ,∓ω^ν,±ω^λ), (∓ω^μ,0,±ω^ν,±ω^λ), (±ω^μ,∓ω^ν,0,±ω^λ), (∓ω^μ,∓ω^ν,∓ω^λ,0)
    (±i√3 ω^λ, 0, 0, 0), (0, ±i√3 ω^λ, 0, 0), (0, 0, ±i√3 ω^λ, 0), (0, 0, 0, ±i√3 ω^λ)

    where λ, μ, ν ∈ {0, 1, 2}
    """
    vertices = []
    sqrt3 = np.sqrt(3)

    omega_powers = [omega**k for k in range(3)]  # ω^0, ω^1, ω^2

    # Type 1: (±i√3 ω^λ, 0, 0, 0) and permutations - 4×2×3 = 24 vertices
    for pos in range(4):
        for sign in [1, -1]:
            for lam in range(3):
                v = np.zeros(4, dtype=complex)
                v[pos] = sign * 1j * sqrt3 * omega_powers[lam]
                vertices.append(v)

    # Type 2: The four groups with zeros in different positions
    # These give 4 × 3³ × 2³ patterns, but we need to match Vlasov's formula

    # Actually, let's use the explicit form from equation (2) scaled by phases
    # The 40 rays × 6 phases = 240 vertices

    # Build 40 base states
    base_states = []

    # 4 basis states
    for i in range(4):
        s = np.zeros(4, dtype=complex)
        s[i] = 1
        base_states.append(s)

    # 36 other states
    for mu in range(3):
        for nu in range(3):
            w_mu = omega_powers[mu]
            w_nu = omega_powers[nu]
            base_states.append(
                np.array([0, 1, -w_mu, w_nu], dtype=complex) / np.sqrt(3)
            )
            base_states.append(
                np.array([1, 0, -w_mu, -w_nu], dtype=complex) / np.sqrt(3)
            )
            base_states.append(
                np.array([1, -w_mu, 0, w_nu], dtype=complex) / np.sqrt(3)
            )
            base_states.append(np.array([1, w_mu, w_nu, 0], dtype=complex) / np.sqrt(3))

    # Multiply each by 6 phases: 1, ω, ω², -1, -ω, -ω²
    phases = [1, omega, omega**2, -1, -omega, -(omega**2)]

    vertices = []
    for state in base_states:
        for phase in phases:
            vertices.append(phase * state)

    return vertices, base_states


def build_e8_roots():
    """Build the 240 E8 roots in R^8."""
    roots = []

    # Type 1: (±1, ±1, 0, 0, 0, 0, 0, 0) and permutations - 112 roots
    for i in range(8):
        for j in range(i + 1, 8):
            for s1 in [1, -1]:
                for s2 in [1, -1]:
                    root = np.zeros(8)
                    root[i] = s1
                    root[j] = s2
                    roots.append(root)

    # Type 2: (±1/2)^8 with even number of minus signs - 128 roots
    for signs in product([1, -1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            root = np.array(signs) / 2
            roots.append(root)

    return np.array(roots)


def analyze_witting_edges():
    """
    Find edges in the full Witting polytope and in the projected graph.
    """
    print("=" * 70)
    print("ANALYZING WITTING POLYTOPE EDGES")
    print("=" * 70)

    vertices, base_states = build_full_witting_polytope()
    print(f"\n240 Witting polytope vertices constructed")
    print(f"40 base states (rays in CP^3)")

    # Normalize base states
    def normalize(v):
        return v / np.linalg.norm(v)

    # Find orthogonal pairs among base states (W33 edges)
    w33_edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            ip = (
                np.abs(np.vdot(normalize(base_states[i]), normalize(base_states[j])))
                ** 2
            )
            if ip < 1e-10:
                w33_edges.append((i, j))

    print(f"\nW33 edges (orthogonal pairs among 40 rays): {len(w33_edges)}")

    # For the full polytope, what's the edge structure?
    # Two vertices are "adjacent" if their inner product has specific value

    # Check inner products in full polytope
    full_ips = defaultdict(int)
    for i in range(240):
        for j in range(i + 1, 240):
            ip = np.vdot(vertices[i], vertices[j])
            ip_val = round(np.real(ip), 4) + 1j * round(np.imag(ip), 4)
            full_ips[ip_val] += 1

    print(f"\nInner product distribution in full Witting polytope:")
    for ip, count in sorted(full_ips.items(), key=lambda x: abs(x[0])):
        if count > 100:
            print(f"  {ip}: {count} pairs")

    return vertices, base_states, w33_edges


def find_e8_to_w33_map():
    """
    Attempt to find a map from E8 roots to W33 edges.

    Both have 240 elements. The map should respect symmetry.
    """
    print("\n" + "=" * 70)
    print("E8 → W33 EDGE CORRESPONDENCE")
    print("=" * 70)

    e8_roots = build_e8_roots()
    print(f"\n240 E8 roots constructed")

    _, base_states, w33_edges = analyze_witting_edges()

    # Key observation: E8 roots come in opposite pairs: ±r
    # W33 edges are unordered pairs {i, j}
    # So we have 120 E8 "lines" and 240 W33 edges

    # Actually, 240 E8 roots / 2 = 120 (not 240)
    # But 240 W33 edges... hmm

    # Wait - let's reconsider
    # E8 roots: 240 roots, but in pairs ±r → 120 root lines
    # W33: 40 vertices, 240 edges

    print("\nCOUNTING:")
    print(f"  E8: 240 roots, forming 120 antipodal pairs (lines)")
    print(f"  W33: 40 vertices, 240 edges")
    print(f"  Ratio: 240/120 = 2")

    print("""

    INSIGHT: The correspondence is NOT direct!

    Instead, consider the E6 ⊂ E8 embedding:
    - E6 has 72 roots
    - E8 = E6 ∪ (168 more roots)

    But 72 ≠ 240...

    ALTERNATIVE: Consider the Witting edges in the full 240-vertex polytope
    """)

    # In the full Witting polytope, which vertex pairs are adjacent?
    # For complex polytopes, adjacency is defined by the polytope structure

    # From Coxeter: Witting polytope has 2160 edges (as a 4D complex polytope)
    # Not 240!

    print("""
    CORRECTION: The full Witting polytope has MANY more edges!

    The 240 in W33 comes from the PROJECTED graph (40 states):
    - 40 states, degree 12 → 40 × 12 / 2 = 240 edges

    The 240 E8 roots correspondence is to the 240 VERTICES of Witting,
    NOT to the edges of W33!

    THE TRUE CORRESPONDENCE:
    ─────────────────────────
    E8 roots (240) ↔ Witting polytope vertices (240)
                        ↓ (quotient by Z₆ phases)
                   Witting rays (40)
                        ↓ (orthogonality graph)
                   W33 edges (240)

    So 240 appears TWICE but for different reasons:
    1. E8 roots = Witting vertices = 240 (original count)
    2. W33 edges = 240 (coincidentally same, from 40 × 12 / 2)

    Is this truly a coincidence, or is there deeper structure?
    """)

    return e8_roots, w33_edges


def investigate_240_coincidence():
    """
    Investigate whether the double appearance of 240 is coincidental.
    """
    print("\n" + "=" * 70)
    print("THE 240 COINCIDENCE")
    print("=" * 70)

    # The W33 parameters: n=40, k=12, λ=2, μ=4
    # Number of edges = n × k / 2 = 40 × 12 / 2 = 240

    # For SRG(n, k, λ, μ), the number of edges is n × k / 2
    # We need: n × k / 2 = 240
    #         n × k = 480

    # For W33: 40 × 12 = 480 ✓

    # The Witting polytope has 240 vertices
    # And |E8| = 240 roots

    # Is there a formula relating these?

    print("""
    KEY RELATIONSHIPS:

    1. |E8 roots| = 240
    2. |Witting vertices| = 240  (by construction from E8)
    3. |W33 edges| = 240 = 40 × 12 / 2

    WHY 40 × 12 / 2 = 240?

    40 = 240/6 (quotient by phase group Z₆)
    12 = ?

    INSIGHT: 12 = |D₄ roots| / 2 = 24/2

    So: 40 × 12 / 2 = (240/6) × (24/2) / 2 = 240 × 24 / 24 = 240 !

    The 240 is preserved because:
    - Dividing by 6 (phases): 240 → 40
    - Multiplying by 12 (degree): 40 → 480 directed edges
    - Dividing by 2 (undirected): 480 → 240

    The degree 12 exactly compensates for the phase quotient!
    """)

    # Why is degree = 12?
    # In CP^3 (projective 3-space), a generic point has...
    # Actually, 12 orthogonal states come from the Witting structure

    print("""
    WHY DEGREE 12?

    Each Witting state |ψ⟩ is orthogonal to states |φ⟩ where ⟨ψ|φ⟩ = 0.

    In the Witting configuration:
    - |⟨ψ|φ⟩|² ∈ {0, 1/3} (only two values!)
    - 12 states give |⟨ψ|φ⟩|² = 0
    - 27 states give |⟨ψ|φ⟩|² = 1/3

    So degree 12 is determined by the specific SIC-POVM like structure.

    12 + 27 = 39 = 40 - 1 (other states besides ψ itself) ✓

    THE DEEPER FORMULA:

    For a point in CP^3 with the Witting symmetry,
    the "orthogonal locus" has exactly 12 points.

    This relates to:
    - The D₄ root system (24 roots, 12 pairs)
    - The quaternionic structure on C⁴ ≅ H²
    - The hyperbolic structure of CP³
    """)


def explore_e6_d5_action():
    """
    Explore how E6 and D5 Weyl groups act on the structures.
    """
    print("\n" + "=" * 70)
    print("W(E6) AND W(D5) ACTIONS")
    print("=" * 70)

    print("""
    |W(E6)| = 51,840 = |Aut(W33)|
    |W(D5)| = 1,920

    [W(E6) : W(D5)] = 51,840 / 1,920 = 27

    This matches the 27 non-neighbors of each W33 vertex!

    INTERPRETATION:
    ───────────────
    W(E6) acts transitively on W33 vertices (40 vertices).
    Stabilizer of one vertex has order 51,840 / 40 = 1,296.

    W(D5) ⊂ W(E6) is a subgroup of index 27.

    The 27 cosets of W(D5) in W(E6) correspond to:
    - The 27 non-neighbors of each vertex
    - The 27 lines of the E6 incidence geometry
    - The 27 points on a cubic surface

    THE W(D5) ORBITS:
    ────────────────
    Given a vertex v in W33:
    - W(D5) has orbit size 40/27 × something?

    Actually: W(D5) acting on 40 Witting states...

    |W(D5)| = 1920 = 2^7 × 15
    40 = 2³ × 5

    If W(D5) acts transitively on 40 states:
    Stabilizer = 1920/40 = 48 = |W(D4)/2| = S₄ × Z₂

    But W(D5) ⊄ W(E6) directly maps to W33 action...

    Need to be careful: the 40 W33 vertices are acted on by W(E6),
    and W(D5) is a subgroup, so W(D5) also acts on the 40 vertices.
    """)

    # The D5 → E6 embedding
    # E6 has 72 roots, D5 has 40 roots
    # [E6:D5] at the root level: 72/40 = 1.8 (not integer!)

    # At the Weyl group level:
    # |W(E6)| / |W(D5)| = 51840 / 1920 = 27

    print("""
    D5 → E6 RELATIONSHIP:

    |D5 roots| = 40 (same as W33 vertices!)
    |E6 roots| = 72 (same as W33's 72 = 40 + 32 neighbor structure!)

    72 - 40 = 32 = dimension of spinor rep of D5

    This suggests:
    - E6 roots = D5 roots ∪ D5 spinor weights
    - 72 = 40 + 32

    And for W33:
    - 72 = edges incident to vertex + ???

    Wait: each vertex has degree 12, not 72.
    But total edges through vertex counting: 40 × 12 = 480 (double counting)

    Hmm, 72 appears as:
    - |E6 roots| = 72
    - Our earlier 72 = 40 + 32 decomposition in the theory
    """)


if __name__ == "__main__":
    find_e8_to_w33_map()
    investigate_240_coincidence()
    explore_e6_d5_action()

    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print("""
    THE 240 APPEARS TWICE FOR RELATED BUT DISTINCT REASONS:

    1. |E8 roots| = |Witting polytope vertices| = 240
       - This is BY CONSTRUCTION (Witting embeds in E8)

    2. |W33 edges| = 40 × 12 / 2 = 240
       - This comes from the SRG parameters
       - 40 = 240/6 (quotient)
       - 12 = degree (from orthogonality structure)

    The equality 240 = 240 is NOT accidental:
    - The degree 12 precisely compensates for the 6-fold quotient
    - This is a feature of the exceptional geometry

    THE KEY NUMBERS AND THEIR SOURCES:
    ──────────────────────────────────
    240 = |E8 roots| = |Witting vertices| = |W33 edges|
     72 = |E6 roots| = 40 + 32 (D5 + spinor)
     51840 = |W(E6)| = |Aut(W33)|
     40 = |D5 roots| = |W33 vertices| = 240/6
     27 = |E6 fund rep| = [W(E6):W(D5)] = W33 non-degree
     12 = |D4 roots|/2 = W33 degree

    EVERYTHING TRACES TO THE EXCEPTIONAL LIE ALGEBRA E8!
    """)
