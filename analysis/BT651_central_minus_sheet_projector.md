# BT651 — Central Minus-Sheet Projector

The BT640 endpoint recurrence has characteristic polynomial

```text
P(x)=(x-11)(x-1)(x+1)(x^2-2x+11)(x^2+4x+11).
```

Let C be the companion or recurrence-shift operator on the endpoint recurrence
module.  The central projector onto the x=-1 sheet is the Lagrange idempotent

```text
Pi_minus = ((C-11I)(C-I)(C^2-2C+11I)(C^2+4C+11I))/2688.
```

The denominator is

```text
(P(x)/(x+1))|_{x=-1}=2688=16*168.
```

BT640 showed that deleting the x+1 factor leaves residual

```text
24(-1)^n.
```

Therefore the scalar amplitude of the central minus sheet in the endpoint
sequence is

```text
24.
```

## Comparison with BT648--BT649

BT648 selected an internal 24-flag regular S4 carrier O0.  BT649 showed that the
coordinate projector P_O onto O0 realizes the same trace carrier

```text
Tr((-I_24)^n)=24(-1)^n.
```

But P_O is not Bose-Mesner central.  Its commutators with A0,...,A4 have absolute
sums

```text
0,144,864,2352,3168.
```

Thus the correct statement is:

```text
Pi_minus is central in the endpoint recurrence module.
P_O is an internal coordinate trace carrier in the Levi flag module.
Both carry amplitude 24, but they are not the same projector.
```
