# Part DCLXXXIV — Holonomy Exchange-Residual Split Bridge

## Why this part exists

`Part DCLXXXIII` identified the exact q-versus-`Φ6` interface law.

The next deeper question is whether that law already resolves the carrier into explicit counted exchange and residual sectors.

This part proves the stronger statement:

> the exact exchange density `Y^2` splits the `40`-point carrier into `12` exchange channels and `28` residual channels.

## Exact exchange split

From `Part DCLXXXII`,

$$
Y^2 = \frac{3}{10}.
$$

So the carrier split is

$$
40 Y^2 = 12,
$$

and

$$
40(1-Y^2) = 28.
$$

Thus the constitutive interface law already separates the carrier into:

- `12` exchange channels,
- `28` residual channels.

## Residual resolution

The verifier then imports the exact transvection geometry from `Part DCLXIV`, where the mobile affine bulk count is exactly `27`.

It proves

$$
28 = 1 + 27,
$$

so the residual shell is exactly:

- `1` stationary transmitted mode,
- `27` affine bulk modes.

Hence the full carrier decomposition becomes

$$
40 = 12 + 28 = 12 + 1 + 27.
$$

## Dual size law

The same split is recovered from the reciprocal size channel:

$$
12(Z^2 - 1) = 28.
$$

So both the exchange side and the size side encode the same carrier decomposition.

## Why this is a breakthrough

This is the first constitutive layer that resolves directly into the earlier transvection geometry.

So the constitutive interface law is not floating above the holonomy story.

It already knows:

- the `12` exchange shell,
- the `1` stationary channel,
- the `27` affine bulk.

That is a very tight closure between the qutrit constitutive picture and the exact `W(3,3)` holonomy carrier geometry.

## Executable artifact

Verifier:

```text
verify_dclxxxiv_holonomy_exchange_residual_split_bridge.py
```

Tests:

```text
tests/test_dclxxxiv_holonomy_exchange_residual_split_bridge.py
```

Generated summary:

```text
data/dclxxxiv_holonomy_exchange_residual_split_bridge.json
```

---
*W33-Theory | Part DCLXXXIV | the ternary constitutive interface law splits the carrier exactly as \(40 = 12 + 28 = 12 + 1 + 27\), linking exchange density directly to the affine transvection bulk.*
