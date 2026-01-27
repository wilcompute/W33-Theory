# Exact Fractional Structure in W33 Eigenspace

## Eigenspace Projection Matrix

- Eigenspace dimension: 24
- Projection matrix P = V V^T

### Entry Values

- Diagonal P[i,i]: 0.6000000000 = 3/5
- Adjacent P[i,j]: 0.1000000000 = 1/10
- Non-adjacent P[i,j]: -0.0666666667 = -1/15

### Uniformity Check (variance)

- Diagonal variance: 4.50e-32
- Adjacent variance: 1.24e-32
- Non-adjacent variance: 1.35e-32

**EXACT**: All entries are uniform within each category!

### Common Denominator Representation

Common denominator: 30

| Entry Type | Fraction | Numerator/30 |
|------------|----------|--------------------------|
| Diagonal | 3/5 | 18/30 |
| Adjacent | 1/10 | 3/30 |
| Non-adjacent | -1/15 | -2/30 |

### Projection Property Verification

max|P² - P| = 7.77e-16
✓ P is a valid projection matrix (P² = P)

### Row Sums

Row sum: -0.0000000000
As fraction: 0

## Numerator Analysis

With denominator 30:
- Diagonal: 18
- Adjacent: 3
- Non-adjacent: -2

### Arithmetic Relationships

18 + 12×3 + 27×-2 = 0

(This checks if 1 ⊥ λ=2 eigenspace: should be 0)
✓ Constant vector is orthogonal to λ=2 eigenspace

### Ratio Analysis

Adjacent/Non-adjacent ratio: 3/-2 = -3/2
Diagonal/Adjacent ratio: 18/3 = 6

### Factor Analysis

- 30 = 2 × 3 × 5
- 18 = 2 × 3 × 3
- 3 = 3
- -2 = -2

## Edge Projection Fractions

Edge projection norm²: 1.4000000000 = 7/5

Expected (2×diag + 2×adj): 1.4000000000
Match: True

### Edge-Edge Inner Products

| Inner Product | Fraction | Count |
|---------------|----------|-------|
| -0.266667 | -4/15 | 5400 |
| -0.100000 | -1/10 | 12960 |
| 0.066667 | 1/15 | 7560 |
| 0.400000 | 2/5 | 120 |
| 0.733333 | 11/15 | 2160 |
| 0.900000 | 9/10 | 480 |

## Summary

The λ=2 eigenspace projection matrix has **exact rational entries**:

P[i,j] ∈ {18, 3, -2} / 30

This exact fractional structure is a strong algebraic constraint
suggesting deep number-theoretic properties of W33.

