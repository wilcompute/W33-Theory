# Part DCCXXXIII — Spatial-Closure / Time Bridge

## Why this part exists

DCCXXX gave the literal Clifford-even basis

```text
{1, B23, B31, B12}
```

and DCCXXXI–DCCXXXII gave the closure clock and codec flow

```text
tau_n,    C_n = 12 * 2^{tau_n}.
```

This part makes the `3 + 1` reading executable:

- the three bivectors `B23, B31, B12` are the spatial triad,
- the fourth channel is not another spatial axis,
- it is the scalar closure clock, equivalently the logarithm of codec scale.

## Exact statement

Define time by

```text
tau_n = log2(C_n / 12).
```

Since DCCXXXII already proves

```text
C_n = 12 * 2^{tau_n},
```

it follows identically that

```text
log2(C_n / 12) = tau_n.
```

So the state splits as

```text
(B23, B31, B12 ; tau)
```

with dimensions

```text
3 + 1 = 4.
```

## Meaning

This is the cleanest disciplined reading of the user's geometric intuition:

- three independent Clifford bivectors encode the 3D spatial rotational channels,
- loop closure generates a fourth scalar update channel,
- that scalar is exactly the discrete clock driving the codec doubling flow.

So the fourth coordinate is **closure-generated time**, not a copied spatial direction.

## What is proved exactly

The verifier checks:

- spatial basis is exactly `B23, B31, B12`,
- full even Clifford basis is exactly `1, B23, B31, B12`,
- `3 + 1 = 4` channels,
- `tau = log2(C/12)` at every step of the DCCXXXII flow,
- closure events advance time exactly when they occur.

## Exact vs conditional

- **Exact:** the discrete W(3,3) / Clifford / codec spine carries a canonical `3+1` split.
- **Conditional:** identifying this scalar clock with macroscopic physical time still requires a genuine continuum or dynamical theorem.

## Executable artifact

- Verifier: `verify_dccxxxiii_spatial_closure_time_bridge.py`
- Tests: `tests/test_dccxxxiii_spatial_closure_time_bridge.py`
- Data: `data/dccxxxiii_spatial_closure_time_bridge.json`
