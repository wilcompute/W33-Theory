# Part DCCLV — Octahedral Transition-Mixing Bridge

## Why this part exists

DCCLIV established exact commute and hitting times. The next natural step is an exact step-by-step mixing law for the same octahedral random walk.

## Exact transition spectrum

For octahedral Laplacian `L`, define random-walk transition operator

```text
P = I - L/4.
```

Using DCCLI projectors, the verifier proves transition spectrum

```text
{1, 0, 0, 0, -1/2, -1/2}.
```

So only one decaying mode family survives after one step.

## Exact power formula

For all `t >= 1`,

```text
P^t = P0 + (-1/2)^t P6.
```

The `P4` mode is annihilated immediately (`P P4 = 0`), so mixing is controlled exactly by the `-1/2` mode pair.

## Exact mixing law

With uniform stationary distribution `pi = (1/6,...,1/6)`, the verifier proves:

- total-variation distance is the same from every starting vertex,
- TV distance decays by exact factor `1/2` per step,
- the full TV profile matches a closed geometric form.

So closure random-walk relaxation is not merely bounded by spectral gap; it is exactly solved by the projector decomposition.

## Meaning

The octahedral closure chain now has:

- resistance and hitting/commute times,
- and exact finite-time convergence-to-equilibrium law.

This is the cleanest exact mixing theorem so far on closure phase-space dynamics.

## Exact vs conditional

- **Exact:** octahedral transition powers satisfy `P^t = P0 + (-1/2)^t P6` and TV contracts exactly by factor `1/2` per step.
- **Conditional:** interpreting this as continuum relaxation/mixing requires a scaling limit.

## Executable artifact

- Verifier: `verify_dcclv_octahedral_transition_mixing_bridge.py`
- Tests: `tests/test_dcclv_octahedral_transition_mixing_bridge.py`
- Data: `data/dcclv_octahedral_transition_mixing_bridge.json`
