# BT966 — Light-rail degeneracy breaker

BT963 found a real tie between the two light rails.

## Tied rails

```text
rail 0: pair [3,68], support 12, xor 71, xor weight 4, score 16
rail 1: pair [4,42], support 12, xor 46, xor weight 4, score 16
```

## ABI tie-break

BT966 fixes the ABI ordering by ascending xor mask:

```text
rail 1 before rail 0 because 46 < 71
```

Thus the packet ABI assignment is:

```text
rail 1 -> prefix 0  -> mirror
rail 0 -> prefix 10 -> schedule
```

## Boundary

This breaks the ABI ordering, not the deeper representation-theoretic doublet. Executable mirror/schedule lane-action maps are still needed to test whether the two light rails split dynamically.

## Witness

```text
analysis/bt966_light_rail_degeneracy_breaker.py
data/bt966_light_rail_degeneracy_breaker.json
```
