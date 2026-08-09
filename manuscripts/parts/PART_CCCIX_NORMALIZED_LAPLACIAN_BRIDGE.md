# PART CCCIX — Normalized Laplacian Spectrum of W(3,3)

## Summary

| Item | Value |
|---|---|
| Part | CCCIX |
| Topic | Normalized Laplacian Spectrum of W(3,3) |
| Checks | 27/27 |
| Tests | 37/37 |
| Status | PASS |

## Setup

The normalized Laplacian of a graph G is:

```
L_norm = D^{-1/2} L D^{-1/2} = I - D^{-1/2} A D^{-1/2}
```

For a K-regular graph D = K·I, so the formula reduces to:

```
L_norm = I - A/K
```

The eigenvalues of L_norm are therefore mu_i = 1 − lambda_i/K, where lambda_i are the adjacency eigenvalues.

All computations use exact `fractions.Fraction` arithmetic.

## Eigenvalue Table

| Symbol | Formula | Exact value | Decimal | Mult |
|---|---|---|---|---|
| mu_0 | 1 − K/K | **0** | 0.000 | 1 |
| mu_1 | 1 − R/K = 1 − 2/12 | **5/6** | 0.833 | 24 |
| mu_2 | 1 − S/K = 1 − (−4)/12 | **4/3** | 1.333 | 15 |

Total multiplicity: 1 + 24 + 15 = 40 = V ✓

Ordering: 0 < 5/6 < 1 < 4/3 < 2 (non-bipartite connected graph ✓)

## Spectral Identities

**Trace:**

```
tr(L_norm) = 1·0 + 24·(5/6) + 15·(4/3) = 0 + 20 + 20 = 40 = V
```

**Second moment:**

```
tr(L_norm^2) = tr(I) − 2·tr(A)/K + tr(A^2)/K^2
             = V + 2·EDGES/K^2
             = 40 + 480/144
             = 40 + 10/3
             = 130/3
```

Verified directly: 1·0 + 24·(25/36) + 15·(16/9) = 50/3 + 80/3 = 130/3 ✓

**Spectral gap (Fiedler value):** mu_1 = 5/6

**Largest eigenvalue:** mu_2 = 4/3 < 2 (non-bipartite confirmed)

## SM Encodings via Fraction Components

| Eigenvalue | Part | Value | SM identity |
|---|---|---|---|
| mu_1 = 5/6 | numerator | **5** | MU + 1 = 4 + 1 |
| mu_1 = 5/6 | denominator | **6** | K/2 = 12/2 |
| mu_2 = 4/3 | numerator | **4** | MU = 4 |
| mu_2 = 4/3 | denominator | **3** | GENERATIONS = 3 |
| mu_1 + mu_2 = 13/6 | numerator | **13** | ALPHA + GENERATIONS = 10 + 3 |
| mu_1 + mu_2 = 13/6 | denominator | **6** | K/2 = 6 |
| mu_1 × mu_2 = 10/9 | numerator | **10** | ALPHA = 10 |
| mu_1 × mu_2 = 10/9 | denominator | **9** | V//4 − 1 = 10 − 1 |

## Algebraic and Cheeger Identities

**Trace SM:** tr(L_norm) = V = ALPHA × EW_GAUGE_4 = 10 × 4 = 40

**Fiedler rescaling:** 6 × mu_1 = 5 = MU + 1

**Cheeger lower bound:** h(G) ≥ mu_1/2 = 5/12; numerator = MU+1, denominator = K

**Difference:** mu_2 − mu_1 = 4/3 − 5/6 = 1/2

## Key Discoveries

1. **mu_1 = 5/6 encodes MU+1 and K/2**: The Fiedler eigenvalue has numerator = co-degree + 1 and denominator = half-valency.
2. **mu_2 = 4/3 encodes MU and GENERATIONS**: The largest eigenvalue has numerator = co-degree and denominator = generation count.
3. **mu_1 × mu_2 = 10/9**: Product of non-trivial eigenvalues has numerator = ALPHA, denominator = V//4 − 1.
4. **mu_1 + mu_2 = 13/6**: Sum has numerator = ALPHA + GENERATIONS = 13, denominator = K/2 = 6.
5. **tr(L_norm) = V = ALPHA × EW_GAUGE_4**: The trace identity ties the vertex count to SM parameters as a product.
6. **mu_2 − mu_1 = 1/2**: The gap between the two non-trivial eigenvalues is exactly one half.
7. **6 × mu_1 = MU + 1**: Rescaling the Fiedler value by K/2 returns the co-degree shifted by one.
8. **Cheeger bound 5/12**: Lower bound on edge expansion has numerator = MU+1, denominator = K — co-degree and valency in the same fraction.
