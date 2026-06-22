# BT1489-BT1491: Row Actions, Fano-E6 Square, and Idempotent Paper Splice

## BT1489

BT1489 lifts the branch symmetry into the actual ABI v2 row machine.

```text
S4 branch actions: 24 unique row permutations
D4 square subgroup: 8 unique row permutations
V4 translations: 4 unique row permutations
Rows: 72 = 24 active/guard packets over 3 C3 channels
```

Every lifted action preserves channel, row kind, qutrit value, guard slot, and
the active/guard column formula.  Tau4 now has a concrete row permutation, while
the shear-induced branch identity fixes all 72 rows at this layer.

## BT1490

The new square is the shared 24-state fiber:

```text
24 = 4 V4 branches * 6 ABI row-value slots
24 = 3 local Fano arms * 8 D4 flag states
72 = 3 C3 channels * 24
81 = 72 + q^2 firewall gap
168 = 7 Fano points * 24 = 21 Fano flags * 8
```

This is the clean bridge between the E6/CSS ABI and the Fano detector-bin count.
It keeps the physical firewall explicit: no waveguide calibration or particle
interpretation is imported.

## BT1491

BT1491 makes the paper update mechanical and rerunnable.  If the BT1480-BT1491
insert chain exists, the splicer writes exactly one controlled input block into
`photonic_holonet.tex` before the software section.  A second run is a no-op.

## Current synthesis

```text
S4/D4/V4 branch actions
  -> 72 concrete ABI row permutations
  -> shared 24-state fiber
  -> E6/CSS 72 and 81
  -> Fano 168 by point and flag factorizations
  -> idempotent main-paper splice.
```
