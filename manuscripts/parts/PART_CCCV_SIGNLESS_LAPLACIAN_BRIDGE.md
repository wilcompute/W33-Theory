# PART CCCV — Signless Laplacian Spectrum of W(3,3)

## Summary

| Metric | Value |
|--------|-------|
| Graph | W(3,3) strongly regular (40, 12, 2, 4) |
| Checks | 27 / 27 |
| Tests | 44 / 44 |
| Status | PASS |

## Definition

For any graph the **signless Laplacian** is

```
Q = D + A
```

where D is the diagonal degree matrix and A is the adjacency matrix.
For a K-regular graph D = K·I, so

```
Q = K·I + A
```

and the eigenvalues of Q are simply the adjacency eigenvalues shifted up by K.

## Adjacency Spectrum of W(3,3)

| Eigenvalue | Value | Multiplicity |
|------------|-------|-------------|
| μ₀ = K    | 12    | 1           |
| μ₁ = R    | 2     | 24          |
| μ₂ = S    | −4    | 15          |

## Signless Laplacian Spectrum

| Q-eigenvalue | Value | Multiplicity | Formula |
|-------------|-------|-------------|---------|
| q₀          | 24    | 1           | K + K = 2K |
| q₁          | 14    | 24          | K + R = 12 + 2 |
| q₂          | 8     | 15          | K + S = 12 − 4 |

### Key identities for eigenvalues

```
q₀ = 24 = MULT_R          (spectral radius = restricted-eigenvalue multiplicity)
q₀ = 24 = 2·ALPHA + EW    (= 2×10 + 4, SM encoding)
q₁ = 14 = GUT_DIM − K − 1 (= 27 − 12 − 1)
q₂ = 8  = 2·EW            (= 2×4)
q₂ = 8  = MU + EW         (= 4 + 4)
q₂ = 8  = K − EW          (= 12 − 4)
```

## Spectral Identities

### Trace identity (sum with multiplicities)

```
Σ qᵢ (weighted) = 2·|E| = 2 × 240 = 480
```

This is the standard identity: the sum of all signless Laplacian eigenvalues equals twice the number of edges.

### Second moment identity

```
tr(Q²) = Σ qᵢ² (weighted)
       = 1·576 + 24·196 + 15·64
       = 576 + 4704 + 960
       = 6240
       = V·K·(K+1) = 40·12·13
```

This is a known identity for K-regular graphs.

### Distinct eigenvalue sums

```
q₀ + q₁ + q₂ = 24 + 14 + 8 = 46 = 4K + R + S
```

### Eigenvalue gaps

```
q₀ − q₁ = 10 = ALPHA
q₁ − q₂ = 6  = K/2
q₀ − q₂ = 16 = K + EW_GAUGE_4
```

## Signless Laplacian Energy

The Q-energy is defined relative to the average eigenvalue 2|E|/V = K = 12:

```
QLE = Σ |qᵢ − K| (weighted)
    = |24−12| + 24·|14−12| + 15·|8−12|
    = 12 + 48 + 60
    = 120
```

Three simultaneous SM encodings:

```
QLE = 120 = EDGES / 2 = 240 / 2
QLE = 120 = K·V / EW_GAUGE_4 = 12·40 / 4
```

## Bipartiteness

Since q₂ = 8 > 0, the signless Laplacian has no zero eigenvalue, confirming W(3,3) is **not bipartite** (as expected: λ = 2 > 0 means triangles exist).

## SM Encoding Table

| Quantity | Value | SM Interpretation |
|---------|-------|------------------|
| q₀ = MULT_R | 24 | Restricted eigenmultiplicity coincides with Q spectral radius |
| q₀ = 2·ALPHA + EW | 24 | Fine-structure analogue and EW-gauge factor |
| q₁ = GUT_DIM − K − 1 | 14 | GUT dimension encodes second Q-eigenvalue |
| q₂ = 2·EW | 8 | Twice the EW-gauge number |
| q₂ = MU + EW | 8 | Sum of co-degree and EW factor |
| QLE = K·V / EW | 120 | Energy encodes valency, vertex count, EW factor |
| q₀ − q₁ = ALPHA | 10 | Eigenvalue gap is fine-structure analogue |

## Files

| File | Description |
|------|-------------|
| `exploration/PART_CCCV_SIGNLESS_LAPLACIAN_BRIDGE.py` | Bridge (27/27 checks) |
| `tests/test_signless_laplacian_cccv.py` | Test suite (44/44 pass) |
| `PART_CCCV_signless_laplacian_results.json` | JSON summary |
| `PART_CCCV_SIGNLESS_LAPLACIAN_BRIDGE.md` | This document |
