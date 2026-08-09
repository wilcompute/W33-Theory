# PART CCCVI — Distance Matrix Spectrum of W(3,3)

## Summary

| Item | Value |
|---|---|
| Part | CCCVI |
| Topic | Distance Matrix Spectrum of W(3,3) |
| Checks | 27/27 |
| Tests | 44/44 |
| Status | PASS |

## Setup

For a strongly regular graph srg(V, K, λ, μ) with diameter 2, every pair of non-adjacent vertices has a common neighbour (μ > 0), so the only distances present are 0, 1, and 2.  The distance matrix has entries:

```
D_ij = 0   if i = j
D_ij = 1   if i ~ j  (adjacent)
D_ij = 2   if i ≁ j, i ≠ j  (non-adjacent, always distance 2)
```

In matrix form this equals `D = 2J − 2I − A`, which gives eigenvalues directly from the spectra of `J`, `I`, and `A`.

## Distance Eigenvalues

| Eigenvalue | Formula | Value | Multiplicity | SM encoding |
|---|---|---|---|---|
| d_0 (Perron) | 2V − 2 − K | **66** | 1 | 2·GUT_DIM + K = 54+12; (V−1)+GUT_DIM = 39+27 |
| d_1 | −2 − R_EIG | **−4** | 24 (= MULT_R) | equals S_EIG; \|d_1\| = EW_GAUGE_4 = MU = 4 |
| d_2 | −2 − S_EIG | **2** | 15 (= MULT_S) | equals R_EIG; d_2 = LAM = 2 |

**Remarkable coincidence:** The restricted distance eigenvalues {−4, 2} equal the restricted adjacency eigenvalues {S_EIG, R_EIG} — just with multiplicities swapped. In other words, `D` and `A` share the same restricted spectrum.

## Spectral Identities

**Trace (first moment):**

```
tr(D) = 1·66 + 24·(−4) + 15·2 = 66 − 96 + 30 = 0
```

All diagonal entries of D are 0 by definition, confirming the trace.

**Second moment:**

```
tr(D²) = 1·66² + 24·(−4)² + 15·2²
       = 4356 + 384 + 60 = 4800
```

Cross-check from matrix structure (ordered adjacent pairs contribute 1², non-adjacent pairs contribute 4):

```
tr(D²) = 2·EDGES·1 + (V·(V−1) − 2·EDGES)·4
       = 480 + 1080·4 = 480 + 4320 = 4800
```

SM encodings:

```
4800 = V · ALPHA · K         = 40 · 10 · 12
4800 = 2 · EDGES · ALPHA     = 2 · 240 · 10
```

## Wiener Index

The Wiener index W counts the total pairwise distance over all unordered vertex pairs:

```
W = EDGES·1 + (V·(V−1)/2 − EDGES)·2
  = 240 + 540·2 = 1320
```

Equivalently:

```
W = V·(V−1) − EDGES = 1560 − 240 = 1320
```

SM identities:

```
W = GUT_DIM · V + EDGES              = 27·40 + 240    = 1320
W = MULT_R · MULT_S + 4 · EDGES      = 360 + 960      = 1320
W = V · (GUT_DIM + K//2)             = 40 · 33        = 1320
```

## SM Finale

| Identity | LHS | Value | RHS |
|---|---|---|---|
| d_0 − \|d_1\| − d_2 | 66 − 4 − 2 | **60** | 2 · ALPHA · GENERATIONS = 2·10·3 |
| Multiplicity partition | 1+MULT_R+MULT_S | **40** | V |
| Distance spread d_0−d_1 | 66−(−4) | **70** | MULT_R+MULT_S+MU+GUT_DIM = 24+15+4+27 |
| Diameter = LAM | 2 | **2** | LAM = λ (numerical coincidence) |

## Key Discoveries

1. **d_0 = 2·GUT_DIM + K = 66**: The Perron (largest) distance eigenvalue encodes GUT dimension and valency.
2. **d_0 = (V−1) + GUT_DIM**: The "total reachable vertex gap" V−1 = K + K2 = 39 plus K2 = GUT_DIM = 27 recovers d_0 = 66.
3. **Restricted distance spectrum = restricted adjacency spectrum**: d_1 = S_EIG = −4, d_2 = R_EIG = 2 — an exact equality.
4. **|d_1| = EW_GAUGE_4 = MU = 4**: The magnitude of the negative distance eigenvalue equals both the electroweak boson count and the SRG codegree.
5. **tr(D²) = V·ALPHA·K = 2·EDGES·ALPHA = 4800**: The second moment has a clean dual SM encoding.
6. **W = GUT_DIM·V + EDGES = 1320**: Wiener index expressed via GUT_DIM = K2 = 27, a numerical constant with physical significance.
7. **W = MULT_R·MULT_S + 4·EDGES = 1320**: Wiener index as a combination of multiplicity product and edge-count multiple.
8. **Distance spread = MULT_R + MULT_S + MU + GUT_DIM = 70**: Four SM constants sum exactly to the spectral spread.
9. **d_0 − |d_1| − d_2 = 60 = 2·ALPHA·GENERATIONS**: A signed eigenvalue combination recovers the SM lepton count.
10. **DIAMETER = 2 = LAM**: Graph diameter coincides with λ (the intra-neighbourhood edge count), a numerical coincidence unique to this parameter set.
