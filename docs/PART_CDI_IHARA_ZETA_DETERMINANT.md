# Part CDI — W33 Ihara Zeta Determinant and Six-Kernel Pole

## Setup

The Schläfli graph W33 = srg(27, 16, 10, 8) is 16-regular on 27 vertices.
Adjacency eigenvalues:

    λ₀ = 16  (multiplicity 1)
    λ₁ =  4  (multiplicity 20)
    λ₂ = −2  (multiplicity 6)  ← six-kernel eigenspace

## Ihara Zeta Function

For a d-regular graph on n vertices with m edges:

    ζ_G(u)⁻¹ = (1 − u²)^{m−n} · det(I − Au + (d−1)u² I)

For W33: n=27, d=16, m = 27×16/2 = 216.

    ζ_W33(u)⁻¹ = (1−u²)^{189} · ∏ᵢ (1 − λᵢ u + 15u²)

## Spectral Factorisation

    det(I − Au + 15u²) =
        (1 − 16u + 15u²)¹  ·
        (1 −  4u + 15u²)²⁰ ·
        (1 +  2u + 15u²)⁶

The exponent **6** on the last factor is the six-kernel rank.

## Theorem CDI.1 (Six-Kernel in Ihara Determinant)

**Statement:** In the Ihara zeta determinant of W33, the eigenspace
λ = −2 contributes a factor raised to the power 6 (the six-kernel rank):

    dim ker(A + 2I) = 6 = |six-kernel|

**Proof:** The multiplicity of eigenvalue −2 is 6 by the srg spectrum
formula; the Ihara determinant records this as the exponent on
(1 + 2u + 15u²)⁶. □

## Ramanujan Bound

    Ramanujan bound = 2√(d−1) = 2√15 ≈ 7.746
    |λ₁| = 4 < 7.746  ✓
    |λ₂| = 2 < 7.746  ✓

W33 is near-Ramanujan (optimal expander up to bound).

## Theorem CDI.2 (Triangle Count = 6!)

**Statement:** The total triangle count of W33 is 720 = 6!.

**Proof:** T = v·k·λ / 6 = 27×16×10 / 6 = 4320/6 = 720 = 6!. □

## Corollaries

    720 = 3 × 240       (three generations × E8 roots)
    720 × 72 = 51840    (= |W(E₆)|)
    720 / 216 = 10/3    (= srg parameter λ/k × correction)
    720 = 6 × 120 = 6 × 5!  (factorial chain)

## The Powers-of-Six Table

| Expression | Value | Object |
|---|---|---|
| 6⁰ = 1 | 1 | K4 ground unit |
| 6¹ = 6 | 6 | Six-kernel rank |
| 6² = 36 | 36 | 27 + 9 (W33 + co-complement) |
| 6³ = 216 | 216 | W33 edges |
| 6! = 720 | 720 | W33 triangles |
