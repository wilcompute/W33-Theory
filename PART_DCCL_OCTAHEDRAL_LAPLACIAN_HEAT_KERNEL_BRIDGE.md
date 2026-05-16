# Part DCCL — Octahedral Laplacian / Heat-Kernel Bridge

## Why this part exists

DCCXLIX identified the closure clock phase space with the octahedron (6 vertices, 12 edges, 8 faces). This part adds the exact harmonic/diffusive dynamics of that same phase space.

## Exact graph operator

Let `A` be the octahedron adjacency matrix and `L = D - A` its graph Laplacian.

The verifier proves:

- `|V| = 6`, `|E| = 12`, regular degree `4`,
- Laplacian spectrum is exactly

```text
0, 4, 4, 4, 6, 6,
```

- triangle count is exactly `8`.

Since octahedron triangles are its faces, this recovers the same 8-mode count already seen in DCCXLIX.

## Exact heat-kernel dynamics

Define

```text
K_t = exp(-tL).
```

For sample times `t = 0, 1/2, 1, 2`, the verifier proves:

- `K_t` is symmetric,
- `K_t` has nonnegative entries,
- each row sums to `1` (stochastic normalization),
- `K_0 = I`.

So the octahedral closure phase space carries a finite exact diffusion law.

## Bridge back to closure clock

The verifier checks that octahedral phase-space size matches closure levels:

```text
|V| = 6 = nilpotence index of the closure generator.
```

So the geometric octahedron and the operator chain share the same finite horizon.

## Meaning

The closure chain now has three synchronized layers:

- **operator layer:** generator, resolvent, jets, Ward/Green structure,
- **geometric layer:** octahedron phase space,
- **harmonic layer:** exact Laplacian spectrum and heat-kernel flow.

This is the first exact spectral-diffusive dynamics bridge on the octahedral closure phase space.

## Exact vs conditional

- **Exact:** the octahedral closure phase space has exact Laplacian spectrum `(0,4,4,4,6,6)` and exact stochastic symmetric heat-kernel dynamics.
- **Conditional:** interpreting this as continuum spacetime diffusion still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dccl_octahedral_laplacian_heat_kernel_bridge.py`
- Tests: `tests/test_dccl_octahedral_laplacian_heat_kernel_bridge.py`
- Data: `data/dccl_octahedral_laplacian_heat_kernel_bridge.json`
