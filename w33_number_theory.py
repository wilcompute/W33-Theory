#!/usr/bin/env python3
"""
W33 AND NUMBER THEORY
=====================

The number 3 is special. Let's explore WHY.

This script explores the deep connections between:
  - W33 structure
  - The prime 3
  - Modular forms
  - The Riemann zeta function
  - The abc conjecture
"""

from collections import defaultdict
from fractions import Fraction

import numpy as np

print("=" * 80)
print("W33 AND NUMBER THEORY")
print("Why 3 is the Magic Number")
print("=" * 80)

# =============================================================================
# PART 1: THE PRIME 3 IS SPECIAL
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: WHY 3?")
print("=" * 80)

print("""
THE UNIQUE PROPERTIES OF 3
==========================

3 is the:
  • Smallest odd prime
  • Only prime p where p = p-1 + 1 (trivially)
  • Only prime where 2p-1 = p + p-1
  • Number of spatial dimensions
  • Number of quark colors
  • Number of generations

3 in W33:
  • q = 3 (field size)
  • 3 points per line (in W33, technically 4, but 3-space!)
  • Z₃ fiber (generations)
  • 81 = 3⁴ (Steinberg dimension)
  • 40 = 4 × 10 = 4 × (3² + 1)
  • 45 = 9 × 5 = 3² × 5

The recurring pattern:
  Everything divides by or relates to 3!
""")

# =============================================================================
# PART 2: FERMAT'S LITTLE THEOREM AND W33
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: FERMAT'S LITTLE THEOREM")
print("=" * 80)

print("""
FERMAT'S LITTLE THEOREM
=======================

For prime p and gcd(a,p) = 1:
  a^(p-1) ≡ 1 (mod p)

For p = 3:
  a² ≡ 1 (mod 3) for a ∈ {1, 2}

This means:
  1² = 1 ≡ 1 (mod 3) ✓
  2² = 4 ≡ 1 (mod 3) ✓

The multiplicative group (Z/3Z)* has order 2.
This is the SIMPLEST non-trivial case!

In W33:
  - Phases take values in Z₁₂
  - Z₁₂ = Z₄ × Z₃ (Chinese Remainder Theorem)
  - The Z₃ part is (Z/3Z)* extended
  - The Z₄ part is related to Gaussian integers
""")

# Verify
for a in [1, 2]:
    print(f"  {a}² mod 3 = {a**2 % 3}")

# =============================================================================
# PART 3: QUADRATIC RECIPROCITY
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: QUADRATIC RECIPROCITY")
print("=" * 80)


def legendre(a, p):
    """Compute Legendre symbol (a/p)."""
    if a % p == 0:
        return 0
    result = pow(a, (p - 1) // 2, p)
    return result if result <= 1 else result - p


print("""
QUADRATIC RECIPROCITY
=====================

The Legendre symbol (a/p) = 1 if a is a square mod p, -1 otherwise.

For p = 3:
  (1/3) = 1  (1 is a square: 1² ≡ 1)
  (2/3) = -1 (2 is not a square mod 3)

Quadratic reciprocity relates (p/q) and (q/p):
  (p/q)(q/p) = (-1)^((p-1)(q-1)/4)

For p = 3, q = 5:
  (3/5)(5/3) = (-1)^((2×4)/4) = (-1)^2 = 1
""")

for a in range(1, 6):
    print(f"  ({a}/3) = {legendre(a, 3):+d}")

# =============================================================================
# PART 4: THE GAUSSIAN INTEGERS AND Z₄
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: GAUSSIAN INTEGERS AND Z₄")
print("=" * 80)

print("""
GAUSSIAN INTEGERS Z[i]
======================

The Gaussian integers are a + bi where a, b ∈ Z.

The units of Z[i] are {1, -1, i, -i} = Z₄!

This Z₄ appears in W33's phase structure:
  Z₁₂ = Z₄ × Z₃

The Z₄ part encodes:
  - Phase shifts by π/2
  - The 4th roots of unity
  - Quaternionic structure

Prime factorization in Z[i]:
  • 2 = (1+i)(1-i) = -i(1+i)² (ramifies)
  • 3 stays prime (inert)
  • 5 = (2+i)(2-i) (splits)

The fact that 3 stays prime in Z[i] is significant!
It means Z₃ and Z₄ are "independent" - no mixing.
""")


# Gaussian primes
def is_gaussian_prime(a, b):
    """Check if a + bi is a Gaussian prime."""
    n = a * a + b * b  # Norm
    if n == 0:
        return False
    if b == 0:
        return abs(a) % 4 == 3 and is_prime(abs(a))
    if a == 0:
        return abs(b) % 4 == 3 and is_prime(abs(b))
    return is_prime(n)


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


print("\nSmall Gaussian primes (norm < 20):")
for a in range(-4, 5):
    for b in range(-4, 5):
        if is_gaussian_prime(a, b):
            n = a * a + b * b
            if n < 20 and n > 0:
                print(f"  {a:+d}{b:+d}i  (norm = {n})")

# =============================================================================
# PART 5: THE EISENSTEIN INTEGERS AND Z₃
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: EISENSTEIN INTEGERS AND Z₃")
print("=" * 80)

print("""
EISENSTEIN INTEGERS Z[ω]
========================

Let ω = e^(2πi/3) = (-1 + √3 i)/2

The Eisenstein integers are a + bω where a, b ∈ Z.

The units of Z[ω] are {1, -1, ω, -ω, ω², -ω²} ≅ Z₆!

But the 3-torsion is Z₃ = {1, ω, ω²}!

This Z₃ appears in W33's phase structure:
  Z₁₂ = Z₄ × Z₃

The Z₃ part encodes:
  - Phase shifts by 2π/3
  - The cube roots of unity
  - Triality (color!)

Prime factorization in Z[ω]:
  • 2 stays prime (inert)
  • 3 = -ω²(1-ω)² (ramifies!)
  • 7 = (3+ω)(2-ω) (splits)

The fact that 3 ramifies in Z[ω] is KEY!
It means the "3" in W33 is deeply connected to
the Eisenstein integers.
""")

# Cube roots of unity
omega = np.exp(2j * np.pi / 3)
print("\nCube roots of unity:")
for k in range(3):
    w = omega**k
    print(f"  ω^{k} = {w.real:+.4f} {w.imag:+.4f}i")

# =============================================================================
# PART 6: MODULAR FORMS AND W33
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: MODULAR FORMS")
print("=" * 80)

print("""
MODULAR FORMS
=============

A modular form of weight k satisfies:
  f((aτ+b)/(cτ+d)) = (cτ+d)^k f(τ)

for all [a b; c d] ∈ SL₂(Z).

The space M_k of modular forms has dimension:
  dim(M_k) ≈ k/12

For k = 12: dim(M_12) = 2
  Basis: E_4³ and Δ (Ramanujan's delta function)

THE CONNECTION TO W33:
  - |Sp(4,3)| = 51840 = 12 × 4320 = 12 × 2^5 × 3^3 × 5
  - The factor of 12 is the same as in modular forms!
  - Z₁₂ = Z₄ × Z₃ is the phase group

The modular group Γ = PSL₂(Z) acts on the upper half-plane.
Its cusps are at rational points, including 3.

W33 lives over GF(3), which corresponds to the
cusp at 3 in the modular curve X₀(3).
""")

# Ramanujan's tau function (first few values)
# τ(n) is the coefficient of q^n in Δ(τ)
tau = {1: 1, 2: -24, 3: 252, 4: -1472, 5: 4830}

print("\nRamanujan's tau function:")
for n, t in tau.items():
    print(f"  τ({n}) = {t}")

print(f"\nNote: τ(3) = 252 = 4 × 63 = 4 × 9 × 7 = 4 × 3² × 7")
print(f"      The factor of 3² reflects the special role of 3!")

# =============================================================================
# PART 7: THE RIEMANN ZETA FUNCTION
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: RIEMANN ZETA FUNCTION")
print("=" * 80)


def zeta(s, terms=1000):
    """Compute ζ(s) for s > 1."""
    if s <= 1:
        return float("inf")
    return sum(1 / n**s for n in range(1, terms + 1))


print("""
THE RIEMANN ZETA FUNCTION
=========================

ζ(s) = Σ 1/n^s = Π (1 - p^(-s))^(-1)

Special values:
  ζ(2) = π²/6
  ζ(3) = Apéry's constant ≈ 1.202...
  ζ(4) = π⁴/90

The Euler product shows that ζ encodes all primes!

For the prime 3:
  Factor at 3: (1 - 3^(-s))^(-1)

At s = 2: (1 - 1/9)^(-1) = 9/8 = 1.125
""")

print(f"\nζ(2) = {zeta(2):.6f} ≈ π²/6 = {np.pi**2/6:.6f}")
print(f"ζ(3) = {zeta(3):.6f} (Apéry's constant)")
print(f"ζ(4) = {zeta(4):.6f} ≈ π⁴/90 = {np.pi**4/90:.6f}")

# Euler product factor at 3
for s in [2, 3, 4]:
    factor_3 = 1 / (1 - 3 ** (-s))
    print(f"\nEuler factor at 3 for ζ({s}): {factor_3:.6f}")

# =============================================================================
# PART 8: THE 81 AND SPECIAL NUMBERS
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: THE NUMBER 81")
print("=" * 80)

print("""
THE NUMBER 81 = 3⁴
==================

81 appears everywhere in W33:
  - H₁ generators: 81
  - π₁ rank: 81
  - Sylow 3-subgroup order: 81
  - Phase space points: 81
  - Vacuum modes: 81

81 in number theory:
  - 81 = 3⁴ (perfect 4th power of 3)
  - 81 = 80 + 1 = 4 × 20 + 1
  - 80 = |points in W33| × 2 = 2 × 40

Factorizations:
  81 = 1 × 81 = 3 × 27 = 9 × 9

Sum of divisors:
  σ(81) = 1 + 3 + 9 + 27 + 81 = 121 = 11²

Number of divisors:
  τ(81) = 5

Euler's totient:
  φ(81) = 81 × (1 - 1/3) = 54

Carmichael's function:
  λ(81) = 27

These are all related to powers of 3!
""")

# Verify
divisors_81 = [d for d in range(1, 82) if 81 % d == 0]
print(f"\nDivisors of 81: {divisors_81}")
print(f"Sum of divisors: {sum(divisors_81)}")
print(f"Number of divisors: {len(divisors_81)}")

# Euler totient
phi_81 = sum(1 for k in range(1, 82) if np.gcd(k, 81) == 1)
print(f"φ(81) = {phi_81}")

# =============================================================================
# PART 9: W33 AND THE MONSTER
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: CONNECTION TO THE MONSTER GROUP")
print("=" * 80)

print("""
THE MONSTER AND W33
===================

The Monster group M is the largest sporadic simple group:
  |M| ≈ 8 × 10^53

The Monster has deep connections to:
  - Modular functions (moonshine)
  - String theory (24-dimensional)
  - The j-invariant

W33's group Sp(4,3) is much smaller:
  |Sp(4,3)| = 51840

But there's a chain:
  Sp(4,3) ⊂ ... ⊂ larger groups ⊂ ... ⊂ ???

The number 3 appears in Monster moonshine:
  - j(τ) - 744 = q^(-1) + 196884q + ...
  - 196884 = 196883 + 1
  - 196883 is the dimension of the smallest nontrivial
    representation of the Monster!

And 196883 = 47 × 59 × 71 = 3 × 65627 + 2

The factor of 3 keeps appearing!
""")

# J-invariant coefficients
j_coeffs = [1, 744, 196884, 21493760, 864299970]
print("\nFirst few coefficients of j(τ):")
for n, c in enumerate(j_coeffs):
    mod3 = c % 3
    print(f"  c_{n} = {c:>12} ≡ {mod3} (mod 3)")

# =============================================================================
# PART 10: THE GRAND SYNTHESIS
# =============================================================================

print("\n" + "=" * 80)
print("PART 10: THE GRAND SYNTHESIS")
print("=" * 80)

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                       W33 AND NUMBER THEORY: SYNTHESIS                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  THE PRIME 3 IS SPECIAL BECAUSE:                                             ║
║                                                                              ║
║  1. ARITHMETIC:                                                              ║
║     • Smallest odd prime                                                     ║
║     • 3 ≡ 3 (mod 4) → inert in Z[i]                                         ║
║     • 3 ramifies in Z[ω] → connected to cube roots                          ║
║     • 3 divides many special numbers                                         ║
║                                                                              ║
║  2. ALGEBRA:                                                                 ║
║     • GF(3) is the smallest non-binary field                                 ║
║     • Z₁₂ = Z₄ × Z₃ factorizes uniquely                                     ║
║     • Sp(4,3) has order divisible by 81 = 3⁴                                ║
║     • Steinberg dimension = 3⁴                                               ║
║                                                                              ║
║  3. GEOMETRY:                                                                ║
║     • 3 spatial dimensions                                                   ║
║     • W(3,3) is self-dual                                                    ║
║     • Q45 = 45 = 3² × 5 → SU(5)                                             ║
║     • 40 points = 4 × 10 = 4 × (3² + 1)                                     ║
║                                                                              ║
║  4. PHYSICS:                                                                 ║
║     • 3 colors in QCD                                                        ║
║     • 3 generations of particles                                             ║
║     • 3 + 1 spacetime dimensions                                             ║
║     • SU(3) gauge group                                                      ║
║                                                                              ║
║  THE CONCLUSION:                                                             ║
║     The universe is built on 3 because 3 is the                              ║
║     smallest prime with all necessary properties:                            ║
║       - Non-binary (needs structure)                                         ║
║       - Odd (needs asymmetry)                                                ║
║       - Ramifies in cyclotomic fields (needs roots)                          ║
║                                                                              ║
║  W33 = W(3,3) is nature's choice because q = 3 is                           ║
║  the GOLDILOCKS VALUE: not too simple, not too complex.                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("""
FINAL MEDITATION:

  "God made the integers; all else is the work of man."
    - Leopold Kronecker

  Perhaps more precisely:

  "God made the number 3; all physics is the work of W(3,3)."

The prime 3 is the atom of mathematics.
W33 is the atom of physics.
They are the same thing.
""")

print("\n" + "=" * 80)
print("END OF NUMBER THEORY EXPLORATION")
print("=" * 80)
