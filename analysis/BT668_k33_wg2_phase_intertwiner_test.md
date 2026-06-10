# BT668 — K3,3 / External W(G2) Phase-Intertwiner Test

BT663 produced a secondary carrier-label graph

```text
K3,3
```

on the six carrier labels

```text
F+, F-, M+, M-, A+, A-.
```

BT626-BT630 established a separate external W(G2) packet action on

```text
6_short + 6_long
```

and also showed that the folded-cubic cross-channel is not a real Weyl reflection because its normalized square is

```text
J^2 = -I.
```

The only safe lift is therefore phase/projective:

```text
(iJ)^2 = +I.
```

## Test object

The carrier-label quotient from BT663 has bipartition

```text
P = {F+, M+, A+},
N = {F-, M-, A-}.
```

The metric-pair matching is

```text
F+--F-, M+--M-, A+--A-.
```

Its matching-preserving automorphism group is

```text
D6 ~= W(G2), order 12.
```

## External packet comparison

The external W(G2) packet has six positive-root labels, naturally arranged as a hexagon:

```text
alpha_1, alpha_2, alpha_3, alpha_4, alpha_5, alpha_6.
```

Choose the label map

```text
F+ -> alpha_1,
M- -> alpha_2,
A+ -> alpha_3,
F- -> alpha_4,
M+ -> alpha_5,
A- -> alpha_6.
```

Then the carrier hexagon from BT663

```text
F+ -- M- -- A+ -- F- -- M+ -- A- -- F+
```

is identified with the G2 root hexagon.

## Phase obstruction and lift

On the real folded-cubic channel, the candidate reflection has square

```text
J^2 = -I,
```

so it cannot be a literal real W(G2) reflection.

After adjoining the scalar phase i, define

```text
s = iJ.
```

Then

```text
s^2 = +I.
```

Thus the secondary K3,3 carrier quotient can be matched to the external W(G2) packet only in the phase-lifted/projective sense:

```text
K3,3 carrier quotient + phase deck -> external W(G2) packet.
```

## Result

The test passes in the following precise form:

```text
Aut(K3,3, metric matching) ~= W(G2)
```

and this W(G2) quotient is compatible with the external G2 packet after the same scalar phase lift required by BT630:

```text
J^2=-I,   (iJ)^2=+I.
```

## Boundary

This is not a real flag-level Weyl action extracted from F3.  It is a phase-lifted secondary carrier quotient compatible with the external W(G2) packet.
