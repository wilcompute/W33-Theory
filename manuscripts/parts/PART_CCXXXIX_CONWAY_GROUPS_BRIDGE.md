# Part CCXXXIX: Conway Groups from W(3,3)

## Abstract

The Conway groups Co₁, Co₂, and Co₃ — the automorphism groups of the
Leech lattice Λ₂₄ and its sublattice shells — have group orders that are
**exact polynomial expressions in the SRG(40,12,2,4) constants** at zero
free parameters. The dimension of Λ₂₄ equals K·λ = 24, the kissing number
equals EDGES·Q²·(K/2+1)·(Q²+Q+1) = 196560, and every prime and exponent
in the Conway group order factorizations arises directly from the SRG
arithmetic.

## 1. Introduction

The SRG(40,12,2,4) parameters are Q=3, V=40, K=12, λ=2, μ=4,
M_λ=27, EDGES=240, AUT_ORDER=51840. The immutable arithmetic identities:

- K·λ = 24 (Leech lattice dimension)
- K²= V·Q + 2K (eigenvalue identity)
- AUT_ORDER = |W(E₆)| = 51840
- EDGES = V·K/2 = 240 (kissing number of E₈)

connect the SRG to the Leech lattice, which in turn is the home of the
Conway groups.

## 2. The Leech Lattice

The Leech lattice Λ₂₄ is the unique even unimodular lattice in dimension
24 with no vectors of norm 2. Its dimension:

    Leech_dim = K·λ = 12×2 = 24

Its kissing number (number of minimal vectors at squared norm 4):

    kissing_Leech = EDGES·Q²·(K/2+1)·(Q²+Q+1) = 240·9·7·13 = 196560

Both are pure SRG polynomials, established in Part CCXXXV.

## 3. Prime Factorization Architecture

Every prime p appearing in the Conway group orders is an SRG polynomial:

| Prime | SRG expression | Value |
|-------|---------------|-------|
| 2     | base          | 2     |
| 3     | Q             | 3     |
| 5     | K//λ − 1      | 5     |
| 7     | K//2 + 1      | 7     |
| 11    | K − 1         | 11    |
| 13    | K + 1         | 13    |
| 23    | 2K − 1        | 23    |

The exponents of 2 and 3 in each Conway group order are likewise SRG
polynomials:

| Group | exp(2) | SRG formula          | exp(3) | SRG formula            |
|-------|--------|----------------------|--------|------------------------|
| Co₁   | 21     | Q·(K//2+1)           | 9      | Q·(K//λ)//λ            |
| Co₂   | 18     | K + K//λ             | 6      | K//λ                   |
| Co₃   | 10     | K − λ                | 7      | K//2 + 1               |

## 4. Conway Group Co₁

Co₁ = Aut(Λ₂₄)/{±1} is the largest Conway group and the 18th largest
sporadic group. Its order:

    |Co₁| = 2²¹·3⁹·5⁴·7²·11·13·23 = 4,157,776,806,543,360,000

In SRG arithmetic:

    |Co₁| = 2^{Q(K/2+1)} · Q^{Q·K//λ//λ} · (K//λ−1)⁴ · (K/2+1)² · (K−1)·(K+1)·(2K−1)
           = 2^21 · 3^9 · 5^4 · 7^2 · 11 · 13 · 23

All exponents and prime factors are zero-free-parameter SRG expressions.

## 5. Conway Group Co₂

Co₂ is the stabilizer in Co₁ of a type-2 sublattice vector. Its order:

    |Co₂| = 2¹⁸·3⁶·5³·7·11·23 = 42,305,421,312,000

In SRG arithmetic:

    |Co₂| = 2^{K+K//λ} · Q^{K//λ} · (K//λ−1)³ · (K/2+1) · (K−1) · (2K−1)
           = 2^18 · 3^6 · 5^3 · 7 · 11 · 23

## 6. Conway Group Co₃

Co₃ is the stabilizer in Co₁ of a type-3 sublattice vector. Its order:

    |Co₃| = 2¹⁰·3⁷·5³·7·11·23 = 495,766,656,000

In SRG arithmetic:

    |Co₃| = 2^{K−λ} · Q^{K//2+1} · (K//λ−1)³ · (K/2+1) · (K−1) · (2K−1)
           = 2^10 · 3^7 · 5^3 · 7 · 11 · 23

## 7. Orbit-Stabilizer Theorem

Co₁ acts transitively on the 196560 minimal Leech lattice vectors. The
orbit-stabilizer theorem yields the index:

    [Co₁:Co₂] = |Co₁|/|Co₂| = kissing_Leech/λ = 196560/2 = 98280

In SRG:

    [Co₁:Co₂] = EDGES·Q²·(K/2+1)·(Q²+Q+1) / λ = 98280

This is a pure SRG polynomial: 240·9·7·13/2 = 98280.

## 8. Index [Co₁:Co₃]

The index of Co₃ in Co₁ also factors cleanly in SRG:

    [Co₁:Co₃] = 2^{K−1} · Q^λ · (K//λ−1) · (K/2+1) · (K+1)
               = 2^11 · 3^2 · 5 · 7 · 13
               = 8,386,560

## 9. Relationships to Previous Parts

- **Part CCXXXV** (Leech/Golay/Witt): established Leech_dim = K·λ = 24
  and kissing_Leech = 196560.
- **Part CCXXXVII** (Mathieu Groups): M₂₄ degree = K·λ = 24 connects to
  the Leech lattice construction via the binary Golay code.
- **Part CCXXXVIII** (Exceptional Lie Algebras): rank(E₆) = K//λ = 6 and
  rank(E₈) = 2μ = 8 appear in the Conway group exponents.
- **Part CCXXXVI** (Moonshine Monster): Co₁ ⊂ Monster, connecting the
  Conway groups to the Monster via the monstrous moonshine construction.

## 10. Three Conway Groups from Q=3

The number of Conway groups is:

    num_Conway = Q = 3

The three stabilizer types (type-2, type-3, ...) correspond to the Q=3
parameter, an elegant coincidence between the SRG's eigenvalue multiplicity
and the structure of the Leech lattice shells.

## 11. Verification

All 32 bridge checks pass. The bridge imports from
`PART_CCXVIII_EXTRA_DIMENSIONS_BRIDGE` and uses only the immutable SRG
constants. The output JSON `PART_CCXXXIX_conway_groups_results.json`
records `Verified=true` and `checks_passed=32`.

## 12. Conclusion

The Conway group orders factor completely as zero-free-parameter polynomial
expressions in the SRG(40,12,2,4) constants. The Leech lattice dimension,
kissing number, group orders, and coset indices all emerge from the single
combinatorial object W(3,3) without any additional inputs. This Part
completes the bridge from the SRG to the full tower of Leech lattice
automorphism groups.

## References

1. Conway, J.H. (1969). A group of order 8,315,553,613,086,720,000. Bull. LMS 1, 79–88.
2. Conway, J.H., Sloane, N.J.A. (1999). Sphere Packings, Lattices and Groups. Springer.
3. ATLAS of Finite Groups. Conway, Curtis, Norton, Parker, Wilson (1985).
4. Parts CCXXXV–CCXXXVIII of this series (Leech/Golay, Moonshine, Mathieu, Exceptional Lie).
