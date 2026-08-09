# Part DCCLI — Octahedral Spectral-Projector Semigroup Bridge

## Why this part exists

DCCL gave the octahedral Laplacian and heat-kernel dynamics. This part expresses that same dynamics in exact modal/projector form.

## Exact projector formulas

For octahedral Laplacian `L` with spectrum `(0,4,4,4,6,6)`, define

```text
P0 = (L-4I)(L-6I)/24,
P4 = L(6I-L)/8,
P6 = L(L-4I)/12.
```

The verifier proves:

- `P0 + P4 + P6 = I`,
- `Pk^2 = Pk`,
- `Pk Pm = 0` for `k != m`,
- rank multiplicities are exactly `(1,3,2)`.

So these are the exact spectral projectors of the octahedral closure phase space.

## Exact semigroup decomposition

The heat kernel satisfies

```text
K_t = exp(-tL) = P0 + e^{-4t} P4 + e^{-6t} P6.
```

The verifier checks this decomposition exactly against direct heat kernels at sampled times `t = 0, 1/2, 1, 2`.

## Structural consequences

- `P0` is exactly the uniform mode projector (`1/6` all-ones matrix),
- `L = 4P4 + 6P6`,
- the spectral gap is exactly `4`.

So the closure diffusion on octahedral phase space has a complete exact mode split: one steady mode, three medium-decay modes (`e^{-4t}`), and two fast-decay modes (`e^{-6t}`).

## Meaning

The closure chain now has:

- geometric phase-space identification (DCCXLIX),
- Laplacian/heat dynamics (DCCL),
- and exact spectral-projector semigroup decomposition (this part).

This is the cleanest finite harmonic mode decomposition of the closure-time phase space so far.

## Exact vs conditional

- **Exact:** octahedral closure heat flow decomposes exactly as `K_t=P0+e^{-4t}P4+e^{-6t}P6`.
- **Conditional:** continuum harmonic-mode interpretation still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dccli_octahedral_spectral_projector_semigroup_bridge.py`
- Tests: `tests/test_dccli_octahedral_spectral_projector_semigroup_bridge.py`
- Data: `data/dccli_octahedral_spectral_projector_semigroup_bridge.json`
