# Part MCXLIV: Green Moment Condition Ladder

## Claim Boundary

MCXLIV is a finite W33 matrix theorem. It takes the MCXLIII Green-kernel
reciprocity and packages the global Green moments and condition numbers forced
by the same corrected floor. It is not a continuum analytic estimate.

## Statement

MCXLIII proved

```text
Delta_sub = 1/12 = (A^-1)_adj = row_sum(A^-1).
```

The global moments of `A^-1` then form an exact floor-scaled ladder:

```text
sum_{i,j} (A^-1)_{ij} = 10/3  = 40 * Delta_sub
tr(A^-1)               = 25/3  = 100 * Delta_sub
||A^-1||_F^2           = 125/18 = 1000 * Delta_sub^2.
```

Thus the Green kernel carries the integer spine

```text
40 -> 100 -> 1000
```

after scaling by `Delta_sub`, `Delta_sub`, and `Delta_sub^2`.

## Moment Reciprocity

The trace-to-total ratio is the same five-halves factor already visible in the
diagonal Green entry:

```text
tr(A^-1) / sum(A^-1) = (25/3) / (10/3) = 5/2.
```

The quadratic Green energy admits two equivalent finite factorizations:

```text
||A^-1||_F^2 = (k - 2) * Delta_sub * tr(A^-1)
             = 10 * (1/12) * (25/3)
             = 125/18,
```

and

```text
||A^-1||_F^2 = (q^2 - 4)^2 * Delta_sub * sum(A^-1)
             = 25 * (1/12) * (10/3)
             = 125/18.
```

## Conditioning Form

The adjacency Frobenius square is

```text
||A||_F^2 = 12^2 + 24*2^2 + 15*4^2 = 480 = 40 / Delta_sub.
```

The spectral condition number is exactly the half-reciprocal of the floor:

```text
cond_2(A) = 12/2 = 6 = 1/(2 Delta_sub).
```

The Frobenius condition square is

```text
cond_F(A)^2 = ||A||_F^2 ||A^-1||_F^2 = 10000/3,
```

so

```text
q * cond_F(A)^2 = 10000 = (tr(A^-1) / Delta_sub)^2.
```

## Artifacts

- Analysis: `analysis/w33_green_moment_condition_ladder.py`
- Tests: `tests/test_w33_green_moment_condition_ladder.py`
- Data: `data/w33_green_moment_condition_ladder.json`
- Result: `PART_MCXLIV_green_moment_condition_ladder_results.json`
