# BT787 - Rank-4 Incidence Revision and the R11 Handle Octet

BT787 tightens BT784 and BT786 into a rank-4 packet assignment.

BT784 saw the count-level tomotope strata inside the rank-32 cube-web alphabet.
BT786 then proved the tomotope face layer is not a primitive 16-orbit:

```text
faces = R09 + R10 = 8 + 8 = 16
```

BT787 recomputes the rank-32 quotient without external graph packages and
checks what this forces.

## Result

The three primitive octets are:

```text
R09, R10, R11
```

Only `R09` and `R10` have the anchored face signature:

```text
{equal: 1, one_side: 1}, overlap 5
```

The third octet has a different signature:

```text
R11: {one_side: 2}, overlap 2
```

So `R11` is not another face sheet.  Once the faces occupy `R09+R10`, `R11`
is the only remaining primitive size-8 packet.  It is the forced
handle/cell-transfer octet.

## Connector Routes

The quotient paths separate the live face route from the handle route:

```text
R09 -> R24 -> R12
R10 -> R26 -> R12

R11 -> R13 -> R08 -> R12
```

Thus the live face sheets attach to the live edge packet `R12` through
`R24/R26`, while the octet `R11` reaches the same live edge packet only through
the shadow route `R13 -> R08`.

## Consequence

The old count-level statement "cells = one size-8 orbit" was correct only at
the level of packet size.  The refined assignment is:

```text
faces       = R09 + R10
handle/cell = R11
edges       = R12 live, R13 shadow
vertices    = R20/R21 chiral sheets
```

This is not yet a full geometric tomotope realization.  It is the exact local
rank-4 packet assignment forced by the rank-32 cube-web quotient.

## Validation

Run:

```bash
python3 analysis/bt787_rank4_incidence_r11_handle.py
```
