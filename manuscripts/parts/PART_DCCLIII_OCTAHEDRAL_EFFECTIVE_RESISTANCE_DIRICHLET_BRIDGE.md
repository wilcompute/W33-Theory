# Part DCCLIII — Octahedral Effective-Resistance / Dirichlet Bridge

## Why this part exists

DCCLII gave the exact octahedral Green/Poisson solver `L+`. The next natural step is to extract the induced resistance geometry and energy law.

## Exact resistance law

With Laplacian pseudoinverse `L+`, define

```text
R_ij = L+_ii + L+_jj - 2L+_ij.
```

The verifier proves the octahedron has exactly two resistance orbits:

- adjacent pairs (12 total):

  ```text
  R_adj = 5/12,
  ```

- antipodal pairs (3 total):

  ```text
  R_opp = 1/2.
  ```

So the closure phase-space resistance geometry is fully explicit.

## Kirchhoff index

The verifier proves

```text
Kf = sum_{i<j} R_ij = 13/2,
```

and matches it with the trace identity

```text
Kf = n * tr(L+).
```

## Exact Dirichlet dipole identity

For dipole source `b = e_i - e_j`, with `x = L+ b`, the verifier proves:

```text
Lx = b,
x^T L x = b^T x = R_ij,
sum(x) = 0.
```

So energy, work, and effective resistance are exactly identical on the closure phase space in zero-mean gauge.

## Meaning

The octahedral closure chain now has:

- spectral semigroup,
- Green/Poisson inversion,
- and exact resistance-energy geometry.

This is the cleanest finite elliptic/energy bridge so far between closure dynamics and measurable network geometry.

## Exact vs conditional

- **Exact:** octahedral closure phase space has exact two-orbit effective resistance and exact dipole Dirichlet identity.
- **Conditional:** interpreting this as continuum resistance/field geometry still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dccliii_octahedral_effective_resistance_dirichlet_bridge.py`
- Tests: `tests/test_dccliii_octahedral_effective_resistance_dirichlet_bridge.py`
- Data: `data/dccliii_octahedral_effective_resistance_dirichlet_bridge.json`
