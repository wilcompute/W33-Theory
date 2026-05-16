# Part DCCLXIII — Inverse Reciprocity (3/13 ↔ 13/3) Bridge

## Why this part exists

You pointed out the key reciprocal pattern directly: the closure weak scalar appears as `3/13`, while the transport scalar appears as `13/3`.

This part turns that observation into an explicit verified bridge.

## Exact reciprocity

Define:

```text
x = 3/13,
K = 13/3.
```

The verifier proves:

```text
x * K = 1,
K = 1/x,
x = 1/K.
```

So weak-angle closure and transport mixing sit in an exact inverse pair on the current octahedral branch.

## Integer normalizations

The same bridge gives rigid integer checks:

```text
13x = 3,
3K = 13.
```

So the reciprocity is not numerical coincidence; it is exact rational duality.

## Meaning

This identifies a concrete dual-map interpretation:

- `x = 3/13` as forward closure scalar,
- `K = 13/3` as inverse transport scale,
- and the bridge relation `xK=1` linking them.

This is the sharpest formal statement so far of your “inverse Koide-side” intuition on the current validated branch.

## Exact vs conditional

- **Exact:** on the validated octahedral chain, `3/13` and `13/3` are exact reciprocals.
- **Conditional:** persistence of this reciprocity under deformations/continuum limits still needs a parameterized extension theorem.

## Executable artifact

- Verifier: `verify_dcclxiii_inverse_reciprocity_3_13_13_3_bridge.py`
- Tests: `tests/test_dcclxiii_inverse_reciprocity_3_13_13_3_bridge.py`
- Data: `data/dcclxiii_inverse_reciprocity_3_13_13_3_bridge.json`
