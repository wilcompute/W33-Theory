# BT671 — Phase-Lifted W(G2) Packet Embedding into E1+E3

This executes the third step: test whether the phase-lifted `W(G2)` packet can live in the `E1+E3` lower-shell sector without violating the BT623 obstruction.

## 1. Starting obstruction from BT623/BT630

The lower conjugate sector has dimension

```text
E1 + E3 = 24 + 24 = 48.
```

This is dimension-compatible with four copies of the twelve-root `G2` packet:

```text
48 = 4 * (6_short + 6_long).
```

But the folded-cubic cross-channel is not a real Weyl reflection.

The normalized channel satisfies

```text
J^2 = -I,
```

whereas a real reflection generator must satisfy

```text
s^2 = +I.
```

Therefore the real flag-level embedding fails.

## 2. Complex/projective repair

After complexification, define

```text
s = iJ.
```

Then

```text
s^2 = (iJ)^2 = +I.
```

So the obstruction is repaired only projectively / after adjoining the scalar phase `i`.

## 3. Packet embedding model

Let

```text
E13_C = (E1 + E3) tensor C.
```

Use the dimension-compatible decomposition

```text
E13_C ~= C^4 tensor (C^6_short direct_sum C^6_long).
```

The external Weyl group

```text
W(G2) ~= D6
```

acts on the second tensor factor by its usual action on the six short and six long roots, and acts trivially on the multiplicity factor `C^4`.

Thus

```text
E1 + E3
```

supports an external `W(G2)` packet after complex/projective phase lift.

## 4. Compatibility with the six-carrier K33 quotient

BT663--BT669 identify the secondary six-frame quotient as

```text
K33 = Cay(S3, transpositions),
```

with metric-matching stabilizer

```text
Aut(K33, M_metric) ~= D6 ~= W(G2).
```

BT671 identifies the lower-shell packet as the compatible external target:

```text
six-frame D6 quotient  -->  four copies of G2 short+long roots inside E1+E3_C.
```

The bridge is valid only after the phase lift

```text
J^2=-I,    (iJ)^2=+I.
```

## Result

The exact outcome is:

```text
real flag-level W(G2) embedding: FAILS
complex/projective phase-lifted packet embedding: PASSES
```

Equivalently,

```text
E1+E3 ~= 24+24 = 4(6_short+6_long)
```

is a representation-packet carrier for external `W(G2)` after adjoining the scalar phase that turns the folded-cubic complex structure into an involution.

## Boundary

This is not a canonical numeric eigenspace intertwiner and not a proof that `F3` itself contains a real `W(G2)` action.  It is a dimension-compatible and obstruction-compatible complex/projective packet embedding.
