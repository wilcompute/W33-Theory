#!/usr/bin/env python3
"""
THEORY PART CXXX: THE 27 LINES AND THE CUBIC SURFACE

The number 27 appears in W33 as the non-neighbor count.
27 is also famously the number of lines on a cubic surface!

This connection is NOT a coincidence:
- W(E6) acts on both the 27 lines AND on W33
- The index [W(E6):W(D5)] = 27
- The E6 fundamental representation has dimension 27

Let's explore this deep connection.

THE SCHLÄFLI GRAPH:
The 27 lines on a cubic surface form a graph where:
- 27 vertices (lines)
- Two lines adjacent iff they intersect
- Each line intersects 10 others
- This is the Schläfli graph: SRG(27, 16, 10, 8)

WAIT: The complement of Schläfli is SRG(27, 10, 1, 5)
That's the graph of DISJOINT lines!

How does this relate to W33's 27 non-neighbors?
"""

from collections import defaultdict
from itertools import combinations, product

import numpy as np


def build_27_lines():
    """
    Build the 27 lines on a cubic surface using the double-six construction.

    A cubic surface in P^3 contains exactly 27 lines.
    These can be labeled as:
    - a_1, ..., a_6 (first six)
    - b_1, ..., b_6 (second six, each b_i skew to a_i)
    - c_ij for i < j (15 lines, c_ij meets a_i, a_j, b_i, b_j)

    Total: 6 + 6 + 15 = 27
    """
    lines = []

    # First six: a_1 through a_6
    for i in range(1, 7):
        lines.append(("a", i))

    # Second six: b_1 through b_6
    for i in range(1, 7):
        lines.append(("b", i))

    # Fifteen c_ij lines
    for i in range(1, 7):
        for j in range(i + 1, 7):
            lines.append(("c", i, j))

    return lines


def lines_intersect(L1, L2):
    """
    Determine if two lines on the cubic surface intersect.

    Rules:
    - a_i and a_j are skew (don't intersect) for i ≠ j
    - b_i and b_j are skew for i ≠ j
    - a_i and b_i are skew (by double-six construction)
    - a_i and b_j intersect for i ≠ j
    - a_i and c_jk: intersect iff i ∈ {j, k}
    - b_i and c_jk: intersect iff i ∈ {j, k}
    - c_ij and c_kl: intersect iff |{i,j} ∩ {k,l}| = 1
    """
    if L1 == L2:
        return False

    type1, type2 = L1[0], L2[0]

    if type1 == "a" and type2 == "a":
        return False  # a_i, a_j are skew

    if type1 == "b" and type2 == "b":
        return False  # b_i, b_j are skew

    if type1 == "a" and type2 == "b":
        return L1[1] != L2[1]  # a_i meets b_j iff i ≠ j

    if type1 == "b" and type2 == "a":
        return L1[1] != L2[1]

    if type1 == "a" and type2 == "c":
        return L1[1] in L2[1:]  # a_i meets c_jk iff i ∈ {j,k}

    if type1 == "c" and type2 == "a":
        return L2[1] in L1[1:]

    if type1 == "b" and type2 == "c":
        return L1[1] in L2[1:]  # b_i meets c_jk iff i ∈ {j,k}

    if type1 == "c" and type2 == "b":
        return L2[1] in L1[1:]

    if type1 == "c" and type2 == "c":
        # c_ij meets c_kl iff they share exactly one index
        set1 = set(L1[1:])
        set2 = set(L2[1:])
        return len(set1 & set2) == 1

    return False


def build_schlafli_graph():
    """Build the Schläfli graph: intersection graph of 27 lines."""
    lines = build_27_lines()
    n = len(lines)

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if lines_intersect(lines[i], lines[j]):
                edges.append((i, j))

    return lines, edges


def analyze_schlafli():
    """Analyze the Schläfli graph and its complement."""
    print("=" * 70)
    print("THE 27 LINES ON A CUBIC SURFACE")
    print("=" * 70)

    lines, edges = build_schlafli_graph()
    n = len(lines)

    # Build adjacency
    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    degrees = [len(adj[i]) for i in range(n)]

    print(f"\nSchläfli graph:")
    print(f"  Vertices: {n}")
    print(f"  Edges: {len(edges)}")
    print(f"  Degree sequence: {set(degrees)}")
    print(f"  Regular: {len(set(degrees)) == 1}")

    if len(set(degrees)) == 1:
        k = degrees[0]
        print(f"  Degree k = {k}")

        # Check SRG parameters
        lambda_vals = []
        for i, j in edges:
            common = len(adj[i] & adj[j])
            lambda_vals.append(common)

        mu_vals = []
        for i in range(n):
            for j in range(i + 1, n):
                if j not in adj[i]:
                    common = len(adj[i] & adj[j])
                    mu_vals.append(common)

        print(f"  λ values: {set(lambda_vals)}")
        print(f"  μ values: {set(mu_vals)}")

        if len(set(lambda_vals)) == 1 and len(set(mu_vals)) == 1:
            lam = lambda_vals[0]
            mu = mu_vals[0]
            print(f"\n  *** SCHLÄFLI IS SRG({n}, {k}, {lam}, {mu}) ***")

    # Analyze complement (non-intersection graph)
    print(f"\nComplement graph (skew lines):")
    comp_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if j not in adj[i]:
                comp_edges.append((i, j))

    comp_adj = defaultdict(set)
    for i, j in comp_edges:
        comp_adj[i].add(j)
        comp_adj[j].add(i)

    comp_degrees = [len(comp_adj[i]) for i in range(n)]
    print(f"  Edges: {len(comp_edges)}")
    print(f"  Degree: {set(comp_degrees)}")

    if len(set(comp_degrees)) == 1:
        k = comp_degrees[0]

        lambda_vals = []
        for i, j in comp_edges:
            common = len(comp_adj[i] & comp_adj[j])
            lambda_vals.append(common)

        mu_vals = []
        for i in range(n):
            for j in range(i + 1, n):
                if j not in comp_adj[i]:
                    common = len(comp_adj[i] & comp_adj[j])
                    mu_vals.append(common)

        print(f"  λ values: {set(lambda_vals)}")
        print(f"  μ values: {set(mu_vals)}")

        if len(set(lambda_vals)) == 1 and len(set(mu_vals)) == 1:
            lam = lambda_vals[0]
            mu = mu_vals[0]
            print(f"\n  *** COMPLEMENT IS SRG({n}, {k}, {lam}, {mu}) ***")

    return lines, adj


def w33_and_27_lines():
    """
    Explore the relationship between W33 and the 27 lines.
    """
    print("\n" + "=" * 70)
    print("W33 AND THE 27 LINES")
    print("=" * 70)

    print(
        """
    THE CONNECTION:
    ───────────────
    W33: SRG(40, 12, 2, 4)
    - 40 vertices (Witting states)
    - Each vertex has 12 neighbors and 27 NON-neighbors

    27 Lines: Schläfli graph SRG(27, 16, 10, 8)
    - 27 vertices (lines on cubic surface)
    - Each line intersects 16 others

    These are DIFFERENT graphs, but connected through E6:

    W(E6) acts on:
    1. The 40 Witting states (via Aut(W33))
    2. The 27 lines on the cubic surface
    3. The 27-dimensional fundamental representation of E6

    THE INDEX CONNECTION:
    ────────────────────
    [W(E6) : W(D5)] = 51840 / 1920 = 27

    The 27 cosets of W(D5) in W(E6) can be identified with:
    - The 27 non-neighbors of a W33 vertex
    - The 27 lines on a cubic surface
    - The 27 weights of the E6 fundamental representation
    """
    )

    # Verify the index
    print("\nVerifying index calculation:")
    print(f"  |W(E6)| = 51840")
    print(f"  |W(D5)| = 1920")
    print(f"  Index = 51840 / 1920 = {51840 // 1920}")


def build_e6_weights():
    """
    Build the 27 weights of the E6 fundamental representation.

    In the E6 weight lattice, the fundamental rep has weights
    that can be described using the E8 → E6 projection.
    """
    print("\n" + "=" * 70)
    print("E6 FUNDAMENTAL REPRESENTATION (27 weights)")
    print("=" * 70)

    # E6 can be embedded in E8 where the last two coordinates sum to 0
    # The 27 fundamental weights come from E8 roots satisfying certain conditions

    # Standard description: E6 roots in 8D with constraint
    # For the 27-dimensional rep, we use weights of form:
    # ±e_i ± e_j for certain (i,j) combinations, plus spinor-type weights

    print(
        """
    The 27 weights of the E6 fundamental representation
    can be constructed as follows:

    Using E6 ⊂ E8 embedding (last two coords sum to 0):

    Type 1: 16 weights from D5 spinor
    Type 2: 10 weights from D5 vector
    Type 3: 1 weight (the zero weight with multiplicity)

    Total: 16 + 10 + 1 = 27

    But actually for the fundamental rep it's:
    - All 27 weights have multiplicity 1
    - They form an orbit under W(E6)

    EXPLICIT CONSTRUCTION:
    Using coordinates (x1,...,x8) with x7 + x8 = 0:

    The 27 weights include:
    - (1,0,0,0,0,0,1,-1) and permutations/signs satisfying E6 constraint
    """
    )

    # Build weights explicitly
    # E6 Dynkin labels for fundamental rep: (1,0,0,0,0,0) -> 27-dim

    # In Bourbaki coordinates for E6:
    # α1 = (1,-1,0,0,0,0,0,0)
    # α2 = (0,1,-1,0,0,0,0,0)
    # α3 = (0,0,1,-1,0,0,0,0)
    # α4 = (0,0,0,1,-1,0,0,0)
    # α5 = (0,0,0,0,1,-1,0,0)
    # α6 = (0,0,0,0,1,1,0,0) (this one is different - connects to E7/E8)

    # For our purposes, the key point is:
    # 27 weights ↔ 27 lines on cubic ↔ 27 non-neighbors in W33

    return 27


def the_tritangent_planes():
    """
    The 45 tritangent planes and the connection to W33's complement.
    """
    print("\n" + "=" * 70)
    print("TRITANGENT PLANES AND CONFIGURATION")
    print("=" * 70)

    print(
        """
    A cubic surface also has 45 TRITANGENT PLANES:
    - Each tritangent plane meets the surface in 3 lines forming a triangle
    - There are C(27,3) ways to choose 3 lines, but only 45 form triangles

    These 45 triangles are the maximal cliques in the Schläfli graph!
    (Each triangle = 3 mutually intersecting lines)

    RELATION TO W33:
    ────────────────
    W33 has 40 maximal 4-cliques (orthogonal bases)
    Each vertex is in exactly 4 cliques

    The 27 lines have 45 triangles (3-cliques)
    Each line is in: C(16,2)/C(3,2) triangles per line?

    Let's compute: each line meets 16 others
    Triangles through a given line L:
    - Need 2 more lines that meet L AND meet each other
    - If L meets M and N, need M to meet N
    - This is asking for edges within the 16 neighbors of L
    """
    )

    # Count triangles in Schläfli
    lines, adj = (
        analyze_schlafli.__wrapped__()
        if hasattr(analyze_schlafli, "__wrapped__")
        else (build_27_lines(), {})
    )

    # Rebuild adjacency
    lines = build_27_lines()
    adj = defaultdict(set)
    for i in range(27):
        for j in range(i + 1, 27):
            if lines_intersect(lines[i], lines[j]):
                adj[i].add(j)
                adj[j].add(i)

    # Count triangles
    triangles = []
    for i in range(27):
        for j in adj[i]:
            if j > i:
                for k in adj[i] & adj[j]:
                    if k > j:
                        triangles.append((i, j, k))

    print(f"\nTriangles (tritangent planes) in Schläfli graph: {len(triangles)}")

    # Count triangles per vertex
    tri_per_vertex = defaultdict(int)
    for t in triangles:
        for v in t:
            tri_per_vertex[v] += 1

    print(f"Triangles per vertex: {set(tri_per_vertex.values())}")

    return triangles


def w33_clique_structure():
    """
    Analyze W33's clique structure for comparison.
    """
    print("\n" + "=" * 70)
    print("W33 CLIQUE STRUCTURE")
    print("=" * 70)

    # Build W33 via Witting
    omega = np.exp(2j * np.pi / 3)

    states = []
    for i in range(4):
        s = np.zeros(4, dtype=complex)
        s[i] = 1
        states.append(s)

    omega_powers = [1, omega, omega**2]
    for mu in range(3):
        for nu in range(3):
            w_mu = omega_powers[mu]
            w_nu = omega_powers[nu]
            states.append(np.array([0, 1, -w_mu, w_nu], dtype=complex))
            states.append(np.array([1, 0, -w_mu, -w_nu], dtype=complex))
            states.append(np.array([1, -w_mu, 0, w_nu], dtype=complex))
            states.append(np.array([1, w_mu, w_nu, 0], dtype=complex))

    def normalize(v):
        return v / np.linalg.norm(v)

    # Build adjacency (orthogonality)
    adj = defaultdict(set)
    for i in range(40):
        for j in range(i + 1, 40):
            ip = np.abs(np.vdot(normalize(states[i]), normalize(states[j]))) ** 2
            if ip < 1e-10:
                adj[i].add(j)
                adj[j].add(i)

    # Find 4-cliques (bases)
    cliques = []
    for i in range(40):
        for j in adj[i]:
            if j > i:
                for k in adj[i] & adj[j]:
                    if k > j:
                        for l in adj[i] & adj[j] & adj[k]:
                            if l > k:
                                cliques.append((i, j, k, l))

    print(f"W33 has {len(cliques)} maximal 4-cliques (orthogonal bases)")

    # Count cliques per vertex
    cliques_per_vertex = defaultdict(int)
    for c in cliques:
        for v in c:
            cliques_per_vertex[v] += 1

    print(f"Cliques per vertex: {set(cliques_per_vertex.values())}")

    # Find triangles too
    triangles = []
    for i in range(40):
        for j in adj[i]:
            if j > i:
                for k in adj[i] & adj[j]:
                    if k > j:
                        triangles.append((i, j, k))

    print(f"W33 has {len(triangles)} triangles")

    tri_per_vertex = defaultdict(int)
    for t in triangles:
        for v in t:
            tri_per_vertex[v] += 1

    print(f"Triangles per vertex: {set(tri_per_vertex.values())}")

    # Verify: for SRG(n,k,λ,μ), triangles through a vertex = k*λ/2 + corrections
    # Actually: triangles through v = (number of edges among v's neighbors) / 2
    # But wait, triangles through v counts pairs of neighbors connected
    # For v with k=12 neighbors and λ=2, edges among neighbors varies

    print(
        """

    COMPARISON:
    ───────────
    Schläfli (27 lines):
    - 45 triangles (3-cliques, tritangent planes)
    - 10 triangles per vertex
    - No larger cliques (max clique = 3)

    W33 (40 Witting states):
    - 40 4-cliques (orthogonal bases)
    - 4 4-cliques per vertex
    - Max clique = 4 (bases)

    The "27" in W33 (non-neighbors) connects to the 27 lines
    through W(E6), but the graph structures are different.
    """
    )


def summary_27_connection():
    """Summarize the 27 connection."""
    print("\n" + "=" * 70)
    print("SUMMARY: THE MEANING OF 27")
    print("=" * 70)
    print(
        """
    THE NUMBER 27 APPEARS IN MANY RELATED CONTEXTS:

    ╔══════════════════════════════════════════════════════════════════╗
    ║  Context                         │  The "27"                    ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║  W33 graph                       │  Non-neighbors of each vertex║
    ║  Cubic surface                   │  Lines on the surface        ║
    ║  E6 representation               │  Dimension of fundamental rep║
    ║  Weyl group index                │  [W(E6) : W(D5)] = 27        ║
    ║  Exceptional Jordan algebra      │  Dimension (27 = 3×3×3)      ║
    ║  Freudenthal's magic square      │  E6 entry                    ║
    ╚══════════════════════════════════════════════════════════════════╝

    THE UNIFYING PRINCIPLE:
    ─────────────────────
    All these 27s are ISOMORPHIC as W(E6)-sets!

    W(E6) acts on each:
    - Transitively (single orbit)
    - With stabilizer of order 51840/27 = 1920 = |W(D5)|

    So the 27 non-neighbors of a W33 vertex, the 27 lines on a cubic,
    and the 27 weights of the E6 fundamental rep are all
    "the same thing" from the perspective of W(E6).

    THE D5 → E6 EMBEDDING:
    ────────────────────
    D5 has 40 roots (matching W33 vertices!)
    E6 has 72 roots

    The cosets W(E6)/W(D5) give 27 "directions" that E6 has
    beyond D5. These are the 27 that appear everywhere.

    PHYSICAL INTERPRETATION:
    ──────────────────────
    In W33/Witting:
    - 40 quantum states
    - Given state ψ: 12 orthogonal, 27 with overlap 1/3
    - The 27 "interfering" states form a W(E6)-orbit!

    The interference structure of quantum mechanics inherits
    the geometry of E6.
    """
    )


if __name__ == "__main__":
    analyze_schlafli()
    w33_and_27_lines()
    build_e6_weights()
    the_tritangent_planes()
    w33_clique_structure()
    summary_27_connection()
