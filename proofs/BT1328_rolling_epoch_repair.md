# BT1328 -- Rolling Epoch Repair

## Purpose

BT1328 repairs the only failing exact arithmetic gate found by BT1327.

## Problem

BT1326 repeats the line:

```text
10980 = lcm(3660,1620)
```

But literally:

```text
lcm(3660,1620) = 98820
```

So the epoch cannot be justified by that lcm statement.

## Correct derivation

BT1321 already contains the right structure: a rolling chart phase.

```text
3660 = 6*540 + 180
180 = 540/3
```

Each Ihara frame advances the chart atlas by one third of a 540-chart cycle. Therefore the atlas phase closes after three Ihara frames:

```text
3*3660 = 10980
```

Equivalently:

```text
3 rolling offsets of 180 = 540
```

## Verifier

```text
tools/bt1328_epoch_repair.py
data/bt1328_epoch_repair.json
```

The verifier confirms:

```text
verified = true
epoch = 10980
literal_lcm_3660_1620 = 98820
```

## The correction

The master epoch statement should read:

```text
10980 is the three-frame rolling chart phase closure, not lcm(3660,1620).
```

## Consequence

BT1327 did its job: it caught the bad derivation. BT1328 restores the 10,980 value with the correct mechanism.
