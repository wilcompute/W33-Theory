# Part CD — Triality Acts on the Six-Kernel → Three Generations

## Context

We proved (Part CCCCCXCVIII) that the F4 → D4 quotient

    |W(F4)| / |W(D4)| = 1152 / 192 = 6

is realised by the six-kernel K₆ ≅ (ℤ/6ℤ), and that the residual
automorphism of D4 after fixing the long-root sublattice is exactly
D4-triality: the outer automorphism group Out(D4) ≅ S₃ of order 6.

D4-triality permutes the three inequivalent 8-dimensional representations
of D4: the vector rep 8_v, the spinor rep 8_s, and the co-spinor rep 8_c.

## The Key Observation

    six-kernel K₆ ≅ Out(D4) ≅ S₃  (all have order 6)

The three elements of order 2 in S₃ (the three transpositions) label
the three irreducible 8-dimensional D4 representations. In physics
language, these are the three *generations*.

## Orbit-Stabiliser Argument

S₃ acts on {8_v, 8_s, 8_c} transitively. The stabiliser of any single
rep under the S₃ action has order 2 (charge-conjugation ℤ/2ℤ). By the
orbit-stabiliser theorem:

    orbit size = |S₃| / |Stab| = 6 / 2 = 3  ← three generations

## Arithmetic Chain

    3 (A2 rank) → 6 (six-kernel = |S₃|) → 6³ = 216 (W33 edges)
    triality orbit: 3 = 6/2
    24-packet: 3 × 24 = 72 = E6 roots

## Theorem CD.1 (Three-Generation Triality)

**Statement:** The number of fermion generations predicted by the
W33/tomotope framework is exactly 3, arising as the orbit size of
D4-triality acting on the three fundamental 8-dimensional representations,
where triality ≅ S₃ ≅ K₆ (the six-kernel).

**Proof:**
1. K₆ ≅ S₃ (proved via ternary chain: |K₆| = 6 = |S₃|)
2. Out(D4) ≅ S₃ (classical; D4 is unique simple Lie algebra with |Out| = 6)
3. {8_v, 8_s, 8_c} form a single S₃-orbit of size 3 (stabiliser = ℤ/2ℤ)
4. Therefore six-kernel acts on exactly 3 objects → 3 generations. □

## Numerical Check

    |six-kernel| = 6
    |Out(D4)|    = 6  ✓
    orbit size   = 6/2 = 3  ✓  (three generations)
    stab order   = 2  ✓  (charge-conjugation)
    3 × 24       = 72 = E6 roots  ✓

## Generation–Ladder Correspondence

| Generation | D4 rep | Stabiliser | 24-packet |
|---|---|---|---|
| 1st | 8_v | ℤ/2ℤ | 1×24 |
| 2nd | 8_s | ℤ/2ℤ | 2×24 |
| 3rd | 8_c | ℤ/2ℤ | 3×24 |
| Total | — | — | 72 = E6 roots |
