# PART CCCX — Krein Parameters of W(3,3)

## Overview

Part CCCX computes the **Krein parameters** (also called *dual intersection numbers*) of the
association scheme underlying W(3,3), the unique strongly regular graph SRG(40, 12, 2, 4).

The Krein parameters q_{ij}^k are the structure constants of the **Krein algebra**
(dual Bose-Mesner algebra): when two minimal idempotents E_i and E_j are multiplied
entry-wise (Hadamard product), the result decomposes as a linear combination of all
minimal idempotents E_k with non-negative rational coefficients:

$$E_i \circ E_j = \frac{1}{v} \sum_k q_{ij}^k \, E_k$$

Non-negativity of all Krein parameters is a necessary feasibility condition for an
association scheme (the *Krein condition*), and for W(3,3) all parameters are indeed
non-negative.

## SRG Parameters

| Parameter | Value |
|-----------|-------|
| V (vertices) | 40 |
| K (valency) | 12 |
| LAM | 2 |
| MU | 4 |
| R_EIG (r) | 2 |
| S_EIG (s) | -4 |
| MULT_R (f) | 24 |
| MULT_S (g) | 15 |

## Q Matrix (Dual Eigenvalue Matrix)

The dual eigenvalue matrix Q is derived from inverting the eigenvalue matrix P of the
scheme. For this SRG the 3x3 P matrix is:

```
P = [[1, 12, 27],
     [1,  2, -3],
     [1, -4,  3]]
```

with det(P) = -240, giving:

```
Q = 40 * P^{-1} = [[1,    24,    15  ],
                   [1,     4,    -5  ],
                   [1,  -8/3,   5/3  ]]
```

The columns of Q satisfy weighted orthogonality:

- Weighted sum of column 0: 1 + 12 + 27 = 40 = V
- Weighted sum of column 1: 1*24 + 12*4 + 27*(-8/3) = 0
- Weighted sum of column 2: 1*15 + 12*(-5) + 27*(5/3) = 0

## Krein Parameter Table

Using the exact formula:

$$q_{ij}^k = \frac{1}{m_k \cdot v} \sum_{\alpha=0}^{2} k_\alpha \, Q[\alpha,i] \, Q[\alpha,j] \, Q[\alpha,k]$$

| q_{ij}^k | Value |
|----------|-------|
| q_{11}^0 | 24 (= MULT_R) |
| q_{11}^1 | 44/3 |
| q_{11}^2 | 40/3 |
| q_{12}^0 | 0 (orthogonality) |
| q_{12}^1 | 25/3 |
| q_{12}^2 | 32/3 |
| q_{22}^0 | 15 (= MULT_S) |
| q_{22}^1 | 20/3 |
| q_{22}^2 | 10/3 |

All Krein parameters are non-negative (Krein feasibility condition satisfied).

## Standard Model Encodings

The Krein parameters carry precise Standard Model fingerprints:

| Encoding | Expression |
|----------|-----------|
| q_{11}^1 = 44/3 | Numerator 44 = (ALPHA+1) * EW_GAUGE_4 = 11*4; denominator = GENERATIONS = 3 |
| q_{11}^2 = 40/3 | Numerator 40 = V = ALPHA * EW_GAUGE_4 = 10*4; denominator = GENERATIONS = 3 |
| q_{22}^0 = 15 | MULT_S = ALPHA + GENERATIONS + LAM = 10+3+2 = 15 |
| q_{22}^2 = 10/3 | Numerator = ALPHA = 10; denominator = GENERATIONS = 3 |
| q_{12}^1 = 25/3 | Numerator = (MU+1)^2 = 5^2 = 25; denominator = GENERATIONS = 3 |
| q_{12}^2 = 32/3 | Numerator = 2^(GENERATIONS+LAM) = 2^5 = 32; denominator = GENERATIONS = 3 |
| Sum of 6 non-trivial | 171/3 = 57 = V + MULT_S + LAM = 40+15+2 |
| Common denominator | 3 = GENERATIONS |

## Key Discoveries

1. **Universal denominator**: All non-integer Krein parameters share denominator 3 = GENERATIONS.
   This is a direct consequence of the eigenvalue multiplicities being divisible by 3.

2. **Alpha encoding in q_{22}^2**: The numerator 10 = ALPHA and denominator 3 = GENERATIONS
   reproduce the fine structure constant digit and the generation count simultaneously.

3. **Higgs/gauge encoding in q_{11}^1**: The numerator 44 = (ALPHA+1)*EW_GAUGE_4 interpolates
   between the Higgs quartic coupling count and the EW gauge structure.

4. **Krein sum = V + MULT_S + LAM**: The total of the six non-trivial Krein parameters equals
   57 = 40 + 15 + 2, combining vertex count, second multiplicity, and lambda.

5. **q_{12}^0 = 0**: The vanishing of the cross Krein parameter at k=0 reflects the
   mutual orthogonality of the two non-trivial eigenspaces.

## Checks Summary

- Total checks: 27
- Passed: 27
- Status: PASS

Groups:
1. SRG parameters (5 checks)
2. Q-matrix orthogonality (3 checks)
3. Krein parameter exact values (9 checks)
4. Krein feasibility / non-negativity (1 check)
5. SM encodings (7 checks)
6. Finale: sums and common denominator (2 checks)
