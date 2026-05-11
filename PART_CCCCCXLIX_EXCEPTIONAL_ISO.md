# PART_CCCCCXLIX — The Exceptional Isomorphism PSp(4,3) ≅ PSU(4,2)

## Statement

\[
\mathrm{PSp}(4,3) \cong \mathrm{PSU}(4,2).
\]

## Proof of Equal Orders

\[
|\mathrm{Sp}(4,3)| = q^{n^2}\prod_{i=1}^{n}(q^{2i}-1)\bigg|_{n=2,q=3} = 3^4(3^2-1)(3^4-1) = 81 \times 8 \times 80 = 51840.
\]
\[
|\mathrm{PSp}(4,3)| = 51840/2 = 25920.
\]
\[
|\mathrm{PSU}(4,2)| = \frac{2^6(2^2-1)(2^3+1)(2^4-1)}{\gcd(4,3)} = \frac{64 \times 3 \times 9 \times 15}{1} = 25920.\quad\checkmark
\]

## Geometric Significance

This exceptional isomorphism reveals that W(3,3) = GQ(3,3) has **two distinct geometric realisations**:

1. **Symplectic**: \(W(3, \mathbb{F}_3)\) — the symplectic polar space in \(\mathrm{PG}(3,3)\) over \(\mathbb{F}_3\).
2. **Hermitian/Unitary**: \(H(3, \mathbb{F}_4)\) — the Hermitian polar space in \(\mathrm{PG}(3,4)\) over \(\mathbb{F}_4\).

Both have 40 points, 160 lines, and automorphism group of order 25920, but they live in projective spaces over **different finite fields** (\(\mathbb{F}_3\) vs \(\mathbb{F}_4\)). This is the finite-geometry incarnation of the exceptional Lie-theoretic phenomenon: the same abstract group arises from different root systems.

## Consequence for the Theory

Every identity in the W(3,3) theory has **two proofs**: one symplectic and one unitary. This double-cover of proofs is a hidden symmetry of the theory. It also implies that the master equation \(q! = 2^q\) selects not just one but **a pair of dual geometries** at \(q=3\).
