"""
W33 THEORY - PART CXX: THE NUMBER 1296 AND THE STABILIZER STRUCTURE
===================================================================

The stabilizer of any vertex in W33 has order 1296.

|Stab(v)| = |Aut(W33)| / 40 = 51,840 / 40 = 1,296

This number has remarkable structure:
  1296 = 2⁴ × 3⁴ = 16 × 81
  1296 = 36²
  1296 = 6⁴
  1296 = 12 × 108
  1296 = 27 × 48

Let's understand what this stabilizer does and how it connects
to the E6/Albert/triality structure.
"""

import json
from datetime import datetime


def main():
    print("=" * 70)
    print(" W33 THEORY - PART CXX: THE NUMBER 1296")
    print(" The Stabilizer Structure")
    print("=" * 70)

    results = {"part": "CXX", "findings": {}}

    # =========================================================================
    # SECTION 1: FACTORIZATIONS OF 1296
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 1: FACTORIZATIONS OF 1296")
    print("=" * 70)

    n = 1296
    print(f"\n  |Stab(v)| = {n}")
    print(f"\n  Prime factorization: {n} = 2^4 × 3^4")

    print(f"\n  Significant factorizations:")
    print(f"    {n} = 36² = (6²)² = 6⁴")
    print(f"    {n} = 16 × 81 = 2⁴ × 3⁴")
    print(f"    {n} = 12 × 108")
    print(f"    {n} = 27 × 48")
    print(f"    {n} = 24 × 54 = 24 × 54")
    print(f"    {n} = 8 × 162 = 8 × 2 × 81")
    print(f"    {n} = 4 × 324 = 4 × 18²")
    print(f"    {n} = 3 × 432")
    print(f"    {n} = 2 × 648 = 2 × 8 × 81")

    # Key connection numbers
    print(f"\n  Key connections:")
    print(f"    12 × 108 = {12 * 108} (neighbors × H27 edges)")
    print(f"    27 × 48 = {27 * 48} (Albert × ?)")
    print(f"    192 × 6.75 = {192 * 6.75} (not integer)")
    print(f"    1296 / 192 = {n / 192} = 6.75 (not integer)")

    results["findings"]["factorizations"] = {
        "prime": "2^4 × 3^4",
        "square": "36²",
        "fourth_power": "6⁴",
        "key_products": ["12 × 108", "27 × 48", "16 × 81"],
    }

    # =========================================================================
    # SECTION 2: THE STABILIZER AS A GROUP
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 2: THE STABILIZER AS A GROUP")
    print("=" * 70)

    stab_analysis = """
  WHAT IS THE STABILIZER?

  Stab(v) = { g ∈ Aut(W33) : g(v) = v }

  This subgroup fixes the vertex v and permutes:
    - The 12 neighbors among themselves
    - The 27 non-neighbors among themselves

  It also must preserve the edge structure between these sets.

  GROUP STRUCTURE CONSTRAINTS:

  |Stab(v)| = 1296 = 2⁴ × 3⁴

  Groups of this order include:
    - (Z/6Z)⁴ (abelian, not likely for automorphisms)
    - Various semidirect products
    - Subgroups of S₁₂ × S₂₇

  Since Stab acts on 12 neighbors and 27 non-neighbors:
    |Stab| divides |S₁₂| × |S₂₇|

  But 1296 << 12! × 27!, so it's a small subgroup.
"""
    print(stab_analysis)

    # =========================================================================
    # SECTION 3: ACTION ON NEIGHBORS
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 3: ACTION ON 12 NEIGHBORS")
    print("=" * 70)

    neighbor_analysis = """
  THE 12 NEIGHBORS FORM SRG(12, 2, 1, 0):

  This is the "cocktail party graph" complement = 6K₂
  = 6 disjoint edges (matching)

  The automorphism group of 6K₂:
    |Aut(6K₂)| = 2⁶ × 6! = 64 × 720 = 46,080

  But Stab(v) ⊆ Aut(W33), and must preserve more structure.

  The restriction Stab(v) → Aut(H12):
    This gives a homomorphism
    Image has order dividing both 1296 and 46080
    gcd(1296, 46080) = 1296

  So potentially all of Stab(v) acts faithfully on H12!

  STRUCTURE OF THE ACTION:

  The 12 neighbors pair up as 6 "matched pairs"
  (this is the SRG(12, 2, 1, 0) structure)

  |Aut(6K₂)| = 2⁶ × 6! = 64 × 720

  If Stab acts as a subgroup:
    1296 = 2⁴ × 3⁴ vs 46080 = 2⁷ × 3² × 5

  The 3⁴ factor is curious - more 3s than in 6!
"""
    print(neighbor_analysis)

    # =========================================================================
    # SECTION 4: THE ROLE OF 6
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 4: THE MAGIC OF 6")
    print("=" * 70)

    six_analysis = """
  THE NUMBER 6 APPEARS EVERYWHERE:

  1296 = 6⁴

  Why is 6 so fundamental?

  6 = 2 × 3 = smallest number with two distinct prime factors
  6 = 3! = |S₃| = triality group order
  6 = dimension of SU(3) / fundamental rep

  IN OUR STRUCTURE:

  - 12 = 2 × 6 neighbors (form 6 pairs)
  - 1296 = 6⁴ stabilizer order
  - 216 = 6³ edges involving non-neighbors
  - 51840 = 6⁴ × 40 automorphism order

  THE 6-FOLD STRUCTURE:

  W33 has a "mod 6" symmetry built in:
    |Aut(W33)| = 51,840 = 6⁴ × 40
    |Stab(v)| = 1,296 = 6⁴

  This connects to:
    - Triality (S₃ = 6)
    - The 6 pairs of neighbors
    - The 6³ = 216 cross-edges
"""
    print(six_analysis)

    print("\n  Verification of 6-powers:")
    print(f"    6¹ = 6")
    print(f"    6² = 36")
    print(f"    6³ = 216 (cross-edges)")
    print(f"    6⁴ = 1296 (stabilizer)")
    print(f"    6⁴ × 40 = 51840 (full automorphism)")

    results["findings"]["powers_of_6"] = {"6^1": 6, "6^2": 36, "6^3": 216, "6^4": 1296}

    # =========================================================================
    # SECTION 5: CONNECTION TO E6
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 5: CONNECTION TO E6 STRUCTURE")
    print("=" * 70)

    e6_connection = """
  E6 AND THE NUMBER 1296:

  |W(E6)| = 51,840 = 1296 × 40

  E6 has:
    - Rank 6
    - 72 roots
    - 27-dimensional fundamental representation
    - Weyl group of order 51,840

  THE WEYL GROUP STRUCTURE:

  W(E6) acts on the E6 root system.

  The stabilizer of a "weight" in the 27 representation
  might have order related to 1296!

  Consider: |W(E6)| / 27 = 51840 / 27 = 1920
  And: |W(E6)| / 40 = 1296

  So the "40" vertices of W33 are like special points
  in the E6 weight lattice!

  QUOTIENT STRUCTURE:

  W(E6) / Stab(v) ≅ {40 vertices}

  This is a homogeneous space for the Weyl group action!
"""
    print(e6_connection)

    # Check various quotients
    print("\n  E6 quotient checks:")
    print(f"    |W(E6)| / 40 = 51840 / 40 = {51840 // 40} = |Stab(v)| ✓")
    print(f"    |W(E6)| / 27 = 51840 / 27 = {51840 // 27} = 1920")
    print(f"    |W(E6)| / 72 = 51840 / 72 = {51840 // 72} = 720 = 6!")
    print(f"    |W(E6)| / 45 = 51840 / 45 = {51840 // 45} = 1152 = |Aut(24-cell)|")

    results["findings"]["e6_quotients"] = {
        "/40": 1296,
        "/27": 1920,
        "/72": 720,
        "/45": 1152,
    }

    # =========================================================================
    # SECTION 6: THE 1296 = 27 × 48 DECOMPOSITION
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 6: THE DECOMPOSITION 1296 = 27 × 48")
    print("=" * 70)

    decomp_27_48 = """
  1296 = 27 × 48

  This is remarkable because:
    - 27 = Albert algebra dimension = |N̄(v)|
    - 48 = ?

  WHAT IS 48?

  48 = 2 × 24 = 2 × (D4 roots)
  48 = 3 × 16 = 3 × (spinor dimension)
  48 = 4 × 12 = 4 × (neighbors)
  48 = 6 × 8 = 6 × (octonion dimension)
  48 = 2⁴ × 3

  INTERPRETATION:

  If Stab(v) acts on 27 non-neighbors with orbits,
  and the orbit is all 27 (single orbit), then:
    |point stabilizer| = 1296 / 27 = 48

  So each non-neighbor has a stabilizer of order 48 within Stab(v)!

  48 = STRUCTURE PRESERVING SYMMETRY OF ONE ALBERT ELEMENT

  This suggests: picking a vertex in W33 + picking a non-neighbor
  leaves 48 degrees of freedom, relating to:
    - 2 × 24 (D4 roots doubled)
    - 6 × 8 (triality × octonions)
"""
    print(decomp_27_48)

    print("\n  The number 48:")
    print(f"    48 = 2 × 24 = 2 × (D4 roots)")
    print(f"    48 = 3 × 16 = 3 × (spinor)")
    print(f"    48 = 4 × 12 = 4 × (neighbors)")
    print(f"    48 = 6 × 8 = 6 × (octonion dim)")
    print(f"    48 = |GL(2, F₃)| = (9-1)(9-3) = 8 × 6")

    results["findings"]["number_48"] = {
        "factorizations": ["2×24", "3×16", "4×12", "6×8"],
        "gl2_f3": True,
    }

    # =========================================================================
    # SECTION 7: THE 1296 = 12 × 108 DECOMPOSITION
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 7: THE DECOMPOSITION 1296 = 12 × 108")
    print("=" * 70)

    decomp_12_108 = """
  1296 = 12 × 108

  This connects directly to our structure:
    - 12 = number of neighbors
    - 108 = edges in H27 = cross-edges from neighbors to non-neighbors

  INTERPRETATION:

  The stabilizer size = (neighbors) × (edges per structure)

  If Stab(v) acts on 12 neighbors with single orbit:
    |neighbor stabilizer| = 1296 / 12 = 108

  108 = STRUCTURE PRESERVING SYMMETRY OF ONE NEIGHBOR

  Picking a vertex v + picking a neighbor n leaves 108 symmetries.

  And 108 is ALSO the edge count!
    - Edges in H27: 108
    - Edges from N(v) to N̄(v): 108
"""
    print(decomp_12_108)

    print("\n  Orbit-stabilizer verification:")
    print(f"    If 12 neighbors form one orbit: |stab| = 1296/12 = {1296//12}")
    print(f"    If 27 non-neighbors form one orbit: |stab| = 1296/27 = {1296//27}")
    print(f"    108 × 48 / 1296 = {108 * 48 / 1296} (not immediately meaningful)")

    # =========================================================================
    # SECTION 8: GROUP THEORY IDENTIFICATION
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 8: IDENTIFYING THE GROUP")
    print("=" * 70)

    group_id = """
  KNOWN GROUPS OF ORDER 1296:

  1296 = 2⁴ × 3⁴

  Some groups of this order:
    - (Z/6Z)⁴ (abelian)
    - Z/2Z ≀ (Z/3Z)⁴ (wreath product)
    - Various semidirect products
    - Subgroups of GL(4, F₃)

  CANDIDATE: A SUBGROUP OF W(E6)

  Since Stab(v) ⊆ Aut(W33) = W(E6), it must be a subgroup of W(E6).

  W(E6) has various subgroups:
    - W(D4) of order 192 (index 270)
    - W(A5) = S6 of order 720 (index 72)
    - W(A4) = S5 of order 120 (index 432)

  1296 is NOT the order of any Weyl subgroup of W(E6).

  It's likely a non-Weyl subgroup, perhaps:
    - Stabilizer of some geometric structure
    - Point stabilizer in the 40-vertex action

  THE KEY INSIGHT:

  Stab(v) is the group that preserves the local structure:
    1 + 12 + 27 decomposition around vertex v
"""
    print(group_id)

    # =========================================================================
    # SECTION 9: THE HIERARCHY
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 9: THE COMPLETE HIERARCHY")
    print("=" * 70)

    hierarchy = """
  THE NUMBER HIERARCHY:

  Starting from 6:

    6¹ = 6        (triality, pairs)
    6² = 36       (6×6)
    6³ = 216      (cross-edges total)
    6⁴ = 1296     (stabilizer)
    6⁴ × 40 = 51840 (full automorphism = W(E6))

  The factor 40 breaks the 6-power pattern:
    40 = 8 × 5 (no 3s!)
    40 = W33 vertices

  INTERPRETATION:

  The 40 vertices are "special" - they break the 6-symmetry.

  Within each vertex's perspective (stabilizer), everything
  is organized by powers of 6:
    - 6 pairs of neighbors
    - 6³ edges involving non-neighbors
    - 6⁴ total symmetries

  But there are 40 such perspectives, and 40 doesn't divide 6^k.

  40 = 8 × 5 connects to:
    - 8 = octonion dimension
    - 5 = ??? (dimension of something)

  Or: 40 = 2³ × 5 = 2(2² × 5) = 2 × 20
"""
    print(hierarchy)

    # =========================================================================
    # SECTION 10: SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 10: SUMMARY")
    print("=" * 70)

    summary = """
  ═══════════════════════════════════════════════════════════════════
  PART CXX SUMMARY: THE NUMBER 1296
  ═══════════════════════════════════════════════════════════════════

  |Stab(v)| = 1296 = 6⁴ = 36² = 2⁴ × 3⁴

  KEY DECOMPOSITIONS:

    1296 = 6⁴           (powers of triality)
    1296 = 12 × 108     (neighbors × edge structure)
    1296 = 27 × 48      (Albert × local symmetry)
    1296 = 36²          (perfect square)

  GEOMETRIC MEANING:

    - Stab(v) preserves the 1 + 12 + 27 decomposition
    - Acts on 12 neighbors (possibly single orbit → 108 point stab)
    - Acts on 27 non-neighbors (possibly single orbit → 48 point stab)

  THE 6-HIERARCHY:

    6¹ = 6         (triality order)
    6² = 36        (6 × 6)
    6³ = 216       (edges involving non-neighbors)
    6⁴ = 1296      (stabilizer order)
    6⁴ × 40 = 51840 (|W(E6)| = |Aut(W33)|)

  ═══════════════════════════════════════════════════════════════════

  THE CENTRAL INSIGHT:

  The stabilizer of order 6⁴ encodes the "local structure"
  of W33 around each vertex. The factor 40 = 8 × 5 that
  relates Stab to the full group is the "global" piece.

  W33 = 40 copies of the local 6⁴-structure, glued consistently!

  ═══════════════════════════════════════════════════════════════════
"""
    print(summary)

    # Save results
    with open("PART_CXX_1296_analysis.json", "w") as f:
        json.dump(results, f, indent=2, default=int)
    print(f"\nResults saved to: PART_CXX_1296_analysis.json")

    print("\n" + "=" * 70)
    print(" END OF PART CXX")
    print("=" * 70)

    return results


if __name__ == "__main__":
    main()
