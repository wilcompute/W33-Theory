# Part MCXLIII: Green-Kernel Floor Reciprocity

## Claim Boundary

MCXLIII is a finite W33 adjacency Green-kernel theorem. It extends the
corrected MCXLI/MCXLII substrate floor into the exact inverse of the
SRG(40,12,2,4) adjacency matrix. It does not assert a new continuum proof.

## Statement

For W(3,3), the adjacency matrix has strongly regular parameters

```text
v = 40, k = 12, lambda = 2, mu = 4.
```

The Bose-Mesner reduction gives the exact inverse

```text
A^-1 = I/4 + A/8 - J/24 = (6I + 3A - J)/24.
```

Thus the Green kernel has only three entry values:

```text
diagonal entry = 5/24
adjacent entry = 1/12
nonedge entry  = -1/24.
```

The corrected substrate floor is therefore not only a spectral floor. It is
also the adjacent Green-kernel entry:

```text
Delta_sub = 1/12 = (A^-1)_adj.
```

## Row-Sum Reciprocity

Each row splits as one diagonal position, twelve neighbors, and twenty-seven
nonneighbors:

```text
40 = 1 + 12 + 27.
```

The row sum is

```text
5/24 + 12*(1/12) + 27*(-1/24) = 1/12.
```

So the same floor is also the Green-kernel row sum:

```text
Delta_sub = (A^-1)_adj = row_sum(A^-1) = 1/k.
```

The nonedge Green entry is exactly the negative half-floor,

```text
(A^-1)_nonedge = -Delta_sub/2,
```

while the diagonal Green entry is exactly five halves of the floor,

```text
(A^-1)_diag = (5/2) Delta_sub.
```

## Integer-Scaled Check

Using

```text
A^2 = (k-mu)I + (lambda-mu)A + mu J = 8I - 2A + 4J,
```

we get

```text
A(6I + 3A - J)
  = 6A + 3(8I - 2A + 4J) - 12J
  = 24I.
```

Therefore `24 A^-1 = 6I + 3A - J` exactly.

## Artifacts

- Analysis: `analysis/w33_green_kernel_floor_reciprocity.py`
- Tests: `tests/test_w33_green_kernel_floor_reciprocity.py`
- Data: `data/w33_green_kernel_floor_reciprocity.json`
- Result: `PART_MCXLIII_green_kernel_floor_reciprocity_results.json`
