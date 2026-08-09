# Part MCXLV: Walk Inverse Shell Normalization

## Claim Boundary

MCXLV is a finite W33 random-walk inverse theorem. It normalizes the MCXLIII
adjacency Green kernel by the simple random-walk matrix `P = A/12`. The inverse
kernel is signed; it is not a stochastic transition matrix.

## Statement

MCXLIII gave

```text
A^-1 = (6I + 3A - J)/24.
```

For the transition matrix

```text
P = A/12,
```

we therefore get

```text
P^-1 = 12 A^-1,
2P^-1 = 6I + 3A - J.
```

Equivalently,

```text
P(6I + 3A - J) = 2I.
```

## Shell Values

The inverse walk kernel has only three shell values:

```text
diagonal entry = 5/2
adjacent entry = 1
nonedge entry  = -1/2.
```

The row shell identity is

```text
5/2 + 12*1 + 27*(-1/2) = 1.
```

So the normalized inverse sends the MCXLIII floor relation into a unit row-sum
signed kernel:

```text
Delta_sub = (P^-1)_adj / 12 = 1/12.
```

## Raw Moment Ladder

MCXLIV showed that the adjacency Green moments become the floor-scaled integer
ladder `40, 100, 1000`. Under walk normalization, the same ladder becomes raw:

```text
sum(P^-1)    = 40
tr(P^-1)     = 100
||P^-1||_F^2 = 1000.
```

Spectrally, this is the inverse of the walk spectrum

```text
P spectrum    = 1, 1/6, -1/3
P^-1 spectrum = 1, 6, -3,
```

with multiplicities `1, 24, 15`, hence

```text
tr(P^-1)     = 1 + 24*6 + 15*(-3) = 100,
||P^-1||_F^2 = 1 + 24*36 + 15*9   = 1000.
```

## Integer Shell Kernel

The doubled inverse kernel is integral:

```text
2P^-1 shell values = 5, 2, -1,
row sum            = 2,
trace              = 200,
Frobenius square   = 4000.
```

## Artifacts

- Analysis: `analysis/w33_walk_inverse_shell_normalization.py`
- Tests: `tests/test_w33_walk_inverse_shell_normalization.py`
- Data: `data/w33_walk_inverse_shell_normalization.json`
- Result: `PART_MCXLV_walk_inverse_shell_normalization_results.json`
