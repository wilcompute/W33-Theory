# Part MCXLVI: Poisson-Kemeny Green Kernel

## Claim Boundary

MCXLVI is a finite W33 Markov-chain theorem. It computes the exact Poisson
kernel of the random walk `P = A/12`, extracts Kemeny's constant, and turns the
older random-walk hitting and resistance facts into exact shell values. It is
not a continuum stochastic-process limit.

## Poisson Kernel

Let

```text
P  = A/12,
Pi = J/40,
Z  = (I - P + Pi)^-1.
```

The walk spectrum is

```text
1, 1/6, -1/3
```

with multiplicities `1, 24, 15`, so `Z` has eigenvalues

```text
1, 6/5, 3/4.
```

In the Bose-Mesner basis,

```text
Z = 21I/20 + 3A/40 - 19J/800.
```

Therefore its shell entries are

```text
Z_diag = 821/800,
Z_adj  = 41/800,
Z_non  = -19/800,
```

with row sum `1`.

## Centered Kernel

Subtracting the stationary projector gives

```text
Z - Pi = 21I/20 + 3A/40 - 39J/800.
```

The centered entries are

```text
(Z-Pi)_diag = 801/800,
(Z-Pi)_adj  = 21/800,
(Z-Pi)_non  = -39/800.
```

The row sum is zero:

```text
801/800 + 12*(21/800) + 27*(-39/800) = 0.
```

## Kemeny Constant

Kemeny's constant is the nontrivial trace:

```text
K = 24*(6/5) + 15*(3/4) = 801/20.
```

It appears on the centered diagonal per vertex:

```text
(Z-Pi)_diag = K/40 = 801/800.
```

## Hitting And Resistance Shells

For the uniform stationary distribution, the hitting-time formula is

```text
H_ij = 40 * (Z_jj - Z_ij).
```

Thus

```text
H_adj = 40*(821/800 - 41/800)  = 39,
H_non = 40*(821/800 - -19/800) = 42.
```

The nonedge hitting time exceeds the adjacent hitting time by exactly `q = 3`.

The commute times and effective resistances are

```text
C_adj = 78,  R_adj = 78/(2*240) = 13/80,
C_non = 84,  R_non = 84/(2*240) = 7/40.
```

Counting `240` adjacent pairs and `540` nonedge pairs gives the Kirchhoff index

```text
240*(13/80) + 540*(7/40) = 267/2.
```

## Artifacts

- Analysis: `analysis/w33_poisson_kemeny_green_kernel.py`
- Tests: `tests/test_w33_poisson_kemeny_green_kernel.py`
- Data: `data/w33_poisson_kemeny_green_kernel.json`
- Result: `PART_MCXLVI_poisson_kemeny_green_kernel_results.json`
