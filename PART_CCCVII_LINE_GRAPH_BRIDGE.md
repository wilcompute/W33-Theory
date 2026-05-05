# PART CCCVII — Line Graph Spectrum of W(3,3)

## Summary

| Item | Value |
|---|---|
| Part | CCCVII |
| Topic | Line Graph Spectrum of W(3,3) |
| Checks | 27/27 |
| Tests | 42/42 |
| Status | PASS |

## Setup

The line graph L(G) of a graph G has the edges of G as its vertices, with two vertices of L(G) adjacent when the corresponding edges of G share an endpoint.

For W(3,3) — srg(40, 12, 2, 4):

```
|V(L(G))| = EDGES           = 240
|E(L(G))| = V·K·(K−1)/2    = 40·66 = 2640
degree(L(G)) = 2·(K−1)     = 22    (L(G) is 22-regular)
```

The spectrum of L(G) follows from the incidence matrix B (n×m), which satisfies `BB^T = A(G) + K·I` and `B^T B = A(L(G)) + 2·I`.

## Line Graph Eigenvalues

Each eigenvalue λ of A(G) produces the eigenvalue `λ + K − 2` in A(L(G)).  The null space of B^T contributes eigenvalue −2 with multiplicity `|E| − |V|`.

| Eigenvalue | Source formula | Value | Multiplicity | SM encoding |
|---|---|---|---|---|
| ℓ_0 | K + K − 2 | **22** | 1 | K + ALPHA = 12+10; equals L_VALENCY |
| ℓ_1 | R + K − 2 | **12** | 24 (= MULT_R) | equals K (SRG valency) |
| ℓ_2 | S + K − 2 | **6** | 15 (= MULT_S) | LAM·GENERATIONS = 2·3 = K//2 |
| ℓ_3 | null(B^T) | **−2** | 200 | (ALPHA//2)·V = 5·40 |

Total multiplicity: 1 + 24 + 15 + 200 = 240 = |V(L(G))| ✓

**Note:** L_EIG_1 = 12 = K — the second-largest eigenvalue of the line graph exactly equals the valency of the original SRG.

## Spectral Identities

**Trace:**

```
tr(A(L)) = 1·22 + 24·12 + 15·6 + 200·(−2)
         = 22 + 288 + 90 − 400 = 0
```

**Second moment:**

```
tr(A(L)²) = 1·484 + 24·144 + 15·36 + 200·4
           = 484 + 3456 + 540 + 800 = 5280
```

Cross-check from edge count (tr(A(L)²) = 2·|E(L)|):

```
2 · 2640 = 5280  ✓
```

SM encodings:

```
5280 = V · K · (K−1)       = 40 · 12 · 11
5280 = 2 · EDGES · (K−1)   = 2 · 240 · 11
```

## SM Encodings

| Identity | LHS | Value | RHS |
|---|---|---|---|
| ℓ_0 = K + ALPHA | 12+10 | **22** | ALPHA = fine-structure proxy |
| ℓ_1 = K | — | **12** | SRG valency equals line eigenvalue |
| ℓ_2 = LAM·GENERATIONS | 2·3 | **6** | also = K//2 |
| MULT_L3 = (ALPHA//2)·V | 5·40 | **200** | half-ALPHA times vertex count |

## SM Finale

| Identity | LHS | Value | RHS |
|---|---|---|---|
| ℓ_0 − ℓ_2 | 22 − 6 | **16** | K + EW_GAUGE_4 = 12+4 |
| ℓ_0 + ℓ_3 | 22 + (−2) | **20** | 2·ALPHA = 2·10 |
| ℓ_1 − \|ℓ_3\| | 12 − 2 | **10** | ALPHA = 10 |

## Key Discoveries

1. **ℓ_0 = K + ALPHA = 22**: The largest line graph eigenvalue (and valency of L(G)) encodes the SRG valency plus the fine-structure proxy ALPHA.
2. **ℓ_1 = K = 12**: The second eigenvalue of the line graph exactly equals the SRG valency — a structural fixed point.
3. **ℓ_2 = LAM·GENERATIONS = 6**: The third eigenvalue encodes the product of the SRG triangle parameter and the generation count, and equals K//2.
4. **MULT_L3 = (ALPHA//2)·V = 200**: The multiplicity of the −2 eigenvalue is exactly half-ALPHA times V.
5. **tr(A(L)²) = V·K·(K−1) = 5280**: The second spectral moment of the line graph has a clean SM encoding involving all three graph parameters.
6. **ℓ_0 − ℓ_2 = 16 = K + EW_GAUGE_4**: Eigenvalue gap recovers the electroweak gauge factor.
7. **ℓ_0 + ℓ_3 = 20 = 2·ALPHA**: Perron eigenvalue plus the null eigenvalue recovers twice the fine-structure proxy.
8. **ℓ_1 − |ℓ_3| = 10 = ALPHA**: The difference between the second eigenvalue and the magnitude of the null eigenvalue returns ALPHA exactly.
