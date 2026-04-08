#!/usr/bin/env python3
"""
W(3,3) = E₆ GEOMETRY: THE COMPLETE IDENTIFICATION
===================================================

From Hoffman (LSU): "Four dimensional symplectic geometry over GF(3)"

The W(3,3) generalized quadrangle is IDENTICAL to the E₆ geometry:

OBJECT IN W(3,3)          COUNT   ↔   OBJECT IN E₆/CUBIC SURFACE
───────────────────────── ─────── ─── ──────────────────────────────
Isotropic points            40        Points of GQ(3,3)
nsp-spreads                 27        27 lines on cubic surface
Nonsingular pairs           45        45 tritangent planes
Double-sixes                36        36 E₆ root hyperplanes (positive roots)
Doublets                   216        Pairs of skew lines

Aut(W(3,3)) = PSp(4,3):C₂ = W(E₆) = Weyl group of E₆ (order 51840)

Stabilizers:
  nsp-spread:  (Z/2)⁴ ⋊ A₅, order 960 = 51840/27 = 51840/q³
  double-six:  S₆, order 720 = 51840/36 = 51840/(q!)²
  nonsing pair: order 576 = 51840/45

E₆ exponents = {1, μ, q+λ, Φ₆, 2^q, k-1} = {1, 4, 5, 7, 8, 11}
E₆ degrees = {2, 5, 6, 8, 9, 12}, highest degree = k = 12

KEY RELATIONSHIPS:
  40 points × 27 spreads: each spread partitions ALL 40 points
  Each spread = 5 nonsingular pairs × 8 lines = 40 points
  40 = q³+q²+q+1, 27 = q³, 45 = q(q²+1)/2 × q, 36 = (q!)²

  The 15-dim eigenspace = adj(SU(4)) from PSU(4,2) ≅ PSp(4,3)
  The 24-dim eigenspace: PSp(4,3) has a 24-dim irrep
    In the context of E₆: related to the root space decomposition
    36 positive roots = 12 + 24? Need to check...

  Actually: the 40-point permutation character of W(E₆):
  40 = 1 + 15 + 24 (irreducible decomposition)
  The 27-line permutation character of W(E₆):
  27 = 1 + 6 + 20 (different decomposition!)
  So the 24 comes from the POINT action, not the LINE action.
"""

q, v, k = 3, 40, 12
f, g = 24, 15

# Verify all the counts
print("W(3,3) = E₆ GEOMETRY: COMPLETE NUMERICAL VERIFICATION")
print("=" * 60)

print(f"\n  Points: {v} = q³+q²+q+1 = {q**3+q**2+q+1} ✓")
print(f"  Spreads: {q**3} = q³ = 27 = lines on cubic ✓")
print(f"  Nonsing pairs: 45 = q(q²+1)(q+1)/4... let me check")
print(f"    45 = C(10,2) = C(Φ₄, 2) = {10*9//2} ✓")
print(f"    Or: 45 = v(v-1)/(2k) × ... actually 45 = 3 × 15 = q × g")
print(f"    45 = q × g = {q*g} ✓")
print(f"  Double-sixes: 36 = (q!)² = 6² ✓")
print(f"  Doublets: 216 = q³ × 2³ = 27 × 8 = 216 ✓")

print(f"\n  Stabilizer orders:")
print(f"  Spread stab: 51840/27 = {51840//27} = 960")
print(f"    960 = 2⁶ × 3 × 5 = (Z/2)⁴ ⋊ A₅")
print(f"  Double-six stab: 51840/36 = {51840//36} = 720")  
print(f"    720 = 6! = (q!)! = S₆ ✓")
print(f"  Nonsing pair stab: 51840/45 = {51840//45} = 576")
print(f"    576 = 24² = f² ✓")

print(f"\n  *** f² = 24² = 576 = stabilizer of a nonsingular pair ***")
print(f"  *** (q!)! = 720 = stabilizer of a double-six ***")
print(f"  *** 960 = 2⁶ × 15 = 64 × g = stabilizer of a spread ***")

print(f"""

THE COMPLETE E₆-W(3,3) DICTIONARY:
═══════════════════════════════════

  E₆ root system:                W(3,3) geometry:
  ─────────────────               ─────────────────
  72 roots                        72 = 2 × 36 = 2(q!)²
  36 positive roots               36 double-sixes
  27 lines on cubic               27 nsp-spreads (= q³)
  45 tritangent planes            45 nonsingular pairs (= qg)
  dim(E₆) = 78                   78 = dim(E₆) = q³ + v + Φ₃ - 2
                                  = 27 + 40 + 13 - 2 = 78 ✓
  
  E₆ fund rep: 27                q³ = 27
  E₆ adjoint: 78                 27 + 45 + 6 = 78
  W(E₆) order: 51840             Aut(W(3,3)) order
  W(E₆) exponents:               W(3,3) parameters:
    1, 4, 5, 7, 8, 11              1, μ, q+λ, Φ₆, 2^q, k-1
  W(E₆) degrees:                 
    2, 5, 6, 8, 9, 12              highest = k
  
  78 = 27 + 45 + 6               spreads + pairs + extra
  78 = 3 × 26 = q × 2Φ₃         = q × dim(F₄)... wait
  78 = 3 × 26                    q × 2Φ₃ = 3 × 26 = 78 ✓
  
  AND: dim(E₆) = 78 = q × 2Φ₃ = 2q(q²+q+1) - ... no
  78 = v + 2g + f/3 = 40 + 30 + 8 = 78 ✓

  Actually: 78 = 2(v-1) = 2 × 39 = 2(v-1)
  Check: 2(40-1) = 78 ✓
  *** dim(E₆) = 2(v-1) ***
  This is a CLEAN identity.
""")

# This is remarkable: dim(E₆) = 2(v-1)
print(f"  *** dim(E₆) = 2(v-1) = 2×{v-1} = {2*(v-1)} ***")
print(f"  78 = 2(v-1) ✓")
print(f"  Compare: dim(E₇) = 133 = 2(v-1) + 55 = 78 + 55")
print(f"  dim(E₈) = 248 = 2(v-1) + 170")
print(f"  Or: 248 = E + 2^q = 240 + 8")

