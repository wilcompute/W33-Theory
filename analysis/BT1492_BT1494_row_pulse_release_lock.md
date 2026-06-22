# BT1492-BT1494: Canonical Fiber, Row Pulses, Release Lock

## BT1492

BT1492 replaces the arbitrary `0..23` fiber indexing with the actual point stabilizer of the Fano plane.

```text
GL(3,2) = 168
point stabilizer = 24
flag stabilizer = 8
24 = 3 Fano lines through an anchor point * 8 flag-stabilizer states
```

The point stabilizer acts as the full `S4` on the four Fano lines not through the
anchor.  A chosen anchor flag gives an order-8 `D4` subgroup.  This is the
canonical source of the BT1490 shared `24` fiber.

## BT1493

BT1493 compiles the row symmetries into the physical holonet interfaces:

```text
BT1411 analyzer slot -> BT1374 mirror_slot mod 4 -> BT1407 Hesse epilogue lane
```

All `24` `S4` actions compile over all `72` rows, for `1728` row-pulse records.
The order-8 `D4` square subgroup is the native square-pulse layer, contributing
`576` row-pulse records.  The other `16` `S4` actions remain analyzer/ABI relabel
actions rather than calibrated optical-loss claims.

## BT1494

BT1494 repairs the broad `photonic-qec` release lock by restoring root-level
legacy `PART_*` artifacts from `manuscripts/parts/` and regenerating the live
CCCCVI scheduler, CCCCXVIII harmonic bus, CCCCXXVI fusion splice, and DCMII
screen/bulk/QEC bridge.

## Current Synthesis

```text
Fano point stabilizer
  -> canonical 24 fiber
  -> S4/D4/V4 ABI row actions
  -> BT1411 detector slots
  -> BT1374 mirror residues
  -> BT1407 Hesse epilogue lanes
  -> repaired photonic-qec release lock.
```
