# Part CCXCIX — Krein Parameters of the W(3,3) Bose-Mesner Algebra

## Summary

| Field | Value |
|-------|-------|
| Part | CCXCIX |
| Checks | 27/27 ✓ |
| Tests | 94/94 ✓ |
| Status | PASS |

## Context

The association scheme of the strongly regular graph W(3,3) = srg(40,12,2,4) is a
2-class Bose–Mesner algebra with basis matrices {A₀ = I, A₁ = W(3,3), A₂ = complement}.
The **first eigenmatrix** P encodes how each adjacency matrix acts on each eigenspace.
Its inverse yields the **second eigenmatrix** Q = v · P⁻¹, from which the
**Krein parameters** q^k_{ij} are derived.

## First Eigenmatrix

```
           A₀   A₁   A₂
E₀  [ 1    12   27 ]    (trivial eigenspace)
E₁  [ 1     2   -3 ]    (r = 2  eigenspace, mult 24)
E₂  [ 1    -4    3 ]    (s = -4 eigenspace, mult 15)
```

- Determinant: det(P) = −240 = −|E(W)|

## Idempotents

The primitive idempotents Eᵢ are recovered from column i of P⁻¹:

```
E₀ = (1/40) I + (1/40) A + (1/40) A₂
E₁ = (3/5)  I + (1/10) A + (−1/15) A₂
E₂ = (3/8)  I + (−1/8) A + (1/24) A₂
```

Each Eᵢ has eigenvalue 1 on its own eigenspace and 0 on the others (verified exactly
using Fraction arithmetic).

## Krein Parameters

The Krein parameters q^k_{ij} are defined by the Hadamard-product decomposition:

> E_i ∘ E_j = (1/v) ∑_k q^k_{ij} E_k

Solved exactly (rational arithmetic) for all pairs:

| Parameter | Exact value | 3 × value |
|-----------|-------------|-----------|
| q⁰₁₁ | 24 | 72 |
| q⁰₁₂ | 0 | 0 |
| q⁰₂₂ | 15 | 45 |
| q¹₁₁ | 44/3 | 44 |
| q¹₁₂ | 25/3 | 25 |
| q¹₂₂ | 20/3 | 20 |
| q²₁₁ | 40/3 | **40 = V** |
| q²₁₂ | 32/3 | 32 |
| q²₂₂ | 10/3 | **10 = α** |

**Krein conditions satisfied**: all q^k_{ij} ≥ 0 ✓

## SM / Combinatorial Identities

| Identity | Equation | Value |
|----------|----------|-------|
| Vertex count | 3 · q²₁₁ = V | 40 |
| Hoffman bound | 3 · q²₂₂ = α | 10 |
| r-multiplicity | q⁰₁₁ = MULT_R | 24 |
| s-multiplicity | q⁰₂₂ = MULT_S | 15 |
| Cross-pair sum | q¹₁₂ + q²₁₂ (×3) = 25 + 32 = 57 | — |
| α + MULT_S | 3 · q¹₁₂ = α + MULT_S | 25 |
| MULT_R + 2·MU | 3 · q²₁₂ = MULT_R + 2·MU | 32 |
| EW³ | 3 · (q¹₁₁ + q¹₂₂) = EW³ | 64 |
| Complement | q¹₁₁ + q²₁₁ = V − K | 28 |
| Hoffman pair | q¹₂₂ + q²₂₂ = α | 10 |

## Relation to Prior Parts

- **CCXCVI** (Hoffman bound α = 10) — 3·q²₂₂ = α confirms the Hoffman bound
  appears directly in the Krein dual algebra.
- **CCXCVII** (Interlacing) — The P matrix rows encode exactly the interlacing
  spectrum {k, r, s} = {12, 2, −4}.
- **CCXCVIII** (Equitable partitions) — The quotient matrix eigenvalues
  {K, R, S} are precisely the columns of P used here.

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCXCIX_KREIN_PARAMETERS_BRIDGE.py` | Bridge (27/27 checks) |
| `tests/test_krein_parameters_ccxcix.py` | Test suite (94/94) |
| `PART_CCXCIX_krein_parameters_results.json` | Machine-readable summary |
| `PART_CCXCIX_KREIN_PARAMETERS_BRIDGE.md` | This document |
