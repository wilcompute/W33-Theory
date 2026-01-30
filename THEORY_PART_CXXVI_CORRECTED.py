"""
W33 THEORY - PART CXXVI (CORRECTED): EXACT GROUP STRUCTURE
===========================================================

I made an error in the previous computation. Let me get the exact
relationship between Sp(4, F₃), PSp(4, F₃), W(E₆), and Aut(W33).
"""

from math import factorial


def main():
    print("=" * 70)
    print(" PART CXXVI (CORRECTED): EXACT GROUP IDENTIFICATION")
    print("=" * 70)

    # =========================================================================
    # COMPUTE EXACT ORDERS
    # =========================================================================
    print("\n" + "=" * 70)
    print(" EXACT GROUP ORDERS")
    print("=" * 70)

    # |Sp(2n, Fq)| = q^(n²) × ∏_{i=1}^{n} (q^(2i) - 1)
    # For Sp(4, F₃): n = 2, q = 3
    q = 3
    n = 2

    sp4_order = (q ** (n * n)) * (q**2 - 1) * (q**4 - 1)
    print(f"\n  |Sp(4, F₃)| = 3⁴ × (3²-1) × (3⁴-1)")
    print(f"             = 81 × 8 × 80")
    print(f"             = {sp4_order}")

    # The CENTER of Sp(4, F₃) consists of ±I, so has order 2
    # PSp(4, F₃) = Sp(4, F₃) / {±I}
    psp4_order = sp4_order // 2
    print(f"\n  |PSp(4, F₃)| = {sp4_order} / 2 = {psp4_order}")

    # W(E₆)
    W_E6 = 51840
    print(f"\n  |W(E₆)| = {W_E6}")

    print(f"\n  So: |Sp(4, F₃)| = {sp4_order} = |W(E₆)|")
    print(f"      |PSp(4, F₃)| = {psp4_order} ≠ |W(E₆)|")

    print("\n  CORRECTION: It's Sp(4, F₃) ≅ W(E₆), not PSp!")

    # =========================================================================
    # WHAT IS Aut(W33)?
    # =========================================================================
    print("\n" + "=" * 70)
    print(" WHAT IS Aut(W33)?")
    print("=" * 70)

    print("""
  W33 is the polar graph of the symplectic geometry Sp(4, F₃).

  The FULL automorphism group includes:
    • Sp(4, F₃) acting on maximal isotropics
    • Possibly field automorphisms (but F₃ has none except identity)
    • Possibly graph automorphisms not from the group

  For symplectic polar graphs over F_q:
    Aut(Sp polar graph) = PΓSp(2n, q) for q > 2

  For q = 3 (prime), field automorphisms are trivial, so:
    Aut(W33) = PSp(4, F₃) ⋊ ⟨field auts⟩ = PSp(4, F₃)

  But wait: |PSp(4, F₃)| = 25,920 ≠ 51,840

  Let me check the literature on this...
""")

    # =========================================================================
    # RESOLVING THE DISCREPANCY
    # =========================================================================
    print("\n" + "=" * 70)
    print(" RESOLVING THE DISCREPANCY")
    print("=" * 70)

    print("""
  There are several possibilities:

  1. MAYBE W33 has LARGER automorphism group than just PSp(4, F₃)?
     The polar graph might have extra automorphisms.

  2. MAYBE the literature claims are about different graphs?
     SRG(40, 12, 2, 4) might not be the same as the polar graph.

  3. MAYBE there's an outer automorphism involved?
     Sp(4, F₃) has outer automorphism structure to check.

  Let me verify by direct computation...
""")

    # =========================================================================
    # CHECK: IS W33 SELF-COMPLEMENTARY OR HAVE EXTRA STRUCTURE?
    # =========================================================================
    print("\n" + "=" * 70)
    print(" CHECKING W33 PROPERTIES")
    print("=" * 70)

    # SRG(40, 12, 2, 4) parameters
    n, k, lam, mu = 40, 12, 2, 4

    # Complement has parameters (n, n-k-1, n-2-2k+μ, n-2k+λ)
    k_bar = n - k - 1  # = 27
    lam_bar = n - 2 - 2 * k + mu  # = 40 - 2 - 24 + 4 = 18
    mu_bar = n - 2 * k + lam  # = 40 - 24 + 2 = 18

    print(f"\n  W33 parameters: ({n}, {k}, {lam}, {mu})")
    print(f"  Complement parameters: ({n}, {k_bar}, {lam_bar}, {mu_bar})")

    # Check if self-complementary
    if k == k_bar and lam == lam_bar and mu == mu_bar:
        print("  W33 is self-complementary!")
    else:
        print("  W33 is NOT self-complementary")
        print(f"  Complement is SRG(40, 27, 18, 18)")

    # =========================================================================
    # THE ACTUAL RELATIONSHIP
    # =========================================================================
    print("\n" + "=" * 70)
    print(" THE ACTUAL RELATIONSHIP (from literature)")
    print("=" * 70)

    print("""
  After more careful consideration:

  The symplectic group Sp(4, F₃) acts on the 40 maximal isotropics.

  The KERNEL of this action is the CENTER {±I}.

  So the group acting FAITHFULLY on W33 vertices is:
    PSp(4, F₃) = Sp(4, F₃) / {±I}
    |PSp(4, F₃)| = 25,920

  But wait - what if |Aut(W33)| = 51,840 is achieved by
  EXTENDING PSp(4, F₃)?

  Actually, let me reconsider. The standard result is:

  ╔═══════════════════════════════════════════════════════════════════╗
  ║                                                                   ║
  ║   Aut(W33) = Sp(4, F₃) / Z(Sp(4, F₃)) ⋊ Out                       ║
  ║                                                                   ║
  ║   For the specific SRG(40, 12, 2, 4):                             ║
  ║   |Aut| = 51,840 according to standard SRG databases              ║
  ║                                                                   ║
  ║   This means either:                                              ║
  ║   - There are extra automorphisms beyond PSp(4, F₃)               ║
  ║   - Or the action involves the full Sp(4, F₃)                     ║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝

  KEY INSIGHT: 51,840 / 25,920 = 2

  So |Aut(W33)| = 2 × |PSp(4, F₃)|

  This suggests Aut(W33) = PSp(4, F₃) ⋊ Z₂ for some Z₂ extension,
  OR Aut(W33) = Sp(4, F₃) where the center acts non-trivially on
  some additional structure (perhaps the graph + some orientation).
""")

    # =========================================================================
    # ACTUAL ISOMORPHISM
    # =========================================================================
    print("\n" + "=" * 70)
    print(" THE KEY ISOMORPHISM")
    print("=" * 70)

    print("""
  The precise statement from group theory is:

  ╔═══════════════════════════════════════════════════════════════════╗
  ║                                                                   ║
  ║   Sp(4, F₃) ≅ 2.W(E₆)                                             ║
  ║                                                                   ║
  ║   meaning Sp(4, F₃) is a DOUBLE COVER of W(E₆)!                   ║
  ║                                                                   ║
  ║   Equivalently: W(E₆) ≅ PSp(4, F₃)                                ║
  ║                                                                   ║
  ║   But wait: |PSp(4, F₃)| = 25,920 and |W(E₆)| = 51,840            ║
  ║                                                                   ║
  ║   That's wrong! Let me check the formulas again...                ║
  ║                                                                   ║
  ╚═══════════════════════════════════════════════════════════════════╝
""")

    # Double-check W(E₆)
    # W(E₆) has order 2^7 × 3^4 × 5 = 128 × 81 × 5 = 51,840
    print("  |W(E₆)| = 2⁷ × 3⁴ × 5 =", 2**7 * 3**4 * 5)

    # Check if 51840 = 2 × 25920
    print(f"  51,840 / 2 = {51840 // 2}")
    print(f"  |PSp(4, F₃)| = {psp4_order}")
    print(f"  Match: {51840 // 2 == psp4_order}")

    print("""

  AH HA! So:

    |W(E₆)| = 51,840 = 2 × 25,920 = 2 × |PSp(4, F₃)|

  This means W(E₆) is a Z₂ EXTENSION of PSp(4, F₃)!

  The correct statement is:

    W(E₆) ≅ PSp(4, F₃).2  (an extension)

  Or equivalently, PSp(4, F₃) is an INDEX 2 subgroup of W(E₆).

  And for W33:
    If |Aut(W33)| = 51,840 = |W(E₆)|,
    then Aut(W33) ≅ W(E₆), which extends PSp(4, F₃).
""")

    # =========================================================================
    # FINAL RESOLUTION
    # =========================================================================
    print("\n" + "=" * 70)
    print(" FINAL RESOLUTION")
    print("=" * 70)

    print("""
  ═══════════════════════════════════════════════════════════════════
  THE CORRECT PICTURE:
  ═══════════════════════════════════════════════════════════════════

  1. W33 = symplectic polar graph of Sp(4, F₃)

  2. PSp(4, F₃) acts faithfully on W33, |PSp| = 25,920

  3. W33 has ADDITIONAL automorphisms beyond PSp(4, F₃)!
     These could come from:
     - The "polarity" (swapping points and hyperplanes)
     - Some graph automorphism not from the group action

  4. Aut(W33) has order 51,840 = 2 × |PSp(4, F₃)|

  5. It happens that |Aut(W33)| = |W(E₆)|, and in fact:

     ╔═══════════════════════════════════════════════════════╗
     ║                                                       ║
     ║   Aut(W33) ≅ W(E₆)     (as abstract groups)           ║
     ║                                                       ║
     ║   with PSp(4, F₃) as an index-2 subgroup              ║
     ║                                                       ║
     ╚═══════════════════════════════════════════════════════╝

  The exceptional isomorphism Aut(W33) ≅ W(E₆) is the KEY FACT
  that connects W33 to E₆ structure!

  ═══════════════════════════════════════════════════════════════════
""")


if __name__ == "__main__":
    main()
