# Part CCCXCVII: Distance-Regular Algebra and Root System Crosswalk

## Summary

W(3,3) is a diameter-2 distance-regular graph (DRG) with intersection array
**{12, 9 ; 1, 4}**.  This part builds the complete adjacency algebra from that
array — intersection parameters, eigenpolynomial family, second adjacency matrix —
and verifies 27 numerical identities that connect graph combinatorics to
Standard-Model representation theory.

**Verification: 27 / 27 checks PASS**

## Intersection Array

| Symbol | Formula | Value |
|--------|---------|-------|
| b₀ | K | 12 |
| b₁ | K − 1 − λ | 9 |
| c₁ | (always 1) | 1 |
| c₂ | μ | 4 |
| a₁ | K − b₁ − c₁ | 2 = λ |
| a₂ | K − c₂ | 8 |

## Eigenvalue Quadratic

Both restricted eigenvalues r = 2 and s = −4 satisfy:

```
x² − (λ − μ) x − (k − μ) = 0
x² + 2x − 8 = (x − 2)(x + 4) = 0
```

Key consequences:

| Identity | Value |
|----------|-------|
| r + s = λ − μ | −2 |
| r · s = −(k − μ) | −8 |
| Δ = (λ−μ)² + 4(k−μ) | **36 = 6²** (perfect square) |

## Second Adjacency Matrix A₂ = J − I − A

The distance-2 adjacency matrix inherits eigenvalues:

| Eigenspace | A eigenvalue | A₂ eigenvalue | Multiplicity |
|------------|-------------|---------------|-------------|
| all-ones   | K = 12      | V−1−K = **27** | 1 |
| R-space    | r = 2       | −3 | 24 |
| S-space    | s = −4      | +3 | 15 |

Weighted sum check: 27 + 24·(−3) + 15·3 = 27 − 72 + 45 = **0** ✓

## Standard-Model Crosswalk

| Graph identity | Numerical value | SM anchor |
|----------------|-----------------|-----------|
| V − 1 − K = 27 | **27** | E6 fundamental representation dim |
| K − r = 10 | **10 = α** | Hoffman independence number |
| K − s = 16 = 4² | **16** | EW₄² (electroweak boson count squared) |
| α·(K−s) = V·μ | **160** | 160 = 40 × 4 |
| mult R = 24 | **24** | SU(5) adjoint dimension |
| mult S = 15 | **15** | SU(5) matter representation |
| mult R + mult S = 39 | **39 = V − 1** | degrees-of-freedom counting |
| A₂ top eig = 3 × b₁ = 27 | **27** | GENERATIONS × b₁ = 3 × 9 |

## Characteristic Polynomial

The minimal polynomial of A over the rationals is:

```
(λ − 12)(λ − 2)(λ + 4) = λ³ − 10λ² − 32λ + 96
```

Checks: trace(A²) = 144 + 96 + 240 = **480 = 2 × EDGES** ✓, trace(A) = **0** ✓.

## Discoveries

1. The intersection array {12, 9; 1, 4} completely encodes W(3,3) geometry.
2. A₂ eigenvalue V−1−K = 27 = GUT_DIM bridges graph distance to the E6 fundamental representation.
3. The restricted eigenvalue discriminant Δ = 36 = 6² is a perfect square.
4. Multiplicities (24, 15) match SU(5) adjoint and matter representations exactly.
5. K − r = 10 = α and α(K−s) = V·μ = 160 link the Hoffman bound to SM constants.
6. The top A₂ eigenvalue 27 = GENERATIONS × b₁ = 3 × 9 ties SM families to intersection geometry.
