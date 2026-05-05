# PART CCCVIII — Seidel Matrix Spectrum of W(3,3)

## Summary

| Item | Value |
|---|---|
| Part | CCCVIII |
| Topic | Seidel Matrix Spectrum of W(3,3) |
| Checks | 27/27 |
| Tests | 40/40 |
| Status | PASS |

## Setup

The Seidel matrix of a graph G on V vertices is

```
S = J - I - 2A
```

where J is the all-ones matrix, I the identity, and A the adjacency matrix.
Diagonal entries are 0; off-diagonal entries are −1 for adjacent pairs and +1 for non-adjacent pairs.

## Eigenvalue Formulae

Because J acts as (V−1) on the all-ones eigenvector of A and as 0 on every orthogonal eigenvector:

| Seidel eig. | Formula | Value | Mult | Source eigenvector |
|---|---|---|---|---|
| σ_0 | V − 1 − 2K | **15** | 1 | all-ones (K-eigenvector of A) |
| σ_1 | −(1 + 2R) | **−5** | 24 (MULT_R) | R-eigenvectors of A |
| σ_2 | −(1 + 2S) | **7** | 15 (MULT_S) | S-eigenvectors of A |

Total multiplicity: 1 + 24 + 15 = 40 = V ✓

## Spectral Identities

**Trace:**

```
tr(S) = 1·15 + 24·(−5) + 15·7 = 15 − 120 + 105 = 0
```

**Second moment:**

```
tr(S²) = 1·225 + 24·25 + 15·49 = 225 + 600 + 735 = 1560
```

Since all off-diagonal entries of S are ±1, there is an independent formula:

```
tr(S²) = V·(V−1) = 40·39 = 1560  ✓
```

**Eigenvalue–multiplicity reflection:**

```
σ_0 = 15 = MULT_S    (Perron eigenvalue equals the multiplicity of S-eigenvectors)
```

## SM Encodings

| Identity | LHS | Value | RHS |
|---|---|---|---|
| σ_0 = ALPHA+GEN+LAM | 10+3+2 | **15** | fine-structure proxy + generations + triangles |
| σ_1 = −(MU+1) | −(4+1) | **−5** | negative co-degree shifted |
| σ_2 = LAM+MU+1 | 2+4+1 | **7** | triangle + co-degree + 1 |
| σ_2 = K//2+1 | 6+1 | **7** | half-valency plus one |
| tr(S²) = ALPHA·(V−1)·MU | 10·39·4 | **1560** | product of three SRG/SM parameters |

## Key Relationships

| Identity | LHS | Value | RHS |
|---|---|---|---|
| σ_0 − \|σ_1\| | 15−5 | **10** | ALPHA (fine-structure proxy) |
| σ_0 + σ_2 | 15+7 | **22** | 2·(K−1) = line graph valency (CCCVII) |
| σ_0 + \|σ_1\| | 15+5 | **20** | 2·ALPHA |
| σ_2 − \|σ_1\| | 7−5 | **2** | LAM (triangle parameter) |

## Key Discoveries

1. **σ_0 = 15 = ALPHA+GENERATIONS+LAM**: The Seidel Perron eigenvalue encodes the fine-structure proxy, generation count, and SRG triangle parameter in a single sum.
2. **σ_0 = MULT_S = 15**: The Perron eigenvalue equals the multiplicity of the smaller adjacency eigenvalue — a self-referential spectral symmetry.
3. **σ_1 = −5 = −(MU+1)**: The sole negative Seidel eigenvalue is fully determined by the SRG co-degree.
4. **σ_2 = 7 = LAM+MU+1 = K//2+1**: The positive off-Perron eigenvalue is encoded both additively (lambda+mu+1) and via half the valency.
5. **σ_0 + σ_2 = 22 = 2(K−1)**: The sum of the two positive Seidel eigenvalues equals the line graph valency from Part CCCVII, bridging two spectral objects.
6. **tr(S²) = 1560 = ALPHA·(V−1)·MU**: The second Seidel moment encodes the fine-structure proxy, vertex-count-minus-one, and co-degree as a product.
7. **σ_0 − |σ_1| = 10 = ALPHA**: Simple subtraction of Seidel eigenvalue magnitudes returns the fine-structure proxy.
8. **σ_2 − |σ_1| = 2 = LAM**: The difference between the two positive/negative Seidel eigenvalue magnitudes returns the SRG triangle parameter.
