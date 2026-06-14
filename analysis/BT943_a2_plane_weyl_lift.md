# BT943 — A2-plane Weyl lift attempt

BT943 attacks the signed/A2-plane part left open by BT940.

## Integral A2 plane

For one A2 plane with Gram

```text
[[2,-1],[-1,2]]
```

the simple reflections are

```text
s1 = [[-1,1],[0,1]]
s2 = [[1,0],[1,-1]]
```

They generate `W(A2)` of order 6 and preserve the A2 Gram matrix exactly.

## Mod-2 chain shadow

Modulo 2, this same group has order 6 and is `GL(2,2)`. Thus each A2 plane has a valid local mod-2 Weyl action after choosing the BT930 tetracode gauge.

## Boundary

Four independent A2 planes would give local order `6^4 = 1296`, but the tetracode glue stabilizer from BT940 has order 48. BT943 constructs the A2-plane Weyl lift in metric coordinates; it does not yet prove that all local Weyl choices preserve the ternary tetracode glue or define canonical chain-complex maps.

## Witness

```text
analysis/bt943_a2_plane_weyl_lift.py
data/bt943_a2_plane_weyl_lift.json
```
