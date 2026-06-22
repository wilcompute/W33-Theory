# Part DCCXVI: Axis-Syndrome Selector Codec Bridge

## Claim

The `40`-trit classical selector is not supposed to encode all `12` local
ouroboros turns.  It encodes the ternary axis coordinate.  The remaining two
binary choices are syndrome/frame data.

The local alphabet factors as:

```text
12 = 3 axes * 2 signs * 2 roles.
```

Therefore the directed photonic/QEC carrier factors as:

```text
480 = 40 * 12 = 40 * 3 * 2 * 2.
```

Adding the KLM primitive rail bit gives:

```text
960 = 40 * 3 * 2 * 2 * 2.
```

## 1. The local codec

The three ternary axis values are:

```text
B23, B31, B12.
```

Each axis carries two signs:

```text
+, -
```

and two fusion roles:

```text
accepted, return.
```

So the local turn set is:

```text
{accepted:+B23, accepted:-B23, return:+B23, return:-B23,
 accepted:+B31, accepted:-B31, return:+B31, return:-B31,
 accepted:+B12, accepted:-B12, return:+B12, return:-B12}.
```

This is exactly the DCCXIV/DCCXV `12 = 6 + 6` loop alphabet, but now parsed
as a codec rather than only as a count.

## 2. Why the selector is trit-sized

The classical selector stores:

```text
one axis trit per W33 vertex.
```

Thus it has:

```text
40 trits,
3^40 states,
2^63 < 3^40 < 2^64.
```

The sign is a Clifford/Pauli-frame bit.  The accepted-vs-return role is a
fusion syndrome bit.  These are not extra classical selector trits; they are
absorbed by the protected runtime.

## 3. Global lift

Across `40` vertices:

```text
axis layer:             40 * 3       = 120
signed-axis layer:      40 * 3 * 2   = 240
fusion-attempt layer:   40 * 3 * 2 * 2 = 480
KLM primitive layer:    40 * 3 * 2 * 2 * 2 = 960.
```

So the architecture has a clean separation:

```text
classical selector:  ternary axis
quantum frame:       binary sign
fusion syndrome:     binary accepted/return role
optical primitive:   binary KLM rail
```

## 4. QEC reading

The protected code still uses:

```text
39 vertex checks + 120 triangle checks + 81 logical H1 = 240.
```

The selector codec does not add stabilizers that kill the logical `H1=81`
tail.  It explains why the runtime can be classical, quantum, deterministic,
and probabilistic at once:

```text
classical axis selector + quantum sign frame + heralded syndrome return.
```

## Boundary

This is a finite codec theorem for the promoted photonic/QEC runtime.  It
does not model hardware noise rates, detector physics, biological chemistry,
or curved 4D spectral-action asymptotics.
