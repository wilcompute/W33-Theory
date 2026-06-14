# BT962 — Final selector rail faces

BT962 uses the final selector as a canonical rail coordinate system.

## Final selector

```text
[[3,68], [4,42], [38,65], [90,144]]
```

## Rail data

```text
rail_support_sums = [12,12,14,22]
rail_xor_masks    = [71,46,91,234]
high_support_rail = 3
```

## 27-face structure

Each exactly-three-rail face has size 27:

```text
(0,1,2), (0,1,3), (0,2,3), (1,2,3)
```

Choosing the three faces containing the high-support rail gives a canonical 81-slot split:

```text
[(0,1,3), (0,2,3), (1,2,3)]
```

The complementary 27-face is:

```text
(0,1,2)
```

## Boundary

This is a rail-coordinate split of the H shadow. Further representation data is needed before interpreting labels beyond the finite-coordinate level.

## Witness

```text
analysis/bt962_selector_rail_faces.py
data/bt962_selector_rail_faces.json
```
