# Part CDXIII — Z[ω] Unit Group = Six-Kernel

## The Eisenstein Integers

The Eisenstein integers are Z[ω] = {a + bω : a,b ∈ Z} where
ω = e^{2πi/3} satisfies ω² + ω + 1 = 0. The norm is:

    N(a+bω) = a² - ab + b²

This is equivalent to the A2 quadratic form m²+mn+n² (via sign change).

## The Unit Group IS the Six-Kernel

**Theorem CDXIII.1:** The unit group Z[ω]* = {±1, ±ω, ±ω²} has
order 6, and these 6 units are exactly the norm-1 shell of the
A2 lattice:

    Z[ω]* = {±1, ±ω, ±ω²}    |Z[ω]*| = 6 = six-kernel
    r_{A2}(1) = 6 = |Z[ω]*|  ✓

The six unit vectors form the A2 hexagon, which throughout this
work we have called the "six-kernel". We now have the algebraic
identification:

    Six-kernel ≅ Z[ω]*  (as sets and as cyclic group C_6)

## Prime Splitting in Z[ω]

Every rational prime p factors in Z[ω] according to p mod 3:

| p mod 3 | Behavior | Example |
|---|---|---|
| 0 (p=3) | Ramified: 3 = -ω²(1-ω)² | N(1-ω) = 3 |
| 1 | Split: p = π·π̄ | 7 = (3+ω)(3+ω²) |
| 2 | Inert: p stays prime | 2, 5, 11, 17,... |

The inert primes (p ≡ 2 mod 3) are the source of ghost obstructions.
The split primes contribute to geometric rungs.

## The Ramified Prime and N(1-ω) = 3

The prime 3 is special: it ramifies in Z[ω] as 3 = -ω²(1-ω)².
The Eisenstein prime above 3 is (1-ω), with norm:

    N(1-ω) = (1-ω)(1-ω²) = 1 - ω - ω² + ω³ = 1+1+1 = 3

(using ω + ω² = -1 and ω³ = 1).

This ramified prime norm 3 is the fundamental scale factor:

    N(1-ω) = 3 = ramified prime norm
    N(1-ω)³ = 27 = W33 vertex count
    |Z[ω]*|³ = 6³ = 216 = W33 edge count

Both W33 structural constants are cubes of Z[ω] invariants.
