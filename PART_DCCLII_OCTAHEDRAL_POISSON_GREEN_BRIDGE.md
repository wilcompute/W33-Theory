# Part DCCLII — Octahedral Poisson-Green Bridge

## Why this part exists

DCCLI gave the exact spectral-projector decomposition of octahedral heat flow. The next natural step is to invert Laplacian dynamics on mean-zero forcing and get an exact Green/Poisson solver.

## Exact pseudoinverse

From the modal split

```text
L = 4P4 + 6P6,
```

the verifier defines

```text
L+ = (1/4)P4 + (1/6)P6.
```

This is the exact Moore-Penrose pseudoinverse on the octahedral closure phase space.

## Exact identities

The verifier proves:

```text
L L+ = L+ L = I - P0,
```

with `P0` the uniform zero mode. Also:

- rank(`L`) = 5,
- nullity(`L`) = 1,
- `L+` is symmetric,
- `L+ 1 = 0` and `1^T L+ = 0`.

So inversion is exact on the mean-zero subspace and correctly excludes the constant gauge mode.

## Exact Poisson solver

For every tested mean-zero source `b`,

```text
x = L+ b
```

satisfies:

```text
Lx = b,
sum(x) = 0.
```

So the closure phase space now has an exact source-to-field map in zero-mean gauge.

## Meaning

The octahedral closure chain now carries:

- geometric phase space,
- heat semigroup,
- spectral projectors,
- and exact Green/Poisson inversion.

This is the first full finite elliptic solver layer for the closure-time harmonic sector.

## Exact vs conditional

- **Exact:** the octahedral Laplacian has exact pseudoinverse `L+ = (1/4)P4 + (1/6)P6` and exact mean-zero Poisson solutions.
- **Conditional:** interpreting this as a continuum Green operator still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dcclii_octahedral_poisson_green_bridge.py`
- Tests: `tests/test_dcclii_octahedral_poisson_green_bridge.py`
- Data: `data/dcclii_octahedral_poisson_green_bridge.json`
