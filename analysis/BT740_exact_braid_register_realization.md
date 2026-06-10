# BT740 — Exact Braid Realization of K33 Register Moves

Closes the BT704/BT707 boundary: "the final generator-respecting lift test
must still compare local rectangle moves to selected Levi-lift braid words."

## The resolution

The obstruction was in the ENCODING, not the functor.  A rectangle move on
the K33 cycle register is a bit-flip; in the computational basis that is X,
and Fibonacci braids cannot realize X exactly (T7: 6172 projective words of
length <= 10, none within 0.159 of X).  But in the anyonic Fibonacci
representation, with zeta = e^{i pi/5}:

```text
sigma_1 = diag(zeta^4, -zeta^2)
sigma_1^5  = diag(1, -1) = Z     EXACTLY (not just projectively)
sigma_1^10 = I                   EXACTLY
```

Choosing the dual (+-) encoding of each cycle bit makes Z the bit-flip.  The
register functor

```text
Phi : H_1(K33; F2) = F2^4 -> U(16),   Phi(e_i) = sigma_1^5 on block i
```

is an exact linear group homomorphism (T6: all 256 products, faithful,
image order 16).  Rectangle moves compose by homology XOR; their braid
words compose by matrix product; Phi intertwines them exactly.

## Exact arithmetic

Conjugating by diag(1, sqrt(phi)) removes all sqrt(phi) entries:

```text
F' = [[phi-1, phi-1], [1, -(phi-1)]],   F'^2 = I,   sigma_2 = F' sigma_1 F'
```

Everything lives in Q(zeta_10); all of T1-T4 are verified by exact
polynomial arithmetic mod Phi_10(z) = z^4 - z^3 + z^2 - z + 1 over Q.
No floating point.

## The one-block exact gate group

```text
sigma_2^5 = F' Z F'                  (T3, exact)
tr(Z sigma_2^5) = 6 - 4 phi          (T4, exact)
cos(rotation angle) = 3 - 2 phi = -phi^{-3}
```

The quadratic-irrational cosines of rational multiples of pi have conductor
n with euler_phi(n) = 4 (n in {5, 8, 10, 12}); the Q(sqrt5)-valued ones are
exactly {+-phi/2, +-(phi-1)/2}.  Since 3 - 2 phi equals none of them (exact
comparison), the rotation Z·sigma_2^5 has infinite order:

```text
<Z, F'ZF'> = infinite dihedral group.
```

This is the same golden-ratio irrationality mechanism that makes the
BC helix aperiodic (BT485 T2): the substrate protects the gate group from
collapsing to a finite group, and protects the helix from closing, by one
and the same number-theoretic fact.

## Chart structure carried to braid words

The 9 rectangles of a local K33 chart have homology classes of weights
{1: 4, 2: 4, 4: 1} in the chord basis (T5); the remaining 6 nonzero classes
are the weight-6 hexagons (16 = 1 + 9 + 6 code states).  Braid word lengths:

```text
5 * weight in {5, 10, 20}.
```

## Substrate consequences (derived, not matched)

- bit-flip braid word length 5 = F_5
- sigma^10 = 1 with 10 = Phi_4
- exact gate group order 16 = register dimension
- infinite-dihedral protection = BC-helix aperiodicity mechanism (BT485)

## Boundary

The functor realizes the register moves exactly; it does not claim the full
local braid group action on the 16-dim register is finite (it is not: each
block's image is dense in PU(2)).  Open: lift Phi from rectangle classes to
the BT718-selected cycles themselves (cycle-level rather than
homology-level), and connect the infinite dihedral one-block group to the
Levi cycle holonomy of BT535.
