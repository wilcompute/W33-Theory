# BT1327--BT1328 -- Q4 Diamond Epoch Audit

## Purpose

This pass turns the BT1326 master synthesis into an executable audit and then repairs the one failing arithmetic claim.

## BT1327 audit

```text
tools/bt1327_q4_diamond_audit.py
data/bt1327_q4_diamond_audit.json
proofs/BT1327_q4_diamond_audit.md
```

The audit verifies the Q4 diamond number table identities and flags the literal epoch line.

The failing literal check is:

```text
10980 = lcm(3660,1620)
```

because:

```text
lcm(3660,1620) = 98820
```

## BT1328 repair

```text
tools/bt1328_epoch_repair.py
data/bt1328_epoch_repair.json
proofs/BT1328_rolling_epoch_repair.md
```

The repaired derivation is rolling phase closure:

```text
3660 = 6*540 + 180
180 = 540/3
3*3660 = 10980
```

So 10,980 is still correct, but it is a three-frame rolling chart phase closure, not an lcm of 3660 and 1620.

## Regression

```text
tests/test_bt1327_bt1328_q4_diamond_audit.py
```

protects both the BT1327 audit and the BT1328 repair.
