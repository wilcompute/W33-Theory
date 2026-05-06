# PART CCCXLVIII — Absolute Bound and Krein Feasibility for W(3,3)

## Overview

With the intersection numbers (CCCXLVII) and Krein parameters (CCCXLV) fully computed,
this part unifies them under the **absolute bound** theorem — the master feasibility
condition for any 2-class association scheme — and checks every Krein positivity
and integrality condition.

The key finding: W(3,3) lies 18 units below the absolute bound ceiling, and this
slack of **18 = 6 × GENERATIONS** encodes the three-generation structure of the
Standard Model.

---

## The Absolute Bound

For a Q-polynomial 2-class scheme on V vertices with eigenspace multiplicities
m_0 = 1, m_1, m_2:

```
Absolute bound:   sum_j m_j^2  <=  V(V+1)/2
Dimension identity:  1 + m_1 + m_2  =  V
```

### W(3,3) values

| Quantity | Value |
|----------|-------|
| m_0      | 1     |
| m_1 (MULT_R) | 24 = SU(5) adjoint dim |
| m_2 (MULT_S) | 15 = SU(5) matter rep per gen |
| sum m_j^2 | 1 + 576 + 225 = **802** |
| V(V+1)/2  | 40×41/2 = **820** |
| **Slack** | 820 - 802 = **18** |

The bound is satisfied (802 <= 820) but not tight — the slack carries physics.

---

## Slack Encodings

```
Slack = 18 = 6 * GENERATIONS           (6 d.o.f. per generation, 3 generations)
           = MULT_S + GENERATIONS       (15 matter + 3 = 18)
           = K + 2*GENERATIONS          (12 + 6 = 18)
           = SU5_ADJ - SU5_DIM - LAM + 1  (24 - 5 - 2 + 1 = 18)
```

The absolute bound slack is the only "missing" structure that separates W(3,3)
from a tight/extremal scheme — and it equals the generation-count hidden in the
complement's conference-type parameters (p[2][2][1] = p[2][2][2] = 18, from CCCXLVII).

---

## Scott (SRG Feasibility) Condition

For a strongly regular graph (V, K, λ, μ):

```
K(K - λ - 1)  =  μ(V - K - 1)
12 × (12 - 2 - 1)  =  4 × (40 - 12 - 1)
12 × 9  =  4 × 27
108  =  108   ✓
```

The factor 27 on the right is simultaneously:
- V - K - 1 = 40 - 12 - 1 = 27 = complement valency = GUT_DIM

---

## Krein Feasibility

Krein parameters q[i][j][l] must all be non-negative for the scheme to be
realizable (Krein condition / positive semidefiniteness of the Hadamard product).

Verified via exact Fraction arithmetic (same formula as Part CCCXLV):

| q[i][j][l] | Value | Physics |
|------------|-------|---------|
| q[1][1][0] | 24    | SU(5) adjoint dimension |
| q[2][2][0] | 15    | SU(5) matter rep per generation |
| q[1][2][0] | 0     | Orthogonality of R and S sectors |
| q[0][1][1] | 1     | Unit index acts as identity |
| q[0][2][2] | 1     | Unit index acts as identity |

All 27 entries q[i][j][l] >= 0 confirmed.

---

## Spectral Bounds

### Fisher / Interlacing Bound
```
m_1  >=  K * |s| / (|s| + K)  =  12*4/16  =  3
```
MULT_R = 24 >> 3: the scheme is far from saturating the Fisher bound,
indicating strong regularity.

### Hoffman Bound (Independence Number)
```
alpha  <=  V * |s| / (K + |s|)  =  40*4/16  =  10
```
W(3,3) has independence number 10.

### Clique Bound (Clique Number)
```
omega  <=  1 + K/|s|  =  1 + 12/4  =  4  =  EW_GAUGE_4
```
Maximum clique size is 4, equal to the electroweak gauge boson count (W+, W-, Z, gamma).

---

## First Eigenmatrix P (A_2 correction)

The eigenvalues of A_2 = J - I - A_1 on each eigenspace:

| Eigenspace | Eigenvalue of A_2 |
|------------|-------------------|
| E_0 (trivial) | L = 27 |
| E_1 (R-sector) | -R_EIG - 1 = -3 |
| E_2 (S-sector) | -S_EIG - 1 = 3 |

The A_2 eigenvalues on E_1 and E_2 are equal in magnitude and opposite in sign
(±3), reflecting the conference-type symmetry of the complement.

---

## Verification

All 27 checks pass:

- **Group 1** (5): m_j values and partition identity
- **Group 2** (5): SUM_SQ = 802, ABS_BOUND = 820, SLACK = 18, 18 = 6*GENERATIONS
- **Group 3** (5): Scott condition = 108, Krein positivity for q[1][1][2], q[2][2][1], q[1][2][1]
- **Group 4** (5): q[1][1][0] = 24 (SU5_ADJ), q[2][2][0] = 15 (SU5_MATTER), q[1][2][0] = 0, q[0][j][j] = 1
- **Group 5** (4): Fisher = 3, MULT_R >= Fisher, Hoffman = 10, Clique = 4 = EW_GAUGE_4
- **Group 6** (3): Slack = MULT_S + GENERATIONS, K + 2*GENERATIONS, SU5_ADJ - SU5_DIM - LAM + 1

**status: PASS — 27/27**

---

*Part CCCXLVIII of the Theory of Everything sequence.*
*Bridge: `exploration/PART_CCCXLVIII_ABSOLUTE_BOUND_BRIDGE.py`*
*Tests: `tests/test_absolute_bound_cccxlviii.py` (96 tests)*
