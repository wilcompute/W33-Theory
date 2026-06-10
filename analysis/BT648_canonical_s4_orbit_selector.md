# BT648 — Canonical S4 Orbit Selector

BT644 found an internal S4 subgroup of PSp(4,3) acting on the 160 Levi flags with orbit profile

```text
8,8,24,24,24,24,24,24.
```

BT648 chooses the canonical carrier after fixing the base flag

```text
f0 = (point 0, line 0).
```

With that hinge/base flag fixed, the selected regular orbit is the 24-flag orbit containing flag index 0:

```text
O0 = [0,4,8,12,22,33,38,42,47,58,66,71,73,86,99,103,105,110,114,131,136,143,152,157].
```

This is a genuine regular S4 carrier because its size is 24 and the acting subgroup has order 24.

## Distance profile inside the selected carrier

For unordered pairs inside O0, the Levi flag distance distribution is

```text
distance 1: 36

distance 3: 60

distance 4: 180
```

Equivalently, ordered including diagonal:

```text
distance 0: 24

distance 1: 72

distance 3: 120

distance 4: 360
```

No distance-2 internal pairs occur in this selected carrier.

## Boundary

There is no absolute unique 24-orbit without choosing a hinge/base flag or S4 subgroup.  With the base flag fixed, O0 is canonical relative to that choice.
